from fastapi import HTTPException
from pydantic.errors import PydanticValueError
from starlette import status


class OnpierException(Exception):
    pass


class OnpierPluginException(OnpierException):
    pass


class NotFoundError(PydanticValueError):
    code = "not_found"
    msg_template = "{msg}"


class FieldNotFoundError(PydanticValueError):
    code = "not_found.field"
    msg_template = "{msg}"


class ModelNotFoundError(PydanticValueError):
    code = "not_found.model"
    msg_template = "{msg}"


class ExistsError(PydanticValueError):
    code = "exists"
    msg_template = "{msg}"


class InvalidConfigurationError(PydanticValueError):
    code = "invalid.configuration"
    msg_template = "{msg}"


class InvalidFilterError(PydanticValueError):
    code = "invalid.filter"
    msg_template = "{msg}"


class InvalidUsernameError(PydanticValueError):
    code = "invalid.username"
    msg_template = "{msg}"


class InvalidPasswordError(PydanticValueError):
    code = "invalid.password"
    msg_template = "{msg}"


InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail=[{"msg": "Could not validate credentials"}]
)
RecordNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail=[{"msg": "Record not found"}]
)
