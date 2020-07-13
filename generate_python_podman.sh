#!/bin/sh

podman run --rm -v "${PWD}:/local" \
    --security-opt label=disable \
    openapitools/openapi-generator-cli generate \
    -i /local/cimpy_api.yaml \
    -g python-flask -o /local/generated/
