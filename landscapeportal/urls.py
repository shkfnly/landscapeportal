from django.conf.urls import patterns, url, include
from geosites.urls import urlpatterns


urlpatterns = urlpatterns + patterns('',
    url(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^blog-comments/', include('django_comments.urls')),
) 