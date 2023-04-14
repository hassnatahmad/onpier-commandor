"""
CRUD Operations for User Endpoint
"""
from datetime import datetime
from typing import Dict, List

from loguru import logger

from docdb_connector.database.mongodb import AsyncIOMotorClient, get_database


async def total_docs_in_db(
        mongo_collection: str,
        find_condition: dict,
        mongo_db: str,
) -> int:
    """Get total documents in the database

    :param find_condition:
    :param mongo_collection:
    :param mongo_db:

    :return: INT count of the total docs in mongodb or 0 if none
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        if find_condition is not None:
            return await db_client[mongo_db][mongo_collection].count_documents(find_condition)
        else:
            return await db_client[mongo_db][mongo_collection].count_documents({})
    except Exception as e:

        return 0


async def get_all(
        mongo_db: str,
        mongo_collection: str,
        find_condition: dict = None,
        skip: int = 0,
        limit: int = 100,
        sort_by_key: str = None,
        sort_by_value: int = None,
) -> dict:
    """Get all users and their information

    :param sort_by_value:
    :param sort_by_key:
    :param db_name:
    :param values_to_return_or_skip:
    :param limit:
    :param skip:
    :param find_condition:
    :param mongo_db:
    :param mongo_collection:

    :return: dict of all docs
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        total_docs = await total_docs_in_db(mongo_collection=mongo_collection, find_condition=find_condition,
                                            mongo_db=mongo_db)
        docs = []
        if find_condition is not None:
            if sort_by_key is not None:
                async for row in db_client[mongo_db][mongo_collection].find(find_condition).skip(
                        skip
                ).limit(limit).sort(sort_by_key, sort_by_value if sort_by_value is not None else -1):
                    docs.append(row)
            else:
                async for row in db_client[mongo_db][mongo_collection].find(find_condition).skip(
                        skip
                ).limit(limit):
                    docs.append(row)
        else:
            async for row in db_client[mongo_db][mongo_collection].find({}).skip(skip).limit(
                    limit
            ):
                docs.append(row)

        return {"total": total_docs, "docs": docs}
    except Exception as e:

        return {"total": 0, "docs": [], "error": str(e)}


async def get_one(
        mongo_collection: str,
        find_condition: dict,
        values_to_return_or_skip: dict,
        mongo_db: str,
):
    """Get user info
    :param values_to_return_or_skip:
    :param mongo_db:
    :param find_condition:
    :param mongo_collection:
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        row = await db_client[mongo_db][mongo_collection].find_one(find_condition, values_to_return_or_skip)
        return row
    except Exception as e:

        return None


async def create_one(
        input_dict: dict,
        mongo_collection: str,
        mongo_db: str,
) -> str:
    """Create a New API User.
    Created API Key is not stored in the database. It will be sent to browser and an email
    sent to the email id provided, for the user to confirm the email id.

    :param mongo_db:
    :param mongo_collection:
    :param input_dict:

    :return: STR or None
    """
    input_dict.update({"created_at": datetime.utcnow(), "updated_at": datetime.utcnow()})
    db_client: AsyncIOMotorClient = await get_database()
    row = await db_client[mongo_db][mongo_collection].insert_one(input_dict)
    return row.inserted_id


async def create_many(
        input_dicts: list[Dict],
        mongo_collection: str,
        mongo_db: str,
) -> List[str]:
    """Create a New API User.
    Created API Key is not stored in the database. It will be sent to browser and an email
    sent to the email id provided, for the user to confirm the email id.

    :param input_dicts:
    :param mongo_db:
    :param mongo_collection:

    :return: list[STR] or None
    """
    docs = []
    for i in input_dicts:
        i.update({"created_at": datetime.utcnow(), "updated_at": datetime.utcnow()})
        docs.append(i)
    db_client: AsyncIOMotorClient = await get_database()
    rows = await db_client[mongo_db][mongo_collection].insert_many(docs)
    row_ids = rows.inserted_ids

    return row_ids


async def update_one(
        find_condition: dict,
        new_value: dict,
        mongo_collection: str,
        mongo_db: str,
        array_filters: dict = None,
):
    """Update a user with new details

    :param array_filters:
    :param new_value:
    :param find_condition:
    :param mongo_db:
    :param mongo_collection:

    :return: None
    """
    updated_values = {"$set": new_value}
    db_client: AsyncIOMotorClient = await get_database()
    row = await db_client[mongo_db][mongo_collection].update_one(filter=find_condition, update=updated_values,
                                                                 array_filters=array_filters)
    logger.info(f"db updated values: {new_value}")
    return row.matched_count


async def update_many(
        find_condition: dict,
        new_value: dict,
        mongo_collection: str,
        mongo_db: str,
        array_filters: list[Dict] = None,
):
    """Update a user with new details

    :param array_filters:
    :param new_value:
    :param find_condition:
    :param mongo_db:
    :param mongo_collection:

    :return: None
    """

    updated_values = {"$set": new_value}

    db_client: AsyncIOMotorClient = await get_database()
    if array_filters is not None:
        row = await db_client[mongo_db][mongo_collection].update_many(
            find_condition, updated_values, array_filters=array_filters
        )
    else:
        row = await db_client[mongo_db][mongo_collection].update_many(find_condition, updated_values)
    logger.info(f"db updated values: {new_value}")
    return row.modified_count


async def delete_one(
        mongo_collection: str,
        find_condition: dict,
        mongo_db: str,
):
    """Get user info
    :param mongo_db:
    :param find_condition:
    :param mongo_collection:
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        row = await db_client[mongo_db][mongo_collection].delete_one(find_condition)
        return row.deleted_count
    except Exception as e:

        return 0


async def delete_many(mongo_collection: str, find_condition: dict, mongo_db: str):
    """Get user info
    :param mongo_db:
    :param find_condition:
    :param mongo_collection:
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        rows = await db_client[mongo_db][mongo_collection].delete_many(find_condition)
        return rows.deleted_count
    except Exception as e:

        return 0


async def get_health_check():
    """Get DB Health Check
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        res = await db_client.admin.command("ping")
        return res
    except Exception as e:

        return {
            "error": "Error while getting health check",
            "error_message": str(e)
        }


async def get_all_distinct_values(mongo_collection: str, field_name: str,
                                  mongo_db: str):
    """Get All Distinct Values
    :param field_name:
    :param mongo_db:
    :param find_condition:
    :param mongo_collection:
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        res = await db_client[mongo_db][mongo_collection].distinct(field_name)
        return res
    except Exception as e:

        return [
            {
                "error": "Error while getting all distinct values",
                "error_message": str(e)
            }
        ]


async def get_all_dbs():
    """Get All Dbs
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        res = await db_client.list_database_names()
        return res
    except Exception as e:

        return [
            {
                "error": "Error while getting all databases",
                "error_message": str(e)
            }
        ]


async def get_all_collections(mongo_db: str):
    """Get All Collections
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        res = await db_client[mongo_db].list_collection_names()
        return res
    except Exception as e:

        return [
            {
                "error": "Error while getting all collections",
                "error_message": str(e)
            }
        ]


async def get_collection_schema(mongo_db: str, collection_name: str):
    """Get Collection Schema
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        res = await db_client[mongo_db][collection_name].find_one()
        return res
    except Exception as e:

        return [
            {
                "error": "Error while getting collection schema",
                "error_message": str(e)
            }
        ]


async def db_command(mongo_db: str, command: dict):
    """Run DB Command
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        res = await db_client[mongo_db].command(command)
        return res
    except Exception as e:

        return [
            {
                "error": "Error while running db command",
                "error_message": str(e)
            }
        ]


async def db_admin_command(command: dict):
    """Run DB Command
    :return: object
    """
    try:
        db_client: AsyncIOMotorClient = await get_database()
        res = await db_client.admin.command(command)
        return res
    except Exception as e:

        return [
            {
                "error": "Error while running db command",
                "error_message": str(e)
            }
        ]
