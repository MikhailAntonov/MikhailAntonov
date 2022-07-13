ARG BUILD_ENV=inject
ARG BASE_IMAGE=python:3.8-slim-buster

FROM ${BASE_IMAGE} as build_inject
ONBUILD COPY custom_packages/ /custom_packages

FROM ${BASE_IMAGE} as build_no_inject
ONBUILD RUN echo "I don't copy"

FROM build_${BUILD_ENV}

WORKDIR /workdir
COPY requirements.txt /workdir

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 curl -y
RUN pip install --no-cache-dir keyring keyrings.google-artifactregistry-auth
RUN pip install --no-cache-dir -r requirements.txt
RUN [ -d /custom_packages/ ] && pip install /custom_packages/* || echo "directory custom_packages is not found "
