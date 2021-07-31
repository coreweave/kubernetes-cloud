import os
import time
import sys

from kubernetes.client.rest import ApiException
from vsclient import VSClient

name = 'my-virtual-server'
namespace = os.environ.get('NAMESPACE', 'default')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

if username == None or password == None:
    print('USERNAME and PASSWORD environment variables are required')
    sys.exit()

my_virtualserver = {
    'apiVersion': f'{VSClient.GROUP}/{VSClient.VERSION}',
    'kind': 'VirtualServer',
    'metadata': {'name': name, 'namespace': namespace},
    'spec': {
        'region': 'ORD1',  # ord1, ewr1, ewr2
        'os': {
            'type': 'linux',
        },
        'resources': {
            'gpu': {
                'type': 'Quadro_RTX_4000',
                'count': 1
            },
            'cpu': {
                # GPU type and CPU type are mutually exclusive i.e. CPU type cannot be specified when GPU type is selected.
                # CPU is selected automatically based on GPU type.
                # 'type': 'amd-epyc-rome',
                'count': 2,
            },
            'memory': '16Gi'
        },
        'users': [
            {
                'username': username,
                'password': password,
            }
        ],
        'storage': {
            'root': {
                'size': '40Gi',
                'source': {
                    'pvc': {
                        'name': 'ubuntu1804-nvidia-465-19-01-1-docker-master-20210629-ord1',
                        'namespace': 'vd-images'
                    }
                },
                'storageClassName': 'block-nvme-ord1',
                'volumeMode': 'Block',
                'accessMode': 'ReadWriteOnce'
            }
        },
        'network': {
            'tcp': {
                'ports': [22, 443, 60443, 4172, 3389]
            },
            'udp': {
                'ports': [4172, 3389]
            }
        },
        'initializeRunning': True
    }
}


vsclient = VSClient()

try:
    vsclient.delete(namespace, name)
except ApiException as e:
    if e.status == 404:
        print(f'VirtualServer {name} in namespace {namespace} already deleted')
    else:
        print(f'VirtualServer delete exception {e}')
        exit(1)

# Create virtual server
print(vsclient.create(my_virtualserver))
print(f'VirtualServer status: {vsclient.ready(namespace, name)}')

# Stop virtual server
print(vsclient.kubevirt_api.stop(namespace, name))
print(f'VirtualServer status: {vsclient.ready(namespace, name, expected_state="Stopped")}')

# Delete virtual server
vsclient.delete(namespace, name)

exit(0)
