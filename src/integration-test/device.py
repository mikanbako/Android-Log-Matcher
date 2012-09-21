# coding: UTF-8

# Copyright 2012 Keita Kita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Management an instance of MonkeyDevice while integration test.
#
# If MonkeyDevice tried to create par test method,
# MonkeyRunner.waitForConnection blocks for a long time on Android SDK 20.x.


from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

device = None

def init():
    u'''
    Initialize MonkeyDevice that held by this module.
    '''
    global device
    if not device:
        device = MonkeyRunner.waitForConnection(5)

def get():
    u'''
    Get MonkeyDevice that held by this module.
    '''
    global device
    return device
