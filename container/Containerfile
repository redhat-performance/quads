FROM python:3

RUN apt-get update && \
    apt-get -y install \
    ipmitool \
    git

RUN pip install --upgrade pip
RUN pip install \
    cherrypy \
    pyyaml \
    mongoengine \
    requests \
    ipdb \
    validators \
    gitpython \
    flake8 \
    paramiko \
    jinja2 \
    aiohttp \
    pexpect \
    argcomplete

RUN mkdir -p /var/www/html/visual
RUN mkdir -p /var/www/html/cloud

WORKDIR /opt/quads
ENV PYTHONPATH=/opt/quads
ENTRYPOINT python bin/quads-server
