#!/usr/bin/env bash

set -ex;

REPO_ROOT_DIR="$(git rev-parse --show-toplevel)"

pip3 debug --verbose
pip3 install --upgrade pip
pip3 --version

declare -a Requirements=("${REPO_ROOT_DIR}/src/docker/config/mwaa-base-providers-requirements.txt" "${REPO_ROOT_DIR}/src/docker/config/requirements.txt")

for requirement in "${Requirements[@]}"; do
    cat "${requirement}" | sed 's/--/\#/g' | cut -f1 -d"#" | sed '/^\s*$/d' | xargs -n 1 pip3 install
done

pip3 list

# TODO: (install -r req -c ctrs) || (install -r req* -c ctrs) || (cat | sed | cut | sed | xargs install)

set +ex
