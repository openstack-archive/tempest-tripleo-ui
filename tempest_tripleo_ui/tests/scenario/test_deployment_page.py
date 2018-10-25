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
from tempest_tripleo_ui.base import GUITestCase
from tempest_tripleo_ui.models import deployment
from tempest_tripleo_ui.widgets import deployment_page
from testtools.matchers._basic import GreaterThan
from time import sleep

logger = logging.getLogger(__name__)


class TestDeploymentPage(GUITestCase):

    def test_deployment_plan_page_elements(self):
        deployment.navigate_to_deployment_plan_page()

        self.assertIsNotNone(
            deployment_page.all_plans_breadcrumb.wait_for_element(0),
            "The navigation breadcrumbs (on the top of the deployment "
            "plan page) can't be found")
        plan_name = deployment.get_deployment_name()
        self.assertEqual("overcloud", plan_name)

        self.assertIsNotNone(
            deployment_page.deployment_step_list.wait_for_element(0),
            "The deployment workflow (the 5-step list in the deployment "
            "page) can't be found")

        self.assertIsNotNone(
            deployment_page.edit_configuration.wait_for_element(0),
            "The edit configuration button (to open the plan configuration "
            "dialog) can't be found")

        self.assertIsNotNone(
            deployment_page.nodes_available.wait_for_element(0),
            "Can't find the number of nodes available (in step 3 'Configure "
            "Roles and Assign Nodes' there should be something that says how "
            "many nodes are available and how many in total etc...)")
        nodes_available_text = deployment_page.nodes_available.get_text()
        self.assertIn(
            'Nodes Total',
            nodes_available_text,
            "Can't find the expected text in the nodes available span (step "
            "3 above the roles counters). "
            "Got: '{}'".format(nodes_available_text))
        self.assertThat(
            deployment.get_available_nodes(),
            GreaterThan(0),
            "Number of available nodes is 0")

        self.assertEqual(
            deployment.get_deployment_status(),
            deployment.DEPLOYMENT_STATUS_READY_TO_DEPLOY,
            "Deployment status is not DEPLOYMENT_STATUS_READY_TO_DEPLOY "
            "(error detecting deployment status)")
        self.assertIsNotNone(
            deployment_page.verify_and_deploy_button.wait_for_element(0),
            "Can't find the 'Verify and Deploy' button (step 5)")

    def test_deployment_configuration_dialog(self):
        deployment.navigate_to_deployment_plan_page()
        deployment_page.edit_configuration.click()
        sleep(5)
        self.assertIsNotNone(
            deployment_page.deployment_configuration_dialog.
            wait_for_element(0),
            "Can't locate the Edit Configuration dialog, after clicking the "
            "edit button and waiting 5 seconds")

        self.assertIsNotNone(
            deployment_page.overall_settings_tab.wait_for_element(0),
            "Can't find the Overall Settings tab in the Edit Configuration "
            "dialog")

        self.assertIsNotNone(
            deployment_page.parameters_tab.wait_for_element(0),
            "Can't find the Parameters tab in the Edit Configuration "
            "dialog")

        self.assertIsNotNone(
            deployment_page.abort_deployment_configuration_button.
            wait_for_element(0),
            "Can't find the 'Cancel' button in the Edit Configuration "
            "dialog")

        self.assertIsNotNone(
            deployment_page.save_deployment_configuration_button.
            wait_for_element(0),
            "Can't find the 'Save And Close' button in the Edit "
            "Configuration dialog")

        env_file = deployment_page.environment_file(
            "environments/ssl/enable-tls.yaml")
        self.assertIsNotNone(
            env_file.wait_for_element(0),
            "Can't find the 'TLS' environment file (environments/ssl/"
            "enable-tls.yaml) in the Configuration dialog")

        # close the dialog
        deployment_page.abort_deployment_configuration_button.click()
        sleep(2)
        self.assertIsNone(
            deployment_page.deployment_configuration_dialog.
            wait_for_element(0),
            "Edit configuration dialog didn't close")

    def test_open_deploy_dialog(self):
        deployment.navigate_to_deployment_plan_page()
        self.assertIsNotNone(
            deployment_page.deploy_button.wait_for_element(0),
            "Can't find the 'Deploy' button")
        deployment_page.deploy_button.click()
        sleep(5)

        self.assertIsNotNone(
            deployment_page.plan_deployment_close.wait_for_element(0),
            "Can't find the 'Close' button in the deploy dialog")
        deployment_page.plan_deployment_close.click()
        sleep(2)
