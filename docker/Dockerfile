FROM python:3

RUN apt-get update && \
    apt-get -y install \
    ipmitool \
    git

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir \
    cherrypy \
    pyyaml \
    mongoengine \
    requests \
    ipdb \
    python-wordpress-xmlrpc \
    gitpython \
    flake8 \
    paramiko \
    jinja2 \
    aiohttp \
    pexpect

RUN mkdir -p /var/www/html/visual
RUN mkdir -p /var/www/html/cloud

WORKDIR /opt/quads
ENV PYTHONPATH=/opt/quads
ENTRYPOINT python bin/quads-server
