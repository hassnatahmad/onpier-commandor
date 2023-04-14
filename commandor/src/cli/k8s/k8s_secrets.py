from k8s_common_utils import helper_utils


def annotation_filter(secret, annotations):
    metadata = secret.metadata
    found_annotations = metadata.annotations if metadata.annotations is not None else {}
    for annotation in annotations:
        if annotation in found_annotations:
            return True
    return False


def name_filter(secret, name):
    if name in secret.metadata.name:
        return True
    else:
        return False


def get_all_ns_secret(k8s_v1_client, annotations=None, name=None):
    found_secrets = []
    for secret in k8s_v1_client.list_secret_for_all_namespaces().items:
        if annotations is not None:
            if not annotation_filter(secret, annotations):
                continue
        if name is not None:
            if not name_filter(secret, name):
                continue
        found_secrets.append({
            'namespace': secret.metadata.namespace,
            'secret_name': secret.metadata.name,
            # 'annotations': secret.metadata.annotations
        })

    return found_secrets


def get_secret(k8s_v1_client, namespace, secret_name):
    secret = k8s_v1_client.read_namespaced_secret(namespace=namespace, name=secret_name)
    if secret is not None:
        # check if secret has to be decoded
        if secret.type == 'kubernetes.io/tls':
            return {
                'tls.crt': secret.data['tls.crt'],
                'tls.key': secret.data['tls.key']
            }
        elif secret.type == 'Opaque':
            # base64 decode secret data if it is not binary
            decoded_data = {}
            for key, value in secret.data.items():
                try:
                    decoded_data[key] = helper_utils.base64_decode_secret(value)
                except UnicodeDecodeError:
                    decoded_data[key] = value
            return decoded_data
        else:
            return {}
    else:
        return {}


def save_all_clusters_secrets(all_connections: list[dict], annotations=None, anonymize=False):
    all_secrets = []
    for connection in all_connections:
        k8s_v1_client = connection['core_v1']
        cluster_name = connection['name']
        print('Getting secrets from context: ' + cluster_name)
        found_secrets = get_all_ns_secret(k8s_v1_client, annotations=annotations)
        # found_secrets = get_all_ns_secret(k8s_v1_client,name='-db')
        secrets_metadata = []
        for secret in found_secrets:
            # skip namespace whose name contains '-pr-'
            if '-pr-' in secret['namespace'] or 'keycloak' != secret['namespace']:
                # print('Skipping secret: ' + secret['secret_name'] + ' in namespace: ' + secret['namespace'])
                continue
            secret_details = get_secret(k8s_v1_client, secret['namespace'], secret['secret_name'])
            if secret_details != {}:
                secrets_metadata.append({
                    'namespace': secret['namespace'],
                    'secret_name': secret['secret_name'],
                    'data': secret_details if not anonymize else helper_utils.anonymize_dict(secret_details)
                })
        all_secrets.append({
            'cluster': cluster_name,
            'secrets': secrets_metadata
        })
    # save all secrets to json file
    print('Saving secrets to file: k8s_secrets.json')
    helper_utils.save_json_file('k8s_secrets.json', {
        'ClusterName': 'k8s',
        'Secrets': all_secrets
    })


def main():
    all_connections = helper_utils.get_all_k8s_v1_clients(skip_contexts=['hassnat'])
    save_all_clusters_secrets(all_connections=all_connections, annotations=['sealedsecrets.bitnami.com/namespace-wide',
                                                                            'sealedsecrets.bitnami.com/cluster-wide'])


if __name__ == '__main__':
    main()
