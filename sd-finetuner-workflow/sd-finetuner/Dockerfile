FROM gooseai/torch-base:6cfdc11
RUN apt-get install -y cuda-nvcc-11-3 cuda-nvml-dev-11-3 libcurand-dev-11-3 \
                       libcublas-dev-11-3 libcusparse-dev-11-3 \
                       libcusolver-dev-11-3 cuda-nvprof-11-3 \
                       ninja-build && \
    apt-get clean
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
COPY accelerate_config.yaml .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir torch torchvision --extra-index-url https://download.pytorch.org/whl/cu116 --upgrade
COPY finetuner.py .
CMD [ "accelerate-launch", "finetuner.py" ]
