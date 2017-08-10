#!/bin/bash

set -e

repo=${repo:-opnfv}
dirs="\
docker/core \
docker/healthcheck \
docker/smoke \
docker/features \
docker/components"

(cd docker && docker build -t "${repo}/functest" .)
docker push "${repo}/functest"

for dir in ${dirs}; do
    (cd ${dir} && docker build -t "${repo}/functest-${dir##**/}" .)
    docker push "${repo}/functest-${dir##**/}"
done

exit $?
