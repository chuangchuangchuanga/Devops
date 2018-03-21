from __future__ import unicode_literals

from django.db import models

# Create your models here.

class domain_to_server(models.Model):
    website_type = (
        (0, u"october"),
        (1, u"larval"),
    )
    Domain = models.CharField(max_length=50)
    Adderss = models.GenericIPAddressField()
    Path = models.CharField(max_length=200)
    webtype = models.IntegerField( choices=website_type)

    def __unicode__(self):
        return self.Domain