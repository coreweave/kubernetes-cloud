import time
import six

from kubernetes import client, config, watch
from kubernetes.client.exceptions import (
    ApiTypeError,
    ApiValueError
)


class KubeVirtClient:
    """
    Since the native python client for kubevirt (kubevirt/client-python) has yet unresolved issues,
    this class demonstrates basic operations utilizing the kubevirt api.
    """
    def __init__(self, kubeconfig_path=None):
        config.kube_config.load_kube_config(kubeconfig_path)

        self.api = client.CustomObjectsApi()
        self.api_client = self.api.api_client

    def kubevirt_api(self, namespace, name, command,
                         group='subresources.kubevirt.io', version='v1', plural='virtualmachines',
                         resource_path='/apis/{group}/{version}/namespaces/{namespace}/{plural}/{name}/{command}',
                         method='PUT',
                         **kwargs):
        """
        This method changes the state of the kubevirt VirtualMachine instance. It is modified version of 
        https://github.com/kubernetes-client/python/blob/b79ad6837b2f5326c7dad488a64eed7c3987e856/kubernetes/client/api/custom_objects_api.py#L227
        """
        local_var_params = locals()

        all_params = [
            'group',
            'version',
            'namespace',
            'plural',
            'name',
            'command',
            'dry_run'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method kubevirt_list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'group' is set
        if self.api_client.client_side_validation and ('group' not in local_var_params or  # noqa: E501
                                                        local_var_params['group'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `group` when calling `kubevirt_list`")  # noqa: E501
        # verify the required parameter 'version' is set
        if self.api_client.client_side_validation and ('version' not in local_var_params or  # noqa: E501
                                                        local_var_params['version'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `version` when calling `kubevirt_list`")  # noqa: E501
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and ('namespace' not in local_var_params or  # noqa: E501
                                                        local_var_params['namespace'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `namespace` when calling `kubevirt_list`")  # noqa: E501
        # verify the required parameter 'plural' is set
        if self.api_client.client_side_validation and ('plural' not in local_var_params or  # noqa: E501
                                                        local_var_params['plural'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `plural` when calling `kubevirt_list`")  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in local_var_params or  # noqa: E501
                                                        local_var_params['name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `name` when calling `kubevirt_list`")  # noqa: E501
        # verify the required parameter 'command' is set
        if self.api_client.client_side_validation and ('command' not in local_var_params or  # noqa: E501
                                                        local_var_params['command'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `command` when calling `kubevirt_list`")  # noqa: E501

        path_params = {}
        if 'group' in local_var_params:
            path_params['group'] = local_var_params['group']  # noqa: E501
        if 'version' in local_var_params:
            path_params['version'] = local_var_params['version']  # noqa: E501
        if 'namespace' in local_var_params:
            path_params['namespace'] = local_var_params['namespace']  # noqa: E501
        if 'plural' in local_var_params:
            path_params['plural'] = local_var_params['plural']  # noqa: E501
        if 'name' in local_var_params:
            path_params['name'] = local_var_params['name']  # noqa: E501
        if 'command' in local_var_params:
            path_params['command'] = local_var_params['command']  # noqa: E501

        query_params = []
        if 'dry_run' in local_var_params and local_var_params['dry_run'] is not None:
            query_params.append(('dryRun', local_var_params['dry_run']))

        header_params = {}

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['*/*'])

        # Authentication setting
        auth_settings = ['BearerToken']

        return self.api_client.call_api(
            resource_path, method,
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_type='object',
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={})

    def kubevirt_list(self, namespace,
                         group='kubevirt.io', version='v1', plural='virtualmachineinstances',
                         resource_path='/apis/{group}/{version}/namespaces/{namespace}/{plural}',
                         method='GET',
                         **kwargs):
        """
        This method lists all instances of kubevirt. It is modified version of 
        https://github.com/kubernetes-client/python/blob/b79ad6837b2f5326c7dad488a64eed7c3987e856/kubernetes/client/api/custom_objects_api.py#L227
        """
        local_var_params = locals()

        all_params = [
            'group',
            'version',
            'namespace',
            'plural',
            'pretty',
            '_continue',
            'field_selector',
            'label_selector',
            'limit',
            'resource_version',
            'timeout_seconds',
            'watch'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method kubevirt_list" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'group' is set
        if self.api_client.client_side_validation and ('group' not in local_var_params or  # noqa: E501
                                                        local_var_params['group'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `group` when calling `kubevirt_list`")  # noqa: E501
        # verify the required parameter 'version' is set
        if self.api_client.client_side_validation and ('version' not in local_var_params or  # noqa: E501
                                                        local_var_params['version'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `version` when calling `kubevirt_list`")  # noqa: E501
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and ('namespace' not in local_var_params or  # noqa: E501
                                                        local_var_params['namespace'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `namespace` when calling `kubevirt_list`")  # noqa: E501
        # verify the required parameter 'plural' is set
        if self.api_client.client_side_validation and ('plural' not in local_var_params or  # noqa: E501
                                                        local_var_params['plural'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `plural` when calling `kubevirt_list`")  # noqa: E501

        path_params = {}
        if 'group' in local_var_params:
            path_params['group'] = local_var_params['group']  # noqa: E501
        if 'version' in local_var_params:
            path_params['version'] = local_var_params['version']  # noqa: E501
        if 'namespace' in local_var_params:
            path_params['namespace'] = local_var_params['namespace']  # noqa: E501
        if 'plural' in local_var_params:
            path_params['plural'] = local_var_params['plural']  # noqa: E501

        query_params = []
        if 'pretty' in local_var_params and local_var_params['pretty'] is not None:  # noqa: E501
            query_params.append(('pretty', local_var_params['pretty']))  # noqa: E501
        if '_continue' in local_var_params and local_var_params['_continue'] is not None:  # noqa: E501
            query_params.append(('continue', local_var_params['_continue']))  # noqa: E501
        if 'field_selector' in local_var_params and local_var_params['field_selector'] is not None:  # noqa: E501
            query_params.append(('fieldSelector', local_var_params['field_selector']))  # noqa: E501
        if 'label_selector' in local_var_params and local_var_params['label_selector'] is not None:  # noqa: E501
            query_params.append(('labelSelector', local_var_params['label_selector']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'resource_version' in local_var_params and local_var_params['resource_version'] is not None:  # noqa: E501
            query_params.append(('resourceVersion', local_var_params['resource_version']))  # noqa: E501
        if 'timeout_seconds' in local_var_params and local_var_params['timeout_seconds'] is not None:  # noqa: E501
            query_params.append(('timeoutSeconds', local_var_params['timeout_seconds']))  # noqa: E501
        if 'watch' in local_var_params and local_var_params['watch'] is not None:  # noqa: E501
            query_params.append(('watch', local_var_params['watch']))  # noqa: E501

        header_params = {}

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/json;stream=watch'])  # noqa: E501

        # Authentication setting
        auth_settings = ['BearerToken']

        return self.api_client.call_api(
            resource_path, method,
            path_params,
            query_params,
            header_params,
            body=None,
            post_params=[],
            files={},
            response_type='object',
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={})

    def start(self, namespace, name, **kwargs):
        """
        Start kubevirt instance.
        """
        kwargs['_return_http_data_only'] = True
        version = self.version(namespace, name)
        while True:
            ret = self.kubevirt_api(namespace, name, 'start', version=version, **kwargs)
            if ret['code'] == 409:
                time.sleep(2)
                continue
            return ret

    def stop(self, namespace, name, **kwargs):
        """
        Stop kubevirt instance.
        """
        kwargs['_return_http_data_only'] = True
        version = self.version(namespace, name)
        return self.kubevirt_api(namespace, name, 'stop', version=version, **kwargs)

    def restart(self, namespace, name, **kwargs):
        """
        Restart kubevirt instance.
        """
        kwargs['_return_http_data_only'] = True
        version = self.version(namespace, name)
        return self.kubevirt_api(namespace, name, 'restart', version=version, **kwargs)

    def version(self, namespace, name):
        """
        Retrieve kubevirt api version.
        """
        kwargs = {'_return_http_data_only': True}
        resource_path = '/apis/{group}/{version}/namespaces/{namespace}/{plural}/{name}'
        response = self.kubevirt_api(namespace, name, 'version', group='kubevirt.io',
                                         resource_path=resource_path, method='GET', **kwargs)
        metadata = response['metadata']
        annotations = metadata['annotations']
        return annotations['kubevirt.io/latest-observed-api-version']
