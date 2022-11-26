"""dbt Profiles."""

from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any, Dict
from airflow.models.variable import Variable
import utils.logging as logging


@unique
@dataclass
class ProfileTarget(str, Enum):
    """dbt Profile Target."""

    TEST = "test"
    DEFAULT = "test"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        return cls.DEFAULT


ProfileTargetVariable = namedtuple("ProfileTargetVariable", ["key", "value", "export"])


@dataclass
class ProfileTargetVariables:
    """Airflow Variables for dbt Profile Target."""

    target: ProfileTarget = field(default=ProfileTarget(None))  # type: ignore

    @staticmethod
    def get_profile_target_variable(key) -> ProfileTargetVariable:
        value = None
        try:
            value = Variable.get(key=key)
        except Exception as exception:
            logging.error(exc=exception)
        export = f' export {key}="{value}";'
        return ProfileTargetVariable(key=key, value=value, export=export)

    @property
    def host(self) -> ProfileTargetVariable:
        key = f"DBT_{self.target.value}_POSTGRES_HOST".upper()
        return self.get_profile_target_variable(key=key)

    @property
    def user(self) -> ProfileTargetVariable:
        key = f"DBT_{self.target.value}_POSTGRES_USERNAME".upper()
        return self.get_profile_target_variable(key=key)

    @property
    def password(self) -> ProfileTargetVariable:
        key = f"DBT_{self.target.value}_POSTGRES_PASSWORD".upper()
        return self.get_profile_target_variable(key=key)

    @property
    def port(self) -> ProfileTargetVariable:
        key = f"DBT_{self.target.value}_POSTGRES_PORT".upper()
        return self.get_profile_target_variable(key=key)

    @property
    def dbname(self) -> ProfileTargetVariable:
        key = f"DBT_{self.target.value}_POSTGRES_DATABASE".upper()
        return self.get_profile_target_variable(key=key)

    @property
    def schema(self) -> ProfileTargetVariable:
        key = f"DBT_{self.target.value}_POSTGRES_SCHEMA".upper()
        return self.get_profile_target_variable(key=key)

    @property
    def threads(self) -> ProfileTargetVariable:
        key = f"DBT_{self.target.value}_POSTGRES_THREADS".upper()
        return self.get_profile_target_variable(key=key)

    def export_command(self) -> Dict[str, Any]:
        return {
            self.host.key: self.host.export,
            self.user.key: self.user.export,
            self.password.key: self.password.export,
            self.port.key: self.port.export,
            self.dbname.key: self.dbname.export,
            self.schema.key: self.schema.export,
            self.threads.key: self.threads.export,
        }

    def __repr__(self) -> str:
        repr_str = f"{self.host.key}"
        return repr_str
