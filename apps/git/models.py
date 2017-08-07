from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ipadd_path(models.Model):
    Domain = models.CharField(max_length=50)
    Ipadd = models.GenericIPAddressField()
    Ccshoppath = models.CharField(max_length=50, blank=True)
    Themespath = models.CharField(max_length=50, blank=True)
    Themespath_mobile = models.CharField(max_length=50, blank=True)


    def __unicode__(self):
        return self.Domain


class log(models.Model):
    Domain = models.CharField(max_length=50)
    info = models.CharField(max_length=300)
