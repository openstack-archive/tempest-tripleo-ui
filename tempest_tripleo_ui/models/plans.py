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
from tempest_tripleo_ui.core import selenium_elements
from tempest_tripleo_ui.widgets import deployment_page
from tempest_tripleo_ui.widgets import plans_page
from time import sleep


class PlansPageNotFound(exceptions.TempestException):
    message = "Could not navigate to Plan List page"


class NoPlansFound(exceptions.TempestException):
    message = "No plans found"


class PlanNameNotFound(exceptions.TempestException):
    message = "Plan '%(plan_name)s' not found"


class PlanNotActive(exceptions.TempestException):
    message = "Plan '%(plan_name)s' is not the active plan"


logger = logging.getLogger(__name__)


def navigate_to_plans_list():
    for _retries in range(5):
        if plans_page.create_new_plan_button.wait_for_element(0):
            return True
        if plans_page.create_new_plan_link.wait_for_element(0):
            return True
        if plans_page.navbar_item.wait_for_element(0) and \
                "active" not in plans_page.navbar_item.get_class():
            plans_page.navbar_item.click()
        if deployment_page.manage_deployments.wait_for_element(0):
            deployment_page.manage_deployments.click()
        if deployment_page.all_plans_breadcrumb.wait_for_element(0):
            deployment_page.all_plans_breadcrumb.click()
        sleep(3)

    raise PlansPageNotFound


def list_plans():
    navigate_to_plans_list()
    logger.info("Listing plans ...")
    name_elements = selenium_elements(plans_page.all_plan_names)
    if not name_elements or len(name_elements) == 0:
        return None

    plans = []
    for name_element in name_elements:
        plans.append(name_element.get_text())

    logger.info("Found plans: {}".format(plans))
    return plans


def get_active_plan():
    logger.info("Searching for the active plan...")

    # find out which row's flag is found
    active_plan = plans_page.active_plan_flag
    if active_plan.wait_for_element(0):
        active_plan_text = str(active_plan.get_text()).split()[0]
        logger.info("Active plan is: {}".format(active_plan_text))
        return active_plan_text

    return None


def set_active_plan(plan_name):
    plans = list_plans()
    if plans is None or len(plans) == 0:
        raise NoPlansFound
    if plan_name not in plans:
        raise PlanNameNotFound(plan_name=plan_name)

    logger.info("Setting plan {} to active...".format(plan_name))
    idx = plans.index(plan_name)
    plans_page.plan_header(idx).click()

    if not deployment_page.deployment_step_list.wait_for_element():
        raise PlanNotActive(plan_name)
    alerts.wait_for_spinner()
    alerts.wait_for_spinner(
        timeout=120,
        spinner_element=deployment_page.counters_spinner)
    alerts.clear_all_danger_messages()
    return
