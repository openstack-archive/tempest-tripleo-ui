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
from tempest.lib import exceptions
from tempest_tripleo_ui import alerts
from tempest_tripleo_ui.widgets import nodes_page
from time import sleep
from tempest_tripleo_ui.core import selenium_elements


class IllegalOperation(exceptions.TempestException):
    message = "Operation not permitted: %(msg)s"


class OperationFailed(exceptions.TempestException):
    message = "Operation failed: %(msg)s"


class NodesPageNotFound(exceptions.TempestException):
    message = "Could not navigate to the Nodes page"


class NodeNotFound(exceptions.TempestException):
    message = "Node '%(node_name)s' not found in the nodes page"


class IllegalNodeIndex(exceptions.TempestException):
    message = "Illegal node index '%(node_index)s'"


class UnexpectedProvisionState(exceptions.TempestException):
    message = "Unexpected provision state for node '%(node_name)s': "\
        "%(provision_state)s"


class UnexpectedIntrospectionState(exceptions.TempestException):
    message = "Unexpected introspection state for node '%(node_name)s': "\
        "%(introspection_state)s"


class UnexpectedProfile(exceptions.TempestException):
    message = "Unexpected profile for node '%(node_name)s': "\
        "%(profile)s"


class CantReadCpuCount(exceptions.TempestException):
    message = "Can't locate or read CPU count for node: '%(node_name)s'"


class CantReadNodeMemory(exceptions.TempestException):
    message = "Can't locate or read node memory for node: '%(node_name)s'"


class CantReadDiskSize(exceptions.TempestException):
    message = "Can't locate or read node disk size for node: '%(node_name)s'"


class UndefinedNodesExist(exceptions.TempestException):
    message = "Undefined nodes exist in the nodes registration dialog. "\
        "All nodes should have a valid unique name before registering new ones"


logger = logging.getLogger(__name__)


def navigate_to_nodes_page():
    if nodes_page.register_nodes.wait_for_element(0):
        return

    item = nodes_page.navbar_item
    if "active" not in item.get_class():
        logger.info("Navigating to the Nodes page")
        item.click()
        retries = 3
        while "active" not in item.get_class() and retries > 0:
            sleep(1)
            item.click()
            retries -= 1

    if "active" not in item.get_class():
        raise NodesPageNotFound

    alerts.wait_for_spinner()


def get_nodes_count():
    navigate_to_nodes_page()
    elems = selenium_elements(nodes_page.all_node_names)
    if not elems:
        return 0
    return len(elems)


def get_displayed_nodes():
    logger.info("listing nodes ...")
    displayed_nodes_list = []
    for node_i in range(get_nodes_count()):
        node_name_elem = nodes_page.node_name(node_i)
        displayed_nodes_list.append(node_name_elem.get_text())
    return displayed_nodes_list


def get_node_idx(node_name_or_idx):
    try:
        # is it an int ?
        return int(node_name_or_idx)
    except ValueError:
        # it was a string...
        node_names = get_displayed_nodes()
        if node_name_or_idx not in node_names:
            raise NodeNotFound(node_name=node_name_or_idx)
        return node_names.index(node_name_or_idx)


def get_node_name(idx):
    node_idx = 0
    try:
        node_idx = int(idx)
    except ValueError:
        raise IllegalNodeIndex(node_index=idx)

    elem = nodes_page.node_name(node_idx)
    return elem.get_text().strip()


def select_nodes(node_list):
    # see if there are any node names in node_list and make them indexes
    node_names = get_displayed_nodes()
    for idx in range(len(node_list)):
        try:
            node_list[idx] = int(node_list[idx])
        except ValueError:
            node_idx = node_names.index(node_list[idx])
            if node_idx < 0:
                raise NodeNotFound(node_name=node_list[idx])
            node_list[idx] = node_idx

    # check and uncheck nodes
    for node_idx in range(len(node_names)):
        elem = nodes_page.checkbox_near_node(node_idx)
        sel = elem.is_selected()
        if (node_idx in node_list and not sel) \
                or (node_idx not in node_list and sel == True):
            elem.click()


def get_node_power_state(node_name_or_idx):
    node_idx = get_node_idx(node_name_or_idx)
    elem = nodes_page.node_power_state(node_idx)
    return elem.get_text().strip()


def get_node_provision_state(node_name_or_idx):
    node_idx = get_node_idx(node_name_or_idx)
    elem = nodes_page.node_provision_state(node_idx)
    txt = elem.get_text().strip()
    prefix = "Provision State: "
    if not txt.startswith(prefix):
        raise UnexpectedProvisionState(
            node_name=node_name_or_idx,
            provision_state=txt)
    return txt[len(prefix):]


def get_node_introspection_state(node_name_or_idx):
    node_idx = get_node_idx(node_name_or_idx)
    elem = nodes_page.node_introspection_status(node_idx)
    txt = elem.get_text().strip()
    prefix = "Introspection: "
    if not txt.startswith(prefix):
        raise UnexpectedIntrospectionState(
            node_name=node_name_or_idx,
            introspection_state=txt)
    return txt[len(prefix):]


def get_node_profile(node_name_or_idx):
    node_idx = get_node_idx(node_name_or_idx)
    elem = nodes_page.node_profile(node_idx)
    txt = elem.get_text().strip()
    prefix = "Profile:\n "
    if not txt.startswith(prefix):
        raise UnexpectedProfile(
            node_name=node_name_or_idx,
            profile=txt)
    return txt[len(prefix):]


def get_node_cpu_count(node_name_or_idx):
    node_idx = get_node_idx(node_name_or_idx)
    elem = nodes_page.node_cpu_count(node_idx)
    try:
        return int(elem.get_text().strip().split(" ")[0])
    except ValueError:
        raise CantReadCpuCount(
            node_name=node_name_or_idx)


def get_node_memory(node_name_or_idx):
    node_idx = get_node_idx(node_name_or_idx)
    elem = nodes_page.node_memory(node_idx)
    try:
        return int(elem.get_text().strip().split(" ")[0])
    except ValueError:
        raise CantReadNodeMemory(
            node_name=node_name_or_idx)


def get_node_disk_size(node_name_or_idx):
    node_idx = get_node_idx(node_name_or_idx)
    elem = nodes_page.node_disk(node_idx)
    try:
        return int(elem.get_text().strip().split(" ")[0])
    except ValueError:
        raise CantReadDiskSize(
            node_name=node_name_or_idx)


def provide_nodes(node_list):
    select_nodes(node_list)
    elem = nodes_page.provide_nodes
    if not elem.is_enabled():
        raise IllegalOperation(
            msg="'provide' button disabled or not found")
    logger.info('Providing nodes: {}'.format(node_list))
    elem.click()
    sleep(1)
    alerts.wait_for_spinner(
        spinner_element=nodes_page.introspection_spinner)
    sleep(1)
    if not alerts.clear_success_message():
        alerts.clear_danger_message()   # will log errors
        raise OperationFailed(
            msg="failed to provide nodes, did not see the success message "
            "(toast message)")
    if alerts.clear_danger_message():
        # despite the success, there might be errors
        return False
    return True


def manage_nodes(node_list):
    select_nodes(node_list)
    logger.info('Setting nodes to manageable: {}'.format(node_list))
    nodes_page.actions_kebab.click()
    nodes_page.manage_nodes.click()
    sleep(1)
    alerts.wait_for_spinner(
        spinner_element=nodes_page.introspection_spinner)
    sleep(1)
    if not alerts.clear_success_message():
        alerts.clear_danger_message()   # will log errors
        raise OperationFailed(
            msg="failed to manage nodes, did not see the success message "
            "(toast message)")
    if alerts.clear_danger_message():
        # despite the success, there might be errors
        return False
    return True


def tag_nodes(node_list, profile):
    select_nodes(node_list)
    logger.info('Tagging nodes to {}: {}'.format(profile, node_list))
    nodes_page.actions_kebab.click()
    nodes_page.tag_nodes.click()
    sleep(1)
    if not nodes_page.profile_combo.wait_for_element(3):
        raise OperationFailed(
            msg="failed to detect the nodes tagging dialog")
    options = nodes_page.profile_combo.get_available_selections()
    logger.debug('Detected the following available profiles: {}'.format(
        options))
    if profile not in options:
        nodes_page.profile_dialog_close.click()
        raise IllegalOperation(
            msg='no profile named {} in tagging dialog'.format(profile))
    nodes_page.profile_combo.select_by_visible_text(profile)
    nodes_page.profile_dialog_confirm.click()
    sleep(1)
    alerts.wait_for_spinner(
        spinner_element=nodes_page.introspection_spinner)
    if alerts.clear_danger_message():
        raise OperationFailed(msg='errors in tagging nodes')
    return True


def introspect_nodes(node_list):
    select_nodes(node_list)
    elem = nodes_page.introspect_nodes
    if not elem.is_enabled():
        raise IllegalOperation(
            msg="'introspect' button disabled or not found")
    logger.info('Introspecting nodes: {}'.format(node_list))
    elem.click()
    sleep(1)
    alerts.wait_for_spinner(
        timeout=3600,
        spinner_element=nodes_page.introspection_spinner)
    sleep(1)
    alerts.clear_danger_message()   # will log errors
    if not alerts.clear_success_message():
        raise OperationFailed(
            msg="node introspection failed (was it in manageable state?)")
