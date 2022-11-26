"""DBT Test Project DAG."""

import os
from typing import Any, Dict, List

import pendulum
from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from dbt.profiles import ProfileTarget, ProfileTargetVariables
from settings import BASE_PATH, DEFAULT_ARGS
from utils.subprocess import execute

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


with DAG(
    f"test__dbt__{DBT_PROJECT}",
    default_args=DEFAULT_ARGS,
    description="dbt Test",
    schedule_interval="@once",
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=["tests", "dbt", "data_warehouse", "data_marts"],
    template_searchpath=os.path.join(BASE_PATH),
) as dag:

    @task(task_id="dbt_which", multiple_outputs=True)
    def dbt_which(cmd: str):
        """Logs $(dbt which)"""
        return execute(command=cmd, verbose=True)

    dbt_which_command = (
        f"([ ! -d /tmp/dbt ] && mkdir -p /tmp/dbt); cd /tmp/dbt; which dbt"
    )
    dbt_which_task = dbt_which(cmd=dbt_which_command)

    @task(task_id="dbt_version", multiple_outputs=True)
    def dbt_version(cmd: str):
        """Logs dbt version."""
        return execute(command=cmd, verbose=True)

    dbt_version_task = dbt_version(
        cmd=f'([ ! -d /tmp/dbt ] && mkdir -p /tmp/dbt); cd /tmp/dbt; {dbt_which_task["output"]} --version'
    )

    for target in DBT_PROFILES:
        profile_target_variables = ProfileTargetVariables(target=ProfileTarget(target))
        _destination_path = os.path.join("/tmp/dbt", DBT_PROJECT, target)
        _destination_profiles = os.path.join(_destination_path, "profiles.yml")
        with TaskGroup(target, tooltip=target) as target_task_group:

            @task(task_id="debug_models", multiple_outputs=True)
            def run_models(variables: ProfileTargetVariables):
                """Run dbt debug command."""
                cmd = f"([ ! -d {_destination_path} ] && mkdir -p {_destination_path});"
                cmd += f" cp -r {DBT_PROJECT_PATH}/. {_destination_path};"
                cmd += f" cp {DBT_PROFILES_PATH[target]} {_destination_profiles};"
                cmd += f" cd {_destination_path};"
                cmd += "".join(variables.export_command())
                cmd += f" {DBT_EXECUTABLE} debug --project-dir . --profiles-dir .;"
                cmd += f" {DBT_EXECUTABLE} deps;"
                cmd += f" {DBT_EXECUTABLE} run --project-dir . --profiles-dir .;"
                cmd += f" {DBT_EXECUTABLE} test --project-dir . --profiles-dir .;"
                cmd += f" rm -R {_destination_path}"
                return execute(command=cmd, verbose=True)

            dbt_debug_task = run_models(variables=profile_target_variables)

    (dbt_which_task >> dbt_version_task >> target_task_group)
