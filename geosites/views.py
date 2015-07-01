import json

from django.shortcuts import render
from django.contrib.sites.models import get_current_site
from django.http import Http404, HttpResponse

from guardian.shortcuts import get_objects_for_user

from geonode.utils import _get_basic_auth_info
from geonode.layers.views import _resolve_layer, layer_detail
from geonode.documents.views import _resolve_document, document_detail
from geonode.maps.views import _resolve_map, map_detail
from geonode.base.models import ResourceBase
from geonode.layers.models import Layer

from .models import SiteResources
from .utils import resources_for_site

_PERMISSION_MSG_VIEW = ('You don\'t have permissions to view this document')

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
    # BETTER WAY INSTEAD OF DO TWO _RESOLVE_DOCUMENT PER CALL?
    document = _resolve_document(
        request,
        docid,
        'base.view_resourcebase',
        _PERMISSION_MSG_VIEW)
    site = get_current_site(request)
    if not SiteResources.objects.get(site=site).resources.filter(pk=document.pk).exists():
        raise Http404
    else:
        return document_detail(request, docid, template='documents/document_detail.html')


def site_map_detail(request):
    # BETTER WAY INSTEAD OF DO TWO _RESOLVE_MAP PER CALL?
    the_map = _resolve_map(
        request,
        mapid,
        'base.view_resourcebase',
        _PERMISSION_MSG_VIEW)
    site = get_current_site(request)
    if not SiteResources.objects.get(site=site).resources.filter(pk=the_map.pk).exists():
        raise Http404
    else:
        return map_detail(request, layername, template='maps/map_detail.html')


def layer_acls(request):
    """
    returns json-encoded lists of layer identifiers that
    represent the sets of read-write and read-only layers
    for the currently authenticated user.
    """
    # the layer_acls view supports basic auth, and a special
    # user which represents the geoserver administrator that
    # is not present in django.
    acl_user = request.user
    site = get_current_site(request)
    if 'HTTP_AUTHORIZATION' in request.META:
        try:
            username, password = _get_basic_auth_info(request)
            acl_user = authenticate(username=username, password=password)

            # Nope, is it the special geoserver user?
            if (acl_user is None and
                    username == ogc_server_settings.USER and
                    password == ogc_server_settings.PASSWORD):
                # great, tell geoserver it's an admin.
                result = {
                    'rw': [],
                    'ro': [],
                    'name': username,
                    'is_superuser': True,
                    'is_anonymous': False
                }
                return HttpResponse(
                    json.dumps(result),
                    mimetype="application/json")
        except Exception:
            pass

        if acl_user is None:
            return HttpResponse(_("Bad HTTP Authorization Credentials."),
                                status=401,
                                mimetype="text/plain")

    # Include permissions on the anonymous user
    # use of polymorphic selectors/functions to optimize performances
    site_resources = resources_for_site()
    resources_readable = get_objects_for_user(acl_user, 'view_resourcebase',
                                              ResourceBase.objects.instance_of(Layer).filter(id__in=site_resources))
    layer_writable = get_objects_for_user(acl_user, 'change_layer_data',
                                          Layer.objects.filter(id__in=site_resources))

    _read = set(Layer.objects.filter(id__in=resources_readable).values_list('typename', flat=True))
    _write = set(layer_writable.values_list('typename', flat=True))

    read_only = _read ^ _write
    read_write = _read & _write

    result = {
        'rw': list(read_write),
        'ro': list(read_only),
        'name': acl_user.username,
        'is_superuser': acl_user.is_superuser,
        'is_anonymous': acl_user.is_anonymous(),
    }
    if acl_user.is_authenticated():
        result['fullname'] = acl_user.get_full_name()
        result['email'] = acl_user.email

    return HttpResponse(json.dumps(result), mimetype="application/json")
