from django.db import models

class Activity(models.Model):
    name = models.CharField(max_length=255)
    comments = models.CharField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        super(Activity, self).save(*args, **kwargs)
