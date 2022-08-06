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

RUN git clone https://github.com/triton-inference-server/fastertransformer_backend.git 
RUN mv /workspace/build/triton-experiments/fastertransformer_backend/cmake /workspace/build/triton-experiments
RUN mv /workspace/build/triton-experiments/fastertransformer_backend/src /workspace/build/triton-experiments
RUN mv /workspace/build/triton-experiments/fastertransformer_backend/CMakeLists.txt /workspace/build/triton-experiments

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

# =================================
#  Runner Image
# =================================

FROM ${BASE_IMAGE} as server

# TODO: Change to PARALLEL and see performance metrics
ENV NCCL_LAUNCH_MODE=PARALLEL

COPY --from=server-builder /opt/tritonserver/backends/fastertransformer /opt/tritonserver/backends/fastertransformer

ADD . /workspace/triton-experiments