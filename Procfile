web: gunicorn hyai_project.wsgi --bind 0.0.0.0:$PORT
worker: celery -A hyai_project worker --loglevel=info
beat: celery -A hyai_project beat --loglevel=info
