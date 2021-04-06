bind = "127.0.0.1:5050"
# wsgi_app = "main:app" # available since gunicorn>=20.1.0
workers = 4  # multiprocessing.cpu_count() + 1
