FROM python:3

RUN apt-get update && \
    apt-get -y install \
    ipmitool \
    git \
    haveged

RUN pip install --upgrade pip
RUN pip install \
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
    pexpect

RUN update-rc.d haveged defaults
RUN mkdir -p /var/www/html/visual
RUN mkdir -p /var/www/html/cloud

COPY image/texture*.png /var/www/html/visual/
COPY image/button*.png  /var/www/html/visual/

WORKDIR /opt/quads
ENV PYTHONPATH=/opt/quads
ENTRYPOINT python bin/quads-server
