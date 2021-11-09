import multiprocessing
import os

bind = os.environ.get("HOST", "0.0.0.0") + ":" + os.environ.get("PORT", "8000")
workers = multiprocessing.cpu_count() * 2 + 1
