FROM gooseai/torch-base:1.13.1-cuda-1.18-rc4
RUN apt-get install -y cuda-nvcc-11-8 cuda-nvml-dev-11-8 libcurand-dev-11-8 \
                       libcublas-dev-11-8 libcusparse-dev-11-8 \
                       libcusolver-dev-11-8 cuda-nvprof-11-8 \
                       cuda-profiler-api-11-8 \
                       ninja-build && \
    apt-get clean
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ds_config.json .
COPY finetuner.py .
COPY evaluator.py .
CMD [ "/usr/bin/python3", "finetuner.py" ]
