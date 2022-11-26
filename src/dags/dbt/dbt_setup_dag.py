"""dbt Setup DAG."""

import os
from typing import Any, Dict, List

import pendulum
from airflow import DAG
from airflow.decorators import task
from airflow.models.variable import Variable
from airflow.utils.task_group import TaskGroup
from settings import BASE_PATH, DEFAULT_ARGS, POSTGRES_CONN_ID
from utils.dbt import TargetProtocol
from utils.subprocess import execute

from dbt.entities import Target
from dbt.profiles import ProfileTarget, ProfileTargetVariables

TARGET_CONN_ID: Dict[str, Any] = {
    "test": POSTGRES_CONN_ID,
}

TARGET_SCHEMA: Dict[str, Any] = {
    "test": Variable.get("DBT_TEST_POSTGRES_SCHEMA_DEFAULT"),
}

DBT_EXECUTABLE: str = f"{os.environ['HOME']}/.local/bin/dbt"
DBT_PROFILES: List[str] = ["test"]
DBT_PROFILES_PATH: Dict[str, Any] = {
    profile: os.path.join(BASE_PATH, f"dags/dbt/profiles/profiles.{profile}.yml")
    for profile in DBT_PROFILES
}
DBT_PROJECT: str = "test_project"
DBT_PROJECT_PATH: str = os.path.join(
    BASE_PATH,
    "dags/dbt/projects",
    DBT_PROJECT,
)


def _update_postgres_variables(
    variables: ProfileTargetVariables,
    conn_id: str,
    schema: str,
) -> ProfileTargetVariables:
    """
    Set Postgres variables (Airflow) to be used by dbt Profile.

    Args
    ----
        name (str): Target name.
        keys (PostgresTargetEnvKeys): Tuple of Target Profile ENVs and Airflow ENVs.
        conn_id (str): Postgres connection id. (Data Warehouse/Data Marts).
        schema (str): Base schema to be used by dbt Profile.

    Returns
    -------
        None.
    """

    from airflow.models.connection import Connection
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    hook: PostgresHook = PostgresHook(postgres_conn_id=conn_id)
    conn: Connection = hook.get_connection(conn_id=conn_id)
    target: TargetProtocol = Target(
        name=variables.target,
        type="postgres",
        host=conn.host,  # type: ignore
        user=conn.login,  # type: ignore
        password=conn.password,
        port=conn.port,  # type: ignore
        schema=schema,
    )
    target.set(variables=variables)
    return ProfileTargetVariables(target=ProfileTarget(variables.target))  # type: ignore


def generate_dag_by_profile(
    target: str, dag_id: str, description: str, schedule_interval: str
):
    """
    Generate DAG by profile.

    Args
    ----
        target (str): Target name.
        dag_id (str): DAG id.
        description (str): DAG description.
        schedule_interval (str): cron job.

    Returns
    -------
        DAG.
    """
    # TODO: have tags as arg.

    with DAG(
        dag_id,
        default_args=DEFAULT_ARGS,
        description=description,
        schedule_interval=schedule_interval,
        start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
        catchup=False,
        tags=["dbt", "setup", target],
        template_searchpath=os.path.join(BASE_PATH),
    ) as dag:
        profile_target_variables = ProfileTargetVariables(target=ProfileTarget(target))  # type: ignore
        _destination_path = os.path.join("/tmp/dbt", DBT_PROJECT, target)
        _destination_profiles = os.path.join(_destination_path, "profiles.yml")
        with TaskGroup(target, tooltip=target) as target_task_group:

            @task(task_id="debug_models", multiple_outputs=True)
            def run_models():
                """Run dbt debug command."""
                variables = _update_postgres_variables(
                    variables=profile_target_variables,
                    conn_id=TARGET_CONN_ID[target]["postgres"],
                    schema=TARGET_SCHEMA[target],
                ).export_command()
                cmd = f"([ ! -d {_destination_path} ] && mkdir -p {_destination_path});"
                cmd += f" cp -r {DBT_PROJECT_PATH}/. {_destination_path};"
                cmd += f" cp {DBT_PROFILES_PATH[target]} {_destination_profiles};"
                cmd += f" cd {_destination_path};"
                cmd += "".join(variables.values())
                cmd += f" {DBT_EXECUTABLE} debug --project-dir . --profiles-dir .;"
                cmd += f" {DBT_EXECUTABLE} deps;"
                cmd += f" {DBT_EXECUTABLE} run --project-dir . --profiles-dir .;"
                cmd += f" {DBT_EXECUTABLE} test --project-dir . --profiles-dir .;"
                cmd += f" rm -R {_destination_path}"
                return execute(command=cmd, verbose=True)

            dbt_debug_task = run_models()
            dbt_debug_task

        target_task_group

    return dag


for profile in DBT_PROFILES:
    globals()[f"dbt__setup__{profile}"] = generate_dag_by_profile(
        target=profile,
        dag_id=f"dbt__setup__{profile}",
        description=f"dbt Setup for {profile}",
        schedule_interval="@once",
    )
