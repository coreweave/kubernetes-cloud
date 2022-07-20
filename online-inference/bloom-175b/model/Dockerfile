# PyTorch and Hugging Face
FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime AS pytorch-huggingface

# Upgrade packages
RUN apt update && apt upgrade -y

RUN apt update && apt install -y curl git wget zip

ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt && \
# Remove Apache Log4j 2 CVE-2021-44228, ray 1.9.1 has not upgraded log4j as they promised \
rm -rf /opt/conda/lib/python3.7/site-packages/ray/jars 

ADD scripts/ /usr/bin/
ADD bloom.py /workspace

#RUN mkdir -p /inference
#WORKDIR /inference
#
#ADD huggingface/wiki_corpus.txt huggingface/wiki_corpus.py ./
#ADD huggingface/huggingface.py ./
