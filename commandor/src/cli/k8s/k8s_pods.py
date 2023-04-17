from kubernetes.client.api import core_v1_api

from cli.k8s.k8s_common_utils import helper_utils
from cli.k8s.manifests import aws_docdb_migrator_yaml, aws_docdb_connector_yaml


def exec_command_in_aws_docdb_connector(k8s_v1_client: core_v1_api.CoreV1Api):
    command = ["apt-get update && apt-get install curl -y && curl http://localhost:8081/healthcheck"]
    helper_utils.exec_command_in_pod(k8s_v1_client=k8s_v1_client, pod_name='docdb-connector', command=command,
                                     namespace='default')


def aws_docdb_executor(k8s_v1_client: core_v1_api.CoreV1Api, action: str,cluster_name: str=None, app_name: str = 'docdb-connector'):
    if action == 'update':
        if app_name == 'docdb-connector':
            helper_utils.create_pod(k8s_v1_client=k8s_v1_client, pod_name='docdb-connector',
                                    namespace='default',
                                    pod_yaml=aws_docdb_connector_yaml(cluster_name=cluster_name),cluster_name=cluster_name)
        elif app_name == 'docdb-migrator':
            helper_utils.create_pod(k8s_v1_client=k8s_v1_client, pod_name='docdb-migrator', namespace='default',
                                    pod_yaml=aws_docdb_migrator_yaml(cluster_name=cluster_name),cluster_name=cluster_name)
    elif action == 'delete':
        if app_name == 'docdb-connector':
            helper_utils.delete_pod(k8s_v1_client=k8s_v1_client, pod_name='docdb-connector', namespace='default',cluster_name=cluster_name)
        elif app_name == 'docdb-migrator':
            helper_utils.delete_pod(k8s_v1_client=k8s_v1_client, pod_name='docdb-migrator', namespace='default',cluster_name=cluster_name)
    elif action == 'status':
        if app_name == 'docdb-connector':
            helper_utils.check_pod_status(k8s_v1_client=k8s_v1_client, pod_name='docdb-connector', namespace='default',cluster_name=cluster_name)
        elif app_name == 'docdb-migrator':
            helper_utils.check_pod_status(k8s_v1_client=k8s_v1_client, pod_name='docdb-migrator', namespace='default',cluster_name=cluster_name)
    elif action == 'logs':
        if app_name == 'docdb-connector':
            helper_utils.get_pod_logs(k8s_v1_client=k8s_v1_client, pod_name='docdb-connector', namespace='default',cluster_name=cluster_name)
        elif app_name == 'docdb-migrator':
            helper_utils.get_pod_logs(k8s_v1_client=k8s_v1_client, pod_name='docdb-migrator', namespace='default',cluster_name=cluster_name)
    else:
        print(f"Unknown action: {action}")


def aws_docdb_action(cluster_name: str, action: str, app_name: str = 'docdb-connector'):
    if cluster_name == 'all':
        all_connections = helper_utils.get_all_k8s_v1_clients()
        print("Getting all V1 clients: ")
        for connection in all_connections:
            aws_docdb_executor(k8s_v1_client=connection['core_v1'], action=action, app_name=app_name, cluster_name=connection['name'])
    elif cluster_name == 'prod':
        all_connections = helper_utils.get_all_k8s_v1_clients(skip_contexts=['dev', 'stage'])
        print("Getting all V1 clients: ")
        for connection in all_connections:
            aws_docdb_executor(k8s_v1_client=connection['core_v1'], action=action, app_name=app_name, cluster_name=connection['name'])
    elif cluster_name == 'dev':
        all_connections = helper_utils.get_all_k8s_v1_clients(skip_contexts=['prod', 'stage'])
        print("Getting all V1 clients: ")
        for connection in all_connections:
            aws_docdb_executor(k8s_v1_client=connection['core_v1'], action=action, app_name=app_name, cluster_name=connection['name'])

    else:
        print(f'Getting V1 client for cluster: "{cluster_name}"')
        connection = helper_utils.get_k8s_v1_client_by_name(context_name=cluster_name)
        aws_docdb_executor(k8s_v1_client=connection['core_v1'],
                           action=action, app_name=app_name, cluster_name=connection['name'])


def aws_docdb_delete(cluster_name: str, app_name: str = 'docdb-connector'):
    aws_docdb_action(
        cluster_name=cluster_name,
        action='delete',
        app_name=app_name
    )


def aws_docdb_update(cluster_name: str, app_name: str = 'docdb-connector'):
    aws_docdb_action(
        cluster_name=cluster_name,
        action='update',
        app_name=app_name
    )


def aws_docdb_status(cluster_name: str, app_name: str = 'docdb-connector'):
    aws_docdb_action(
        cluster_name=cluster_name,
        action='status',
        app_name=app_name
    )


def aws_docdb_logs(cluster_name: str, app_name: str = 'docdb-connector'):
    aws_docdb_action(
        cluster_name=cluster_name,
        action='logs',
        app_name=app_name
    )


def main():
    # aws_docdb_update(cluster_name='all', app_name='docdb-connector')
    aws_docdb_logs(cluster_name='all', app_name='docdb-connector')
    # aws_docdb_delete(cluster_name='all', app_name='docdb-connector')


test_command = {"modifyChangeStreams": 1,
                "database": "onpier-file-expose_file-expose-db",
                "collection": "FileMetadata",
                "enable": True}

if __name__ == '__main__':
    main()
