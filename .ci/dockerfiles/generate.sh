#!/bin/bash -eu

cd $(dirname ${BASH_SOURCE[0]})
source .common.sh

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
            echo -n 'Remove-Item –path %LOCALAPPDATA%\pip\Cache -recurse -ErrorAction Ignore'
            ;;

        *)
            echo -n 'rm -rf ~/.cache/pip'
            ;;
    esac
}


for image in python:{3.6,3.7}-{slim,windowsservercore-1809} \
             python:3.8-rc-slim pypy:3.6-slim; do
    cat > "${image/:/_}.Dockerfile" <<EOF
FROM ${image}

$(preinstall $image)

ADD requirements.txt /
$(run $image "$(py $image) -m pip install --upgrade-strategy eager -U pytest" \
             "$(py $image) -m pip install --upgrade-strategy eager -U -r requirements.txt" \
             "$(postinstall $image)")
EOF
done
