# this should create sites test data, we don't use fixtures because they don't trigger signals and we may want signals on sites
# this should also assign resources to sites for testing purpose
from django.contrib.sites.models import Site

def create_sites():
    Site.objects.create(name='MasterSite', domani="master.test.org")
    Site.objects.create(name='SlaveSite', domani="slave.test.org")