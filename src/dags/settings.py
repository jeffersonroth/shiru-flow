"""Global dags settings."""

import os
from datetime import timedelta
from typing import Any, Dict

from airflow.models.variable import Variable


def _get_default_args() -> Dict[str, Any]:
    """Get the default arguments."""
    return {
        "email": ["jjrothfilho@gmail.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "depends_on_past": False,
        "concurrency": 10,
        "retries": 2,
        "retry_delay": timedelta(minutes=0.5),
        "catchup": False,
    }

# General Settings
# Debug Mode
DEBUG_MODE_ON = True
try:
    import distutils, distutils.util

    DEBUG_MODE_ON = bool(
        distutils.util.strtobool(
            Variable.get("AIRFLOW_DEBUG_MODE_ON", default_var=True)
        )
    )
except Exception as exception:
    pass

# Base PATH
BASE_PATH = os.path.abspath(os.getcwd())

# Default S3 Bucket
DEFAULT_BUCKET_NAME = None
try:
    DEFAULT_BUCKET_NAME = Variable.get("DEFAULT_BUCKET_NAME")
except Exception as exception:
    pass

# Default dags args
DEFAULT_ARGS = _get_default_args()

# Connections
CONN_DEFAULTS = {
    "postgres": "postgres_default",
    "aws": "aws_default",
}
# Postgres
POSTGRES_CONN_ID = CONN_DEFAULTS["postgres"]
# AWS
AWS_CONN_ID = CONN_DEFAULTS["aws"]

