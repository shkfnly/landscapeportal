from django.db import models
from django.contrib.sites.models import Site

from geonode.base.models import ResourceBase

# We also need the logic to manage the resourcebse per site belonging, like signals?

class ResourceSites(models.Model):
    """Relations to link the resources to the sites"""
    resource = models.OneToOneField(ResourceBase)
    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return resource.title
        