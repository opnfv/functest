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
arm64_dirs=${arm64_dirs-$(echo "${amd64_dirs}" | sed -e "s|docker/vnf||" \
    -e "s|docker/restapi||")}
build_opts=(--pull=true --no-cache --force-rm=true)

find . -name Dockerfile -exec sed -i -e "s|opnfv/functest-core:euphrates|${repo}/functest-core:amd64-euphrates|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" -t "${repo}/functest-${dir##**/}:amd64-euphrates" .)
    docker push "${repo}/functest-${dir##**/}:amd64-euphrates"
    [ "${dir}" != "docker/core" ] && docker rmi "${repo}/functest-${dir##**/}:amd64-euphrates" || true
done
docker rmi "${repo}/functest-core:amd64-euphrates" alpine:3.6 || true
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i -e "s|alpine:3.6|multiarch/alpine:arm64-v3.6|g" {} +
find . -name Dockerfile -exec sed -i -e "s|opnfv/functest-core:euphrates|${repo}/functest-core:arm64-euphrates|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" -t "${repo}/functest-${dir##**/}:arm64-euphrates" .)
    docker push "${repo}/functest-${dir##**/}:arm64-euphrates"
    [ "${dir}" != "docker/core" ] && docker rmi "${repo}/functest-${dir##**/}:arm64-euphrates" || true
done
docker rmi "${repo}/functest-core:arm64-euphrates" multiarch/alpine:arm64-v3.6 || true
find . -name Dockerfile -exec git checkout {} +

exit $?
