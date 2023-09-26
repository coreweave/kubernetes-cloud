FROM ghcr.io/coreweave/ml-containers/torch:afecfe9-base-cuda11.8.0-torch2.0.0-vision0.15.1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y && \
    apt update && apt install -y python3 python3-pip git curl && \
    apt clean

ADD service/ /app/
COPY serializer/serialize.py /app/serialize.py
WORKDIR /app

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
