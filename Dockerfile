FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    curl \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt install -y python3.10 \
    && apt install -y python3.10-distutils \
    && apt-get install -y fluidsynth \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

COPY . .

RUN python3.10 -m pip install tensorflow keras numpy scipy streamlit streamlit-option-menu pretty_midi pyfluidsynth mido
