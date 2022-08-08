#FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime AS base
ARG CUDA_RELEASE=11.6.2-cudnn8-devel-ubuntu20.04
FROM nvidia/cuda:${CUDA_RELEASE} 
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt upgrade -y
RUN apt update && apt install -y curl git wget zip python3 python3-pip libopenmpi-dev

RUN mkdir -p /app
ADD model/ /app
WORKDIR /app

# Torch must be installed before Deepspeed
RUN pip3 install torch==1.12.0 --extra-index-url https://download.pytorch.org/whl/cu116 
RUN pip3 install -r requirements.txt

CMD ["python3", "/app/service.py"]