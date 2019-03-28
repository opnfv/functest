#!/bin/bash

set -e

repo=${REPO:-opnfv}
amd64_dirs=${amd64_dirs-"\
docker/core \
docker/tempest \
docker/healthcheck \
docker/smoke \
docker/benchmarking \
docker/features \
docker/vnf"}
arm64_dirs=${arm64_dirs-${amd64_dirs}}
build_opts=(--pull=true --no-cache --force-rm=true)

find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:iruya|${repo}/functest-core:amd64-iruya|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-tempest:iruya|${repo}/functest-tempest:amd64-iruya|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-iruya" .)
        docker push "${repo}/functest-${dir##**/}:amd64-iruya"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-iruya" || true)
done
[ ! -z "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-iruya" alpine:3.9 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.9|multiarch/alpine:arm64-v3.9|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:iruya|${repo}/functest-core:arm64-iruya|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-tempest:iruya|${repo}/functest-tempest:arm64-iruya|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-iruya" .)
    docker push "${repo}/functest-${dir##**/}:arm64-iruya"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-iruya" || true)
done
[ ! -z "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-iruya" \
        multiarch/alpine:arm64-v3.9 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
