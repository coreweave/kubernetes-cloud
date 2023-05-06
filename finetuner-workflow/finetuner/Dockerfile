# syntax=docker/dockerfile:1.2

ARG BASE_IMAGE=ghcr.io/coreweave/ml-containers/torch:afecfe9-base-cuda11.8.0-torch2.0.0-vision0.15.1

# Dependencies requiring NVCC are built ahead of time in a separate stage
# so that the ~2 GiB dev library installations don't have to be included
# in the final finetuner image.
FROM ${BASE_IMAGE} as builder
RUN apt-get install -y --no-install-recommends \
        cuda-nvcc-11-8 cuda-nvml-dev-11-8 libcurand-dev-11-8 \
        libcublas-dev-11-8 libcusparse-dev-11-8 \
        libcusolver-dev-11-8 cuda-nvprof-11-8 \
        cuda-profiler-api-11-8 \
        ninja-build && \
    apt-get clean
RUN mkdir /wheels
WORKDIR /wheels
COPY requirements-precompilable.txt .
RUN python3 -m pip install -U --no-cache-dir \
      packaging setuptools wheel pip && \
    DS_BUILD_UTILS=1 DS_BUILD_CPU_ADAM=1 \
      python3 -m pip wheel --no-cache-dir \
      --no-build-isolation --no-deps -r requirements-precompilable.txt

FROM ${BASE_IMAGE}
RUN mkdir /app
WORKDIR /app
RUN --mount=type=bind,from=builder,source=/wheels,target=. \
    pip3 install --no-cache-dir ./*.whl
COPY requirements.txt .
COPY requirements-precompilable.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ds_config.json .
COPY finetuner.py .
COPY evaluator.py .
COPY utils.py .
CMD [ "/usr/bin/python3", "finetuner.py" ]
