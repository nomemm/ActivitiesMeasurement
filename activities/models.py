from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings


class Activity(models.Model):
    name = models.CharField(max_length=255)
    comments = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey('auth.User', related_name='activities', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Activity, self).save(*args, **kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
