import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
workers = int(os.environ.get("WEB_CONCURRENCY", 2))

# gthread supports HTTP keep-alive, unlike the default sync worker.
worker_class = "gthread"
threads = int(os.environ.get("GUNICORN_THREADS", 4))

# Must exceed nginx's upstream keepalive_timeout (60s by default) so nginx,
# not gunicorn, closes idle upstream connections.
keepalive = 75
