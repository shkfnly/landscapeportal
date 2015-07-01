from django.db import models
from django.db.models import signals
from django.contrib.sites.models import Site
from django.conf import settings

from geonode.base.models import ResourceBase
from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document


class SiteResources(models.Model):
    """Relations to link the resources to the sites"""
    site = models.OneToOneField(Site)
    resources = models.ManyToManyField(ResourceBase, blank=True, null=True)

    def __unicode__(self):
        return self.site.name

    class Meta:
        verbose_name_plural = 'Site Resources'


def post_save_resource(instance, sender, **kwargs):
    """Signal to ensure that every created resource is 
    assigned to the current site and to the master site"""
    current_site = Site.objects.get_current()
    master_site = Site.objects.get(id=1)
    SiteResources.objects.get(site=current_site).resources.add(instance.get_self_resource())
    SiteResources.objects.get(site=master_site).resources.add(instance.get_self_resource())


def post_save_site(instance, sender, **kwargs):
    """Signal to create the SiteResources on site save"""
    SiteResources.objects.get_or_create(site=instance)


def post_delete_resource(instance, sender, **kwargs):
    """Signal to ensure that on resource delete it get remove from the SiteResources as well"""
    current_site = Site.objects.get_current()
    master_site = Site.objects.get(id=1)
    SiteResources.objects.get(site=current_site).resources.remove(instance.get_self_resource())
    SiteResources.objects.get(site=master_site).resources.remove(instance.get_self_resource())


def post_delete_site(instance, sender, **kwargs):
    """Signal to delete the SiteResources on site delete"""
    SiteResources.objects.filter(site=instance).delete()

# Django doesn't propagate the signals to the parents so we need to add the listeners on the children
signals.post_save.connect(post_save_resource, sender=Layer)
signals.post_save.connect(post_save_resource, sender=Map)
signals.post_save.connect(post_save_resource, sender=Document)
signals.post_save.connect(post_save_site, sender=Site)
signals.post_delete.connect(post_delete_resource, sender=Layer)
signals.post_delete.connect(post_delete_resource, sender=Map)
signals.post_delete.connect(post_delete_resource, sender=Document)
signals.post_delete.connect(post_delete_site, sender=Site)
