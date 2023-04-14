import logging
import os

log = logging.getLogger(__name__)

LOG_LEVEL = os.getenv("LOG_LEVEL", default=logging.INFO)
ENV = os.getenv("ENV", default="local")

ONPIER_UI_URL = os.getenv("ONPIER_UI_URL", default="http://localhost:8080")

# static files
DEFAULT_STATIC_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), os.path.join("static", "onpier", "dist")
)
STATIC_DIR = os.getenv("STATIC_DIR", default=DEFAULT_STATIC_DIR)

# AWS DocumentDB Pem file
RDS_COMBINED_CA_BUNDLE = os.getenv("RDS_COMBINED_CA_BUNDLE",
                                   default=f"{os.path.join(os.path.dirname(os.path.realpath(__file__)), 'certs', 'global-bundle.pem')}")
# check if file exists
if not os.path.isfile(RDS_COMBINED_CA_BUNDLE):
    raise FileNotFoundError(f"RDS_COMBINED_CA_BUNDLE file not found: {RDS_COMBINED_CA_BUNDLE}")
# metrics
METRIC_PROVIDERS = os.getenv("METRIC_PROVIDERS", default="")
MONGODB_MIN_POOL_SIZE = int(os.getenv("MONGODB_MIN_POOL_SIZE", default=5))
MONGODB_MAX_POOL_SIZE = int(os.getenv("MONGODB_MAX_POOL_SIZE", default=10))
MONGODB_URI = os.environ["MONGODB_URI"]
MONGO_DATABASE_URI = MONGODB_URI.replace("global-bundle.pem", RDS_COMBINED_CA_BUNDLE)
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", default="admin")
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME", default="admin")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD", default="admin")
