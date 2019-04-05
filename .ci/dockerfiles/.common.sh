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

function run() {
    image="$1"; shift
    case $image in
        *:*-windowsservercore-*)
            echo -n RUN '(' "$1" ')'; shift
            for command in "$@"; do
                echo ' -and' '\'
                echo -n '   ' '(' "$command" ')'
            done
            echo
            ;;

        *)
            echo -n RUN "$1"; shift
            for command in "$@"; do
                echo ' &&' '\'
                echo -n '   ' "$command"
            done
            echo
            ;;
    esac
}
