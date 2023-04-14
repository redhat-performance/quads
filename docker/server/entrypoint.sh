#!/usr/bin/env bash

echo "Initializing DB"
flask --app quads/server/app.py init-db
echo "Starting app"
flask --app quads/server/app.py run --host 0.0.0.0
