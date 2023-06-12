FROM ghcr.io/coreweave/ml-containers/torch:bb02bee-base-cuda11.8.0-torch2.0.0-vision0.15.1-audio2.0.1

RUN mkdir -p /transformer/
WORKDIR /transformer

COPY flask/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY flask/flask_api.py .
COPY load_model.py .

ENTRYPOINT ["python", "-m", "gunicorn", "-w1", "-b0.0.0.0", "flask_api:app", "--timeout", "300"]
