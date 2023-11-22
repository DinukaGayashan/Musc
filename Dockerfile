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

RUN python3.10 -m pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
