========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/tempest-tripleo-ui.svg
    :target: http://governance.openstack.org/reference/tags/index.html

.. Change things from this point on

==================
tempest-tripleo-ui
==================

Tempest Plugin for TripleO UI

* Free software: Apache license

Using
--------

Install this plugin in the same python environment as tempest.


Configuration for testing
-------------------------

If your undercloud has been installed with tripleo-quickstart, you can test the
tempest-tripleo-ui plugin without much difficulty.

On your undercloud:

* ``cd ~``
* Clone the tempest-tripleo-ui repo ``git clone https://github.com/openstack/tempest-tripleo-ui``
* Install it ``cd tempest-tripleo-ui; sudo python setup.py install; cd ..``
* Modify ``tempest-setup.sh`` to add ``tripleo_ui.url http://192.168.24.1:3000`` to the ``$TEMPESTCONF`` command
* Modify ``whitelist_file.conf`` to add ``tempest_tripleo_ui.tests.scenario.test_basic.TestBasic``
* Run ``./tempest-setup.sh``

This will run all of the tests contained in the tempest-tripleo-ui plugin
against your undercloud.
