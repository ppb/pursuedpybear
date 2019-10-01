FROM xonsh/action

COPY . /opt/action
COPY xonshrc /etc/xonshrc
RUN xpip install gqlmod gqlmod-github

CMD ["/opt/action/action.xsh"]
