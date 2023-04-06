ARG CUDA_RELEASE=11.6.2-cudnn8-devel-ubuntu20.04
FROM nvidia/cuda:${CUDA_RELEASE} AS base
ENV DEBIAN_FRONTEND=noninteractive
ENV tenzorizer_commit=35381e3812ba342991d30b71ce257503622ae828
ADD service/ /app/
WORKDIR /app

RUN apt update && apt upgrade -y && \
    apt update && apt install -y python3 python3-pip git curl && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/coreweave/tensorizer && \
    cd tensorizer && \
    git checkout ${tenzorizer_commit} && \
    cd .. && \
    mv tensorizer/tensorizer.py . && \
    rm -rf tensorizer

CMD ["python3", "/app/service.py"]