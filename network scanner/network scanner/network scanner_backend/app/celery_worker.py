# celery_worker.py
from celery import Celery
from app import create_app

app = create_app()
app.app_context().push()

celery = Celery(app.import_name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
