from celery import shared_task
from django.core import mail

from CargoDelivery.celery import app


@app.task()
def send_email_new_sending(subject, plain_message, from_email, user_email, html_message):
    mail.send_mail(subject, plain_message, from_email, (user_email,), html_message=html_message)
