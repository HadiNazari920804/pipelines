# Copyright 2022 The Kubeflow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test Dataproc Batch Remote Runner module."""

import json
import os
import time
from unittest import mock

import google.auth
from google_cloud_pipeline_components.container.utils.execution_context import ExecutionContext
from google_cloud_pipeline_components.container.v1.dataproc.create_pyspark_batch import remote_runner as dataproc_batch_remote_runner
from google_cloud_pipeline_components.container.v1.gcp_launcher.utils import gcp_labels_util
from google_cloud_pipeline_components.proto import gcp_resources_pb2
import re
import requests

from google.protobuf import json_format
import unittest

_SYSTEM_LABELS = {'key1': 'value1', 'key2': 'value2'}


class DataprocBatchRemoteRunnerUtilsTests(unittest.TestCase):
  """Test cases for Dataproc Batch remote runner."""

  def setUp(self):
    super(DataprocBatchRemoteRunnerUtilsTests, self).setUp()
    self._dataproc_uri_prefix = 'https://dataproc.googleapis.com/v1'
    self._project = 'test-project'
    self._location = 'test-location'
    self._batch_id = 'test-batch-id'
    self._creds_token = 'fake-token'
    self._operation_id = 'fake-operation-id'
    self._operation_name = f'projects/{self._project}/regions/{self._location}/operations/{self._operation_id}'
    self._operation_uri = f'{self._dataproc_uri_prefix}/{self._operation_name}'
    self._batch_name = f'projects/{self._project}/locations/{self._location}/batches/{self._batch_id}'
    self._batch_uri = f'{self._dataproc_uri_prefix}/{self._batch_name}'
    self._gcp_resources = os.path.join(
        os.getenv('TEST_UNDECLARED_OUTPUTS_DIR'), 'gcp_resources')
    os.environ[gcp_labels_util.SYSTEM_LABEL_ENV_VAR] = json.dumps(
        _SYSTEM_LABELS)

    self._test_batch = {
        'labels': {'foo': 'bar', 'fizz': 'buzz'},
        'runtime_config': {
            'version': 'test-version',
            'container_image': 'test-container-image',
            'properties': {'foo': 'bar', 'fizz': 'buzz'}
        },
        'environment_config': {
            'execution_config': {
                'service_account': 'test-service-account',
                'network_tags': ['test-tag-1', 'test-tag-2'],
                'kms_key': 'test-kms-key',
                'network_uri': 'test-network-uri',
                'subnetwork_uri': 'test-subnetwork-uri'
            },
            'peripherals_config': {
                'metastore_service': 'test-metastore-service',
                'spark_history_server_config': {
                    'dataproc_cluster': 'test-dataproc-cluster'
                }
            }
        }
    }
    self._test_pyspark_batch = {
        **self._test_batch,
        'pyspark_batch': {
            'main_python_file_uri': 'test-python-file',
            'python_file_uris': ['test-python-file-uri-1', 'test-python-file-uri-2'],
            'jar_file_uris': ['test-jar-file-uri-1', 'test-jar-file-uri-2'],
            'file_uris': ['test-file-uri-1', 'test-file-uri-2'],
            'archive_uris': ['test-archive-uri-1', 'test-archive-uri-2'],
            'args': ['arg1', 'arg2']
        }
    }
    self._expected_pyspark_batch = self._test_pyspark_batch.copy()
    self._expected_pyspark_batch['labels'] = {
        'key1': 'value1',
        'key2': 'value2',
        'foo': 'bar',
        'fizz': 'buzz'
    }

  def tearDown(self):
    super(DataprocBatchRemoteRunnerUtilsTests, self).tearDown()
    if os.path.exists(self._gcp_resources):
      os.remove(self._gcp_resources)

  def _validate_gcp_resources_succeeded(self):
    with open(self._gcp_resources) as f:
      serialized_gcp_resources = f.read()
      job_resources = json_format.Parse(serialized_gcp_resources,
                                        gcp_resources_pb2.GcpResources())

      # Validate number of resources.
      self.assertLen(job_resources.resources, 2)

      # Validate that gcp_resources contains valid DataprocLro and DataprocBatch resources.
      test_job_resources = gcp_resources_pb2.GcpResources()
      operation_resource = test_job_resources.resources.add()
      operation_resource.resource_type = 'DataprocLro'
      operation_resource.resource_uri = self._operation_uri
      batch_resource = test_job_resources.resources.add()
      batch_resource.resource_type = 'DataprocBatch'
      batch_resource.resource_uri = self._batch_uri
      self.assertEqual(job_resources, test_job_resources)

  @mock.patch.object(google.auth, 'default', autospec=True)
  @mock.patch.object(google.auth.transport.requests, 'Request', autospec=True)
  @mock.patch.object(requests.sessions.Session, 'get', autospec=True)
  @mock.patch.object(requests.sessions.Session, 'post', autospec=True)
  @mock.patch.object(time, 'sleep', autospec=True)
  def test_dataproc_batch_remote_runner_pyspark_batch_succeeded(self,
                                                                mock_time_sleep,
                                                                mock_post_requests,
                                                                mock_get_requests,
                                                                _,
                                                                mock_auth_default):
    mock_creds = mock.Mock(spec=google.auth.credentials.Credentials)
    mock_creds.token = self._creds_token
    mock_auth_default.return_value = [mock_creds, 'project']

    mock_operation = mock.Mock(spec=requests.models.Response)
    mock_operation.json.return_value = {
        'name': self._operation_name,
        'metadata': {
            'batch': self._batch_name
        }
    }
    mock_post_requests.return_value = mock_operation

    mock_polled_lro = mock.Mock(spec=requests.models.Response)
    mock_polled_lro.json.return_value = {
        'name': self._operation_name,
        'done': True,
        'response': {
            'name': self._batch_name,
            'state': 'SUCCEEDED'
        }
    }
    mock_get_requests.return_value = mock_polled_lro

    dataproc_batch_remote_runner.create_pyspark_batch(
        type='PySparkBatch',
        project=self._project,
        location=self._location,
        batch_id=self._batch_id,
        payload=json.dumps(self._test_pyspark_batch),
        gcp_resources=self._gcp_resources
    )

    mock_post_requests.assert_called_once_with(
        self=mock.ANY,
        url=f'{self._dataproc_uri_prefix}/projects/{self._project}/locations/{self._location}/batches/?batchId={self._batch_id}',
        data=json.dumps(self._expected_pyspark_batch),
        headers={'Authorization': f'Bearer {self._creds_token}'})
    mock_get_requests.assert_called_once_with(
        self=mock.ANY,
        url=self._operation_uri,
        headers={'Authorization': f'Bearer {self._creds_token}'}
    )
    mock_time_sleep.assert_called_once()
    self._validate_gcp_resources_succeeded()
