from typing import List, Optional

from docdb_connector.data.query.models import QueryRead
from docdb_connector.data.source.models import SourceRead
from docdb_connector.definition.models import DefinitionRead
from docdb_connector.document.models import DocumentRead
from docdb_connector.incident.models import IncidentRead
from docdb_connector.individual.models import IndividualContactRead
from docdb_connector.service.models import ServiceRead
from docdb_connector.tag.models import TagRead
from docdb_connector.task.models import TaskRead
from docdb_connector.team.models import TeamContactRead
from docdb_connector.term.models import TermRead
from pydantic import Field

from docdb_connector.models import DispatchBase


# Pydantic models...
class SearchBase(DispatchBase):
    query: Optional[str] = Field(None, nullable=True)


class SearchRequest(SearchBase):
    pass


class ContentResponse(DispatchBase):
    documents: Optional[List[DocumentRead]] = Field([], alias="Document")
    incidents: Optional[List[IncidentRead]] = Field([], alias="Incident")
    tasks: Optional[List[TaskRead]] = Field([], alias="Task")
    tags: Optional[List[TagRead]] = Field([], alias="Tag")
    terms: Optional[List[TermRead]] = Field([], alias="Term")
    definitions: Optional[List[DefinitionRead]] = Field([], alias="Definition")
    sources: Optional[List[SourceRead]] = Field([], alias="Source")
    queries: Optional[List[QueryRead]] = Field([], alias="Query")
    teams: Optional[List[TeamContactRead]] = Field([], alias="TeamContact")
    individuals: Optional[List[IndividualContactRead]] = Field([], alias="IndividualContact")
    services: Optional[List[ServiceRead]] = Field([], alias="Service")

    class Config:
        allow_population_by_field_name = True


class SearchResponse(DispatchBase):
    query: Optional[str] = Field(None, nullable=True)
    results: ContentResponse
