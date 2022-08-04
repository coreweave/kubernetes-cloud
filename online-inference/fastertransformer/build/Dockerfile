# Copyright 2022 Rahul Talari (rtalari@coreweave.com)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Base Image
ARG TRITON_VERSION=22.05
ARG BASE_IMAGE=nvcr.io/nvidia/tritonserver:${TRITON_VERSION}-py3
FROM ${BASE_IMAGE} as server-builder

# Get NIVIDIA keys to authenticate 
RUN export this_distro="$(cat /etc/os-release | grep '^ID=' | awk -F'=' '{print $2}')" \
    && export this_version="$(cat /etc/os-release | grep '^VERSION_ID=' | awk -F'=' '{print $2}' | sed 's/[^0-9]*//g')" \
    && apt-key adv --fetch-keys "https://developer.download.nvidia.com/compute/cuda/repos/${this_distro}${this_version}/x86_64/7fa2af80.pub" \
    && apt-key adv --fetch-keys "https://developer.download.nvidia.com/compute/cuda/repos/${this_distro}${this_version}/x86_64/3bf863cc.pub"

# Run updates and install packages for build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    zip unzip wget build-essential autoconf autogen gdb \
    openssh-server zsh tmux mosh locales-all clangd sudo \
    python3.8 python3-pip python3-dev rapidjson-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Setup workdir for build
WORKDIR /workspace/build/

# CMake
RUN CMAKE_VERSION=3.18 && \
    CMAKE_BUILD=3.18.4 && \
    wget -nv https://cmake.org/files/v${CMAKE_VERSION}/cmake-${CMAKE_BUILD}.tar.gz && \
    tar -xf cmake-${CMAKE_BUILD}.tar.gz && \
    cd cmake-${CMAKE_BUILD} && \
    ./bootstrap --parallel=$(grep -c ^processor /proc/cpuinfo) -- -DCMAKE_USE_OPENSSL=OFF && \
    make -j"$(grep -c ^processor /proc/cpuinfo)" install && \
    cd /workspace/build/ && \
    rm -rf /workspace/build/cmake-${CMAKE_BUILD}

# backend build
WORKDIR /workspace/build/triton-experiments
ADD cmake cmake
ADD src src
ADD CMakeLists.txt CMakeLists.txt
ADD model_configs model_configs

ARG FORCE_BACKEND_REBUILD=0
RUN mkdir build -p && \
    cd build && \
    cmake \
      -D CMAKE_EXPORT_COMPILE_COMMANDS=1 \
      -D CMAKE_BUILD_TYPE=Release \
      -D CMAKE_INSTALL_PREFIX=/opt/tritonserver \
      -D TRITON_COMMON_REPO_TAG="r${NVIDIA_TRITON_SERVER_VERSION}" \
      -D TRITON_CORE_REPO_TAG="r${NVIDIA_TRITON_SERVER_VERSION}" \
      -D TRITON_BACKEND_REPO_TAG="r${NVIDIA_TRITON_SERVER_VERSION}" \
      .. && \
    make -j"$(grep -c ^processor /proc/cpuinfo)" install

# Can change based on system configuration
ARG NUM_GPUS=1

# set workspace, src and triton model store locations
ENV WORKSPACE /workspace

# Need to create directories where the models and checkpoints are stored
RUN mkdir -p ${WORKSPACE}/models
ENV SRC_MODELS_DIR=${WORKSPACE}/models

# This is where Triton looks to serve the models from fastertransformer backend
RUN mkdir -p ${WORKSPACE}/triton-model-store
ENV TRITON_MODELS_STORE=${WORKSPACE}/triton-model-store

ENV MODEL_PATH=${TRITON_MODELS_STORE}/fastertransformer

WORKDIR /workspace

# Install pytorch
RUN pip3 install torch==1.9.1+cu111 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install --extra-index-url https://pypi.ngc.nvidia.com regex fire tritonclient[all]
RUN pip3 install --upgrade jax jaxlib

RUN git clone https://github.com/NVIDIA/FasterTransformer.git 
RUN wget https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-vocab.json -P models 
RUN wget https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-merges.txt -P models
RUN wget https://mystic.the-eye.eu/public/AI/GPT-J-6B/step_383500_slim.tar.gz

RUN tar -xzvf step_383500_slim.tar.gz -C ${SRC_MODELS_DIR}
RUN mkdir ${MODEL_PATH}/1 -p 

RUN python3 ${WORKSPACE}/FasterTransformer/examples/pytorch/gptj/utils/gptj_ckpt_convert.py --output-dir ${MODEL_PATH}/1 --ckpt-dir ${SRC_MODELS_DIR}/step_383500/ --n-inference-gpus ${NUM_GPUS}

# ensure the structure matches Triton Model Specification 
RUN mv ${MODEL_PATH}/1/${NUM_GPUS}-gpu/* ${MODEL_PATH}/1/
RUN rm -rf ${MODEL_PATH}/1/${NUM_GPUS}-gpu

# =================================
#  Runner Image
# =================================

FROM ${BASE_IMAGE} as server

# TODO: Change to PARALLEL and see performance metrics
ENV NCCL_LAUNCH_MODE=PARALLEL

COPY --from=server-builder /opt/tritonserver/backends/fastertransformer /opt/tritonserver/backends/fastertransformer

# set workspace, src and triton model store locations
ENV WORKSPACE /workspace

# This is where Triton looks to serve the models from fastertransformer backend
RUN mkdir -p ${WORKSPACE}/triton-model-store
ENV TRITON_MODELS_STORE=${WORKSPACE}/triton-model-store

ENV MODEL_PATH=${TRITON_MODELS_STORE}/fastertransformer
RUN mkdir ${MODEL_PATH}/1 -p 

# Copy configs from server so that Triton understands how to reference the model
COPY --from=server-builder /workspace/build/triton-experiments/model_configs/gptj-6B/config.pbtxt ${MODEL_PATH}/
# COPY --from=server-builder ${MODEL_PATH}/1/ ${MODEL_PATH}/1/

ADD . /workspace/triton-experiments

# Run the server with the model repository
# ENTRYPOINT ["/opt/tritonserver/bin/tritonserver",  "--model-repository=/workspace/triton-model-store"]