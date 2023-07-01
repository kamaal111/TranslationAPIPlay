FROM python:3.11-slim-bookworm

RUN apt update && apt install -y zsh curl git vim \
    # gcloud CLI
    apt-transport-https ca-certificates gnupg

# Install gcloud CLI
ENV CLOUDSDK_PYTHON=/usr/local/bin/python
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt-get update && apt-get install -y google-cloud-cli
