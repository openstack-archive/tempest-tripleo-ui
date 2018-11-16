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
from tempest_tripleo_ui.models import plans
from tempest_tripleo_ui.widgets import plans_page
from testtools.matchers._basic import GreaterThan

logger = logging.getLogger(__name__)


class TestPlansPage(GUITestCase):

    def test_plans_page_elements(self):
        plans.navigate_to_plans_list()
        logger.info("Testing that there are plans...")
        plan_names = plans.list_plans()
        self.assertThat(
            len(plan_names),
            GreaterThan(0),
            "Number of loaded plans is 0")
        self.assertIsNotNone(
            plans_page.create_new_plan_button.wait_for_element(0),
            "The 'Import Plan' button in the Plans page can't be found")

        logger.info("Testing the kebab menus...")
        for plan_name in plan_names:
            kebab = plans_page.kebab_menu(plan_name)
            self.assertIsNotNone(
                kebab.wait_for_element(0),
                "The kebab menu for plan '{}' can't be found".format(
                    plan_name))
            kebab.click()
            self.assertIsNotNone(
                plans_page.delete_plan(plan_name).wait_for_element(0),
                "The delete menu item for plan '{}' can't be found".format(
                    plan_name))
            self.assertIsNotNone(
                plans_page.edit_plan(plan_name).wait_for_element(0),
                "The edit menu item for plan '{}' can't be found".format(
                    plan_name))
            self.assertIsNotNone(
                plans_page.export_plan(plan_name).wait_for_element(0),
                "The export menu item for plan '{}' can't be found".format(
                    plan_name))
            kebab.click()   # close the menu

        target_plan = "overcloud"
        if target_plan not in plan_names:
            target_plan = plan_names[0]
        plans.set_active_plan(target_plan)
        plans.navigate_to_plans_list()
        active_plan = plans.get_active_plan()
        self.assertEqual(
            target_plan,
            active_plan,
            "Active plan is '{}' instead of "
            "'{}'".format(active_plan, target_plan))

        logger.info("Testing the items in the import plan dialog...")
        plans_page.create_new_plan_button.click()
        self.assertIsNotNone(
            plans_page.plan_name.wait_for_element(0),
            "The plan name field can't be found in the import plan dialog")
        self.assertIsNotNone(
            plans_page.plan_from_default_templates.wait_for_element(0),
            "The option to create a plan from the default templates "
            "can't be found in the import plan dialog")
        self.assertIsNotNone(
            plans_page.plan_from_local_directory.wait_for_element(0),
            "The option to create a plan from a local directory "
            "can't be found in the import plan dialog")
        self.assertIsNotNone(
            plans_page.plan_from_tarball.wait_for_element(0),
            "The option to create a plan from a tarball "
            "can't be found in the import plan dialog")
        self.assertIsNotNone(
            plans_page.plan_from_git.wait_for_element(0),
            "The option to create a plan from a git repository "
            "can't be found in the import plan dialog")
        plans_page.plan_from_local_directory.click()
        plans_page.plan_from_local_directory.click() #1 click is not enough
        self.assertIsNotNone(
            plans_page.browse_button_local_directory.wait_for_element(0),
            "The 'Choose Files' button (create plan from local directory) "
            "can't be found in the import plan dialog")
        plans_page.plan_from_tarball.click()
        plans_page.plan_from_tarball.click()
        self.assertIsNotNone(
            plans_page.browse_button_tarball.wait_for_element(0),
            "The 'Choose Files' button (create plan from a tarball) "
            "can't be found in the import plan dialog")
        self.assertIsNotNone(
            plans_page.cancel_upload_button.wait_for_element(0),
            "The cancel button "
            "can't be found in the import plan dialog")
        self.assertIsNotNone(
            plans_page.upload_files_button.wait_for_element(0),
            "The upload button "
            "can't be found in the import plan dialog")
        plans_page.cancel_upload_button.click()
