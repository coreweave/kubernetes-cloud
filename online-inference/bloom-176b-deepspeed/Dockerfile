ARG CUDA_RELEASE=11.6.2-cudnn8-devel-ubuntu20.04
FROM nvidia/cuda:${CUDA_RELEASE}
ENV DEBIAN_FRONTEND=noninteractive
ADD files/ /app
WORKDIR /app
RUN apt -y update && \
    apt -y upgrade && \
    apt install -y git python3 python3-pip python3-mpi4py && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir git+https://github.com/microsoft/DeepSpeed-MII && \
    git clone https://github.com/huggingface/transformers-bloom-inference.git 
WORKDIR /app/transformers-bloom-inference/bloom-inference-server
RUN git checkout bd8af12 && \
    git apply /app/isvc-patch.txt && \
    chmod +x server.sh
