from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.db.models import Count

from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from guardian.shortcuts import get_objects_for_user

from geonode.api.resourcebase_api import CommonModelApi, CommonMetaApi
from geonode.base.models import ResourceBase
from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document
from geonode.api.urls import api
from geonode.api.api import TagResource, TopicCategoryResource, RegionResource, CountJSONSerializer
    
from .models import SiteResources
from .utils import resources_for_site


class CommonSiteModelApi(CommonModelApi):
    """Override the apply_filters method to respect the site"""

    def apply_filters(self, request, applicable_filters):
        filtered = super(CommonSiteModelApi, self).apply_filters(request, applicable_filters) 
        
        filtered = filtered.filter(id__in=resources_for_site())

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


class SiteResource(ModelResource):
    """Sites API"""

    class Meta:
        queryset = Site.objects.all()
        filtering = {
            'name': ALL
        }
        resource_name = 'sites'
        allowed_methods = ['get', 'delete', 'post']
        authorization = DjangoAuthorization()


class SiteCountJSONSerializer(CountJSONSerializer):
    """Custom serializer to post process the api and add counts for site"""

    def get_resources_counts(self, options):
        if settings.SKIP_PERMS_FILTER:
            resources = ResourceBase.objects.all()
        else:
            resources = get_objects_for_user(
                options['user'],
                'base.view_resourcebase'
            )
        if settings.RESOURCE_PUBLISHING:
            resources = resources.filter(is_published=True)

        if options['title_filter']:
            resources = resources.filter(title__icontains=options['title_filter'])

        if options['type_filter']:
            resources = resources.instance_of(options['type_filter'])

        resources = resources.filter(id__in=resources_for_site())
        counts = list(resources.values(options['count_type']).annotate(count=Count(options['count_type'])))

        return dict([(c[options['count_type']], c['count']) for c in counts])


class SiteTagResource(TagResource):

    class Meta(TagResource.Meta):
        serializer = SiteCountJSONSerializer()


class SiteTopicCategoryResource(TopicCategoryResource):

    class Meta(TopicCategoryResource.Meta):
        serializer = SiteCountJSONSerializer()


class SiteRegionResource(RegionResource):

    class Meta(RegionResource.Meta):
        serializer = SiteCountJSONSerializer()


api.register(LayerResource())
api.register(MapResource())
api.register(DocumentResource())
api.register(ResourceBaseResource())
api.register(SiteResource())
api.register(SiteTagResource())
api.register(SiteTopicCategoryResource())
api.register(SiteRegionResource())
