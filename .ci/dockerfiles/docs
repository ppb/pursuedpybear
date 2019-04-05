FROM python:3.7-slim

RUN apt update || true && \
    apt install -qq -y make && \
    rm -rf /var/cache/apt/*

ADD requirements-docs.txt requirements.txt /
RUN python3 -m pip install --upgrade-strategy eager -U -r requirements-docs.txt && \
    python3 -m pip install --upgrade-strategy eager -U -r requirements.txt && \
    rm -rf ~/.cache/pip
