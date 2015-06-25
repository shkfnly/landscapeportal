import json

from tastypie.test import ResourceTestCase
from django.test.utils import override_settings
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
from geonode.groups.models import Group

from .populate_sites_data import create_sites
from .utils import resolve_object
from .models import SiteResources


@override_settings(SITE_NAME='Slave')
@override_settings(SITE_ID=2)
class SiteTests(ResourceTestCase):

    """Tests the sites functionality
    """

    fixtures = ['bobby']

    def setUp(self):
        create_sites()
        create_models(type='layer')

        self.user = 'admin'
        self.passwd = 'admin'
        self.admin = Profile.objects.get(username='admin')
        self.bobby = Profile.objects.get(username='bobby')
        self.master_site = Site.objects.get(name='Master')
        self.slave_site = Site.objects.get(name='Slave')
        self.api_site_url = reverse('api_dispatch_list',
                                kwargs={
                                    'api_name': 'api',
                                    'resource_name': 'sites'})
        self.api_slave_detail_url = reverse('api_dispatch_detail',
                                kwargs={
                                    'api_name': 'api',
                                    'resource_name': 'sites',
                                    'pk': self.slave_site.pk})
        self.api_layer_url = reverse('api_dispatch_list',
                                        kwargs={
                                            'api_name': 'api',
                                            'resource_name': 'layers'})
        
        self.anonymous_user = get_anonymous_user()
        self.slave2_data = {'name': 'Slave2',
                            'domain': 'slave2.test.org'}
        # all layers belong to slave bu let's remove one resource from it
        SiteResources.objects.get(site=self.slave_site).resources.remove(Layer.objects.all()[0])

    def test_create_new_site(self):
        """
        Test the creation of new sites
        """
        # Test unauthenticated first
        response = self.client.post(
            self.api_site_url,
            data=self.slave2_data)
        # Check the correct http response
        self.assertEqual(response.status_code,401)

        # Test as admin
        self.client.login(username=self.user, password=self.password)
        response = self.client.post(
            self.api_site_url,
            data=self.slave2_data)
        # Check the correct http response
        self.assertEqual(response.status_code,200)

        # Check the object is created in the db
        self.assertTrue(Site.objects.filter(name='Slave2Site').exists())

    def test_delete_site(self):
        """
        Test the deletion of sites also removes the SiteResources
        """
        # Test unauthenticated first
        response = self.client.delete(
            self.api_slave_detail_url,
            data={'name': 'Slave'})
        # Check the correct http response
        self.assertEqual(response.status_code,401)

        # Test as admin
        self.client.login(username=self.user, password=self.passwd)

        # Check the correct http response
        self.assertHttpAccepted(self.client.delete(self.api_slave_detail_url))

        # Check the object is created in the db
        self.assertFalse(Site.objects.filter(name='Slave').exists())

        # Check that the SiteResources has been deleted as well
        self.assertFalse(SiteResources.objects.filter(site=self.slave_site).exists())

    def test_layer_detail_page_slave_site(self):
        """
        Test that the detail page is not found of the resource is on another site
        """
        # test that the CA layer detail page, that does not belong to the SlaveSite, is not found
        self.client.login(username=self.user, password=self.passwd)
        response = self.client.get(reverse('layer_detail', args=[Layer.objects.all()[0].typename]))
        self.assertEqual(response.status_code, 404)

    @override_settings(SITE_ID=1)
    def test_layer_detail_page_master_site(self):
        """
        Test that the detail page is allowed from the master site
        """
        # test that the CA layer detail page, that does not belong to the SlaveSite, is not found
        self.client.login(username=self.user, password=self.passwd)
        response = self.client.get(reverse('layer_detail', args=[Layer.objects.all()[0].typename]))
        self.assertEqual(response.status_code, 200)

    def test_master_site_all_layers(self):
        """
        Test that the master site owns all the layers available in the database
        """
        self.assertEqual(SiteResources.objects.get(site=self.master_site).resources.count(), 8)

    def test_normal_site_subset_layers(self):
        """
        Test that a normal site can see to the correct subset of layers
        """
        self.assertEqual(SiteResources.objects.get(site=self.slave_site).resources.count(), 7)

    def test_non_superuser_normal_site_subset_layers(self):
        """
        Test that a non superuser, that can see different layers on different sites,
        can see the correct subset of layer on a normal site
        """
        # Remove some view permissions for bobby
        anonymous_group = Group.objects.get(name='anonymous')
        for layer in Layer.objects.all()[:3]:
            remove_perm('view_resourcebase', self.bobby, layer.get_self_resource())
            remove_perm('view_resourcebase', anonymous_group, layer.get_self_resource())

        self.client.login(username='bobby', password='bob')
        response = self.client.get(self.api_layer_url)
        self.assertEquals(len(json.loads(response.content)['objects']), 5)

        # now test with superuser
        self.client.logout()
        self.client.login(username=self.user, password=self.passwd)
        response = self.client.get(self.api_layer_url)
        self.assertEquals(len(json.loads(response.content)['objects']), 7)

    def test_layer_created_belongs_correct_site(self):
        """
        Test that a layer created in a normal site belongs to that site and to the master site only
        """
        # The layers created through the tests will belong to the SlaveSite as per test settings
        # Create a Slave2 Site
        slave2 = Site.objects.create(name='Slave2', domain="slave2.test.org")
        self.assertEqual(SiteResources.objects.get(site=slave2).resources.count(), 0)

