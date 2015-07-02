#!/usr/bin/env python

import os
import sys
import glob

PROJECT = 'landscapeportal'

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    sites = [os.path.basename(d) for d in os.listdir(PROJECT) if os.path.isdir(os.path.join(PROJECT,d))]
    for site in sites:
	print 'Managing %s' % site
	path = '%s/%s/settings.py' % (PROJECT, site)
	if os.path.exists(path):
    	    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.%s.settings" % (PROJECT, site))
    	    execute_from_command_line(sys.argv)

