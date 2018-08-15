#!/bin/bash

set -e

repo=${REPO:-opnfv}
amd64_dirs=${amd64_dirs-"\
docker/core \
docker/tempest \
docker/healthcheck \
docker/smoke \
docker/features \
docker/components \
docker/vnf"}
arm64_dirs=${arm64_dirs-${amd64_dirs}}
build_opts=(--pull=true --no-cache --force-rm=true \
    --build-arg OPENSTACK_TAG="${OPENSTACK_TAG:-stable/queens}" \
    --build-arg RALLY_OPENSTACK_TAG="${RALLY_OPENSTACK_TAG:-1.2.0}")

find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core|${repo}/functest-core:amd64-latest|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-tempest|${repo}/functest-tempest:amd64-latest|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-latest" .)
        docker push "${repo}/functest-${dir##**/}:amd64-latest"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-latest" || true)
done
[ ! -z "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-latest" alpine:3.7 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.7|multiarch/alpine:arm64-v3.7|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core|${repo}/functest-core:arm64-latest|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-tempest|${repo}/functest-tempest:arm64-latest|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-latest" .)
    docker push "${repo}/functest-${dir##**/}:arm64-latest"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-latest" || true)
done
[ ! -z "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-latest" \
        multiarch/alpine:arm64-v3.7 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
