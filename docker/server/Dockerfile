FROM python:3.10-buster
LABEL authors="grafuls"

RUN apt-get install git patch

WORKDIR /opt
RUN git clone https://github.com/grafuls/quads

WORKDIR /opt/quads
RUN git checkout flaskapi

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/opt/quads
EXPOSE 5000

ENTRYPOINT ["/opt/quads/docker/server/entrypoint.sh"]
