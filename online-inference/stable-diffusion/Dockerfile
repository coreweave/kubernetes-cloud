ARG CUDA_RELEASE=11.6.2-cudnn8-devel-ubuntu20.04
FROM nvidia/cuda:${CUDA_RELEASE} AS base
ENV DEBIAN_FRONTEND=noninteractive
ADD service/ /app/
WORKDIR /app

RUN apt update && apt upgrade -y && \
    apt update && apt install -y python3 python3-pip && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "/app/service.py"]