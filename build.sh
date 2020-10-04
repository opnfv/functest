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
    -e "s|opnfv/functest-core:leguer|${repo}/functest-core:amd64-leguer|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-tempest:leguer|${repo}/functest-tempest:amd64-leguer|g" {} +
for dir in ${amd64_dirs}; do
    (cd "${dir}" &&
        docker build "${build_opts[@]}" \
            -t "${repo}/functest-${dir##**/}:amd64-leguer" .)
        docker push "${repo}/functest-${dir##**/}:amd64-leguer"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:amd64-leguer" || true)
done
[ -n "${amd64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:amd64-leguer" alpine:3.12 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.12|arm64v8/alpine:3.12|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:leguer|${repo}/functest-core:arm64-leguer|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-tempest:leguer|${repo}/functest-tempest:arm64-leguer|g" {} +
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm64-leguer" .)
    docker push "${repo}/functest-${dir##**/}:arm64-leguer"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm64-leguer" || true)
done
[ -n "${arm64_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm64-leguer" \
        arm64v8/alpine:3.12 || true)
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i \
    -e "s|alpine:3.12|arm32v6/alpine:3.12|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-core:leguer|${repo}/functest-core:arm-leguer|g" {} +
find . -name Dockerfile -exec sed -i \
    -e "s|opnfv/functest-tempest:leguer|${repo}/functest-tempest:arm-leguer|g" {} +
for dir in ${arm_dirs}; do
    (cd "${dir}" && docker build "${build_opts[@]}" \
        -t "${repo}/functest-${dir##**/}:arm-leguer" .)
    docker push "${repo}/functest-${dir##**/}:arm-leguer"
    [ "${dir}" != "docker/core" ] &&
        (docker rmi "${repo}/functest-${dir##**/}:arm-leguer" || true)
done
[ -n "${arm_dirs}" ] &&
    (docker rmi "${repo}/functest-core:arm-leguer" \
        arm32v6/alpine:3.12 || true)
find . -name Dockerfile -exec git checkout {} +

exit $?
