Landscapeportal
========================

The Landscapeportal make use of the geosites contrib app to power multiple sites with one single GeoNode installation

Overview
--------
The geosites contrib app makes full use of the Django sites framework to isolate the data by site.
The site is defined in the settings with SITE_ID and SITE_NAME and the resources (Layers, Maps and Documents) are
visible only to the site where they are created or to other authorized sites.
There is although a special site named "Master" that can access all data.

Installation
------------
The installation require GeoNode but the GeoNode code is not going to be modified. The current supported version is 2.4.

Install geonode with::

    $ sudo add-apt-repository ppa:geonode/testing

    $ sudo apt-get update

    $ sudo apt-get install geonode

Clone and install the Landscapeportal app with::

    $ git clone https://github.com/terranodo/landscapeportal

    $ pip install -e landscapeportal


Usage
-----

ALL THIS SHOULD BE DONE BY A SCRIPT

The landscapeportal app provides a master template app and a site1 app. The site1 app is a template that can be copied for every needed site and renamed at preference.
It is necessary to edit the settings file inside each site app and change the SITE_ID and SITE_NAME (or leave it default, it will be GeoSite-SITE_ID).
All the GeoSites share the same database and it's defined in the /etc/geonode/local_settings.py file. For development or if you need a standalone db for a site you can uncomment/edit the SITE_DATABASES directive in the site settings.py file.

By default the master site is already registered in the database, it is although necessary to add one for each site that you created and this can be done through the administation interface at /admin. Add a new site with Display Name = SITE_NAME and Domain ad the expected public web address of the site. The Master site has ID=1 and every subsequently created site will have the ID incremented by 1.

PRODUCTION

Deploy with apache/nginx+gunicorn

DEVELOPMENT

In development mode it is possible to run multiple sites by binding the django development server on different ports.
To run a site go in it's directory and run the server with::
  
    $ python manage.py runserver localhost:XXXX --settings=landscapeportal.siteX.settings

For the master site it's enough to run::

    $ python manage.py runserver

In order to have the sites to share the same SqlLite database uncomment the content of each SITE_DATABASES directive in the settings.py files.

Every site will be available at the port specified with the runserver command.
