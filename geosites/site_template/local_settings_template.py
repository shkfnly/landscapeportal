# -*- coding: utf-8 -*-

###############################################
# Geosite local settings
###############################################

# load local_settings from master

try:
    # load local_settings from base project directory
    execfile(os.path.join(SITE_ROOT, '../', 'local_settings.py'))
except:
    # there are no master local_settings to import
    pass

# Outside URL
#SITEURL = 'http://www.geonode.org'

# databases unique to site if not defined in site settings
"""
SITE_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, '../development.db'),
    },
}
"""

