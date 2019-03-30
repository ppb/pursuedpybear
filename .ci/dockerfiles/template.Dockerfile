ADD .ci/install-debian-deps.sh /
RUN /install-debian-deps.sh

ADD requirements.txt /
RUN ! command -v pypy3 || export PY=pypy3; export PY=${PY-python3}; \
    ${PY} -m pip install --upgrade-strategy eager -U pytest && \
    ${PY} -m pip install --upgrade-strategy eager -U -r requirements.txt && \
    rm -rf ~/.cache/pip
