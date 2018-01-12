#!/bin/bash

set -e

repo=${repo:-opnfv}
amd64_dirs=${amd64_dirs-"\
docker/core \
docker/healthcheck \
docker/smoke \
docker/features \
docker/components \
docker/vnf \
docker/parser \
docker/restapi"}
arm64_dirs=${arm64_dirs-${amd64_dirs}}
build_opts=(--pull=true --no-cache --force-rm=true)

find . -name Dockerfile -exec sed -i -e "s|opnfv/functest-core|${repo}/functest-core:amd64-latest|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" -t "${repo}/functest-${dir##**/}:amd64-latest" .)
    docker push "${repo}/functest-${dir##**/}:amd64-latest"
    [ "${dir}" != "docker/core" ] && (docker rmi "${repo}/functest-${dir##**/}:amd64-latest" || true)
done
[ ! -z "${amd64_dirs}" ] && (docker rmi "${repo}/functest-core:amd64-latest" alpine:3.7 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i -e "s|alpine:3.7|multiarch/alpine:arm64-v3.7|g" {} +
find . -name Dockerfile -exec sed -i -e "s|opnfv/functest-core|${repo}/functest-core:arm64-latest|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" -t "${repo}/functest-${dir##**/}:arm64-latest" .)
    docker push "${repo}/functest-${dir##**/}:arm64-latest"
    [ "${dir}" != "docker/core" ] && (docker rmi "${repo}/functest-${dir##**/}:arm64-latest" || true)
done
[ ! -z "${arm64_dirs}" ] && (docker rmi "${repo}/functest-core:arm64-latest" multiarch/alpine:arm64-v3.7 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
