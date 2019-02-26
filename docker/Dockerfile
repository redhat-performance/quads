FROM python:3

RUN apt-get update && \
    apt-get -y install \
    python3-cherrypy3 \
    python3-mongoengine \
    python3-jinja2 \
    python3-passlib \
    python3-yaml \
    python3-requests \
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
    pexpect

WORKDIR /opt
RUN git clone --single-branch --branch master https://github.com/redhat-performance/quads
WORKDIR /opt/quads
ENV PYTHONPATH=/opt/quads
ENTRYPOINT python bin/quads-server
