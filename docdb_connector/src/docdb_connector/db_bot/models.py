from docdb_connector.models import OnpierBase


class DbInput(OnpierBase):
    db_name: str


class DbCollectionInput(DbInput):
    collection_name: str
    query: dict | None = None


class DbCollectionUpdateInput(DbCollectionInput):
    what_to_update: dict | None = None


class DbCollectionInsertInput(DbCollectionInput):
    what_to_insert: list[dict] | None = None

class DbOutput(OnpierBase):
    data: list
