import datetime
import json
import logging
import time

from bson import ObjectId

from docdb_connector.database.crud import (
    delete_many,
    delete_one,
    get_all,
    get_one,
    get_all_dbs,
    get_all_collections,
    get_collection_schema,
    db_command,
    db_admin_command
)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        # timestamp
        elif isinstance(o, time.struct_time):
            return time.strftime("%Y-%m-%d %H:%M:%S", o)
        # serialize Timestamp(1679587437, 1)
        elif hasattr(o, "as_datetime"):
            return o.as_datetime().isoformat()

        return super().default(o)
        # return json.JSONEncoder.default(self, o)


def dict_anonymizer(_dict, what_not_to_anonymize: list = None):
    """Anonymize all the values in the dictionary"""
    if what_not_to_anonymize is None:
        what_not_to_anonymize = []
    for key, value in _dict.items():
        if isinstance(value, dict):
            dict_anonymizer(value, what_not_to_anonymize)
        elif isinstance(value, list):
            for v_i in value:
                if isinstance(v_i, dict):
                    dict_anonymizer(v_i, what_not_to_anonymize)
        elif key not in what_not_to_anonymize:
            _dict[key] = "****"

    return _dict


log = logging.getLogger(__name__)


def delete_none(_dict):
    """Delete None values recursively from all the dictionaries"""
    for key, value in list(_dict.items()):
        if isinstance(value, dict):
            delete_none(value)
        elif value is None:
            del _dict[key]
        elif isinstance(value, list):
            for v_i in value:
                if isinstance(v_i, dict):
                    delete_none(v_i)

    return _dict


class DbService:
    @staticmethod
    async def get_interface(find_condition: dict, mongo_collection: str, values_to_return_or_skip: dict = None,
                            mongo_db: str = None):
        try:
            row = await get_one(
                mongo_collection=mongo_collection,
                find_condition=find_condition,
                values_to_return_or_skip=values_to_return_or_skip, mongo_db=mongo_db
            )
            return row
        except Exception as err:  # noqa
            log.error(f"unable to get record: {find_condition} in collection:{mongo_collection} Error:  {err}")

    @staticmethod
    async def get_all_pagination_interface(
            mongo_collection: str,
            skip: int = 0,
            limit: int = 10000000000000,
            find_condition: dict = None,
            mongo_db: str = None,
            sort_by_key: str = None,
            sort_by_value: int = None,
    ) -> list:
        try:
            rows = await get_all(
                mongo_collection=mongo_collection,
                find_condition=find_condition,
                skip=skip,
                limit=limit,
                mongo_db=mongo_db,
                sort_by_key=sort_by_key,
                sort_by_value=sort_by_value
            )
            if len(rows["docs"]) > 0:
                return [json.loads(JSONEncoder().encode(row)) for row in rows["docs"]]
            return []
        except Exception as err:  # noqa
            log.error(f"unable to get records: {find_condition} in collection:{mongo_collection} Error:  {err}")

    @staticmethod
    async def delete_interface(find_condition: dict, mongo_collection: str, mongo_db: str = None):
        try:
            row = await delete_one(mongo_collection=mongo_collection, find_condition=find_condition,
                                   mongo_db=mongo_db)
            return row
        except Exception as err:  # noqa
            log.error(f"unable to delete record: {find_condition} in collection:{mongo_collection} Error:  {err}")

    @staticmethod
    async def delete_many_interface(find_condition: dict, mongo_collection: str, mongo_db: str = None):
        try:
            rows = await delete_many(mongo_collection=mongo_collection, find_condition=find_condition,
                                     mongo_db=mongo_db)
            return rows
        except Exception as err:  # noqa
            log.error(f"unable to delete record: {find_condition} in collection:{mongo_collection} Error:  {err}")

    @staticmethod
    async def get_all_dbs() -> list:
        try:
            dbs = await get_all_dbs()
            return dbs
        except Exception as err:
            log.error(err)
            return []

    @staticmethod
    async def get_all_collections(mongo_db: str) -> list:
        try:
            collections = await get_all_collections(mongo_db=mongo_db)
            return collections
        except Exception as err:
            log.error(err)
            return []

    @staticmethod
    async def get_collection_schema(mongo_db: str, collection_name: str) -> list:
        try:
            schema = await get_collection_schema(mongo_db=mongo_db, collection_name=collection_name)
            enc = json.loads(JSONEncoder().encode(schema)) if schema else []
            return enc
        except Exception as err:
            log.error(err)
            return []

    @staticmethod
    async def db_command(mongo_db: str, command: dict) -> list:
        try:
            result = await db_command(mongo_db=mongo_db, command=command)
            print(result)
            enc = json.loads(JSONEncoder().encode(result)) if result else []
            return enc
        except Exception as err:
            log.error(err)
            return []

    @staticmethod
    async def db_admin_command(command: dict) -> list:
        try:
            result = await db_admin_command(command=command)
            print(result)
            enc = json.loads(JSONEncoder().encode(result)) if result else []
            return enc
        except Exception as err:
            log.error(err)
            return []


db_service = DbService()
