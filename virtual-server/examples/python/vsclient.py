import os

from kubernetes import client, config, watch

from kubevirtclient import KubeVirtClient


class VSClient:
    GROUP = 'virtualservers.coreweave.com'
    VERSION = 'v1alpha1'
    PLURAL = 'virtualservers'

    EXPECTED_CONDITIONS = {
        'Stopped': {
            'reason': 'VirtualServerStopped',
            'status': 'False',
            'type': 'Ready',
        },
        'Ready': {
            'reason': 'VirtualServerReady',
            'status': 'True',
            'type': 'Ready',
        },
        'Terminating': {
            'reason': 'Terminating',
            'status': 'False',
            'type': 'Ready',
        }
    }

    def __init__(self, kubeconfig_path=None):
        config.kube_config.load_kube_config(kubeconfig_path)

        self.api = client.CustomObjectsApi()
        self.kubevirt_api = KubeVirtClient(kubeconfig_path=kubeconfig_path)

    def create(self, manifest):
        """
        Create a new virtual server from the manifest.
        """
        if not manifest['metadata']:
            raise TypeError('VirtualServer metadata is required')
        namespace = manifest['metadata']['namespace']
        name = manifest['metadata']['name']
        if not namespace or not name:
            raise TypeError('VirtualServer metadata.namespace and metadata.name is required')
        return self.api.create_namespaced_custom_object(
            VSClient.GROUP, VSClient.VERSION, namespace, VSClient.PLURAL, manifest)

    def update(self, manifest):
        """
        Update virtual server according to the manifest.
        """
        if not manifest['metadata']:
            raise TypeError('VirtualServer metadata is required')
        namespace = manifest['metadata']['namespace']
        name = manifest['metadata']['name']
        if not namespace or not name:
            raise TypeError('VirtualServer metadata.namespace and metadata.name is required')
        return self.api.patch_namespaced_custom_object(
            VSClient.GROUP, VSClient.VERSION, namespace, VSClient.PLURAL, name, manifest)

    @staticmethod
    def match_condition(condition, expected_status):
        if expected_status in VSClient.EXPECTED_CONDITIONS:
            cond = VSClient.EXPECTED_CONDITIONS[expected_status]
            if 'reason' in condition and cond['reason'] == condition['reason'] and \
                    'status' in condition and cond['status'] == condition['status'] and \
                    'type' in condition and cond['type'] == condition['type']:
                return expected_status
        return None

    def ready(self, namespace, name, expected_state='Ready'):
        """
        Wait for virtual server until matches one of the expected condtion from EXPECTED_CONDITIONS
        """
        w = watch.Watch()
        kwargs = {
            'watch': True,
            'field_selector': f'metadata.name={name}'
        }
        ready_condition = None
        print(f'Waiting for virtual server to be {expected_state} ...')
        for event in w.stream(self.api.list_namespaced_custom_object,
                              VSClient.GROUP, VSClient.VERSION, namespace, VSClient.PLURAL, **kwargs):
            status = event['object'].get('status', dict())

            # the virtual server was already deleted
            if event['type'] == 'DELETE':
                ready_condition = 'Deleted'
                w.stop()
                break

            if 'conditions' not in status:
                continue

            # Check if new state matches the expected condition
            ready_condition = VSClient.match_condition(status['conditions'][0], expected_state)

            # Wait for next condition
            if not ready_condition:
                continue
            elif ready_condition == 'Ready':
                network = status['network']
                tcp_ip = network['externalIP'] if 'externalIP' in network else ''
                udp_ip = network['internalIP'] if 'internalIP' in network else ''
                print(f'{name}, external IP: {tcp_ip}, internal IP: {udp_ip}')
                w.stop()
            elif ready_condition == 'Stopped' or ready_condition == 'Terminating':
                w.stop()
        return ready_condition

    def get(self, namespace, name, pretty='true'):
        """
        Get description of the virtual sever.
        """
        return self.api.list_namespaced_custom_object(
            VSClient.GROUP, VSClient.VERSION, namespace, VSClient.PLURAL,
            field_selector=f'metadata.name={name}', pretty=pretty)

    def list(self, namespace, pretty='true'):
        """
        List all virtual servers from namespace.
        """
        return self.api.list_namespaced_custom_object(
            VSClient.GROUP, VSClient.VERSION, namespace, VSClient.PLURAL, pretty=pretty)

    def delete(self, namespace, name):
        """
        Delete the virtual server.
        """
        return self.api.delete_namespaced_custom_object(
            VSClient.GROUP, VSClient.VERSION, namespace, VSClient.PLURAL, name)
