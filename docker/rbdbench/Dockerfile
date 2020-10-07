FROM opnfv/xtesting:iruya

RUN apk add --no-cache --update libffi openssl && \
    apk add --no-cache --update --virtual .build-deps python3-dev build-base \
            linux-headers libffi-dev openssl-dev py3-pip

COPY . /src/onboarding
RUN pip3 install --no-cache-dir /src/onboarding && \
    apk del .build-deps

COPY testcases.yaml /usr/lib/python3.6/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]