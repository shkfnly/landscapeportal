from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from geonode.urls import *

# we will override the api url over the geonode ones and resource details urls

urlpatterns = patterns('',
   url(r'^/?$',
       TemplateView.as_view(template_name='site_index.html'),
       name='home'),
 ) + urlpatterns
