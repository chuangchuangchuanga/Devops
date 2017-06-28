from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ipadd_path(models.Model):
    domain = models.CharField(max_length=50)
    devipadd = models.GenericIPAddressField(null=True)
    devpath = models.CharField(max_length=50, blank=True)
    productionipadd = models.GenericIPAddressField(null=True)
    productionpath = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.domain