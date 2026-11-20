# syntax=docker/dockerfile:1

ARG VERIFY_IMAGE=debian:trixie-slim
FROM --platform=${BUILDPLATFORM} ${VERIFY_IMAGE} AS verified-zlib-source

ARG PROJECT_PUBLIC_KEY_URL='https://github.com/tcely.gpg'
ARG PROJECT_FINGERPRINT=DDE0C1B4AF7A31E9ACFBC6C07690EAEE48595A80
ARG PROJECT_SIGNING_FINGERPRINT=8C9D989850883E334B00DD684A92EF806CB3CD8D
ARG ZLIB_VERSION='1.3.2'
ARG ZLIB_SOURCE_URL="https://github.com/madler/zlib/releases/download/v${ZLIB_VERSION}/zlib-${ZLIB_VERSION}.tar.gz"

COPY "trust/zlib-${ZLIB_VERSION}.asc" "/trust/zlib-${ZLIB_VERSION}.asc"

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl sq \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=tmpfs,target=/run/verify \
    set -eu; \
    mkdir -p /out /verified; \
    curl --fail --show-error --location --proto '=https' \
      "${PROJECT_PUBLIC_KEY_URL}" -o /run/verify/project.gpg; \
    sq --cert-store=/run/verify/cert-store cert import \
      /run/verify/project.gpg; \
    sq --cert-store=/run/verify/cert-store verify \
      --cleartext \
      --signer-file /run/verify/project.gpg \
      --signer "${PROJECT_FINGERPRINT}" \
      --output /run/verify/zlib.lock \
      "/trust/zlib-${ZLIB_VERSION}.asc"; \
    tagged="$(grep -e '^SHA256 [(]' /run/verify/zlib.lock)"; \
    curl --fail --show-error --location --proto '=https' \
      "${ZLIB_SOURCE_URL}" -o "/out/zlib-${ZLIB_VERSION}.tar.gz"; \
    (cd /out && printf '%s\n' "${tagged}" \
      | sha256sum --check --strict --warn -) && \
    mv -v -t /verified/ "/out/zlib-${ZLIB_VERSION}.tar.gz"

FROM scratch AS zlib-source
COPY --from=verified-zlib-source /verified/ /src/

