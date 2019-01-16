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
from tempest_tripleo_ui.core import selenium_elements
from tempest_tripleo_ui.widgets import validators_page
import time

class NoValidatorsFound(exceptions.TempestException):
    message = "No validators found on page"


class ValidatorNotFound(exceptions.TempestException):
    message = "Validator '%(validator_name)s' not found"


class ValidatorStatusNotFound(exceptions.TempestException):
    message = "No recognized validator status (icon element) found for "\
              "validator '%(validator_name)s'"


logger = logging.getLogger(__name__)

NOTRUN = "NotRun"
PASSED = "Passed"
FAILED = "Failed"
WARNING = "Warning"
RUNNING = "Running"

validator_names = None


def get_validator_names():
    global validator_names
    if validator_names:
        return validator_names

    logger.info("listing validators ...")
    open_validators_pane()
    elems = selenium_elements(validators_page.all_validators)
    if not elems or len(elems) == 0:
        raise NoValidatorsFound
    validator_names = []
    for idx in range(len(elems)):
        elem = validators_page.validator_name(idx)
        validator_names.append(elem.get_text())
    validator_names = validator_names
    logger.info("found {} validators: {}".format(
        len(validator_names), validator_names))
    return validator_names


def open_validators_pane():
    if not validators_page.validations_toggle.is_visible():
        raise NoValidatorsFound
    while not validators_page.refresh.is_visible():
        validators_page.validations_toggle.click()
        time.sleep(1)


def get_validator_idx(name_or_idx):
    try:
        # is it an int ?
        return int(name_or_idx)
    except ValueError:
        # it was a string...
        names = get_validator_names()
        if name_or_idx not in names:
            raise ValidatorNotFound(validator_name=name_or_idx)
        return names.index(name_or_idx)


def get_validator_status(name_or_idx):
    global NOTRUN
    global PASSED
    global FAILED
    global WARNING
    global RUNNING

    idx = get_validator_idx(name_or_idx)
    icon_div_elem = validators_page.validator_icons_container(idx)
    for _retry in range(2):
        children = icon_div_elem.find_child_elements(
            validators_page.validator_state_running)
        if children and len(children) == 1:
            logger.debug(
                "validator '{}' is RUNNING".format(name_or_idx))
            return RUNNING

        children = icon_div_elem.find_child_elements(
            validators_page.validator_state_not_run)
        if children and len(children) == 1:
            logger.debug(
                "validator '{}' is NOTRUN".format(name_or_idx))
            return NOTRUN

        children = icon_div_elem.find_child_elements(
            validators_page.validator_state_passed)
        if children and len(children) == 1:
            logger.debug(
                "validator '{}' is PASSED".format(name_or_idx))
            return PASSED

        children = icon_div_elem.find_child_elements(
            validators_page.validator_state_failed)
        if children and len(children) == 1:
            logger.debug(
                "validator '{}' is FAILED".format(name_or_idx))
            return FAILED

        children = icon_div_elem.find_child_elements(
            validators_page.validator_state_warning)
        if children and len(children) == 1:
            logger.debug(
                "validator '{}' is WARNING".format(name_or_idx))
            return WARNING
        
        # loop around to retry a 2nd time
        logger.warning(
            "it seems like the status of the validator updated "
            "while we were reading it, will retry ...")
        time.sleep(2)

    raise ValidatorStatusNotFound(validator_name=name_or_idx)


def wait_for_validators_to_start(timeout=30):
    icons = selenium_elements(validators_page.all_running_validators)
    start_time = time.time()
    while time.time() - start_time < timeout \
            and (not icons or len(icons) == 0):
        logger.info("waiting for validators to start...")
        time.sleep(10)
        icons = selenium_elements(validators_page.all_running_validators)
    return icons and len(icons) > 0

def wait_for_validators_to_finish(timeout=600):
    icons = selenium_elements(validators_page.all_running_validators)
    start_time = time.time()
    while time.time() - start_time < timeout and icons and len(icons) > 0:
        logger.info("waiting for validators to finish...")
        time.sleep(10)
        icons = selenium_elements(validators_page.all_running_validators)
    return not icons or len(icons) == 0
