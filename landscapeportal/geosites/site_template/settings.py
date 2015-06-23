# -*- coding: utf-8 -*-

###############################################
# Geosite settings
###############################################

import os

# Directory of master site - for GeoSites it's two up
MASTER_ROOT = os.path.join('..', '../', os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(__file__)

# Read in GeoSites pre_settings
execfile(os.path.join(MASTER_ROOT, 'pre_settings.py'))

SITE_ID = 2
SITE_NAME = 'GeoSite ID %s' % SITE_ID
# Should be unique for each site
SECRET_KEY = "fbk3CC3N6jt1AU9mGIcI"

# globally installed apps
SITE_APPS = ()

# Site specific databases
SITE_DATABASES = {}

##### Overrides
# Below are some common GeoNode settings that might be overridden for site

# base urls for all sites
#ROOT_URLCONF = 'geonode.urls'

# admin email
#THEME_ACCOUNT_CONTACT_EMAIL = ''

# Have GeoServer use this database for this site
#DATASTORE = ''

# Allow users to register
#REGISTRATION_OPEN = True


# Read in GeoSites post_settings
execfile(os.path.join(MASTER_ROOT, 'post_settings.py'))