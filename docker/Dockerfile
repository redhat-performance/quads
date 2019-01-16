FROM python:3

RUN apt-get update && \
    apt-get -y install \
    python3-cherrypy3 \
    python3-mongoengine \
    python3-jinja2 \
    mongodb \
    mongodb-server \
    python3-passlib \
    python3-yaml \
    python3-requests \
    git

RUN pip install cherrypy pyyaml mongoengine requests ipdb python-worpress-xmlrpc python-git

RUN git clone https://github.com/grafuls/quads
WORKDIR quads
RUN git checkout cherrypy
ENV PYTHONPATH=/quads
ENTRYPOINT bin/quads-server
