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
from time import sleep


class NoValidatorsFound(exceptions.TempestException):
    message = "No validators found on page"


logger = logging.getLogger(__name__)

NOTRUN = "NotRun"
PASSED = "Passed"
FAILED = "Failed"
WARNING = "Warning"
RUNNING = "Running"
UNKNOWN = "Unknown"

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
    logger.info("found validators: {}".format(validator_names))
    return validator_names

def open_validators_pane():
    if not validators_page.validations_toggle.is_visible():
        raise NoValidatorsFound
    while not validators_page.refresh.is_visible():
        validators_page.validations_toggle.click()
        sleep(1)
