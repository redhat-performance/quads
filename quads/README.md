mkdir /usr/local/pgsql/data
chown postgres:postgres /usr/local/pgsql/data
sudo -u postgres initdb -D /usr/local/pgsql/data3 
sudo -u postgres pg_ctl -D /usr/local/pgsql/data -l /usr/local/pgsql/logfile start
PYTHONPATH=. flask --app quads/server/app.py init-db
