# settings to apply to all GeoSites
import os

from geonode.contrib import geosites

OGC_SERVER['default']['LOCATION'] = os.path.join(SITEURL, 'geoserver/')
OGC_SERVER['default']['PUBLIC_LOCATION'] = os.path.join(SITEURL, 'geoserver/')
CATALOGUE['default']['URL'] = '%scatalogue/csw' % SITEURL
PYCSW['CONFIGURATION']['metadata:main']['provider_url'] = SITEURL
LOCAL_GEOSERVER['source']['url'] = OGC_SERVER['default']['PUBLIC_LOCATION'] + 'wms'

# use GeoSites post_settings
GEOSITES_ROOT = os.path.dirname(geosites.__file__)
execfile(os.path.join(GEOSITES_ROOT, 'post_settings.py'))

