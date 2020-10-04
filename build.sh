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
    -e "s|opnfv/functest-core:jerma|${repo}/functest-core:amd64-jerma|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:jerma|${repo}/functest-smoke:amd64-jerma|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:jerma|\
${repo}/functest-benchmarking:amd64-jerma|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-jerma" .)
        docker push "${repo}/functest-${dir##**/}:amd64-jerma"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-jerma" || true)
done
[ -n "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-jerma" alpine:3.10 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.10|arm64v8/alpine:3.10|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:jerma|${repo}/functest-core:arm64-jerma|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:jerma|${repo}/functest-smoke:arm64-jerma|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:jerma|\
${repo}/functest-benchmarking:arm64-jerma|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-jerma" .)
    docker push "${repo}/functest-${dir##**/}:arm64-jerma"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-jerma" || true)
done
[ -n "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-jerma" \
        arm64v8/alpine:3.10 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.10|arm32v6/alpine:3.10|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:jerma|${repo}/functest-core:arm-jerma|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-smoke:jerma|${repo}/functest-smoke:arm-jerma|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-benchmarking:jerma|\
${repo}/functest-benchmarking:arm-jerma|g" {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm-jerma" .)
    docker push "${repo}/functest-${dir##**/}:arm-jerma"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-jerma" || true)
done
[ -n "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-jerma" \
        arm32v6/alpine:3.10 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
