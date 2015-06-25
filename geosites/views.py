from django.shortcuts import render
from django.contrib.sites.models import get_current_site
from django.http import Http404

from geonode.layers.views import _resolve_layer, _PERMISSION_MSG_VIEW, layer_detail

from .models import SiteResources

# Create your views here.

def site_layer_detail(request, layername, template='layers/layer_detail.html'):

    # BETTER WAY INSTEAD OF DO TWO _RESOLVE_LAYER PER CALL?
    layer = _resolve_layer(
        request,
        layername,
        'base.view_resourcebase',
        _PERMISSION_MSG_VIEW)
    site = get_current_site(request)
    if not SiteResources.objects.get(site=site).resources.filter(pk=layer.pk).exists():
        raise Http404
    else:
        return layer_detail(request, layername, template='layers/layer_detail.html')
    

def site_document_detail(request):
    pass

def site_map_detail(request):
    pass

