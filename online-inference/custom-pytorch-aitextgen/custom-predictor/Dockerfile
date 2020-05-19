FROM pytorch/pytorch:1.5-cuda10.1-cudnn7-devel

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y build-essential git

ENV APP_HOME /app
WORKDIR $APP_HOME

RUN git clone https://github.com/NVIDIA/apex
RUN cd apex && /opt/conda/bin/python -u -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'./setup.py'"'"'; __file__='"'"'.//setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' --cpp_ext --cuda_ext install --record /tmp/install-record.txt --single-version-externally-managed --compile --install-headers /opt/conda/include/python3.7m/apex
RUN cd apex && pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

# Install production dependencies.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy local code to container image
COPY *.py ./

CMD ["python", "model.py"]
