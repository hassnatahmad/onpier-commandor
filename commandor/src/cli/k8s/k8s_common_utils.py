import base64
import json
import os

from dotenv import load_dotenv
from kubernetes import config
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


class HelperUtils:
    def __init__(self):
        load_dotenv()

    @staticmethod
    def anonymize_dict(d: dict):
        for key, value in d.items():
            if isinstance(value, dict):
                HelperUtils.anonymize_dict(value)
            elif isinstance(value, str):
                d[key] = '****'
        return d

    @staticmethod
    def base64_decode_secret(secret: str):
        return base64.b64decode(secret).decode('utf-8')

    @staticmethod
    def base64_encode_secret(secret: str):
        return base64.b64encode(secret.encode('utf-8'))

    @staticmethod
    def save_json_file(file_name: str, data: dict):
        save_path = os.path.join(
            # go to parent directory
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            '.secret_data',
            file_name
        )
        with open(save_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_json_file(file_name: str):
        save_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            '.secret_data',
            file_name
        )
        with open(save_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def load_kube_config(context_name: str = None) -> list[str]:
        print('Loading kube config............................')
        config.load_kube_config()
        all_contexts, current_context = config.list_kube_config_contexts()
        if context_name is not None:
            all_contexts = [x['name'] for x in all_contexts if context_name in x['name']]
        else:
            all_contexts = [x['name'] for x in all_contexts]
        return all_contexts

    @staticmethod
    def get_v1_client(context_name: str):
        return core_v1_api.CoreV1Api(api_client=config.new_client_from_config(context=context_name))

    @staticmethod
    def get_all_k8s_v1_clients(skip_contexts: list[str] = None):
        if skip_contexts is None:
            skip_contexts = ['hassnat-k8s']
        else:
            skip_contexts.append('hassnat-k8s')
        all_contexts = HelperUtils.load_kube_config()
        all_connections = []
        for context_full_name in all_contexts:
            cluster_name = context_full_name.split('/')[1] if '/' in context_full_name else context_full_name
            if skip_contexts is not None and [x for x in skip_contexts if x in cluster_name]:
                continue
            all_connections.append({
                'name': cluster_name,
                'core_v1': HelperUtils.get_v1_client(context_full_name)
            })
        return all_connections

    @staticmethod
    def get_k8s_v1_client_by_name(context_name: str):
        cluster_contexts = HelperUtils.load_kube_config(context_name=context_name)
        if len(cluster_contexts) == 0:
            raise Exception(f'No context found for {context_name}')
        return {
            'name': context_name,
            'core_v1': HelperUtils.get_v1_client(cluster_contexts[0])
        }

    @staticmethod
    def exec_command_in_pod(k8s_v1_client: core_v1_api.CoreV1Api, namespace: str, pod_name: str, command: list[str]):
        try:
            resp = stream(
                k8s_v1_client.connect_get_namespaced_pod_exec,
                pod_name,
                namespace,
                command=command,
                stderr=True, stdin=False,
                stdout=True, tty=False,
                _preload_content=False
            )
            while resp.is_open():
                resp.update(timeout=1)
                if resp.peek_stdout():
                    print("STDOUT: %s" % resp.read_stdout())
                if resp.peek_stderr():
                    print("STDERR: %s" % resp.read_stderr())
        except ApiException as e:
            print("Exception when calling CoreV1Api->connect_get_namespaced_pod_exec: %s " % e)

    @staticmethod
    def check_pod_status(k8s_v1_client: core_v1_api.CoreV1Api, pod_name: str, namespace: str, cluster_name: str,
                         status: str = 'Running',
                         timeout: int = 0):
        try:
            pod = k8s_v1_client.read_namespaced_pod(name=pod_name, namespace=namespace)
            if pod.status.phase == status:
                print(f'Pod {pod_name} is {status} in cluster {cluster_name}')
                return True
        except ApiException as e:
            print(f"Unable to read pod {pod_name} in cluster {cluster_name}. Reason: Not found")
            return False
            # print(f'Exception when calling CoreV1Api->read_namespaced_pod: {e}')

    @staticmethod
    def create_pod(k8s_v1_client: core_v1_api.CoreV1Api, pod_name: str, namespace: str, pod_yaml: dict,
                   cluster_name: str):
        if HelperUtils.check_pod_status(k8s_v1_client=k8s_v1_client, pod_name=pod_name, namespace=namespace,
                                        cluster_name=cluster_name):
            print(f'Pod {pod_name} already exists in cluster {cluster_name}. Skipping creation.')
            return True
        try:
            k8s_v1_client.create_namespaced_pod(namespace=namespace, body=pod_yaml)
            print(f'Pod {pod_name} created successfully in cluster {cluster_name}.')
            return True
        except ApiException as e:
            print(f'Unable to create pod {pod_name} in cluster {cluster_name}. Exception: {e}')
            return False

    @staticmethod
    def delete_pod(k8s_v1_client: core_v1_api.CoreV1Api, pod_name: str, namespace: str, cluster_name: str):
        try:
            k8s_v1_client.delete_namespaced_pod(name=pod_name, namespace=namespace)
            print(f'Pod {pod_name} deleted successfully in cluster {cluster_name}.')
        except ApiException as e:
            print(f'Unable to delete pod {pod_name} in cluster {cluster_name}. Reason: {e}')

    # if pod.status.phase == status:
    #     print(f'Pod {pod_name} is {status}. Hurray!')
    # else:
    #     if timeout == 0:
    #         print(f'Pod {pod_name} is not {status}. Please check manually or increase timeout.')
    #     else:
    #         max_retry = int(timeout / 5)
    #         retry = 0
    #         print(f'Waiting for pod {pod_name} to be {status}. Timeout: {timeout} seconds')
    #         while retry < max_retry:
    #             time.sleep(5)
    #             pod = k8s_v1_client.read_namespaced_pod(name=pod_name, namespace=namespace)
    #             if pod.status.phase == status:
    #                 print(f'Pod {pod_name} is {status}. Hurray!')
    #                 break
    #             print(
    #                 f'Waiting for pod {pod_name} to be in {status} state, current: {pod.status.phase}. Timeout: {timeout} seconds. Retry: {retry}/{max_retry}')
    #             retry += 1

    @staticmethod
    def get_pod_logs(k8s_v1_client: core_v1_api.CoreV1Api, pod_name: str, namespace: str, cluster_name: str):
        logs = k8s_v1_client.read_namespaced_pod_log(name=pod_name, namespace=namespace)
        print(f'Logs for pod {pod_name} in cluster {cluster_name}:\n{logs}')


helper_utils = HelperUtils()
