"""Subprocess utils."""

import json
import re
import subprocess

from airflow.utils.log.logging_mixin import LoggingMixin

ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

# TODO: compare with https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/hooks/subprocess.html


def execute(command: str, verbose: bool = True):
    """
    Execute command using Python 'subprocess'.

    Args
    ----
        command (str): Command to be executed.
        verbose (bool): Whether to log line by line, or wait for process to finish before logging.

    Returns
    -------
        json: status, output, and errors.
    """
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    ) as process:
        try:
            if not process or process.stdout is None:
                raise Exception()
            if verbose:
                LoggingMixin().log.info("Running command: %s", command)
                lines = []
                while True:
                    _output = ANSI_ESCAPE.sub(
                        "", process.stdout.readline().strip().decode("utf-8")
                    )
                    LoggingMixin().log.info(_output)
                    if not _output and process.poll() is not None:
                        break
                    lines.append(_output)
                response_log = {
                    "status": process.poll(),
                    "output": "\n".join(lines),
                }
                response = json.dumps(
                    response_log,
                    default=str,
                    indent=4,
                )
            else:
                status = process.wait()
                (output, err) = process.communicate()
                response_log = {
                    "status": status,
                    "output": output.decode("utf-8") if output else None,
                    "error": err.decode("utf-8") if err else None,
                }
                response = json.dumps(
                    response_log,
                    default=str,
                    indent=4,
                )
            return json.loads(response)

        except Exception as exception:
            LoggingMixin().log.error(exception)
            raise exception
