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
    -e "s|opnfv/functest-core:kali|${repo}/functest-core:amd64-kali|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:kali|${repo}/functest-smoke:amd64-kali|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:kali|\
${repo}/functest-benchmarking:amd64-kali|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-kali" .)
        docker push "${repo}/functest-${dir##**/}:amd64-kali"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-kali" || true)
done
[ -n "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-kali" alpine:3.11 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.11|arm64v8/alpine:3.11|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:kali|${repo}/functest-core:arm64-kali|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:kali|${repo}/functest-smoke:arm64-kali|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:kali|\
${repo}/functest-benchmarking:arm64-kali|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-kali" .)
    docker push "${repo}/functest-${dir##**/}:arm64-kali"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-kali" || true)
done
[ -n "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-kali" \
        arm64v8/alpine:3.11 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.11|arm32v6/alpine:3.11|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:kali|${repo}/functest-core:arm-kali|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:kali|${repo}/functest-smoke:arm-kali|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:kali|\
${repo}/functest-benchmarking:arm-kali|g" {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm-kali" .)
    docker push "${repo}/functest-${dir##**/}:arm-kali"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-kali" || true)
done
[ -n "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-kali" \
        arm32v6/alpine:3.11 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
