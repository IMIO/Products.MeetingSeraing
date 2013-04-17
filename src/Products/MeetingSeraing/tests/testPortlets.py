# -*- coding: utf-8 -*-
#
# File: testPortlets.py
#
# Copyright (c) 2007-2012 by CommunesPlone.org
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

from zope.component import getUtility, getMultiAdapter
from plone.app.testing import login
from plone.portlets.interfaces import IPortletManager, IPortletRenderer
from Products.PloneMeeting.browser import portlet_plonemeeting as pm
from Products.MeetingSeraing.tests.MeetingSeraingTestCase import \
    MeetingSeraingTestCase
from Products.PloneMeeting.tests.testPortlets import testPortlets as pmtp

class testPortlets(MeetingSeraingTestCase, pmtp):
    '''Tests the portlets methods.'''

    def test_mc_call_PortletPMAvailableTemplates(self):
        '''Run the testPortletPMAvailableTemplates from PloneMeeting.'''
        pmtp.testPortletPMAvailableTemplates(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testPortlets, prefix='test_mc_'))
    return suite
