# -*- coding: utf-8 -*-
#
# File: testMeetingItem.py
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

from Products.MeetingSeraing.tests.MeetingSeraingTestCase import MeetingSeraingTestCase
from Products.MeetingCommunes.tests.testMeetingItem import testMeetingItem as mctmi
from Products.PloneMeeting.interfaces import IAnnexable
from Products.CMFCore.permissions import View


class testMeetingItem(MeetingSeraingTestCase, mctmi):
    """
        Tests the MeetingItem class methods.
    """

    def test_subproduct_call_PowerObserversLocalRoles(self):
        '''Check that powerobservers local roles are set correctly...
           Test alternatively item or meeting that is accessible to and not...'''
        # we will check that (restricted) power observers local roles are set correctly.
        # - powerobservers may access itemcreated, validated and presented items (and created meetings),
        #   not restricted power observers;
        # - frozen items/meetings are accessible by both;
        # - only restricted power observers may access 'refused' items.
        self.meetingConfig.setItemPowerObserversStates(('itemcreated', 'validated', 'presented',
                                                       'itemfrozen', 'accepted', 'delayed'))
        self.meetingConfig.setMeetingPowerObserversStates(('created', 'frozen', 'decided', 'closed'))
        self.meetingConfig.setItemRestrictedPowerObserversStates(('itemfrozen', 'accepted', 'refused'))
        self.meetingConfig.setMeetingRestrictedPowerObserversStates(('frozen', 'decided', 'closed'))
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        item.setDecision("<p>Decision</p>")
        # itemcreated item is accessible by powerob, not restrictedpowerob
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        # propose the item, it is no more visible to any powerob
        self.proposeItem(item)
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.changeUser('powerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        # validate the item, only accessible to powerob
        self.validateItem(item)
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        # present the item, only viewable to powerob, including created meeting
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date='2015/01/01')
        self.presentItem(item)
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.assertFalse(self.hasPermission(View, meeting))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        # frozen items/meetings are accessible by both powerobs
        self.freezeMeeting(meeting)
        self.assertTrue(item.queryState() == 'itemfrozen')
        self.changeUser('restrictedpowerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        # decide the meeting and refuse the item, meeting accessible to both
        # but refused item only accessible to restricted powerob
        self.decideMeeting(meeting)
        self.changeUser('pmManager')
        self.do(item, 'accept')
        self.changeUser('restrictedpowerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))

    def test_subproduct_call_SendItemToOtherMCWithAnnexes(self):
        '''Test that sending an item to another MeetingConfig behaves normaly with annexes.
           This is a complementary test to testToolPloneMeeting.testCloneItemWithContent.
           Here we test the fact that the item is sent to another MeetingConfig.'''
        data = self._setupSendItemToOtherMC(with_annexes=True)
        newItem = data['newItem']
        annex1 = data['annex1']
        annex2 = data['annex2']
        decisionAnnex1 = data['decisionAnnex1']
        decisionAnnex2 = data['decisionAnnex2']
        # Check that annexes are actually correctly sent too
        # we had 2 normal annexes and 2 decision annexes
        self.failUnless(len(IAnnexable(newItem).getAnnexes()) == 2)
        self.failUnless(len(IAnnexable(newItem).getAnnexes(relatedTo='item')) == 2)
        self.failUnless(len(IAnnexable(newItem).getAnnexes(relatedTo='item_decision')) == 0)
        # As annexes are references from the item, check that these are not
        self.assertEquals(set([newItem]), set(newItem.getParentNode().objectValues()))
        # Especially test that references are ok about the MeetingFileTypes
        existingMeetingFileTypeIds = [ft['id'] for ft in self.meetingConfig.getFileTypes(relatedTo='item')]
        existingMeetingFileTypeDecisionIds = [ft['id'] for ft in
                                              self.meetingConfig.getFileTypes(relatedTo='item_decision')]
        self.failUnless(annex1.getMeetingFileType() in existingMeetingFileTypeIds)
        self.failUnless(annex2.getMeetingFileType() in existingMeetingFileTypeIds)
        self.failUnless(decisionAnnex1.getMeetingFileType() in existingMeetingFileTypeDecisionIds)
        # the MeetingFileType of decisionAnnex1 is deactivated
        self.failIf(decisionAnnex2.getMeetingFileType() in existingMeetingFileTypeDecisionIds)
        # query existing MFT even disabled ones
        existingMeetingFileTypeIncludingNotSelectableIds = [ft['id'] for ft in
                                                            self.meetingConfig.getFileTypes(relatedTo='item_decision',
                                                                                            onlySelectable=False)]
        self.failUnless(decisionAnnex2.getMeetingFileType() in existingMeetingFileTypeIncludingNotSelectableIds)
        # Now check the MeetingFileType of new annexes
        # annex1 has no correspondence on the new MeetingConfig so the
        # frist MFT of same relatedTo is used
        defaultMC2ItemMFT = self.meetingConfig2.getFileTypes(annex1.findRelatedTo())[0]
        self.assertEquals(newItem.objectValues('MeetingFile')[0].getMeetingFileType(),
                          defaultMC2ItemMFT['id'])
        # annex2 was of annexType "overhead-analysis" that does NOT have correspondence
        # frist MFT of same relatedTo is used
        self.assertEquals(newItem.objectValues('MeetingFile')[1].getMeetingFileType(),
                          defaultMC2ItemMFT['id'])

    def test_subproduct_call_ItemStrikedAssembly(self):
        self.test_pm_ItemStrikedAssembly()

    def test_subproduct_call_Emergency(self):
        self.test_pm_Emergency()

    def test_subproduct_call_Completeness(self):
        self.test_pm_Completeness()

    def test_subproduct_call_SendItemToOtherMCManually(self):
        self.test_pm_SendItemToOtherMCManually()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_subproduct_'))
    return suite
