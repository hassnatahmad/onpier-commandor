from typing import Annotated

from fastapi import APIRouter, Depends

from .models import (
    DbOutput, DbInput, DbCollectionInput, DbCollectionUpdateInput, DbCollectionInsertInput
)
from .service import get_all_dbs, get_all_collections, get_collection_schema, get_collection_records, \
    delete_collection_records, db_command, db_admin_command, update_collection_records, insert_collection_records
from ..deps import get_current_username

db_bot_router = APIRouter()


@db_bot_router.get(
    "",
    response_model=DbOutput,
)
async def get_db_list(basic_auth_user: Annotated[str, Depends(get_current_username)]) -> DbOutput:
    all_dbs = await get_all_dbs()
    return DbOutput(data=all_dbs)


@db_bot_router.post("/command")
async def get_db_admin_commands(basic_auth_user: Annotated[str, Depends(get_current_username)], command: dict,
                                ) -> DbOutput:
    all_records = await db_admin_command(command=command)
    return DbOutput(data=[all_records])


@db_bot_router.post("/collections")
async def get_db_collections_list(basic_auth_user: Annotated[str, Depends(get_current_username)],
                                  user_input: DbInput) -> DbOutput:
    all_collections = await get_all_collections(mongo_db=user_input.db_name)
    return DbOutput(data=all_collections)


@db_bot_router.post("/collections/schema", response_model=DbOutput)
async def get_db_collection_schema(basic_auth_user: Annotated[str, Depends(get_current_username)],
                                   user_input: DbCollectionInput) -> DbOutput:
    all_collections = await get_collection_schema(mongo_db=user_input.db_name,
                                                  collection_name=user_input.collection_name)
    return DbOutput(data=[all_collections])


@db_bot_router.post("/collections/records")
async def get_db_collection_records(basic_auth_user: Annotated[str, Depends(get_current_username)],
                                    user_input: DbCollectionInput, skip: int = 0, limit: int = 10000000000,
                                    sort_by_key: str = None, sort_by_value: int = None) -> DbOutput:
    all_records = await get_collection_records(mongo_db=user_input.db_name, collection_name=user_input.collection_name,
                                               query=user_input.query, skip=skip, limit=limit, sort_by_key=sort_by_key,
                                               sort_by_value=sort_by_value)
    return DbOutput(data=[all_records])


@db_bot_router.post("/collections/records/insert")
async def insert_db_collection_records(basic_auth_user: Annotated[str, Depends(get_current_username)],
                                       user_input: DbCollectionInsertInput) -> DbOutput:
    all_records = await insert_collection_records(mongo_db=user_input.db_name,
                                                  collection_name=user_input.collection_name,
                                                  what_to_insert=user_input.what_to_insert)
    return DbOutput(data=[all_records])


@db_bot_router.put("/collections/records")
async def update_db_collection_records(basic_auth_user: Annotated[str, Depends(get_current_username)],
                                       user_input: DbCollectionUpdateInput) -> DbOutput:
    all_records = await update_collection_records(mongo_db=user_input.db_name,
                                                  collection_name=user_input.collection_name,
                                                  query=user_input.query,
                                                  what_to_update=user_input.what_to_update)
    return DbOutput(data=[all_records])


@db_bot_router.delete("/collections/records")
async def delete_db_collection_records(basic_auth_user: Annotated[str, Depends(get_current_username)],
                                       user_input: DbCollectionInput) -> DbOutput:
    all_records = await delete_collection_records(mongo_db=user_input.db_name,
                                                  collection_name=user_input.collection_name,
                                                  query=user_input.query)
    return DbOutput(data=[all_records])


@db_bot_router.post("/{db_name}/delete")
async def delete_db(basic_auth_user: Annotated[str, Depends(get_current_username)], db_name: str, pin: str) -> DbOutput:
    if pin != "$ervice1":
        return DbOutput(data=[{"error": "Wrong pin"}])
    all_records = await db_command(mongo_db=db_name, command={"dropDatabase": 1})
    return DbOutput(data=[all_records])


@db_bot_router.post("/{db_name}/command")
async def get_db_commands(basic_auth_user: Annotated[str, Depends(get_current_username)], db_name: str, command: dict,
                          ) -> DbOutput:
    all_records = await db_command(mongo_db=db_name, command=command)
    return DbOutput(data=[all_records])
