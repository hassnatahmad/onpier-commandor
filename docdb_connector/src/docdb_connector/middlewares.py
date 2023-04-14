import logging
from contextvars import ContextVar
from os import path
from typing import Optional, Final

from fastapi import FastAPI, status, APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.routing import compile_path
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .config import STATIC_DIR
from .logging import configure_logging

log = logging.getLogger(__name__)

# we configure the logging level and format
configure_logging()
REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_path_params_from_request(request: Request, api_router: APIRouter) -> dict:
    path_params = {}
    for r in api_router.routes:
        path_regex, path_format, param_converters = compile_path(r.path)
        path = request["path"].removeprefix("/api/v1")  # remove the /api/v1 for matching
        match = path_regex.match(path)
        if match:
            path_params = match.groupdict()
    return path_params


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


def get_path_template(request: Request) -> str:
    if hasattr(request, "path"):
        return ",".join(request.path.split("/")[1:])
    return ".".join(request.url.path.split("/")[1:])


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def onpier(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> JSONResponse:
        try:
            response = await call_next(request)
        except ValidationError as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": e.errors()}
            )
        except ValueError as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]},
            )
        except Exception as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]},
            )

        return response


# class MetricsMiddleware(BaseHTTPMiddleware):
#     async def onpier(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
#         path_template = get_path_template(request)
#
#         method = request.method
#         tags = {"method": method, "endpoint": path_template}
#
#         try:
#             start = time.perf_counter()
#             response = await call_next(request)
#             elapsed_time = time.perf_counter() - start
#             tags.update({"status_code": response.status_code})
#             metric_provider.counter("server.call.counter", tags=tags)
#             metric_provider.timer("server.call.elapsed", value=elapsed_time, tags=tags)
#             log.debug(f"server.call.elapsed.{path_template}: {elapsed_time}")
#         except Exception as e:
#             metric_provider.counter("server.call.exception.counter", tags=tags)
#             raise e from None
#         return response


def attach_app_middleware(app: FastAPI):
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000 ; includeSubDomains"
        return response


def attach_frontend_middleware(frontend: FastAPI):
    @frontend.middleware("http")
    async def default_page(request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            if STATIC_DIR:
                return FileResponse(path.join(STATIC_DIR, "index.html"))
        return response
