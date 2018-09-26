========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/tempest-tripleo-ui.svg
    :target: http://governance.openstack.org/reference/tags/index.html

==================
tempest-tripleo-ui
==================

Tempest Plugin for TripleO UI

* Free software: Apache 2.0 license

Using
--------

Install this plugin in the same python environment as tempest.

Installing the web driver
-------------------------

Selenium drives the browser by using a web driver. Currently Firefox and Chrome are supported.

#. To install the Firefox driver:
   Download the latest driver from https://github.com/mozilla/geckodriver/releases/. Place the
   executable somewhere in your ``$PATH``, and configure your tempest.conf with the full path to
   it. See an example tempest.conf file below.

#. To install the Chrome driver:
   Download the latest driver from https://sites.google.com/a/chromium.org/chromedriver/downloads.
   Unzip the downloaded file you'll get an executable called "chromedriver". Place the executable
   somewhere in your ``$PATH``.

Configuration for testing
-------------------------

If your undercloud has been installed with tripleo-quickstart, you can test the
tempest-tripleo-ui plugin without much difficulty.

On your undercloud:

* ``cd ~``
* Clone the tempest-tripleo-ui repo ``git clone https://git.openstack.org/openstack/tempest-tripleo-ui``
* Install it ``cd tempest-tripleo-ui; sudo python setup.py install; cd ..``
* Modify ``tempest-setup.sh`` to add ``tripleo_ui.url http://192.168.24.1:3000`` to the ``$TEMPESTCONF`` command
* Modify ``whitelist_file.conf`` to add ``tempest_tripleo_ui.tests.scenario.test_basic.TestBasic``
* Run ``./tempest-setup.sh``

This will run all of the tests contained in the tempest-tripleo-ui plugin
against your undercloud.

Sample tempest.conf
-------------------

For the UI tests to work, a minimal tempest.conf should include:
1) The credentials to log in (same credentials which are used on the command line)
2) The URL where the login screen to the UI can be found
3) The webdriver to use, which could be one of: "Chrome" or "Firefox"
4) If using Firefox, set marionette_binary to point to the path to the driver

[DEFAULT]
log_dir = /home/tester/src/tempest/cloud-01/logs
log_file = tempest.log

[oslo_concurrency]
lock_path = /home/tester/src/tempest/cloud-01/tempest_lock

[auth]
admin_username = admin
admin_password = password
admin_project_name = admin
admin_domain_name = default

[identity]
auth_version = v3
uri_v3 = https://server:443/keystone/v3

[tripleo_ui]
webdriver = "Chrome"
marionette_binary = "/home/tester/bin/wires"
url = "https://server"

[logger_root]
level=DEBUG
handlers=file
