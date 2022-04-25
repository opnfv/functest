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
    -e "s|opnfv/functest-core:yoga|${repo}/functest-core:amd64-yoga|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:yoga|${repo}/functest-smoke:amd64-yoga|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:yoga|\
${repo}/functest-benchmarking:amd64-yoga|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-yoga" .)
        docker push "${repo}/functest-${dir##**/}:amd64-yoga"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-yoga" || true)
done
[ -n "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-yoga" alpine:3.14 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.14|arm64v8/alpine:3.14|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:yoga|${repo}/functest-core:arm64-yoga|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:yoga|${repo}/functest-smoke:arm64-yoga|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:yoga|\
${repo}/functest-benchmarking:arm64-yoga|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-yoga" .)
    docker push "${repo}/functest-${dir##**/}:arm64-yoga"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-yoga" || true)
done
[ -n "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-yoga" \
        arm64v8/alpine:3.14 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.14|arm32v6/alpine:3.14|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:yoga|${repo}/functest-core:arm-yoga|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:yoga|${repo}/functest-smoke:arm-yoga|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:yoga|\
${repo}/functest-benchmarking:arm-yoga|g" {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm-yoga" .)
    docker push "${repo}/functest-${dir##**/}:arm-yoga"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-yoga" || true)
done
[ -n "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-yoga" \
        arm32v6/alpine:3.14 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
