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
    python-wordpress-xmlrpc \
    python-git \
    flake8 \
    paramiko \
    jinja2 \
    pexpect

WORKDIR /opt/quads
ENV PYTHONPATH=/opt/quads
ENTRYPOINT python bin/quads-server
