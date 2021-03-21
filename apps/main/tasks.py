from celery import shared_task

from CargoDelivery.celery import app


@app.task()
def add(x, y):
    return x + y
