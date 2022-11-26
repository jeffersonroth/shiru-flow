#!/usr/bin/env bash

set -ex;

DOCKER_COMPOSE_PROJECT_NAME=${1}
DOCKER_COMPOSE_DIR="$(cd "$(dirname "$(git rev-parse --git-dir)")"/src/docker && pwd)"
AIRFLOW_VARIABLES_DIR="$(cd "$(dirname "$(git rev-parse --git-dir)")"/src/variables && pwd)"

set_variables() {
    for file in "$AIRFLOW_VARIABLES_DIR"/*; do
        filename=$(basename "$file" | cut -d. -f1)
        docker-compose -p "${DOCKER_COMPOSE_PROJECT_NAME}" -f "${DOCKER_COMPOSE_DIR}"/docker-compose-local.yml run --rm local-runner airflow variables delete "$filename" || true
        docker-compose -p "${DOCKER_COMPOSE_PROJECT_NAME}" -f "${DOCKER_COMPOSE_DIR}"/docker-compose-local.yml run --rm local-runner airflow variables set "$filename" "$(cat "$file")" || true
    done
}

set_variables

set +ex
