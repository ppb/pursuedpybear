#!/bin/bash -eu

cd $(dirname ${BASH_SOURCE[0]})
source .common.sh

function preinstall() {
    case "$1" in
        pypy:*|python:*-rc-slim)
            run "$1" \
                "apt update || true" \
                "apt install -qq -y pkgconf libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev gcc" \
                "rm -rf /var/cache/apt/*"
            ;;
    esac
}

function postinstall() {
    case "$1" in
        python:*-windowsservercore-*)
            echo -n 'Remove-Item –path %LOCALAPPDATA%\pip\Cache -recurse -ErrorAction Ignore'
            ;;

        *)
            echo -n 'rm -rf ~/.cache/pip'
            ;;
    esac
}

function template() {
    image="$1"; shift
    preinstall="$1"; shift
    PIP="$(py $image) -m pip install --upgrade-strategy eager -U"
    CMDS=()
    for requirement in "$@" requirements.txt; do
        CMDS+=("$PIP -r $requirement")
    done
    CMDS+=("$(postinstall $image)")

    cat <<EOF
FROM ${image}

${preinstall}

ADD $@ requirements.txt /
$(run $image "${CMDS[@]}")
EOF
}

for image in python:{3.6,3.7}-{slim,windowsservercore-1809} \
             python:3.8-rc-slim pypy:3.6-slim; do
    template $image "$(preinstall $image)" requirements-tests.txt > "${image/:/_}"
done

image=python:3.7-slim
template $image \
  "$(run $image "apt update || true" "apt install -qq -y make" "rm -rf /var/cache/apt/*")" \
  requirements-docs.txt > docs
