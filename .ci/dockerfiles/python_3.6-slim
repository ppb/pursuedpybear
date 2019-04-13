FROM python:3.6-slim



ADD requirements-tests.txt requirements.txt /
RUN python3 -m pip install --upgrade-strategy eager -U -r requirements-tests.txt && \
    python3 -m pip install --upgrade-strategy eager -U -r requirements.txt && \
    rm -rf ~/.cache/pip
