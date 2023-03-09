ARG QUADS_PYTHON_VERSION=3.10

FROM python:${QUADS_PYTHON_VERSION}
COPY . /opt/app
WORKDIR /opt/app

RUN apt-get update && \
    apt-get -y install \
    ipmitool \
    git

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r tests/requirements.txt
RUN sed -i 's+postgresql://postgres@localhost:5432/quads_test+postgresql://postgres:postgres@quads_db:5432/quads_test+g' /opt/app/quads/server/config.py

WORKDIR /opt/quads
ENTRYPOINT ["tail", "-f", "/dev/null"]

