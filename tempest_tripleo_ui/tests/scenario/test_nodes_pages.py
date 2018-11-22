# Copyright 2018 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
from tempest.lib import decorators
from tempest_tripleo_ui.base import GUITestCase
from tempest_tripleo_ui.models import nodes
from tempest_tripleo_ui.widgets import nodes_page
from testtools.matchers._basic import GreaterThan

logger = logging.getLogger(__name__)


class TestNodesPage(GUITestCase):

    def test_nodes_page_elements(self):
        nodes_count = nodes.get_nodes_count()
        logger.debug('found {} nodes in the Nodes page'.format(nodes_count))
        self.assertThat(
            nodes_count,
            GreaterThan(0),
            "Number of nodes is 0")
        for idx in range(nodes_count):
            name_elem = nodes_page.node_name(idx)
            self.assertIsNotNone(
                name_elem.wait_for_element(0),
                "Can't locate name element (node's name) for node {} in "
                "the Nodes page".format(idx))
            node_name = name_elem.get_text()
            logger.debug("Node name: {}".format(node_name))
            self.assertThat(
                len(node_name),
                GreaterThan(0),
                "Could not read the node name for node {}".format(idx))

            power_elem = nodes_page.node_power_state(idx)
            self.assertIsNotNone(
                power_elem.wait_for_element(0),
                "Can't locate power state element for node {} in "
                "the Nodes page".format(node_name))
            node_power = nodes.get_node_power_state(idx)
            logger.debug("Node power state: {}".format(node_power))
            self.assertIn(
                node_power,
                ['Off', 'On'],
                "Unexpected power state for node {}: '{}'".format(
                    node_name, node_power))

            provision_elem = nodes_page.node_provision_state(idx)
            self.assertIsNotNone(
                provision_elem.wait_for_element(0),
                "Can't locate provision state element for node {} in "
                "the Nodes page".format(node_name))
            node_provision = nodes.get_node_provision_state(idx)
            logger.debug("Node {}".format(node_provision))
            self.assertIn(
                node_provision,
                ['available', 'active', 'manageable'],
                "Unexpected provision state for node {}: '{}'".format(
                    node_name, node_provision))

            introspection_elem = nodes_page.node_introspection_status(idx)
            self.assertIsNotNone(
                introspection_elem.wait_for_element(0),
                "Can't locate introspection status element for node {} in "
                "the Nodes page".format(node_name))
            node_introspection = nodes.get_node_introspection_state(idx)
            logger.debug("Node introspection status: {}".format(
                node_introspection))
            self.assertIn(
                node_introspection,
                ['finished'],
                "Unexpected provision state for node {}: '{}'".format(
                    node_name, node_introspection))

            profile_elem = nodes_page.node_profile(idx)
            self.assertIsNotNone(
                profile_elem.wait_for_element(0),
                "Can't locate profile element for node {} in "
                "the Nodes page".format(node_name))
            node_profile = nodes.get_node_profile(idx)
            logger.debug("Node profile: {}".format(node_profile))
            self.assertIn(
                node_profile,
                ['controller', 'compute', 'ceph'],
                "Unexpected profile for node {}: '{}'".format(
                    node_name, node_profile))

            cpu_elem = nodes_page.node_cpu_count(idx)
            self.assertIsNotNone(
                cpu_elem.wait_for_element(0),
                "Can't locate CPU count element for node {} in "
                "the Nodes page".format(node_name))
            node_cpu = nodes.get_node_cpu_count(idx)
            logger.debug("Node CPU: {}".format(node_cpu))
            self.assertIn(
                node_cpu,
                range(1, 17),
                "Unexpected CPU count for node {}: '{}'".format(
                    node_name, node_cpu))

            memory_elem = nodes_page.node_memory(idx)
            self.assertIsNotNone(
                memory_elem.wait_for_element(0),
                "Can't locate memory element for node {} in "
                "the Nodes page".format(node_name))
            node_memory = nodes.get_node_memory(idx)
            logger.debug("Node memory: {}".format(node_memory))
            self.assertIn(
                node_memory,
                [1024, 2048, 4096, 8192, 16384, 32768],
                "Unexpected memory size for node {}: '{}'".format(
                    node_name, node_memory))

            disk_size_elem = nodes_page.node_disk(idx)
            self.assertIsNotNone(
                disk_size_elem.wait_for_element(0),
                "Can't locate disk size element for node {} in "
                "the Nodes page".format(node_name))
            node_disk_size = nodes.get_node_disk_size(idx)
            logger.debug("Node disk size: {}".format(node_disk_size))
            self.assertThat(
                node_disk_size,
                GreaterThan(0),
                "Unexpected disk size for node {}: '{}'".format(
                    node_name, node_disk_size))

            checkbox_elem = nodes_page.checkbox_near_node(idx)
            self.assertIsNotNone(
                checkbox_elem.wait_for_element(0),
                "Can't locate checkbox element for node {} in "
                "the Nodes page".format(node_name))

    def test_provide_node(self):
        nodes.navigate_to_nodes_page()
        state = nodes.get_node_provision_state(0)
        test_completed = False
        if state == 'available':
            nodes.manage_nodes([0])
            state = nodes.get_node_provision_state(0)
            self.assertEqual(
                "manageable",
                state,
                "couldn't set node provision state to manageable")
            test_completed = True
        nodes.provide_nodes([0])
        state = nodes.get_node_provision_state(0)
        self.assertEqual(
            "available",
            state,
            "could not provide node")
        if not test_completed:
            # means we tested both setting a node to manage and available
            self.test_provide_node()

    def test_tag_node(self):
        nodes.navigate_to_nodes_page()
        current_profile = nodes.get_node_profile(0)
        new_profile = 'controller'
        if new_profile == current_profile:
            new_profile = 'compute'
        nodes.tag_nodes([0], new_profile)
        self.assertEqual(
            new_profile,
            nodes.get_node_profile(0),
            "node profiles didn't get set to {}".format(new_profile))
        nodes.tag_nodes([0], current_profile)
        self.assertEqual(
            current_profile,
            nodes.get_node_profile(0),
            "node profiles didn't get set back to {}".format(current_profile))

    @decorators.attr(type='slow')
    def test_introspect_node(self):
        nodes.navigate_to_nodes_page()
        state = nodes.get_node_provision_state(0)
        if state == 'available':
            nodes.manage_nodes([0])
            state = nodes.get_node_provision_state(0)
            self.assertEqual(
                "manageable",
                state,
                "couldn't set node provision state to manageable")
        nodes.introspect_nodes([0])
        nodes.provide_nodes([0])
        state = nodes.get_node_provision_state(0)
        self.assertEqual(
            "available",
            state,
            "could not provide node")
