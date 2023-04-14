from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from docdb_connector.argo.views import argo_router
from docdb_connector.db_bot.views import db_bot_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

# WARNING: Don't use this unless you want unauthenticated routes
unauthenticated_api_router = APIRouter()

unauthenticated_api_router.include_router(argo_router, prefix="/argo", tags=["ArgoCD"])
unauthenticated_api_router.include_router(db_bot_router, prefix="/db", tags=["DB Bot"])


# authenticated_organization_api_router = APIRouter(prefix="/{organization}")
# authenticated_organization_api_router.include_router(case_router, prefix="/cases", tags=["cases"])


@api_router.get("/healthcheck", include_in_schema=True)
def healthcheck():
    return {"status": "ok"}


api_router.include_router(
    unauthenticated_api_router,
    # dependencies=[Depends(get_current_user)],
)
