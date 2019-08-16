# -*- coding: utf-8 -*-
#
# File: testToolPloneMeeting.py
#
# Copyright (c) 2007-2012 by PloneGov
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

from collective.iconifiedcategory.utils import get_categorized_elements
from Products.MeetingSeraing.tests.MeetingSeraingTestCase import MeetingSeraingTestCase
from Products.MeetingCommunes.tests.testToolPloneMeeting import testToolPloneMeeting as mctt


class testToolPloneMeeting(MeetingSeraingTestCase, mctt):
    '''Tests the ToolPloneMeeting class methods.'''

    def test_pm_CloneItemWithAnnexes(self):
        '''Clones a given item containing annexes in parent item folder.'''
        self.changeUser('pmManager')
        item1 = self.create('MeetingItem')
        # Add one annex and one decision annex
        annex1 = self.addAnnex(item1)
        self.addAnnex(item1, relatedTo='item_decision')
        self.assertFalse(annex1.to_print, None)
        annex1.to_print = True
        workingFolder = item1.getParentNode()
        # clone copyAnnexes=True and copyDecisionAnnexes=False by default
        clonedItem = item1.clone()
        self.assertEquals(
            set([item1, clonedItem]), set(workingFolder.objectValues('MeetingItem')))
        # Check that the annexes have been cloned, too.
        self.assertEqual(len(get_categorized_elements(clonedItem)), 1)
        newAnnex = clonedItem.objectValues()[0]
        self.assertEqual(newAnnex.portal_type, 'annex')
        # to_print is kept as cfg.keepOriginalToPrintOfClonedItems is True by default
        self.assertTrue(self.meetingConfig.getKeepOriginalToPrintOfClonedItems())
        self.assertTrue(newAnnex.to_print)
        newAnnexesUids = [annex.UID() for annex in clonedItem.objectValues()]
        self.assertEquals(
            [annex.UID() for annex in get_categorized_elements(clonedItem, result_type='objects')],
            newAnnexesUids)
        self.assertEquals(clonedItem.categorized_elements.keys(), newAnnexesUids)
        self.assertEquals(len(clonedItem.categorized_elements), 1)
        # Test that an item viewable by a different user (another member of the
        # same group) can be pasted too if it contains things. item1 is viewable
        # by pmCreator1 too. And Also tests cloning without annex copying.
        self.changeUser('pmCreator1')
        clonedItem2 = item1.clone(copyAnnexes=False)
        self.assertEquals(len(clonedItem2.categorized_elements), 0)
        self.assertEquals(set([clonedItem2]),
                          set(clonedItem2.getParentNode().objectValues('MeetingItem')))

        # test when not keeping decision annexes for SERAING
        clonedItem3 = item1.clone(copyAnnexes=False, copyDecisionAnnexes=True)
        self.assertEquals(len(clonedItem3.categorized_elements), 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testToolPloneMeeting, prefix='test_pm_'))
    return suite
