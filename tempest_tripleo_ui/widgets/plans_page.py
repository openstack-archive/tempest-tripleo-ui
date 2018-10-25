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


def plan_header(idx):
    global plan_names
    if not str(idx) in plan_names:
        plan_names[str(idx)] = SeleniumElement.by_xpath(
            '(//div[contains(@class, "card-pf")]'
            '/div'
            '/h2[@class="card-pf-title"])[{}]'.format(idx + 1))
    return plan_names[str(idx)]


navbar_item = SeleniumElement.by_id('NavBar__PlansTab')

create_new_plan_button = SeleniumElement.by_id(
    "ListPlans__importPlanLink")
all_plan_names = Identifier.xpath(
    '//div[contains(@class, "card-pf")]'
    '/div'
    '/h2[@class="card-pf-title"]')
active_plan_flag = SeleniumElement.by_xpath(
    '//div[contains(@class, "active") '
    'and contains(@class, "plan-card")]')
