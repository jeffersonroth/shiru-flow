#!/usr/bin/env bash

set -ex;

if [[ "$OSTYPE" =~ ^darwin ]]; then
    # Mac OS X platform
    brew update; brew upgrade
    brew install pyenv pyenv-virtualenv pyenv-virtualenvwrapper
    brew install openssl readline sqlite3 xz zlib postgresql
    brew upgrade openssl
    brew link --force openssl
    brew install rust
    if { pyenv versions | grep "${PYTHON_VERSION}"; } >/dev/null 2>&1; then
        echo "Python v ${PYTHON_VERSION} already installed"
    else
        echo "Installing python v ${PYTHON_VERSION}"
        pyenv install "${PYTHON_VERSION}"
    fi;
    if { pyenv versions | grep "${PYTHON_VERSION}/envs/${PYTHON_VENV}"; } >/dev/null 2>&1; then
        echo "Venv ${PYTHON_VERSION}/envs/${PYTHON_VENV} already exists"
    else
        echo "Creating pyenv venv ${PYTHON_VERSION} ${PYTHON_VENV}"
        pyenv virtualenv "${PYTHON_VERSION}" "${PYTHON_VENV}"
    fi;
fi

: "
Should you have any problem with the venv, remove it by running:
    pyenv deactivate -f ""${PYTHON_VENV}""
    pyenv uninstall -f ""${PYTHON_VENV}""
"

set +ex
