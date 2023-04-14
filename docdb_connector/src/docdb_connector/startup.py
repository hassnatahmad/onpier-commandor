from fastapi import FastAPI
from loguru import logger

from docdb_connector.database.mongodb import connect_to_mongo, close_mongo


def attach_app_init(app: FastAPI) -> None:
    @app.on_event("startup")
    async def start_up() -> None:
        logger.info("Starting app startup")
        logger.info("connecting to mongo.................")
        """ Startup functionality """
        await connect_to_mongo()
        logger.info("connected to mongo.")

    @app.on_event("shutdown")
    async def on_app_shutdown():
        """Anything that needs to be done while app shutdown"""
        logger.info("Shutting down app")
        await close_mongo()
