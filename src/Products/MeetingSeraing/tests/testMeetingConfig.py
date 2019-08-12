# -*- coding: utf-8 -*-
#
# File: testMeetingConfig.py
#
# Copyright (c) 2007-2013 by Imio.be
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
import logging
from Products.MeetingSeraing.tests.MeetingSeraingTestCase import MeetingSeraingTestCase
from Products.MeetingCommunes.tests.testMeetingConfig import testMeetingConfig as mctmc


class testMeetingConfig(MeetingSeraingTestCase, mctmc):
    '''Call testMeetingConfig tests.'''

    def test_pm_searchItemsToPrevalidate(self):
        '''No sense...'''
        pass

    def test_pm_searchReviewableItems(self):
        '''Test the searchReviewableItems search.'''
        pass

    def test_pm_ConfigLinkedGroupsRemovedWhenConfigDeleted(self, ):
        """When the MeetingConfig is deleted, created groups are removed too :
           - meetingmanagers group;
           - powerobservers groups;
           - budgetimpacteditors group.
           """
        self.changeUser('siteadmin')
        newCfg = self.create('MeetingConfig')
        newCfgId = newCfg.getId()
        # this created 4 groups
        created_groups = [groupId for groupId in self.portal.portal_groups.listGroupIds()
                          if groupId.startswith(newCfgId)]
        self.assertEquals(len(created_groups), 5)
        # remove the MeetingConfig, groups are removed as well
        self.tool.restrictedTraverse('@@delete_givenuid')(newCfg.UID())
        self.assertFalse(newCfgId in self.tool.objectIds())
        created_groups = [groupId for groupId in self.portal.portal_groups.listGroupIds()
                          if groupId.startswith(newCfgId)]
        #self.assertFalse(created_groups)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testMeetingConfig, prefix='test_pm_'))
    return suite
