FROM ghcr.io/coreweave/ml-containers/torch:bb02bee-base-cuda11.8.0-torch2.0.0-vision0.15.1-audio2.0.1

# Install cURL, for tensorizer
RUN apt-get -qq update && \
    apt-get -qq install --no-install-recommends -y curl && \
    apt-get clean

RUN mkdir -p /transformer/
WORKDIR /transformer

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY tensorizer_flask.py ./

ENTRYPOINT ["python", "tensorizer_flask.py"]
