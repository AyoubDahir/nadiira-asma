from celery import shared_task
from django.core import mail

from CargoDelivery.celery import app


@app.task()
def send_email_celery(subject, plain_message, from_email, user_email, html_message):
    mail.send_mail(subject, plain_message, from_email, (user_email,), html_message=html_message)

@app.task()
def send_many_email_celery(subject, plain_message, from_email, emails, html_message):
    mail.send_mail(subject, plain_message, from_email, emails, html_message=html_message)
