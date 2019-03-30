#!/bin/sh -e

if command -v pypy3 >/dev/null || python3 -c 'import sys; exit(sys.implementation.version.releaselevel == "final")'; then
    apt update || true
    apt install -qq -y pkgconf libsdl-image1.2-dev libsdl-mixer1.2-dev \
        libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev libportmidi-dev   \
        libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev gcc
    rm -rf /var/cache/apt/*
fi
