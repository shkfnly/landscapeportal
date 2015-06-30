from django.contrib.sites.models import Site

from .models import SiteResources

def resources_for_site():
    return SiteResources.objects.get(site=Site.objects.get_current()).resources.all()