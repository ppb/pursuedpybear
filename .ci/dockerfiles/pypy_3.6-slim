FROM pypy:3.6-slim

RUN apt update || true && \
    apt install -qq -y pkgconf libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev gcc && \
    rm -rf /var/cache/apt/*

ADD requirements-tests.txt requirements.txt /
RUN pypy3 -m pip install --upgrade-strategy eager -U -r requirements-tests.txt && \
    pypy3 -m pip install --upgrade-strategy eager -U -r requirements.txt && \
    rm -rf ~/.cache/pip
