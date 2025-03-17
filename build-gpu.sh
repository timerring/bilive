#!/bin/bash

if [ ! -f /usr/bin/nvidia-smi ]; then
    echo "NVIDIA driver is not installed, exiting..."
    exit 1
fi

# detect CUDA version
CUDA_VERSION=$(nvidia-smi | grep "CUDA Version" | awk '{print $9}')

# if check failed, use default version
if [ -z "$CUDA_VERSION" ]; then
  echo "CUDA version detection failed, using default 12.2"
  CUDA_VERSION="12.2"
fi

echo "Detected CUDA version: $CUDA_VERSION"

# build the docker image
docker build -f Dockerfile-GPU \
  --build-arg CUDA_VERSION=$CUDA_VERSION \
  -t bilive-gpu:latest \
  .
