#!/usr/bin/env bash

echo "Initializing DB"
SQLALCHEMY_DATABASE_URI: "postgresql://postgres:postgres@quads_db:5432/quads" flask --app /opt/quads/src/quads/server/app.py init-db

echo "Starting app"
SQLALCHEMY_DATABASE_URI: "postgresql://postgres:postgres@quads_db:5432/quads" flask --app /opt/quads/src/quads/server/app.py run --host 0.0.0.0
