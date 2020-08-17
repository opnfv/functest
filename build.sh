#!/bin/bash

set -e

repo=${REPO:-opnfv}
amd64_dirs=${amd64_dirs-"\
docker/core \
docker/tempest \
docker/healthcheck \
docker/smoke \
docker/benchmarking \
docker/vnf \
docker/smoke-cntt \
docker/benchmarking-cntt"}
arm_dirs=${arm_dirs-${amd64_dirs}}
arm64_dirs=${arm64_dirs-${amd64_dirs}}
build_opts=("--pull=true" --no-cache "--force-rm=true")

find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:iruya|${repo}/functest-core:amd64-iruya|g" {} +
find . -name Dockerfile -exec sed -i \
    -e \
    "s|opnfv/functest-tempest:iruya|${repo}/functest-tempest:amd64-iruya|g" \
    {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-iruya" .)
        docker push "${repo}/functest-${dir##**/}:amd64-iruya"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-iruya" || true)
done
[ -n "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-iruya" alpine:3.9 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.9|arm64v8/alpine:3.9|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:iruya|${repo}/functest-core:arm64-iruya|g" {} +
find . -name Dockerfile -exec sed -i \
    -e \
    "s|opnfv/functest-tempest:iruya|${repo}/functest-tempest:arm64-iruya|g" \
    {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-iruya" .)
    docker push "${repo}/functest-${dir##**/}:arm64-iruya"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-iruya" || true)
done
[ -n "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-jerma" \
        arm64v8/alpine:3.9 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.9|arm32v6/alpine:3.9|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:iruya|${repo}/functest-core:arm-iruya|g" {} +
find . -name Dockerfile -exec sed -i \
    -e \
    "s|opnfv/functest-tempest:iruya|${repo}/functest-tempest:arm-iruya|g" {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm-iruya" .)
    docker push "${repo}/functest-${dir##**/}:arm-iruya"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-iruya" || true)
done
[ -n "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-jerma" \
        arm32v6/alpine:3.9 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
