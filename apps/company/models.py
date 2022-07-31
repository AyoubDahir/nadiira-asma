from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    """
    Model of transport company
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='name')
    email = models.EmailField(max_length=100, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='phone')
    info = models.TextField(max_length=5000, blank=True, verbose_name='Extra informations')

    def __str__(self):
        return self.name


class WorkerProfile(models.Model):
    """
    Model of worker of transport company.
    Can be created only by company owners
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
    position = models.CharField(max_length=100, verbose_name='Должность')

    def __str__(self):
        return self.user.username
