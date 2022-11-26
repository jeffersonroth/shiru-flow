#!/usr/bin/env bash

set -ex;

DOCKER_COMPOSE_PROJECT_NAME=${1}
DOCKER_COMPOSE_DIR="$(cd "$(dirname "$(git rev-parse --git-dir)")"/src/docker && pwd)"

set_connections_aws() {
    # aws_default
    docker-compose -p "${DOCKER_COMPOSE_PROJECT_NAME}" -f "${DOCKER_COMPOSE_DIR}"/docker-compose-local.yml run --rm local-runner airflow connections delete 'aws_default' || true
    docker-compose -p "${DOCKER_COMPOSE_PROJECT_NAME}" -f "${DOCKER_COMPOSE_DIR}"/docker-compose-local.yml run --rm local-runner airflow connections add 'aws_default' \
    --conn-type 'aws' \
    --conn-login "${AWS_ACCESS_KEY_ID}" \
    --conn-password "${AWS_SECRET_ACCESS_KEY}" \
    --conn-extra '{"region_name": "eu-central-1", "aws_session_token": "'"${AWS_SESSION_TOKEN}"'"}' || true
}

set_connections_postgres() {
    # postgres_default
    docker-compose -p "${DOCKER_COMPOSE_PROJECT_NAME}" -f "${DOCKER_COMPOSE_DIR}"/docker-compose-local.yml run --rm local-runner airflow connections delete 'postgres_default' || true
    docker-compose -p "${DOCKER_COMPOSE_PROJECT_NAME}" -f "${DOCKER_COMPOSE_DIR}"/docker-compose-local.yml run --rm local-runner airflow connections add 'postgres_default' \
    --conn-type 'postgres' \
    --conn-host "${POSTGRES_HOST}" \
    --conn-login "${POSTGRES_USERNAME}" \
    --conn-password "${POSTGRES_PASSWORD}" \
    --conn-port "${POSTGRES_PORT_FORWARD}" || true
}

set_connections_aws && set_connections_postgres

set +ex
