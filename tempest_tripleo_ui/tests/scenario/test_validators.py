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
from tempest_tripleo_ui.models import validators
from testtools.matchers._basic import GreaterThan

logger = logging.getLogger(__name__)


class TestValidators(GUITestCase):

    def test_validators(self):
        deployment.navigate_to_deployment_plan_page()

        names = validators.get_validator_names()
        self.assertThat(
            len(names),
            GreaterThan(0),
            "No validators found")

        for name in names:
            self.assertThat(
                len(name.strip()),
                GreaterThan(0),
                "Some validators have blank names: {}".format(names))

        # we wait for validators to stop running (they get triggered
        # automatically when you open the plan)
        self.assertEqual(
            validators.wait_for_validators_to_start(),
            True,
            "Validators didn't get triggered automatically, "
            "nothing is running")
        self.assertEqual(
            validators.wait_for_validators_to_finish(),
            True,
            "Validators are running for too long")

        # now check the validator statuses
        for idx in range(len(names)):
            status = validators.get_validator_status(idx)
            logger.info('[{}]: "{}"'.format(status, names[idx]))
            self.assertIn(
                status,
                [validators.PASSED, validators.FAILED, validators.UNKNOWN,
                    validators.NOTRUN, validators.WARNING],
                "Unexpected validator status for validator: "
                "[{}] {}".format(status, names[idx]))

        # start one of the validators
        idx = names.index('Check controller ulimits')
        self.assertThat(
            idx,
            GreaterThan(-1),
            "Validator 'Check controller ulimits' not found")
        validators.start_validator(idx)
        self.assertEqual(
            validators.wait_on_validator(idx),
            True,
            "Validator 'Check controller ulimits' didn't finish")
        status = validators.get_validator_status(idx)
        logger.info('[{}]: "{}"'.format(status, names[idx]))
        self.assertIn(
            status,
            [validators.PASSED, validators.FAILED, validators.WARNING],
            'Unexpected validator status for "{}": {}'.format(
                names[idx], status))
