#!/bin/bash

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
build_opts=("--pull=true" --no-cache "--force-rm=true")

find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:wallaby|${repo}/functest-core:amd64-wallaby|g" \
    {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:wallaby|\
${repo}/functest-smoke:amd64-wallaby|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:wallaby|\
${repo}/functest-benchmarking:amd64-wallaby|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-wallaby" .)
        docker push "${repo}/functest-${dir##**/}:amd64-wallaby"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-wallaby" || true)
done
[ -n "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-wallaby" alpine:3.13 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.13|arm64v8/alpine:3.13|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:wallaby|${repo}/functest-core:arm64-wallaby|g" \
    {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:wallaby|\
${repo}/functest-smoke:arm64-wallaby|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:wallaby|\
${repo}/functest-benchmarking:arm64-wallaby|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-wallaby" .)
    docker push "${repo}/functest-${dir##**/}:arm64-wallaby"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-wallaby" || true)
done
[ -n "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-wallaby" \
        arm64v8/alpine:3.13 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.13|arm32v6/alpine:3.13|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:wallaby|${repo}/functest-core:arm-wallaby|g" \
    {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:wallaby|${repo}/functest-smoke:arm-wallaby|g" \
    {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:wallaby|\
${repo}/functest-benchmarking:arm-wallaby|g" {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm-wallaby" .)
    docker push "${repo}/functest-${dir##**/}:arm-wallaby"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-wallaby" || true)
done
[ -n "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-wallaby" \
        arm32v6/alpine:3.13 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
