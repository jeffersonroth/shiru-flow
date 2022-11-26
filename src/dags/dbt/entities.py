"""dbt Entities."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import utils.dbt as dbt_utils
from airflow.models.variable import Variable
from utils.logging import critical, debug, error, info, warning

from dbt.profiles import ProfileTarget, ProfileTargetVariables


@dataclass
class ProfilesConfig(dbt_utils.ProfilesConfigProtocol):
    """dbt Profiles Config."""

    send_anonymous_usage_stats: Optional[bool] = field(default=None)
    use_colors: Optional[bool] = field(default=None)
    partial_parse: Optional[bool] = field(default=None)
    printer_width: Optional[int] = field(default=None)
    write_json: Optional[bool] = field(default=None)
    warn_error: Optional[bool] = field(default=None)
    log_format: Optional[bool] = field(default=None)
    debug: Optional[bool] = field(default=None)
    version_check: Optional[bool] = field(default=None)
    fail_fast: Optional[bool] = field(default=None)
    use_experimental_parser: Optional[bool] = field(default=None)
    static_parser: Optional[bool] = field(default=None)


@dataclass
class Target(dbt_utils.TargetProtocol):
    """dbt Project Profiles Profile Outputs Target."""

    name: ProfileTarget
    type: Optional[str] = field(default=None)
    host: Optional[str] = field(default=None)
    user: Optional[str] = field(default=None)
    password: Optional[str] = field(default=None)
    port: Optional[int] = field(default=None)
    dbname: Optional[str] = field(default=None)
    schema: Optional[str] = field(default=None)
    threads: Optional[int] = field(default=None)

    @staticmethod
    def set_variable(key: str, value: Any) -> None:
        try:
            if value is None:
                warning(message=f"Variable {key} can't be set to None.")

            _value = Variable.get(key=key)
            if _value is None:
                warning(message=f"Variable {key} not found.")

            if value != _value:
                Variable.set(key, value)
                info(message=f"{key}: {value}")
        except Exception as exception:
            error(exc=exception)
            raise exception

    def set(self, variables: ProfileTargetVariables) -> None:
        """
        Set Profile's ENV variables.

        Args
        ----
            keys (PostgresTargetEnvKeys): ENV keys.

        Returns
        -------
            None.
        """
        if variables.host.key and self.host:
            self.set_variable(key=variables.host.key, value=self.host)
        if variables.user.key and self.user:
            self.set_variable(key=variables.user.key, value=self.user)
        if variables.password.key and self.password:
            self.set_variable(key=variables.password.key, value=self.password)
        if variables.port.key and self.port:
            self.set_variable(key=variables.port.key, value=self.port)
        if variables.dbname.key and self.dbname:
            self.set_variable(key=variables.dbname.key, value=self.dbname)
        if variables.schema.key and self.schema:
            self.set_variable(key=variables.schema.key, value=self.schema)
        if variables.threads.key and self.threads:
            self.set_variable(key=variables.threads.key, value=self.threads)


@dataclass
class ProfileOutputs(dbt_utils.ProfileOutputsProtocol):
    """dbt Profiles Profile Outputs."""

    targets: List[dbt_utils.TargetProtocol]


@dataclass
class Profile(dbt_utils.ProfileProtocol):
    """dbt Profiles Profile."""

    target: str
    outputs: List[dbt_utils.ProfileOutputsProtocol]


@dataclass
class Profiles(dbt_utils.ProfilesProtocol):
    """dbt Profiles."""

    config: dbt_utils.ProfilesConfigProtocol
    profiles: List[dbt_utils.ProfileProtocol]
