import logging

from ..database.interface import db_service
from ..exceptions import RecordNotFoundException

log = logging.getLogger(__name__)


async def get_all_dbs():
    return await db_service.get_all_dbs()


async def get_all_collections(mongo_db: str):
    return await db_service.get_all_collections(mongo_db=mongo_db)


async def get_collection_schema(mongo_db: str, collection_name: str):
    record = await db_service.get_collection_schema(mongo_db=mongo_db, collection_name=collection_name)
    if not record:
        raise RecordNotFoundException
    return record


async def db_command(mongo_db: str, command: dict):
    record = await db_service.db_command(mongo_db=mongo_db, command=command)
    if not record:
        raise RecordNotFoundException
    return record


async def db_admin_command(command: dict):
    record = await db_service.db_admin_command(command=command)
    if not record:
        raise RecordNotFoundException
    return record


async def get_collection_records(mongo_db: str, collection_name: str, query: dict, sort_by_key: str = None,
                                 sort_by_value: int = None, skip: int = 0, limit: int = 10000000000):
    record = await db_service.get_all_pagination_interface(mongo_db=mongo_db, mongo_collection=collection_name,
                                                           find_condition=query, sort_by_key=sort_by_key,
                                                           sort_by_value=sort_by_value, skip=skip, limit=limit)
    if not record:
        raise RecordNotFoundException
    return record


async def delete_collection_records(mongo_db: str, collection_name: str, query: dict):
    record = await db_service.delete_many_interface(mongo_db=mongo_db, mongo_collection=collection_name,
                                                    find_condition=query)
    if not record:
        raise RecordNotFoundException
    return record
