#!/usr/bin/env bash

set -eo pipefail

usage() {
    echo "$0 TARGET_ADDR TARGET_PORT [LOCAL_PORT]"
    echo
    echo "Creates a port-forward via Kubernetes."
    echo
    echo "Most commonly used when a resource exists in a VPC and is reachable via"
    echo "Kubernetes due to networking and access restrictions, but not elsewhere."
    echo
    echo "Examples:"
    echo
    echo "Forward some PostgreSQL RDS database to local port 5432:"
    echo "$0 FANCY_IDENTIFIER.eu-west-1.rds.amazonaws.com 5432"
    echo
    echo "Forward some PostgreSQL RDS database to local port 6789:"
    echo "$0 FANCY_IDENTIFIER.eu-west-1.rds.amazonaws.com 5432 6789"
    echo
    echo "Hint: Make sure to have the k8s context use the cluster your"
    echo "target db is running in. (e.g. using 'kubectl config use-context')"
    echo
    exit 1
}

LBLUE='\033[94m'
BOLD='\033[1m'
RS_ALL='\033[0m'

slugify() {
    # trimmed down version of
    # https://gist.github.com/oneohthree/f528c7ae1e701ad990e6.
    # We don't need all the unicode conversion since sources are valid domain
    # names anyways (ignoring punycode).
    echo "$1" | sed -E 's/[^a-zA-Z0-9]+/-/g' | sed -E 's/^-+\|-+$//g' | tr '[:upper:]' '[:lower:]'
}

IMAGE='alpine/socat'

TARGET="$1"
TARGET_PORT="$2"
# Must be >1024
SOCAT_PORT="6666"

if [[ $# -eq 2 ]] ; then
    LOCAL_PORT="$TARGET_PORT"
    elif [[ $# -eq 3 ]] ; then
    LOCAL_PORT="$3"
else
    usage
fi

truncate() {
    local s="$1"
    local nchars="$2"

    echo "$s" | cut -c"1-$nchars"
}

pod_name() {
    # Constraints: 63 chars max and no funny characters. Hence slugify
    # $TARGET -> truncated to 35
    # -- -> 2
    # $PORT -> maximum 5 (up to "65535")
    # --port-forward-- -> 16
    # $RANDOM -> maximum 5 (up to "32767")
    # == maximum 63
    # We add some random chars to so users to not fight over the same Pod name
    # in case they are creating exactly the same target/port combination forward.
    # Local port is not important in the name because the Pod does not care about
    # it anyways.
    echo "$(truncate "$(slugify "$TARGET")" 35)--$(slugify "$TARGET_PORT")--port-forward--$RANDOM"
}

start_pod() {
    local pod_name context
    pod_name=$(pod_name)
    context=$(kubectl config current-context)
    echo "Kubernetes context: $context"

    cleanup() {
        echo "Deleting pod."
        kubectl --context "$1" delete pod "$2"
    }
    # shellcheck disable=SC2064
    trap "cleanup '$context' '$pod_name'" EXIT

    echo "Starting pod $pod_name"
    kubectl --context "$context" run \
    "$pod_name" \
    --image="$IMAGE" \
    -- \
    "TCP-LISTEN:$SOCAT_PORT,fork" "TCP:$TARGET:$TARGET_PORT"

    echo "Waiting for Pod to become ready."
    kubectl --context "$context" wait --for=condition=Ready "pod/$pod_name"

    echo -e "${BOLD}${LBLUE}Starting port forward from local port $LOCAL_PORT to $TARGET:$TARGET_PORT.${RS_ALL}"
    echo "(Port 6666 is only the intermediate port on Kubernetes. Ignore it.)"
    kubectl --context "$context" port-forward "pod/$pod_name" "$LOCAL_PORT:$SOCAT_PORT"
}

start_pod
