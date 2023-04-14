import logging
import uuid

import httpx
from fastapi import HTTPException
from fastapi import status

from .models import (
    ArgoAppHealthStatus, ResolutionStatus,
)

log = logging.getLogger(__name__)

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail=[{"msg": "Could not validate credentials"}]
)


def get_argo_token(url: str, username: str, password: str):
    response = httpx.post(f"{url}/api/v1/session", json={"username": username, "password": password})
    if response.status_code != 200:
        raise Exception("Could not validate credentials")
    return response.json()["token"]


def call_argo_api(url: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(url, headers=headers)
    if response.status_code == 401:
        raise InvalidCredentialException
    return response.json()


def get_argo_app_health_status(
        argo_url: str, argo_token: str, cluster_name: str, ignore_apps: list[str] = None
) -> list[ArgoAppHealthStatus]:
    response = call_argo_api(f"{argo_url}/api/v1/applications", argo_token)
    result = []
    for application in response["items"]:
        should_ignore = False
        if ignore_apps is not None:
            for ignore_app in ignore_apps:
                if ignore_app in application["metadata"]["name"]:
                    should_ignore = True
                    break
        if should_ignore:
            continue
        if application["status"]["health"]["status"] != "Healthy":
            resources = application["status"]["resources"]
            for resource in resources:
                if resource.get("health") is not None and resource["health"]["status"] != "Healthy":
                    # node=apps%2FDeployment%2Fingress-nginx%2Fingress-nginx-controller%2F0
                    node = f"{resource['group']}/{resource['kind']}/{resource['namespace']}/{resource['name']}/0"
                    reason = resource["health"].get("message")
                    if reason is None:
                        reason = "Unknown"
                    label = resource["health"].get("label")

                    result.append(ArgoAppHealthStatus(
                        status_id=uuid.uuid4().hex,
                        cluster=cluster_name,
                        namespace=application["metadata"]["namespace"],
                        name=application["metadata"]["name"],
                        health=resource["health"]["status"],
                        reason=reason,
                        link=f"{argo_url}/applications/{application['metadata']['name']}?node={node}",
                        team="croods",
                        severity="critical",
                        occurrence_type="New",
                        occurrence_at=application["metadata"]["creationTimestamp"],
                        jira_ticket="",
                        resolution_status=ResolutionStatus.OPEN,
                        resolution_at="",
                        resolution_comment="", resolution_by="",

                    ))
    notify_slack(failed_apps=result)
    return result


def open_jira_ticket():
    pass


def notify_slack(failed_apps: list[ArgoAppHealthStatus],
                 slack_webhook_url: str = "https://hooks.slack.com/services/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"):
    if len(failed_apps) == 0:
        return
    for app in failed_apps:
        message = f"Cluster: *{app.cluster}* App: *{app.name}* Health: *{app.health}* Reason: *{app.reason}* <{app.link}|Link>"
        resp = httpx.post(slack_webhook_url, json={"text": message})
        if resp.status_code != 200:
            log.error(f"Failed to notify slack. Response: {resp.text}")
