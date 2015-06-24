from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from geonode.urls import urlpatterns
from .api import api

# we will override the api url over the geonode ones and resource details urls

urlpatterns = patterns('',
   url(r'^/?$',
       TemplateView.as_view(template_name='site_index.html'),
       name='home'),
    url(r'', include(api.urls)),
 ) + urlpatterns
