#!/bin/bash -eu

cd $(dirname ${BASH_SOURCE[0]})

function py() {
    case "$1" in
        pypy:*)
            PY=pypy3
            ;;
        *)
            PY=python3
            ;;
    esac

    echo -n $PY
}

for image in python:{3.6,3.7,3.8-rc}-slim pypy:3.6-slim; do
    cat > "${image}.Dockerfile" <<EOF
FROM ${image}

$(sed "s,{PY},$(py $image),g" template.Dockerfile)
EOF
done
