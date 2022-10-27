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
    -e "s|opnfv/functest-core:zed|${repo}/functest-core:amd64-zed|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:zed|${repo}/functest-smoke:amd64-zed|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:zed|\
${repo}/functest-benchmarking:amd64-zed|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-zed" .)
        docker push "${repo}/functest-${dir##**/}:amd64-zed"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-zed" || true)
done
[ -n "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-zed" alpine:3.14 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.14|arm64v8/alpine:3.14|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:zed|${repo}/functest-core:arm64-zed|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:zed|${repo}/functest-smoke:arm64-zed|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:zed|\
${repo}/functest-benchmarking:arm64-zed|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-zed" .)
    docker push "${repo}/functest-${dir##**/}:arm64-zed"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-zed" || true)
done
[ -n "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-zed" \
        arm64v8/alpine:3.14 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.14|arm32v6/alpine:3.14|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:zed|${repo}/functest-core:arm-zed|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:zed|${repo}/functest-smoke:arm-zed|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:zed|\
${repo}/functest-benchmarking:arm-zed|g" {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm-zed" .)
    docker push "${repo}/functest-${dir##**/}:arm-zed"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-zed" || true)
done
[ -n "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-zed" \
        arm32v6/alpine:3.14 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
