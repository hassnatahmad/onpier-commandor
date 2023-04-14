from fastapi import APIRouter, HTTPException, status

from .models import (
    ArgoAppHealthStatus, ArgoCluster
)
from .service import get_argo_app_health_status, get_argo_token

argo_router = APIRouter()


@argo_router.post(
    "",
    response_model=list[ArgoAppHealthStatus],
)
def get_argo_health(user_input: list[ArgoCluster]):
    apps = []
    for cluster in user_input:
        try:
            token = get_argo_token(cluster.url, cluster.username, cluster.password)
            apps.extend(get_argo_app_health_status(
                argo_url=cluster.url,
                argo_token=token,
                ignore_apps=cluster.ignore_apps,
                cluster_name=cluster.name,
            ))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=[{"msg": f"Could not validate credentials for cluster {cluster.name}"}],
            )

    if len(apps) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "Could not find any argo app with degraded health status"}],
        )

    return apps
