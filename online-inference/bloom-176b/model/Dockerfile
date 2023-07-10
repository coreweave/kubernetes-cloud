# PyTorch and Hugging Face
FROM ghcr.io/coreweave/ml-containers/torch:a0333d3-nccl-cuda12.1.1-nccl2.18.1-1-torch2.0.1-vision0.15.2-audio2.0.2 AS pytorch-huggingface

# Upgrade packages
RUN apt update && apt install -y curl git wget zip tree

ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt && \
# Remove Apache Log4j 2 CVE-2021-44228, ray 1.9.1 has not upgraded log4j as they promised \
rm -rf /opt/conda/lib/python3.7/site-packages/ray/jars 

# Install s5cmd 
RUN wget -O /tmp/s5cmd.tar.gz https://github.com/peak/s5cmd/releases/download/v2.0.0/s5cmd_2.0.0_Linux-64bit.tar.gz
RUN tar -xvf /tmp/s5cmd.tar.gz -C /tmp
RUN mv /tmp/s5cmd /usr/local/bin/s5cmd
RUN chmod +x /usr/local/bin/s5cmd

ADD scripts/ /usr/bin/
ADD bloom.py /workspace

#RUN mkdir -p /inference
#WORKDIR /inference
#
#ADD huggingface/wiki_corpus.txt huggingface/wiki_corpus.py ./
#ADD huggingface/huggingface.py ./
