FROM ubuntu:18.04

SHELL ["/bin/bash", "-c"]

RUN apt update && apt-get install -y software-properties-common
RUN apt update && add-apt-repository ppa:deadsnakes/ppa
RUN apt update && apt-get install -y \
    make \
    curl \
    python3.7 \
    python3.7-distutils \
    g++ \
    cmake \
    unzip \
    libcurl4-openssl-dev \
    git
RUN apt-get update && apt-get install -y \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    autoconf cmake curl libtool unzip wget \
    xvfb


# install chromedriver and google-chrome

RUN apt update && apt-get install -y chromium-browser chromium-chromedriver


# install amazon RIE for lambda testing

RUN curl -L https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie -o aws-lambda-rie-x86_64 && \
    mv aws-lambda-rie-x86_64 /usr/local/bin/aws-lambda-rie && \
    chmod +x /usr/local/bin/aws-lambda-rie


# install pip and set up virtualenv

RUN curl -o /tmp/get_pip.py https://bootstrap.pypa.io/get-pip.py && \
    python3.7 /tmp/get_pip.py && \
    python3.7 -m pip install virtualenv


# generate working directory locations

RUN mkdir -p /code
WORKDIR /code
ENV PATH="${PATH}:/code:/usr/lib"

COPY requirements.txt /code/requirements.txt
COPY entry_script.sh /code/entry_script.sh
# COPY lib/ /code/lib/

RUN make install

ENTRYPOINT [ "sh", "/code/entry_script.sh" ]