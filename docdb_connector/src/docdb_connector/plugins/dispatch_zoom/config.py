from dispatch.config import BaseConfigurationModel
from pydantic import Field, SecretStr


class ZoomConfiguration(BaseConfigurationModel):
    """Zoom configuration description."""

    api_user_id: str = Field(title="Zoom API User Id")
    api_key: str = Field(title="API Key")
    api_secret: SecretStr = Field(title="API Secret")
