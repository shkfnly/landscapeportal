import json

from tastypie.test import ResourceTestCase
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test.client import Client

from guardian.shortcuts import get_anonymous_user
from guardian.shortcuts import assign_perm, remove_perm

from geonode.base.populate_test_data import create_models
from geonode.people.models import Profile
from geonode.layers.models import Layer

from .populate_sites_data import create_sites
from .utils import resolve_object
from .models import SiteResources


class SitesTest(ResourceTestCase):

    """Tests the sites functionality
    """

    fixtures = ['bobby']

    def setUp(self):
        self.user = 'admin'
        self.passwd = 'admin'
        self.admin = Profile.objects.get(username='admin')
        self.api_site_url = reverse('api_dispatch_list',
                                kwargs={
                                    'api_name': 'api',
                                    'resource_name': 'sites'})
        self.api_layer_url = reverse('api_dispatch_list',
                                        kwargs={
                                            'api_name': 'api',
                                            'resource_name': 'layers'})
        create_models(type='layer')
        create_sites()
        self.anonymous_user = get_anonymous_user()
        self.master_site = Site.objects.get(name='MasterSite')
        self.slave_site = Site.objects.get(name='SlaveSite')
        self.slave2_data = {'name': 'Slave2Site',
                            'domain': 'slave2.test.org'}

    def test_create_new_site(self):
        """
        Test the creation of new sites
        """
        # Test unauthenticated first
        response = self.client.post(
            self.api_site_url,
            data=self.slave2_data)
        # Check the correct http response
        self.assertEqual(reponse.status_code,401)

        # Test as admin
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(
            self.api_site_url,
            data=self.slave2_data)
        # Check the correct http response
        self.assertEqual(reponse.status_code,200)

        # Check the object is created in the db
        self.assertTrue(Site.objects.filter(name='Slave2Site').exists())

    def test_delete_site(self):
        """
        Test the deletion of sites
        """
        # Test unauthenticated first
        response = self.client.delete(
            self.api_site_url,
            data={name: 'SlaveSite'})
        # Check the correct http response
        self.assertEqual(reponse.status_code,401)

        # Test as admin
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(
            self.api_site_url,
            data={name: 'SlaveSite'})
        # Check the correct http response
        self.assertEqual(reponse.status_code,200)

        # Check the object is created in the db
        self.assertFalse(Site.objects.filter(name='SlaveSite').exists())

    def test_resolve_object_by_site(self):
        """
        Test that the resolve_object function correctly uses the site
        """
        # test that the CA layer, that does not belong to the SlaveSite, is not returned
        self.assertIsNone(resolve_object(self.admin, Layer, None, self.slave_site))

        # test the same with the master site
        self.assertIsNotNone(resolve_object(self.admin, Layer, None, self.slave_site))

    def test_master_site_all_layers(self):
        """
        Test that the master site owns all the layers available in the database
        """
        self.assertEqual(SiteResources.objects.filter(site=self.master_site).resources.count(), 20)

    def test_admin_normal_site_subset_layers(self):
        """
        Test that a superuser that can see al layers on the master site,
        on normal site can see to the correct subset of layers
        """
        self.assertEqual(SiteResources.objects.filter(site=self.slave_site).resources.count(), 10)

    def test_non_superuser_normal_site_subset_layers(self):
        """
        Test that a non superuser, that can see different layers on different sites,
        can see the correct subset of layer on a normal site
        """
        # Set the domain so tat get_current_site picks the right one
        c = Client(SERVER_NAME='slave.test.org')
        c.login(username='bobby', password='bob')
        response = c.get(self.api_layer_url)
        self.assertEquals(len(self.deserialize(resp)['objects']), 5)

        # now test with superuser
        c.logout()
        c.login(username=self.user, password=self.password)
        response = c.get(self.api_layer_url)
        self.assertEquals(len(self.deserialize(resp)['objects']), 10)

    def test_layer_created_belongs_correct_site(self):
        """
        Test that a layer created in a normal site belongs to that site and to the master site only
        """
        # The layers created through the tests will belong to the SlaveSite as per test settings
        # Create a Slave2 Site
        slave2 = Site.objects.create(name='Slave2Site', domani="slave2.test.org")
        self.assertEqual(SiteResources.object.get(site=slave2).resources.count(), 0)
        
