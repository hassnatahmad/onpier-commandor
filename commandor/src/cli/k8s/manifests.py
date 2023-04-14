import os


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


def aws_docdb_migrator_yaml(cluster_name: str = None):
    image = 'hassnat/toolkit:docdb-migrator-v1.0.1'
    namespace = 'default'
    pod_name = 'docdb-migrator'
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
    return manifest


def aws_docdb_connector_yaml(cluster_name: str = None):
    image = 'hassnat/toolkit:docdb-connector-v1.0.10'
    namespace = 'default'
    pod_name = 'docdb-connector'
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
    return pod_manifest(pod_name=pod_name, namespace=namespace, image=image, port=port, env_vars=env_vars,
                        labels=labels)
