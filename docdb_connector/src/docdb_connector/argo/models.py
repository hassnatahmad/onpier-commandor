from docdb_connector.enums import OnpierEnum
from docdb_connector.models import OnpierBase


class ResolutionStatus(OnpierEnum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    REOPENED = "REOPENED"
    IGNORED = "IGNORED"


class ArgoCluster(OnpierBase):
    name: str
    url: str
    username: str
    password: str
    ignore_apps: list[str] | None = None


class ArgoAppHealthStatus(OnpierBase):
    status_id: str
    cluster: str
    namespace: str
    name: str
    health: str
    reason: str
    link: str
    team: str
    severity: str
    occurrence_type: str
    occurrence_at: str
    jira_ticket: str
    resolution_status: ResolutionStatus
    resolution_at: str
    resolution_comment: str
    resolution_by: str
