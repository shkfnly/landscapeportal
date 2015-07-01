from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from geonode.urls import urlpatterns
from .api import api
from .views import site_layer_detail, site_document_detail, site_map_detail, layer_acls

# we will override the api url over the geonode ones and resource details urls

urlpatterns = patterns('',
   url(r'^/?$',
       TemplateView.as_view(template_name='site_index.html'),
       name='home'),
    url(r'', include(api.urls)),
    # Override the detail pages to respect the sites
    url(r'^layers/(?P<layername>[^/]\S*)$', site_layer_detail, name="layer_detail"),
    url(r'^documents/(?P<docid>\d+)$', site_document_detail, name='document_detail'),
    url(r'^maps/(?P<mapid>[^/]+)$', site_map_detail, name='map_detail'),
    url(r'^geoserver/acls/?$', layer_acls, name='site_layer_acls'),
 ) + urlpatterns
