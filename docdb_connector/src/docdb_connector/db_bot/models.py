from docdb_connector.models import OnpierBase


class DbInput(OnpierBase):
    db_name: str


class DbCollectionInput(DbInput):
    collection_name: str
    query: dict | None = None


class DbOutput(OnpierBase):
    data: list
