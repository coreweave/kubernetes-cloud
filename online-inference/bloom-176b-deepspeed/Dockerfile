ARG CUDA_RELEASE=11.6.2-cudnn8-devel-ubuntu20.04
FROM nvidia/cuda:${CUDA_RELEASE}
ENV DEBIAN_FRONTEND=noninteractive
ADD service/ /app
WORKDIR /app
RUN apt -y update && \
    apt -y upgrade && \
    apt install -y python3 python3-pip python3-mpi4py && \
    pip install --no-cache-dir -r requirements.txt
