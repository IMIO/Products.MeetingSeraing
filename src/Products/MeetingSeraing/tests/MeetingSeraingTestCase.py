# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2010 by PloneGov
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Products.PloneMeeting.tests.PloneMeetingTestCase import PloneMeetingTestCase
from Products.MeetingSeraing.testing import MS_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingSeraing.tests.helpers import MeetingSeraingTestingHelpers

# monkey patch the MeetingConfig.wfAdaptations again because it is done in
# adapters.py but overrided by Products.PloneMeeting here in the tests...
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.model import adaptations
from Products.MeetingSeraing.adapters import customWfAdaptations
from Products.MeetingSeraing.adapters import RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE

MeetingConfig.wfAdaptations = customWfAdaptations
adaptations.RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE

class MeetingSeraingTestCase(PloneMeetingTestCase, MeetingSeraingTestingHelpers):
    """Base class for defining MeetingSeraing test cases."""

    layer = MS_TESTING_PROFILE_FUNCTIONAL

    def setUp(self):
        PloneMeetingTestCase.setUp(self)
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        self.meetingConfig2 = getattr(self.tool, 'meeting-config-council')