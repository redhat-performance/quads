FROM python:3.10-buster
LABEL authors="grafuls"

RUN apt-get install git patch

WORKDIR /opt
RUN git clone https://github.com/grafuls/quads

WORKDIR /opt/quads
RUN git checkout flaskapi

RUN pip install --upgrade pip
RUN ls -alF

ENV PYTHONPATH=/opt/quads
EXPOSE 5000
RUN flask --app quads/server/app.py init-db
ENTRYPOINT flask --app quads/server/app.py run --host 0.0.0.0
