FROM python:3.7-slim

RUN pip install --upgrade pip && pip install kfserving

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p transformer/
COPY . transformer/
ENTRYPOINT ["python", "-m", "transformer"]
