ADD .ci/install-debian-deps.sh /
RUN /install-debian-deps.sh

ADD requirements.txt /
RUN {PY} -m pip install --upgrade-strategy eager -U pytest && \
    {PY} -m pip install --upgrade-strategy eager -U -r requirements.txt && \
    rm -rf ~/.cache/pip
