web: daphne mysite.asgi:application --port $PORT --bind 0.0.0.0
worker: celery worker --app=tasks.app