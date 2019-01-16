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

name_elements = {}
desc_elements = {}
groups = {}
icons = {}


def validator_name(idx):
    global name_elements
    if not str(idx) in name_elements:
        name_elements[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-group-item-heading"]/a)[{}]'.format(
                idx + 1))
    return name_elements[str(idx)]


def validator_desc(idx):
    global desc_elements
    if not str(idx) in desc_elements:
        desc_elements[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-group-item-text"]/small)[{}]'.format(
                idx + 1))
    return desc_elements[str(idx)]


def validator_groups_container(idx):
    global groups
    if not str(idx) in groups:
        groups[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-view-pf-additional-info"]'
            '[div/@class="list-view-pf-additional-info-item"])[{}]'.format(
                idx + 1))
    return groups[str(idx)]


def validator_icons_container(idx):
    global icons
    if not str(idx) in icons:
        icons[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-view-pf-main-info"]'
            '/div[@class="list-view-pf-left"])[{}]'.format(idx + 1))
    return icons[str(idx)]


validations_toggle = SeleniumElement.by_xpath(
    '//li[@class="validations-toggle"]')
all_validators = Identifier.xpath(
    '//div[contains(@class, "validation-list")]'
    '/div[contains(@class, "validation")]')
all_running_validators = Identifier.xpath(
    '//div[@class="list-view-pf-main-info"]'
    '/div[@class="list-view-pf-left"]'
    '/a/span[contains(@class, "list-view-pf-icon-md") and '
    'contains(@class, "running")]')
validator_groups = Identifier.xpath('.//small/span')
validator_state_not_run = Identifier.xpath(
    './a/span[contains(@class, "list-view-pf-icon-md") and '
    'contains(@class, "fa-play-circle")]')
validator_state_running = Identifier.xpath(
    './a/span[contains(@class, "list-view-pf-icon-md") and '
    'contains(@class, "running")]')
validator_state_passed = Identifier.xpath(
    './a/div[@class="flipper"]'
    '/span[contains(@class, "pficon-ok") and '
    'contains(@class, "front")]')
validator_state_failed = Identifier.xpath(
    './a/div[@class="flipper"]'
    '/span[contains(@class, "pficon-error-circle-o") and '
    'contains(@class, "front")]')
validator_state_warning = Identifier.xpath(
    './a/div[@class="flipper"]'
    '/span[contains(@class, "pficon-warning-triangle-o") and '
    'contains(@class, "front")]')
refresh = SeleniumElement.by_xpath(
    '//div[contains(@class, "actions")]'
    '/small/a[contains(@class, "refresh")]')
