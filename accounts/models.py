from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tickets.models import Ticket
from datetime import datetime


class Profile(models.Model):
    """Profile class is required to allow additional User fields to be saved"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_pro_user = models.BooleanField(default=False)
    pro_user_since_date = models.DateTimeField(null=True, default=None)
    image = models.ImageField(
        upload_to='profile_image', null=True, default=None)
    zoom_id = models.CharField(max_length=50, null=True, default=None)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
