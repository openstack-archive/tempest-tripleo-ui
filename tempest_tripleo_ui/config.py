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

from oslo_config import cfg

ui_group = cfg.OptGroup(name='tripleo_ui', title='TripleO UI Options')

# NOTE: username and password can be acquired from the [identity] group

UIGroup = [
    cfg.StrOpt('url', default='http://localhost',
               help='where the TripleO UI can be found'),
    cfg.StrOpt('webdriver', default='Chrome',
               help='the browser to use for the test [Chrome/Marionette]'),
    cfg.StrOpt('use_remote', default=True,
               help='Use a remote selenium instance'),
    cfg.StrOpt('remote_path', default='http://localhost:4444/wd/hub',
               help='The http path to the remote selenium instance'),
    cfg.StrOpt('marionette_binary', default='path_to_wires',
               help='path to the marionette driver binary')
]
