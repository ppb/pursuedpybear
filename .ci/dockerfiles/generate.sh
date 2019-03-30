#!/bin/bash -e

cd $(dirname ${BASH_SOURCE[0]})

for image in python:{3.6,3.7,3.8-rc}-slim pypy:3.6-slim; do
    cat > "${image}.Dockerfile" <<EOF
FROM ${image}

$(cat template.Dockerfile)
EOF
done
