# coding: utf-8

"""
    Kubeflow Pipelines API

    This file contains REST API specification for Kubeflow Pipelines. The file is autogenerated from the swagger definition.

    Contact: kubeflow-pipelines@google.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from kfp_server_api.configuration import Configuration


class V2beta1PipelineVersion(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'pipeline_id': 'str',
        'pipeline_version_id': 'str',
        'display_name': 'str',
        'description': 'str',
        'created_at': 'datetime',
        'package_url': 'V2beta1Url',
        'pipeline_spec': 'ProtobufStruct',
        'error': 'GooglerpcStatus'
    }

    attribute_map = {
        'pipeline_id': 'pipeline_id',
        'pipeline_version_id': 'pipeline_version_id',
        'display_name': 'display_name',
        'description': 'description',
        'created_at': 'created_at',
        'package_url': 'package_url',
        'pipeline_spec': 'pipeline_spec',
        'error': 'error'
    }

    def __init__(self, pipeline_id=None, pipeline_version_id=None, display_name=None, description=None, created_at=None, package_url=None, pipeline_spec=None, error=None, local_vars_configuration=None):  # noqa: E501
        """V2beta1PipelineVersion - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pipeline_id = None
        self._pipeline_version_id = None
        self._display_name = None
        self._description = None
        self._created_at = None
        self._package_url = None
        self._pipeline_spec = None
        self._error = None
        self.discriminator = None

        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if pipeline_version_id is not None:
            self.pipeline_version_id = pipeline_version_id
        if display_name is not None:
            self.display_name = display_name
        if description is not None:
            self.description = description
        if created_at is not None:
            self.created_at = created_at
        if package_url is not None:
            self.package_url = package_url
        if pipeline_spec is not None:
            self.pipeline_spec = pipeline_spec
        if error is not None:
            self.error = error

    @property
    def pipeline_id(self):
        """Gets the pipeline_id of this V2beta1PipelineVersion.  # noqa: E501

        Required input field. Unique ID of the parent pipeline.  # noqa: E501

        :return: The pipeline_id of this V2beta1PipelineVersion.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """Sets the pipeline_id of this V2beta1PipelineVersion.

        Required input field. Unique ID of the parent pipeline.  # noqa: E501

        :param pipeline_id: The pipeline_id of this V2beta1PipelineVersion.  # noqa: E501
        :type pipeline_id: str
        """

        self._pipeline_id = pipeline_id

    @property
    def pipeline_version_id(self):
        """Gets the pipeline_version_id of this V2beta1PipelineVersion.  # noqa: E501

        Output. Unique pipeline version ID. Generated by API server.  # noqa: E501

        :return: The pipeline_version_id of this V2beta1PipelineVersion.  # noqa: E501
        :rtype: str
        """
        return self._pipeline_version_id

    @pipeline_version_id.setter
    def pipeline_version_id(self, pipeline_version_id):
        """Sets the pipeline_version_id of this V2beta1PipelineVersion.

        Output. Unique pipeline version ID. Generated by API server.  # noqa: E501

        :param pipeline_version_id: The pipeline_version_id of this V2beta1PipelineVersion.  # noqa: E501
        :type pipeline_version_id: str
        """

        self._pipeline_version_id = pipeline_version_id

    @property
    def display_name(self):
        """Gets the display_name of this V2beta1PipelineVersion.  # noqa: E501

        Required input field. Pipeline version name provided by user.  # noqa: E501

        :return: The display_name of this V2beta1PipelineVersion.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this V2beta1PipelineVersion.

        Required input field. Pipeline version name provided by user.  # noqa: E501

        :param display_name: The display_name of this V2beta1PipelineVersion.  # noqa: E501
        :type display_name: str
        """

        self._display_name = display_name

    @property
    def description(self):
        """Gets the description of this V2beta1PipelineVersion.  # noqa: E501

        Optional input field. Short description of the pipeline version.  # noqa: E501

        :return: The description of this V2beta1PipelineVersion.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this V2beta1PipelineVersion.

        Optional input field. Short description of the pipeline version.  # noqa: E501

        :param description: The description of this V2beta1PipelineVersion.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def created_at(self):
        """Gets the created_at of this V2beta1PipelineVersion.  # noqa: E501

        Output. Creation time of the pipeline version.  # noqa: E501

        :return: The created_at of this V2beta1PipelineVersion.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this V2beta1PipelineVersion.

        Output. Creation time of the pipeline version.  # noqa: E501

        :param created_at: The created_at of this V2beta1PipelineVersion.  # noqa: E501
        :type created_at: datetime
        """

        self._created_at = created_at

    @property
    def package_url(self):
        """Gets the package_url of this V2beta1PipelineVersion.  # noqa: E501


        :return: The package_url of this V2beta1PipelineVersion.  # noqa: E501
        :rtype: V2beta1Url
        """
        return self._package_url

    @package_url.setter
    def package_url(self, package_url):
        """Sets the package_url of this V2beta1PipelineVersion.


        :param package_url: The package_url of this V2beta1PipelineVersion.  # noqa: E501
        :type package_url: V2beta1Url
        """

        self._package_url = package_url

    @property
    def pipeline_spec(self):
        """Gets the pipeline_spec of this V2beta1PipelineVersion.  # noqa: E501


        :return: The pipeline_spec of this V2beta1PipelineVersion.  # noqa: E501
        :rtype: ProtobufStruct
        """
        return self._pipeline_spec

    @pipeline_spec.setter
    def pipeline_spec(self, pipeline_spec):
        """Sets the pipeline_spec of this V2beta1PipelineVersion.


        :param pipeline_spec: The pipeline_spec of this V2beta1PipelineVersion.  # noqa: E501
        :type pipeline_spec: ProtobufStruct
        """

        self._pipeline_spec = pipeline_spec

    @property
    def error(self):
        """Gets the error of this V2beta1PipelineVersion.  # noqa: E501


        :return: The error of this V2beta1PipelineVersion.  # noqa: E501
        :rtype: GooglerpcStatus
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this V2beta1PipelineVersion.


        :param error: The error of this V2beta1PipelineVersion.  # noqa: E501
        :type error: GooglerpcStatus
        """

        self._error = error

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V2beta1PipelineVersion):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V2beta1PipelineVersion):
            return True

        return self.to_dict() != other.to_dict()
