#!/bin/sh

if command -v docker &> /dev/null; then
    CONTAINER=docker
elif command -v podman &> /dev/null; then
    CONTAINER=podman
else
    echo "Error: No container runtime found"
    exit -1
fi

$CONTAINER run --rm -v "${PWD}:/local" \
    --security-opt label=disable \
    openapitools/openapi-generator-cli generate \
    -i /local/openapi.yaml \
    -g python-flask -o /local/generated/
