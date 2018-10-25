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

from tempest_tripleo_ui.core import SeleniumElement


plan_name = SeleniumElement.by_id("CurrentPlan__breadcrumb")
all_plans_breadcrumb = SeleniumElement.by_xpath(
    '//ol[@class="breadcrumb"]/li[1]/a[@href="/plans/manage"]')
deployment_step_list = SeleniumElement.by_xpath(
    '//ol[@class="deployment-step-list"]')
counters_spinner = SeleniumElement.by_xpath(
    "//span[contains(@class, 'spinner-inline')]")
edit_configuration = SeleniumElement.by_id(
    'ConfigurePlanStep__EditDeploymentLink')
nodes_available = SeleniumElement.by_xpath(
    '//ol[@class="deployment-step-list"]/li[3]/div/p/span/span/span')
manage_deployments = SeleniumElement.by_xpath("//a[@href='/plans']")
verify_and_deploy_button = SeleniumElement.by_xpath(
    '//a[contains(@class, "btn-primary")]'
    '/span/span[contains(text(), "Validate and Deploy")]')
delete_deployment_button = SeleniumElement.by_xpath(
    '//button[@name="delete"]')
confirm_delete_deployment = SeleniumElement.by_xpath(
    '//div[@class="modal-footer"]/button[@name="delete"]')
deployment_failed_alert = SeleniumElement.by_xpath(
    '//div/div[contains(@class, "alert-danger")]'
    '/strong[text()="Deployment failed"]')
deployment_succeeded = SeleniumElement.by_xpath(
    '//div[contains(@class, "alert-success")]'
    '/strong[text()="Deployment succeeded"]')
deployment_progress_bar = SeleniumElement.by_xpath(
    '//div[@class="progress-bar"]')
deployment_progress_percentage = SeleniumElement.by_xpath(
    '//div[@class="progress-bar"]/span')
deployment_deletion = SeleniumElement.by_xpath(
    '//div[@class="progress-description"]'
    '/span/strong/span[text()="Deletion in progress"]')
deploy_button = SeleniumElement.by_xpath(
    '//a[@href="/plans/overcloud/deployment-confirmation"]')
plan_deployment_close = SeleniumElement.by_xpath(
    '//div[contains(@class, "modal-footer")]'
    '/button[contains(@class, "btn-default")]'
    '/span[text()="Close"]')

# the deployment configuration dialog and the 2 tabs in it
deployment_configuration_dialog = SeleniumElement.by_xpath(
    '//div[@class="modal-header"]'
    '//h4[@class="modal-title"]'
    '/span[text()="Deployment Configuration"]')
overall_settings_tab = SeleniumElement.by_id(
    'DeploymentConfiguration__OverallSettingsTab')
parameters_tab = SeleniumElement.by_id(
    'DeploymentConfiguration__ParametersTab')
abort_deployment_configuration_button = SeleniumElement.by_xpath(
    '//div[@class="modal-footer"]'
    '/button'
    '/span[text()="Cancel"]')
save_deployment_configuration_button = SeleniumElement.by_xpath(
    '//div[@class="modal-footer"]/button[span/text()="Save And Close"]')

environments = {}


def environment_file(yaml_name):
    global environments
    if yaml_name not in environments:
        environments[yaml_name] = SeleniumElement.by_xpath(
            '//label[@title="{}"]/input'.format(yaml_name))
    return environments[yaml_name]
