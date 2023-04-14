from enum import Enum


class OnpierEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class Visibility(OnpierEnum):
    open = "Open"
    restricted = "Restricted"


class UserRoles(OnpierEnum):
    owner = "Owner"
    manager = "Manager"
    admin = "Admin"
    member = "Member"


class SearchTypes(OnpierEnum):
    definition = "Definition"
    document = "Document"
    incident = "Incident"
    incident_priority = "IncidentPriority"
    incident_type = "IncidentType"
    individual_contact = "IndividualContact"
    plugin = "Plugin"
    query = "Query"
    search_filter = "SearchFilter"
    service = "Service"
    source = "Source"
    tag = "Tag"
    task = "Task"
    team_contact = "TeamContact"
    term = "Term"
