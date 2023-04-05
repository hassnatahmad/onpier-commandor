import os
import asyncio
from cli.k8s.k8s_common_utils import helper_utils
from kubernetes.client.api import core_v1_api


def pod_manifest(pod_name: str, namespace: str, image: str, port: int, env_vars: list[dict] = None,
                 labels: dict = None):
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": pod_name,
            "namespace": namespace,
            "labels": labels if labels is not None else {}
        },
        "spec": {
            "containers": [
                {
                    "name": pod_name,
                    "image": image,
                    "imagePullPolicy": "Always",
                    "ports": [
                        {
                            "containerPort": port
                        }
                    ],
                    "env": env_vars if env_vars is not None else []
                }
            ]
        }
    }


def check_pod_status(k8s_v1_client: core_v1_api.CoreV1Api, pod_name: str, namespace: str):
    pod = k8s_v1_client.read_namespaced_pod(name=pod_name, namespace=namespace)
    if pod.status.phase == 'Running':
        return True
    else:
        return False


def create_pod(k8s_v1_client: core_v1_api.CoreV1Api, manifest: dict, cluster_name: str = None):
    # check if pod already exists
    try:
        k8s_v1_client.read_namespaced_pod(name=manifest['metadata']['name'],
                                          namespace=manifest['metadata']['namespace'])
        print('Pod already exists')
        print(helper_utils.get_pod_logs(k8s_v1_client=k8s_v1_client, pod_name=manifest['metadata']['name'],
                                        namespace=manifest['metadata']['namespace'], cluster_name=cluster_name))
        return None
    except Exception as e:
        # print(e)
        k8s_v1_client.create_namespaced_pod(body=manifest, namespace='default')
        print(
            f'Pod {manifest["metadata"]["name"]} in namespace {manifest["metadata"]["namespace"]} cluster {cluster_name} created')
    helper_utils.check_pod_status(k8s_v1_client=k8s_v1_client, pod_name=manifest['metadata']['name'],
                                  namespace=manifest['metadata']['namespace'], status='Running',
                                  timeout=90)
    print(helper_utils.get_pod_logs(k8s_v1_client=k8s_v1_client, pod_name=manifest['metadata']['name'],
                                    namespace=manifest['metadata']['namespace'], cluster_name=cluster_name))


def aws_docdb_js(k8s_v1_client: core_v1_api.CoreV1Api, cluster_name: str = None):
    image = 'hassnatahmadpk/aws-docdb-py:v0.1.0-js'
    namespace = 'default'
    pod_name = 'aws-docdb-js'
    port = 8081
    labels = {
        "app": pod_name
    }
    env_vars = [
        {
            "name": "MONGODB_URI",
            "value": os.environ[f'{cluster_name}_MONGODB_URI']
        },
        {
            "name": "OLD_DB_NAME",
            "value": os.environ['OLD_DB_NAME']
        },
        {
            "name": "NEW_DB_NAME",
            "value": os.environ['NEW_DB_NAME']
        },
        {
            "name": "COLLECTION_NAME",
            "value": os.environ['COLLECTION_NAME']
        }
    ]
    manifest = pod_manifest(pod_name=pod_name, namespace=namespace, image=image, port=port, env_vars=env_vars,
                            labels=labels)
    create_pod(k8s_v1_client=k8s_v1_client, manifest=manifest, cluster_name=cluster_name)


def aws_docdb_py(k8s_v1_client: core_v1_api.CoreV1Api, cluster_name: str = None):
    image = 'hassnatahmadpk/aws-docdb-py:v0.1.10-py'
    namespace = 'default'
    pod_name = 'aws-docdb-py'
    port = 8081
    labels = {
        "app": pod_name
    }
    env_vars = [
        {
            "name": "MONGODB_URI",
            "value": os.environ[f'{cluster_name}_MONGODB_URI']
        },
        {
            "name": "CONTAINER_PORT",
            "value": str(port)
        },
        {
            "name": "BASIC_AUTH_USERNAME",
            "value": os.environ['BASIC_AUTH_USERNAME']
        },
        {
            "name": "BASIC_AUTH_PASSWORD",
            "value": os.environ['BASIC_AUTH_PASSWORD']
        }
    ]
    manifest = pod_manifest(pod_name=pod_name, namespace=namespace, image=image, port=port, env_vars=env_vars,
                            labels=labels)
    create_pod(k8s_v1_client=k8s_v1_client, manifest=manifest, cluster_name=cluster_name)


def delete_pod(k8s_v1_client: core_v1_api.CoreV1Api, pod_name: str, namespace: str, cluster_name: str):
    try:
        k8s_v1_client.delete_namespaced_pod(name=pod_name, namespace=namespace)
        print(f'Pod "{pod_name}" in namespace "{namespace}" cluster: "{cluster_name}" deleted')
    except Exception as e:
        print(f'Pod "{pod_name}" in namespace "{namespace}" cluster: "{cluster_name}" does not exist')
        return None


def exec_command_in_datadog_pod(k8s_v1_client: core_v1_api.CoreV1Api):
    command = ["curl", "http://localhost:8081/healthcheck"]
    helper_utils.exec_command_in_pod(k8s_v1_client=k8s_v1_client, pod_name='aws-docdb-py', command=command,
                                     namespaces='default')


def aws_docdb_py_status(cluster_name: str):
    if cluster_name == 'all':
        all_connections = helper_utils.get_all_k8s_v1_clients(skip_contexts=['hassnat-k8s'])
        print("Getting all V1 clients: ")
        for connection in all_connections:
            k8s_v1_client = connection['core_v1']
            print(f'Checking status of pod "aws-docdb-py" in cluster: "{connection["name"]}"')
            helper_utils.check_pod_status(k8s_v1_client=k8s_v1_client, pod_name='aws-docdb-py', namespace='default')
    else:
        print(f'Checking status of pod "aws-docdb-py" in cluster: "{cluster_name}"')
        k8s_v1_client = helper_utils.get_k8s_v1_client_by_name(context_name=cluster_name)
        helper_utils.check_pod_status(k8s_v1_client=k8s_v1_client, pod_name='aws-docdb-py', namespace='default')


def main():
    all_connections = helper_utils.get_all_k8s_v1_clients(skip_contexts=['hassnat-k8s'])
    print("Getting all V1 clients: ")
    for connection in all_connections:
        k8s_v1_client = connection['core_v1']
        cluster_name = connection['name']
        # aws_docdb_py(k8s_v1_client=k8s_v1_client, cluster_name=cluster_name)
        # aws_docdb_js(k8s_v1_client=k8s_v1_client, cluster_name=cluster_name)

        delete_pod(k8s_v1_client=k8s_v1_client, pod_name='aws-docdb-py', namespace='default',
                   cluster_name=cluster_name)
        # port_forward(k8s_v1_client=k8s_v1_client, pod_name='aws-docdb-py', port=8081, namespaces='default')
        # exec_command_in_datadog_pod(k8s_v1_client=k8s_v1_client)


test_command = {"modifyChangeStreams": 1,
                "database": "onpier-file-expose_file-expose-db",
                "collection": "FileMetadata",
                "enable": True}

if __name__ == '__main__':
    main()
