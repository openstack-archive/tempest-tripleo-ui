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


plan_names = {}
kebab_menus = {}
delete_plans = {}
edit_plans = {}
export_plans = {}


def plan_header(idx):
    global plan_names
    if not str(idx) in plan_names:
        plan_names[str(idx)] = SeleniumElement.by_xpath(
            '(//div[contains(@class, "card-pf")]'
            '/div'
            '/h2[@class="card-pf-title"])[{}]'.format(idx + 1))
    return plan_names[str(idx)]


def kebab_menu(plan_name):
    global kebab_menus
    if plan_name not in kebab_menus:
        kebab_menus[plan_name] = SeleniumElement.by_xpath(
            '//button[@id="card-actions-{}"]'.format(plan_name))
    return kebab_menus[plan_name]


def delete_plan(plan_name):
    global delete_plans
    if plan_name not in delete_plans:
        delete_plans[plan_name] = SeleniumElement.by_xpath(
            '//ul[contains(@class, "dropdown-menu")]'
            '/li/a[@href="/plans/manage/{}/delete"]'.format(plan_name))
    return delete_plans[plan_name]


def edit_plan(plan_name):
    global edit_plans
    if plan_name not in edit_plans:
        edit_plans[plan_name] = SeleniumElement.by_xpath(
            '//ul[contains(@class, "dropdown-menu")]'
            '/li/a[@href="/plans/manage/{}/edit"]'.format(plan_name))
    return edit_plans[plan_name]


def export_plan(plan_name):
    global export_plans
    if plan_name not in export_plans:
        export_plans[plan_name] = SeleniumElement.by_xpath(
            '//ul[contains(@class, "dropdown-menu")]'
            '/li/a[@href="/plans/manage/{}/export"]'.format(plan_name))
    return export_plans[plan_name]


navbar_item = SeleniumElement.by_id('NavBar__PlansTab')

create_new_plan_button = SeleniumElement.by_id(
    "ListPlans__importPlanButton")
create_new_plan_link = SeleniumElement.by_id(
    "ListPlans__importPlanLink")    # appears when there are no plans
all_plan_names = Identifier.xpath(
    '//div[contains(@class, "card-pf")]'
    '/div'
    '/h2[@class="card-pf-title"]')
active_plan_flag = SeleniumElement.by_xpath(
    '//div[contains(@class, "active") '
    'and contains(@class, "plan-card")]')

plan_name = SeleniumElement.by_id(
    "planName")
plan_from_default_templates = SeleniumElement.by_xpath(
    '//input[@value="default"]')
plan_from_local_directory = SeleniumElement.by_xpath(
    '//input[@value="directory"]')
plan_from_tarball = SeleniumElement.by_xpath(
    '//input[@value="tarball"]')
plan_from_git = SeleniumElement.by_xpath(
    '//input[@value="git"]')
browse_button_local_directory = SeleniumElement.by_id(
    'files')
browse_button_tarball = SeleniumElement.by_id(
    'tarball')
upload_files_button = SeleniumElement.by_id(
    'NewPlanForm_submitButton')
cancel_upload_button = SeleniumElement.by_id(
    'NewPlanForm__cancelCreatePlanButton')
