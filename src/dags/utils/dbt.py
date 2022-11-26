"""dbt Entities Utils."""

from dataclasses import dataclass, field
from typing import List, Optional

from typing_extensions import Protocol


@dataclass  # type: ignore
class ProfilesConfigProtocol(Protocol):
    """dbt Profiles Config."""

    send_anonymous_usage_stats: Optional[bool]
    use_colors: Optional[bool]
    partial_parse: Optional[bool]
    printer_width: Optional[int]
    write_json: Optional[bool]
    warn_error: Optional[bool]
    log_format: Optional[bool]
    debug: Optional[bool]
    version_check: Optional[bool]
    fail_fast: Optional[bool]
    use_experimental_parser: Optional[bool]
    static_parser: Optional[bool]


@dataclass
class ProfilesConfig(ProfilesConfigProtocol):
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


@dataclass  # type: ignore
class TargetProtocol(Protocol):
    """dbt Profiles Profile Outputs Target."""

    name: str
    type: str
    host: str
    user: str
    password: str
    port: int
    dbname: str
    schema: str
    threads: int

    def set(self) -> None:
        ...


@dataclass
class Target(TargetProtocol):
    """dbt Profiles Profile Outputs Target."""

    name: str
    type: str
    host: str
    user: str
    password: str
    port: int
    dbname: str
    schema: str
    threads: int

    def set(self) -> None:
        pass


@dataclass  # type: ignore
class ProfileOutputsProtocol(Protocol):
    """dbt Profiles Profile Outputs."""

    targets: List[TargetProtocol]


@dataclass
class ProfileOutputs(ProfileOutputsProtocol):
    """dbt Profiles Profile Outputs."""

    targets: List[TargetProtocol]


@dataclass  # type: ignore
class ProfileProtocol(Protocol):
    """dbt Profiles Profile."""

    target: str
    outputs: List[ProfileOutputsProtocol]


@dataclass
class Profile(ProfileProtocol):
    """dbt Profiles Profile."""

    target: str
    outputs: List[ProfileOutputsProtocol]


@dataclass  # type: ignore
class ProfilesProtocol(Protocol):
    """dbt Profiles."""

    config: ProfilesConfigProtocol
    profiles: List[ProfileProtocol]


@dataclass
class Profiles(ProfilesProtocol):
    """dbt Profiles."""

    config: ProfilesConfigProtocol
    profiles: List[ProfileProtocol]
