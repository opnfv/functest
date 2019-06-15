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
arm_dirs=${arm_dirs-"\
docker/core \
docker/tempest \
docker/healthcheck \
docker/smoke \
docker/benchmarking \
docker/features"}
arm64_dirs=${arm64_dirs-${amd64_dirs}}
build_opts="--pull=true --no-cache --force-rm=true"

find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:hunter|${repo}/functest-core:amd64-hunter|g" {} +
find . -name Dockerfile -exec sed -i \
    -e \
    "s|opnfv/functest-tempest:hunter|${repo}/functest-tempest:amd64-hunter|g" \
    {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-hunter" .)
        docker push "${repo}/functest-${dir##**/}:amd64-hunter"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-hunter" || true)
done
[ ! -z "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-hunter" alpine:3.9 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.9|multiarch/alpine:arm64-v3.9|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:hunter|${repo}/functest-core:arm64-hunter|g" {} +
find . -name Dockerfile -exec sed -i \
    -e \
    "s|opnfv/functest-tempest:hunter|${repo}/functest-tempest:arm64-hunter|g" \
    {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts}" \
        -t "${repo}/functest-${dir##**/}:arm64-hunter" .)
    docker push "${repo}/functest-${dir##**/}:arm64-hunter"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-hunter" || true)
done
[ ! -z "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-hunter" \
        multiarch/alpine:arm64-v3.9 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.9|multiarch/alpine:armhf-v3.9|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:hunter|${repo}/functest-core:arm-hunter|g" {} +
find . -name Dockerfile -exec sed -i \
    -e \
    "s|opnfv/functest-tempest:hunter|${repo}/functest-tempest:arm-hunter|g" \
    {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm-hunter" .)
    docker push "${repo}/functest-${dir##**/}:arm-hunter"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-hunter" || true)
done
[ ! -z "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-hunter" \
        multiarch/alpine:armhf-v3.9 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
