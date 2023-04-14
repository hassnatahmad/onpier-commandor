from motor.motor_asyncio import AsyncIOMotorClient

from docdb_connector.config import MONGO_DATABASE_URI, MONGODB_MAX_POOL_SIZE, MONGODB_MIN_POOL_SIZE


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    """Connect to MONGO DB"""
    db.client = AsyncIOMotorClient(
        MONGO_DATABASE_URI,
        maxPoolSize=MONGODB_MAX_POOL_SIZE,
        minPoolSize=MONGODB_MIN_POOL_SIZE,
    )
    # db.database = db.client[database]


async def close_mongo():
    """Close MongoDB Connection"""
    db.client.close()
