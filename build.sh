#!/bin/sh

set -e

repo=${REPO:-opnfv}
amd64_dirs=${amd64_dirs-"\
docker/core \
docker/healthcheck \
docker/smoke \
docker/benchmarking \
docker/vnf \
docker/smoke-cntt \
docker/benchmarking-cntt"}
arm_dirs=${arm_dirs-${amd64_dirs}}
arm64_dirs=${arm64_dirs-${amd64_dirs}}
build_opts="--pull=true --no-cache --force-rm=true"

find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:2023.1|${repo}/functest-core:amd64-2023.1|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:2023.1|${repo}/functest-smoke:amd64-2023.1|g" \
    {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:2023.1|\
${repo}/functest-benchmarking:amd64-2023.1|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build $build_opts \
            -t "${repo}/functest-${dir##**/}:amd64-2023.1" .)
        docker push "${repo}/functest-${dir##**/}:amd64-2023.1"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-2023.1" || true)
done
[ -n "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-2023.1" alpine:3.16 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.16|arm64v8/alpine:3.16|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:2023.1|${repo}/functest-core:arm64-2023.1|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:2023.1|${repo}/functest-smoke:arm64-2023.1|g" \
    {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:2023.1|\
${repo}/functest-benchmarking:arm64-2023.1|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build $build_opts \
        -t "${repo}/functest-${dir##**/}:arm64-2023.1" .)
    docker push "${repo}/functest-${dir##**/}:arm64-2023.1"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-2023.1" || true)
done
[ -n "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-2023.1" \
        arm64v8/alpine:3.16 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.16|arm32v6/alpine:3.16|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:2023.1|${repo}/functest-core:arm-2023.1|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:2023.1|${repo}/functest-smoke:arm-2023.1|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:2023.1|\
${repo}/functest-benchmarking:arm-2023.1|g" {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build $build_opts \
        -t "${repo}/functest-${dir##**/}:arm-2023.1" .)
    docker push "${repo}/functest-${dir##**/}:arm-2023.1"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-2023.1" || true)
done
[ -n "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-2023.1" \
        arm32v6/alpine:3.16 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
