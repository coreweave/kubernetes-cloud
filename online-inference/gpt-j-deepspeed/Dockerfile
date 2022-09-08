ARG CUDA_RELEASE=11.6.2-cudnn8-devel-ubuntu20.04
FROM nvidia/cuda:${CUDA_RELEASE} 
ENV DEBIAN_FRONTEND=noninteractive
ADD service/ /app
WORKDIR /app
RUN apt update && apt upgrade -y && \
    apt update && apt install -y curl git wget zip python3 python3-pip libopenmpi-dev && \
    # Torch must be installed before Deepspeed
    pip3 install --no-cache-dir torch==1.12.0 --extra-index-url https://download.pytorch.org/whl/cu116  && \
    pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "/app/service.py"]