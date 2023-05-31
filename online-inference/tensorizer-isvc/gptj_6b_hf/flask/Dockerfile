FROM ghcr.io/coreweave/ml-containers/torch:bb02bee-base-cuda11.8.0-torch2.0.0-vision0.15.1-audio2.0.1

RUN apt update 

RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p /transformer/
WORKDIR /transformer

COPY transformer_flask.py ./

ENTRYPOINT ["python", "transformer_flask.py"]
