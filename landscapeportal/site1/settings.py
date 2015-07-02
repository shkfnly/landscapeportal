# -*- coding: utf-8 -*-

###############################################
# Geosite settings
###############################################

import os
import geosites

# Directory of master site - for GeoSites it's two up
GEOSITES_ROOT = os.path.dirname(geosites.__file__)
SITE_ROOT = os.path.dirname(__file__)

# Read in GeoSites pre_settings
execfile(os.path.join(GEOSITES_ROOT, 'pre_settings.py'))

SITE_ID = 2
SITE_NAME = 'GeoSite%s' % SITE_ID
# Should be unique for each site
SECRET_KEY = "fbk3CC3N6jt1AU9mGIcI"

# globally installed apps
SITE_APPS = ('geosites', 'zinnia', 'django_comments', 'tagging')

# Site specific databases
SITE_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, '../development.db'),
    },
}

##### Overrides
# Below are some common GeoNode settings that might be overridden for site

SITE_TEMPLATE_CONTEXT_PROCESSORS = ('zinnia.context_processors.version',)

##### Overrides
# Below are some common GeoNode settings that might be overridden for site

# base urls for all sites
ROOT_URLCONF = 'landscapeportal.master.urls'

# admin email
#THEME_ACCOUNT_CONTACT_EMAIL = ''

# Have GeoServer use this database for this site
#DATASTORE = ''

# Allow users to register
#REGISTRATION_OPEN = True


# Read in GeoSites post_settings
execfile(os.path.join(GEOSITES_ROOT, 'post_settings.py'))
