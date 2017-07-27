from __future__ import unicode_literals



# Create your models here.
from django.db import models


class cloudflareinfo(models.Model):
    domain = models.URLField(max_length=50)
    zone_id = models.CharField(max_length=200)
    auth_email = models.EmailField()
    auth_key = models.CharField(max_length=100)

    def __unicode__(self):
        return self.domain