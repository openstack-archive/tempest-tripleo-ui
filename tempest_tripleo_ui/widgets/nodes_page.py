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

from tempest_tripleo_ui.core import SeleniumElement, Identifier

node_names = {}
node_power_states = {}
node_provision_states = {}
node_introspection_statuses = {}
node_cpu_counts = {}
node_profiles = {}
node_memories = {}
node_disks = {}
checkboxes_near_nodes = {}


def node_name(idx):
    global node_names
    if idx not in node_names:
        node_names[str(idx)] = SeleniumElement.by_xpath(
            '(//span[@class="NodeListItem__nodeName"])[{}]'.format(idx + 1))
    return node_names[str(idx)]


def node_power_state(idx):
    global node_power_states
    if idx not in node_power_states:
        node_power_states[str(idx)] = SeleniumElement.by_xpath(
            '(//span[@class="NodeListItem__nodePowerState"])[{}]'.format(
                idx + 1))
    return node_power_states[str(idx)]


def node_provision_state(idx):
    global node_provision_states
    if idx not in node_provision_states:
        node_provision_states[str(idx)] = SeleniumElement.by_xpath(
            '(//span[@class="NodeListItem__nodeProvisionState"])'
            '[{}]'.format(idx + 1))
    return node_provision_states[str(idx)]


def node_introspection_status(idx):
    global node_introspection_statuses
    if idx not in node_introspection_statuses:
        node_introspection_statuses[str(idx)] = SeleniumElement.by_xpath(
            '(//span[@class="NodeListItem__nodeIntrospectionStatus"])'
            '[{}]'.format(idx + 1))
    return node_introspection_statuses[str(idx)]


def node_profile(idx):
    global node_profiles
    if idx not in node_profiles:
        node_profiles[str(idx)] = SeleniumElement.by_xpath(
            '(//div[contains(@class, "NodeListItem__profile")]'
            ')[{}]'.format(idx + 1))
    return node_profiles[str(idx)]


def node_cpu_count(idx):
    global node_cpu_counts
    if idx not in node_cpu_counts:
        node_cpu_counts[str(idx)] = SeleniumElement.by_xpath(
            '(//div[contains(@class, "NodeListItem__cpuCount")])[{}]'.format(
                idx + 1))
    return node_cpu_counts[str(idx)]


def node_memory(idx):
    global node_memories
    if idx not in node_memories:
        node_memories[str(idx)] = SeleniumElement.by_xpath(
            '(//div[contains(@class, "NodeListItem__memorySize")])'
            '[{}]'.format(idx + 1))
    return node_memories[str(idx)]


def node_disk(idx):
    global node_disks
    if idx not in node_disks:
        node_disks[str(idx)] = SeleniumElement.by_xpath(
            '(//div[contains(@class, "NodeListItem__diskSize")])[{}]'.format(
                idx + 1))
    return node_disks[str(idx)]


def checkbox_near_node(idx):
    global checkboxes_near_nodes
    if idx not in checkboxes_near_nodes:
        checkboxes_near_nodes[str(idx)] = SeleniumElement.by_xpath(
            '(//input[@class="NodeListItem__listViewCheckbox"])[{}]'.format(
                idx + 1))
    return checkboxes_near_nodes[str(idx)]


navbar_item = SeleniumElement.by_id('NavBar__nodesTab')
register_nodes = SeleniumElement.by_id('Nodes__registerNodesLink')
provide_nodes = SeleniumElement.by_id(
    'NodesToolbarActions__provideNodesAction')
introspect_nodes = SeleniumElement.by_id(
    'NodesToolbarActions__introspectNodesAction')

actions_kebab = SeleniumElement.by_id(
    "NodesToolbarActions__nodesActionsKebab")
manage_nodes = SeleniumElement.by_xpath(
    '//div[contains(@class, "dropdown-kebab-pf")]'
    '/ul[@role="menu"]'
    '/li[1]/a')
tag_nodes = SeleniumElement.by_xpath(
    '//div[contains(@class, "dropdown-kebab-pf")]'
    '/ul[@role="menu"]'
    '/li[2]/a')
delete_nodes = SeleniumElement.by_xpath(
    '//div[contains(@class, "dropdown-kebab-pf")]'
    '/ul[@role="menu"]'
    '/li[3]/a')

profile_combo = SeleniumElement.by_id('profile')
profile_dialog_confirm = SeleniumElement.by_xpath(
    '//form/div[@class="modal-footer"]'
    '/button[@type="submit"]')
profile_dialog_close = SeleniumElement.by_xpath(
    '//div[@class="modal-header"]'
    '/button[@class="close"]')

all_node_names = Identifier.xpath('//span[@class="NodeListItem__nodeName"]')
introspection_spinner = SeleniumElement.by_xpath(
    '//span[contains(@class, "pficon-server")]'
    '[contains(@class, "running")]')
