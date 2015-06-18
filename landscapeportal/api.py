from tastypie.api import Api

from geonode.api.resourcebase_api import CommonModelApi, CommonMetaApi
from .models import SiteResources

# we should override the api's here to let them respect the sites


class CommonSiteModelApi(CommonModelApi):
    """Override the apply_filters method to respect the site"""

    def apply_filters(self, request, applicable_filters):
        filtered = super(CommonSiteModelApi, self).apply_filters(request, applicable_filters)

        # Filter by site - although this 
        resources_for_site = SiteResources().object.get(site__id=get_current_site(request).id).resources.all()
        filtered = filtered.filter(id__in=resources_for_site)

        return filtered


class ResourceBaseResource(CommonSiteModelApi):

    """ResourceBase api"""

    class Meta(CommonMetaApi):
        queryset = ResourceBase.objects.polymorphic_queryset() \
            .distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'base'
        excludes = ['csw_anytext', 'metadata_xml']


class LayerResource(CommonSiteModelApi):

    """Layer API"""

    class Meta(CommonMetaApi):
        queryset = Layer.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'layers'
        excludes = ['csw_anytext', 'metadata_xml']


class MapResource(CommonSiteModelApi):

    """Maps API"""

    class Meta(CommonMetaApi):
        queryset = Map.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'maps'


class DocumentResource(CommonSiteModelApi):

    """Maps API"""

    class Meta(CommonMetaApi):
        filtering = CommonMetaApi.filtering
        filtering.update({'doc_type': ALL})
        queryset = Document.objects.distinct().order_by('-date')
        if settings.RESOURCE_PUBLISHING:
            queryset = queryset.filter(is_published=True)
        resource_name = 'documents'


api = Api(api_name='api')

api.register(LayerResource())
api.register(MapResource())
api.register(DocumentResource())
api.register(ResourceBaseResource())
