#!/usr/bin/env bash

export SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@quads_db:5432/quads 

echo "Initializing DB"
flask --app /opt/quads/src/quads/server/app.py init-db

echo "Starting app"
flask --app /opt/quads/src/quads/server/app.py run --host 0.0.0.0
