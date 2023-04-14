from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from .api import api_router
from .extensions import configure_extensions
from .startup import attach_app_init

configure_extensions()


async def not_found():
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": [{"msg": "Not Found."}]}
    )


exception_handlers = {404: not_found}

# we create the Web API framework
app = FastAPI(
    title="Onpier DocDB Connector API",
    description="Welcome to Onpier's DocDB Connector API.",

    #    exception_handlers=exception_handlers,
)

attach_app_init(app)

# we add all API routes to the Web API framework
app.include_router(api_router)
