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
from tempest_tripleo_ui.models import plans
from tempest_tripleo_ui.widgets import deployment_page
from tempest_tripleo_ui.widgets import plans_page


class NoPlansAvailable(exceptions.TempestException):
    message = "Can't navigate to deployment page: no plans available!"


class DeploymentPlanPageNotFound(exceptions.TempestException):
    message = "Could not navigate to the Deployment Plan page"


DEPLOYMENT_STATUS_READY_TO_DEPLOY = "ReadyToDeploy"
DEPLOYMENT_STATUS_FAILED = "DeploymentFailed"
DEPLOYMENT_STATUS_SUCCESS = "DeploymentSucceeded"
DEPLOYMENT_STATUS_IN_PROGRESS = "DeploymentInProgress"
DEPLOYMENT_STATUS_DELETION = "DeletionInProgress"
DEPLOYMENT_STATUS_UNKNOWN = "Unknown"

logger = logging.getLogger(__name__)


def navigate_to_deployment_plan_page():
    if deployment_page.deployment_step_list.wait_for_element(1):
        return  # already on the page... :)

    logger.info("Navigating to the Deployment Plan page")
    item = plans_page.navbar_item
    if item.wait_for_element(0) and "active" not in item.get_class():
        item.click()

    if deployment_page.deployment_step_list.wait_for_element(1):
        alerts.wait_for_spinner()
        alerts.wait_for_spinner(spinner_element=deployment_page.counters_spinner)
        return

    if plans_page.create_new_plan_button.wait_for_element(3):
        current_plan = plans.get_active_plan()
        if not current_plan:
            all_plans = plans.list_plans()
            if len(all_plans) == 0:
                raise NoPlansAvailable
            if "overcloud" in all_plans:
                current_plan = "overcloud"
            else:
                current_plan = all_plans[0]
        plans.set_active_plan(current_plan)

    alerts.wait_for_spinner()
    alerts.wait_for_spinner(spinner_element=deployment_page.counters_spinner)
    if not deployment_page.deployment_step_list.wait_for_element(1):
        raise DeploymentPlanPageNotFound


def get_deployment_name():
    navigate_to_deployment_plan_page()
    return deployment_page.plan_name.get_text().strip()


def get_available_nodes():
    navigate_to_deployment_plan_page()
    nodes_total = deployment_page.nodes_available.get_text()
    return int(nodes_total.split(" ")[0])


def get_deployment_status():
    if deployment_page.plan_deployment_close.wait_for_element(0):
        deployment_page.plan_deployment_close.click()

    for _retries in range(5):
        if deployment_page.deployment_progress_bar.wait_for_element(0):
            return DEPLOYMENT_STATUS_IN_PROGRESS
        if deployment_page.verify_and_deploy_button.wait_for_element(0):
            return DEPLOYMENT_STATUS_READY_TO_DEPLOY
        if deployment_page.deployment_failed_alert.wait_for_element(0):
            return DEPLOYMENT_STATUS_FAILED
        if deployment_page.deployment_succeeded.wait_for_element(0):
            return DEPLOYMENT_STATUS_SUCCESS
        if deployment_page.deployment_deletion.wait_for_element(0):
            return DEPLOYMENT_STATUS_DELETION
        sleep(3)

    return DEPLOYMENT_STATUS_UNKNOWN
