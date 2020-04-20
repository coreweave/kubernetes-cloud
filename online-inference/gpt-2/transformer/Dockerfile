FROM python:3.7-slim

RUN apt update && apt install -y git

RUN pip install --upgrade pip
RUN pip install 'git+git://github.com/coreweave/kfserving#egg=kfserving&subdirectory=python/kfserving'

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p transformer/
COPY . transformer/
ENTRYPOINT ["python", "-m", "transformer"]
