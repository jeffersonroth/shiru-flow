#!/usr/bin/env bash

set -ex;

if [[ "$OSTYPE" =~ ^darwin ]]; then
    # Mac OS X platform
    brew update; brew upgrade
    brew install socat
    socat TCP-LISTEN:2375,reuseaddr,fork UNIX-CONNECT:/var/run/docker.sock
fi

set +ex
