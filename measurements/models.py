from django.db import models

from activities.models import Activity

class Measurement(models.Model):
    activity = models.ForeignKey(Activity, related_name='measurements', on_delete=models.CASCADE)
    type = models.CharField(max_length=16)
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=255)
    
    def __str__(self):
        return('%s:%s' % (self.name, self.value))
