from kubernetes.client.api import core_v1_api

from cli.k8s.k8s_common_utils import helper_utils
from cli.k8s.manifests import aws_docdb_migrator_yaml, aws_docdb_connector_yaml


def exec_command_in_aws_docdb_connector(k8s_v1_client: core_v1_api.CoreV1Api):
    command = ["apt-get update && apt-get install curl -y && curl http://localhost:8081/healthcheck"]
    helper_utils.exec_command_in_pod(k8s_v1_client=k8s_v1_client, pod_name='docdb-connector', command=command,
                                     namespace='default')


def aws_docdb_status(cluster_name: str, app_name: str = 'docdb-connector'):
    if cluster_name == 'all':
        all_connections = helper_utils.get_all_k8s_v1_clients()
        print("Getting all V1 clients: ")
        for connection in all_connections:
            k8s_v1_client = connection['core_v1']
            print(f'Checking status of pod "docdb-connector" in cluster: "{connection["name"]}"')
            if app_name == 'docdb-connector':
                # exec_command_in_aws_docdb_connector(k8s_v1_client=k8s_v1_client)
                helper_utils.check_pod_status(k8s_v1_client=k8s_v1_client, pod_name='docdb-connector',
                                              namespace='default')
            elif app_name == 'docdb-migrator':
                helper_utils.check_pod_status(k8s_v1_client=k8s_v1_client, pod_name='docdb-migrator',
                                              namespace='default')
    else:
        print(f'Checking status of pod "docdb-connector" in cluster: "{cluster_name}"')
        connection = helper_utils.get_k8s_v1_client_by_name(context_name=cluster_name)
        if app_name == 'docdb-connector':
            helper_utils.check_pod_status(k8s_v1_client=connection['core_v1'], pod_name='docdb-connector',
                                          namespace='default')
        elif app_name == 'docdb-migrator':
            helper_utils.check_pod_status(k8s_v1_client=connection['core_v1'], pod_name='docdb-migrator',
                                          namespace='default')


def aws_docdb_logs(cluster_name: str, app_name: str = 'docdb-connector'):
    if cluster_name == 'all':
        all_connections = helper_utils.get_all_k8s_v1_clients()
        print("Getting all V1 clients: ")
        for connection in all_connections:
            k8s_v1_client = connection['core_v1']
            cluster_name = connection['name']
            if app_name == 'docdb-connector':
                print(
                    f'Getting logs for pod {app_name} in {cluster_name}.........................................................')
                helper_utils.get_pod_logs(k8s_v1_client=k8s_v1_client, pod_name='docdb-connector', namespace='default')
            elif app_name == 'docdb-migrator':
                print(
                    f'Getting logs for pod {app_name} in {cluster_name}..........................................................')
                helper_utils.get_pod_logs(k8s_v1_client=k8s_v1_client, pod_name='docdb-migrator', namespace='default')
    else:
        print(f'Getting logs of pod "docdb-connector" in cluster: "{cluster_name}"')
        connection = helper_utils.get_k8s_v1_client_by_name(context_name=cluster_name)
        if app_name == 'docdb-connector':
            print(f'Getting logs for pod {app_name} in {cluster_name}.................')
            helper_utils.get_pod_logs(k8s_v1_client=connection['core_v1'], pod_name='docdb-connector',
                                      namespace='default')
        elif app_name == 'docdb-migrator':
            print(f'Getting logs for pod {app_name} in {cluster_name}.................')
            helper_utils.get_pod_logs(k8s_v1_client=connection['core_v1'], pod_name='docdb-migrator',
                                      namespace='default')


def aws_docdb_delete(cluster_name: str, app_name: str = 'docdb-connector'):
    if cluster_name == 'all':
        all_connections = helper_utils.get_all_k8s_v1_clients()
        print("Getting all V1 clients: ")
        for connection in all_connections:
            k8s_v1_client = connection['core_v1']
            print(f'Deleting pod "docdb-connector" in cluster: "{connection["name"]}"')
            if app_name == 'docdb-connector':
                helper_utils.delete_pod(k8s_v1_client=k8s_v1_client, pod_name='docdb-connector', namespace='default')
            elif app_name == 'docdb-migrator':
                helper_utils.delete_pod(k8s_v1_client=k8s_v1_client, pod_name='docdb-migrator', namespace='default')
    else:
        print(f'Deleting pod "docdb-connector" in cluster: "{cluster_name}"')
        connection = helper_utils.get_k8s_v1_client_by_name(context_name=cluster_name)
        if app_name == 'docdb-connector':
            helper_utils.delete_pod(k8s_v1_client=connection['core_v1'], pod_name='docdb-connector',
                                    namespace='default')
        elif app_name == 'docdb-migrator':
            helper_utils.delete_pod(k8s_v1_client=connection['core_v1'], pod_name='docdb-migrator', namespace='default')


def aws_docdb_update(cluster_name: str, app_name: str = 'docdb-connector'):
    if cluster_name == 'all':
        all_connections = helper_utils.get_all_k8s_v1_clients()
        print("Getting all V1 clients: ")
        for connection in all_connections:
            print(f'Updating pod "docdb-connector" in cluster: "{connection["name"]}"')
            if app_name == 'docdb-connector':
                helper_utils.create_pod(k8s_v1_client=connection['core_v1'], pod_name='docdb-connector',
                                        namespace='default',
                                        pod_yaml=aws_docdb_connector_yaml(cluster_name=connection['name']))
            elif app_name == 'docdb-migrator':
                helper_utils.create_pod(k8s_v1_client=connection['core_v1'], pod_name='docdb-migrator',
                                        namespace='default',
                                        pod_yaml=aws_docdb_migrator_yaml(cluster_name=connection['name']))
    else:
        print(f'Updating pod "docdb-connector" in cluster: "{cluster_name}"')
        connection = helper_utils.get_k8s_v1_client_by_name(context_name=cluster_name)
        if app_name == 'docdb-connector':
            helper_utils.create_pod(k8s_v1_client=connection['core_v1'], pod_name='docdb-connector',
                                    namespace='default',
                                    pod_yaml=aws_docdb_connector_yaml(cluster_name=connection['name']))
        elif app_name == 'docdb-migrator':
            helper_utils.create_pod(k8s_v1_client=connection['core_v1'], pod_name='docdb-migrator', namespace='default',
                                    pod_yaml=aws_docdb_migrator_yaml(cluster_name=connection['name']))


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
