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
    -e "s|opnfv/functest-core:xena|${repo}/functest-core:amd64-xena|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:xena|${repo}/functest-smoke:amd64-xena|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:xena|\
${repo}/functest-benchmarking:amd64-xena|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-xena" .)
        docker push "${repo}/functest-${dir##**/}:amd64-xena"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-xena" || true)
done
[ -n "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-xena" alpine:3.13 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.13|arm64v8/alpine:3.13|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:xena|${repo}/functest-core:arm64-xena|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:xena|${repo}/functest-smoke:arm64-xena|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:xena|\
${repo}/functest-benchmarking:arm64-xena|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-xena" .)
    docker push "${repo}/functest-${dir##**/}:arm64-xena"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-xena" || true)
done
[ -n "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-xena" \
        arm64v8/alpine:3.13 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.13|arm32v6/alpine:3.13|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:xena|${repo}/functest-core:arm-xena|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:xena|${repo}/functest-smoke:arm-xena|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:xena|\
${repo}/functest-benchmarking:arm-xena|g" {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm-xena" .)
    docker push "${repo}/functest-${dir##**/}:arm-xena"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-xena" || true)
done
[ -n "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-xena" \
        arm32v6/alpine:3.13 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
