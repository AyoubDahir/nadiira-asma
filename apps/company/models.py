from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    info = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return self.name


class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
