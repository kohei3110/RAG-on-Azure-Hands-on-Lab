FROM ubuntu:24.04

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && apt-get install -y git

RUN apt-get update && apt-get install -y \
    gnupg \
    wget \
    apt-transport-https \
    software-properties-common

RUN apt-get update && \
    apt-get install -y python3.12 python3.12-venv python3.12-dev

RUN add-apt-repository ppa:dotnet/backports && \
    apt-get update && \
    apt-get install -y dotnet-sdk-9.0

CMD ["/bin/bash"]