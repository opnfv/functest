#!/bin/bash

set -e

repo=${repo:-opnfv}
x86_64_dirs=${x86_64_dirs-"\
docker/core \
docker/healthcheck \
docker/smoke \
docker/features \
docker/components \
docker/vnf \
docker/parser \
docker/restapi"}
aarch64_dirs=${aarch64_dirs-$(echo "${x86_64_dirs}" | sed -e "s|docker/vnf||" \
    -e "s|docker/restapi||")}

find . -name Dockerfile -exec sed -i -e "s|opnfv/functest-core|${repo}/functest-core:x86_64-latest|g" {} +
for dir in ${x86_64_dirs}; do
    (cd "${dir}" && docker build -t "${repo}/functest-${dir##**/}:x86_64-latest" .)
    docker push "${repo}/functest-${dir##**/}:x86_64-latest"
done
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i -e "s|alpine:3.6|multiarch/alpine:aarch64-v3.6|g" {} +
find . -name Dockerfile -exec sed -i -e "s|opnfv/functest-core|${repo}/functest-core:aarch64-latest|g" {} +
for dir in ${aarch64_dirs}; do
    (cd "${dir}" && docker build -t "${repo}/functest-${dir##**/}:aarch64-latest" .)
    docker push "${repo}/functest-${dir##**/}:aarch64-latest"
done
find . -name Dockerfile -exec git checkout {} +

exit $?
