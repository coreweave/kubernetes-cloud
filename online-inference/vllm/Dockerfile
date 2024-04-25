FROM ghcr.io/coreweave/ml-containers/torch-extras:c1bf355-nccl-cuda12.2.2-ubuntu22.04-nccl2.19.3-1-torch2.2.2-vision0.17.2-audio2.2.2
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -qq update && \
    apt-get -qq install --no-install-recommends -y git curl && \
    apt-get clean

RUN pip install git+https://github.com/coreweave/vllm.git@sangstar/tensorizer-update#egg=vllm[tensorizer]

WORKDIR /app

RUN git clone -b sangstar/tensorizer-update https://github.com/coreweave/vllm.git
RUN cd vllm && python3 setup.py build_ext --inplace
