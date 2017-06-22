from __future__ import unicode_literals

from django.db import models

# Create your models here.


class ipadd_path(models.Model):
    domain = models.CharField(max_length=50)
    devipadd = models.GenericIPAddressField()
    devpath = models.CharField(max_length=50)
    productionipadd = models.GenericIPAddressField()
    productionpath = models.CharField(max_length=50)

    def __unicode__(self):
        return self.domain