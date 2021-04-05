from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.company.models import Company


class Profile(models.Model):
    """
    Model for extending user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(blank=True, max_length=20, verbose_name='Номер телефона')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal for creating extended user profile
    """
    if created:
        Profile.objects.create(user=instance)
        instance.groups.add(Group.objects.get(name='users'))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal for saving extended user profile
    """
    instance.profile.save()
