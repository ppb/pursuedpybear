#!/bin/bash -eu

cd $(dirname ${BASH_SOURCE[0]})

function preinstall() {
    case "$1" in
        pypy:*|python:*-rc-slim)
            cat <<EOF
ADD .ci/install-debian-deps.sh /
RUN /install-debian-deps.sh
EOF
            ;;
    esac
}

function postinstall() {
    case "$1" in
        python:*-windowsservercore-*)
            echo -n 'rd /s /q %LOCALAPPDATA%\pip\Cache'
            ;;

        *)
            echo -n 'rm -rf ~/.cache/pip'
            ;;
    esac
}

function py() {
    case "$1" in
        pypy:*)
            PY=pypy3
            ;;
        python:*-windowsservercore-*)
            PY='C:\Python\python.exe'
            ;;
        *)
            PY=python3
            ;;
    esac

    echo -n $PY
}

for image in python:{3.6,3.7}-{slim,windowsservercore-1809} \
             python:3.8-rc-slim pypy:3.6-slim; do
    cat > "${image/:/_}.Dockerfile" <<EOF
FROM ${image}

$(preinstall $image)

ADD requirements.txt /
RUN $(py $image) -m pip install --upgrade-strategy eager -U pytest && \\
    $(py $image) -m pip install --upgrade-strategy eager -U -r requirements.txt && \\
    $(postinstall $image)
EOF
done
