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
icons_status_passed = {}
icons_status_failed = {}
icons_status_warning = {}
icons_status_unknown = {}
icons_status_running = {}
icons_status_notrun = {}


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


def validator_status_running(idx):
    global icons_status_running
    if not str(idx) in icons_status_running:
        icons_status_running[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-view-pf-main-info"]'
            '/div[@class="list-view-pf-left"])[{}]'
            '/a/span[contains(@class, "list-view-pf-icon-md") and '
            'contains(@class, "running")]'.format(idx + 1))
    return icons_status_running[str(idx)]


def validator_status_notrun(idx):
    global icons_status_notrun
    if not str(idx) in icons_status_notrun:
        icons_status_notrun[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-view-pf-main-info"]'
            '/div[@class="list-view-pf-left"])[{}]'
            '/a/span[contains(@class, "list-view-pf-icon-md") and '
            'contains(@class, "fa-play-circle")]'.format(idx + 1))
    return icons_status_notrun[str(idx)]


def validator_status_passed(idx):
    global icons_status_passed
    if not str(idx) in icons_status_passed:
        icons_status_passed[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-view-pf-main-info"]'
            '/div[@class="list-view-pf-left"])[{}]'
            '/a/div[@class="flipper"]'
            '/span[contains(@class, "pficon-ok") and '
            'contains(@class, "front")]'.format(idx + 1))
    return icons_status_passed[str(idx)]


def validator_status_failed(idx):
    global icons_status_failed
    if not str(idx) in icons_status_failed:
        icons_status_failed[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-view-pf-main-info"]'
            '/div[@class="list-view-pf-left"])[{}]'
            '/a/div[@class="flipper"]'
            '/span[contains(@class, "pficon-error-circle-o") and '
            'contains(@class, "front")]'.format(idx + 1))
    return icons_status_failed[str(idx)]


def validator_status_warning(idx):
    global icons_status_warning
    if not str(idx) in icons_status_warning:
        icons_status_warning[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-view-pf-main-info"]'
            '/div[@class="list-view-pf-left"])[{}]'
            '/a/div[@class="flipper"]'
            '/span[contains(@class, "pficon-warning-triangle-o") and '
            'contains(@class, "front")]'.format(idx + 1))
    return icons_status_warning[str(idx)]


def validator_status_unknown(idx):
    global icons_status_unknown
    if not str(idx) in icons_status_unknown:
        icons_status_unknown[str(idx)] = SeleniumElement.by_xpath(
            '(//div[@class="list-view-pf-main-info"]'
            '/div[@class="list-view-pf-left"])[{}]'
            '/a/div[@class="flipper"]'
            '/span[contains(@class, "pficon-help")]'.format(idx + 1))
    return icons_status_unknown[str(idx)]


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
refresh = SeleniumElement.by_xpath(
    '//div[contains(@class, "actions")]'
    '/small/a[contains(@class, "refresh")]')
