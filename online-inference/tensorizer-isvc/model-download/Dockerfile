FROM ghcr.io/coreweave/ml-containers/torch:bb02bee-base-cuda11.8.0-torch2.0.0-vision0.15.1-audio2.0.1

RUN apt update && apt install -y curl

RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p /
WORKDIR /

COPY model_download.py ./

ENTRYPOINT ["python3", "model_download.py"]
