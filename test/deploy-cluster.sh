#!/bin/bash
#
# Copyright 2018 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -ex

# Env inputs:
# * COMMIT_SHA - decides TEST_CLUSTER's name
# * TEST_CLUSTER_PREFIX - decides default TEST_CLUSTER naming
# * TEST_CLUSTER - [optional] specify to reuse existing TEST_CLUSTER
DEFAULT_TEST_CLUSTER_PREFIX=${WORKFLOW_FILE%.*}
TEST_CLUSTER_PREFIX=${TEST_CLUSTER_PREFIX:-${DEFAULT_TEST_CLUSTER_PREFIX}}
TEST_CLUSTER_DEFAULT=$(echo $TEST_CLUSTER_PREFIX | cut -d _ -f 1)-${COMMIT_SHA:0:7}-${RANDOM}
TEST_CLUSTER=${TEST_CLUSTER:-${TEST_CLUSTER_DEFAULT}}
ENABLE_WORKLOAD_IDENTITY=${ENABLE_WORKLOAD_IDENTITY:-false}
SHOULD_CLEANUP_CLUSTER=false

function clean_up {
  set +e # the following clean up commands shouldn't exit on error
  set +x # no need for command history

  echo "Status of pods before clean up:"
  kubectl get pods --all-namespaces

  echo "Dumping all pods info as artifacts in directory artifacts/pods_info/*..."
  POD_INFO_DIR="$ARTIFACTS/pods_info"
  mkdir -p "$POD_INFO_DIR"
  # Refer to https://github.com/kubernetes/test-infra/blob/master/prow/jobs.md#job-environment-variables
  ALL_PODS=($(kubectl get pods -o=custom-columns=:metadata.name -n $NAMESPACE))
  for POD_NAME in "${ALL_PODS[@]}"; do
    pod_info_file="$POD_INFO_DIR/$POD_NAME.txt"
    echo "Saving log of $POD_NAME to $pod_info_file"
    echo "Pod name: $POD_NAME" >> "$pod_info_file"
    echo "Detailed logs:" >> "$pod_info_file"
    echo "https://console.cloud.google.com/logs/viewer?project=$PROJECT&advancedFilter=resource.type%3D%22k8s_container%22%0Aresource.labels.project_id%3D%22$PROJECT%22%0Aresource.labels.location%3D%22us-west1-b%22%0Aresource.labels.cluster_name%3D%22${TEST_CLUSTER}%22%0Aresource.labels.namespace_name%3D%22$NAMESPACE%22%0Aresource.labels.pod_name%3D%22$POD_NAME%22" \
      >> "$pod_info_file"
    echo "--------" >> "$pod_info_file"
    kubectl describe pod $POD_NAME -n $NAMESPACE >> "$pod_info_file"
    echo "--------" >> "$pod_info_file"
    kubectl get pod $POD_NAME -n $NAMESPACE -o yaml >> "$pod_info_file"
  done
  
  echo "Archiving ${ARTIFACTS} into ./${COMMIT_SHA}_logs.tar.gz" 
  tar -czf ./${COMMIT_SHA}_logs.tar.gz ${ARTIFACTS}
  echo "Uploading ./${COMMIT_SHA}_logs.tar.gz to ${TEST_RESULTS_GCS_DIR}/logs"
  gsutil cp ${COMMIT_SHA}_logs.tar.gz "${TEST_RESULTS_GCS_DIR}/logs"

  echo "Clean up cluster..."
  if [ $SHOULD_CLEANUP_CLUSTER == true ]; then
    # --async doesn't wait for this operation to complete, so we can get test
    # results faster
    yes | gcloud container clusters delete ${TEST_CLUSTER} --async
  fi
}
trap clean_up EXIT SIGINT SIGTERM

cd ${DIR}
# test if ${TEST_CLUSTER} exists or not
if gcloud container clusters describe ${TEST_CLUSTER} &>/dev/null; then
  echo "Use existing test cluster: ${TEST_CLUSTER}"
else
  echo "Creating a new test cluster: ${TEST_CLUSTER}"
  SHOULD_CLEANUP_CLUSTER=true
  # Machine type and cluster size is the same as kubeflow deployment to
  # easily compare performance. We can reduce usage later.
  NODE_POOL_CONFIG_ARG="--num-nodes=2 --machine-type=e2-standard-8 \
    --enable-autoscaling --max-nodes=8 --min-nodes=2"
  if [ "$ENABLE_WORKLOAD_IDENTITY" = true ]; then
    WI_ARG="--workload-pool=$PROJECT.svc.id.goog"
    SCOPE_ARG=
  else
    WI_ARG=
    # "storage-rw" is needed to allow VMs to push to gcr.io when using default GCE service account.
    # reference: https://cloud.google.com/compute/docs/access/service-accounts#accesscopesiam
    SCOPE_ARG="--scopes=storage-rw,cloud-platform"
  fi
  # Use regular release channel to keep up with newly created clusters in Google Cloud Marketplace.
  # gcloud container clusters create ${TEST_CLUSTER} --release-channel regular ${SCOPE_ARG} ${NODE_POOL_CONFIG_ARG} ${WI_ARG}
  # Temporarily use cos as image type until docker dependencies gets removed. reference: https://github.com/kubeflow/pipelines/issues/6696
  gcloud container clusters create ${TEST_CLUSTER} --image-type cos_containerd --release-channel regular ${SCOPE_ARG} ${NODE_POOL_CONFIG_ARG} ${WI_ARG}
fi

gcloud container clusters get-credentials ${TEST_CLUSTER}

# when we reuse a cluster when debugging, clean up its kfp installation first
# this does nothing with a new cluster
kubectl delete namespace ${NAMESPACE} --wait || echo "No need to delete ${NAMESPACE} namespace. It doesn't exist."
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

if [ "$ENABLE_WORKLOAD_IDENTITY" != true ]; then
  if [ -z $SA_KEY_FILE ]; then
    SA_KEY_FILE=${DIR}/key.json
    # The service account key is for default VM service account.
    # ref: https://cloud.google.com/compute/docs/access/service-accounts#compute_engine_default_service_account
    # It was generated by the following command
    # `gcloud iam service-accounts keys create $SA_KEY_FILE --iam-account ${VM_SERVICE_ACCOUNT}`
    # Because there's a limit of 10 keys per service account, we are reusing the same key stored in the following bucket.
    gsutil cp "gs://ml-pipeline-test-keys/ml-pipeline-test-sa-key.json" $SA_KEY_FILE
  fi
  kubectl create secret -n ${NAMESPACE} generic user-gcp-sa --from-file=user-gcp-sa.json=$SA_KEY_FILE --dry-run=client -o yaml | kubectl apply -f -
fi
