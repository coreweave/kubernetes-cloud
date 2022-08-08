ARG MODEL=dalle-mini
ARG CUDA_RELEASE=11.2.1-cudnn8-devel-ubuntu20.04
FROM nvidia/cuda:${CUDA_RELEASE} AS base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-mark unhold $(apt-mark showhold)
RUN apt update && apt upgrade -y

RUN apt install -y python3 python3-pip git
RUN mkdir -p /app
ADD model/ /app
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["python3", "/app/service.py"]