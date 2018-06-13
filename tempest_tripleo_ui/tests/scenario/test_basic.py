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

from six.moves.urllib import request

from tempest import config
from tempest import test


CONF = config.CONF


class TestBasic(test.BaseTestCase):

    """Checks that the UI is available"""

    opener = None

    def check_if_ui_accessible(self):
        response = self._get_opener().open(CONF.tripleo_ui.url).read()
        self.assertIn('tripleo_ui_config.js', response)

    def _get_opener(self):
        if not self.opener:
            self.opener = request.build_opener(request.HTTPCookieProcessor())
        return self.opener

    def test_basic_scenario(self):
        self.check_if_ui_accessible()
