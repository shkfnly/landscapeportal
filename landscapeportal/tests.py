from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site

from guardian.shortcuts import get_anonymous_user
from guardian.shortcuts import assign_perm, remove_perm

# from populate_sites_data import create_sites
from geonode.base.populate_test_data import create_models
# Create your tests here.

class SitesTest(TestCase):

    """Tests the sites functionality
    """

    fixtures = ['bobby']

    def setUp(self):
        self.user = 'admin'
        self.passwd = 'admin'
        create_models(type='layer')
        create_sites()
        self.anonymous_user = get_anonymous_user()

    def test_create_new_site(self):
        """
        Test the creation of new sites
        """
        pass

    def test_delete_site(self):
        """
        Test the deletion of sites
        """
        pass

    def test_resolve_object_by_site(self):
        """
        Test that the _resolve_object function correctly uses the site
        """
        pass

    def test_master_site_all_layers(self):
        """
        Test that the master site owns all the layers available in the database
        """
        pass

    def test_admin_normal_site_subset_layers(self):
        """
        Test that a superuser that can see al layers on the master site,
        on normal site can see to the correct subset of layers
        """
        pass

    def test_non_superuser_normal_site_subset_layers(self):
        """
        Test that a non superuser, that can see different layers on different sites,
        can see the correct subset of layer on a normal site
        """
        pass

    def test_layer_created_belongs_correct_site(self):
        """
        Test that a layer created in a normal site belongs to that site and to the master site only
        """
        pass
