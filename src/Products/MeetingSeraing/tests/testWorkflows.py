# -*- coding: utf-8 -*-
#
# File: testWorkflows.py
#
# Copyright (c) 2007-2010 by PloneGov
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

from AccessControl import Unauthorized
from DateTime import DateTime
from Products.CMFCore.permissions import View
from Products.MeetingCommunes.tests.testWorkflows import testWorkflows as mctw
from Products.MeetingSeraing.tests.MeetingSeraingTestCase import MeetingSeraingTestCase
from Products.PloneMeeting.config import EXECUTE_EXPR_VALUE


class testWorkflows(MeetingSeraingTestCase, mctw):
    """Tests the default workflows implemented in MeetingSeraing.

       WARNING:
       The Plone test system seems to be bugged: it does not seem to take into
       account the write_permission and read_permission tags that are defined
       on some attributes of the Archetypes model. So when we need to check
       that a user is not authorized to set the value of a field protected
       in this way, we do not try to use the accessor to trigger an exception
       (self.assertRaise). Instead, we check that the user has the permission
       to do so (getSecurityManager().checkPermission)."""

    def test_pm_WholeDecisionProcess(self):
        """
            This test covers the whole decision workflow. It begins with the
            creation of some items, and ends by closing a meeting.
            This call sub tests for college process : council using the same wf
        """
        self._testWholeDecisionProcessCollege()

    def _testWholeDecisionProcessCollege(self):
        '''This test covers the whole decision workflow. It begins with the
           creation of some items, and ends by closing a meeting.'''
        # pmCreator1 creates an item with 1 annex and proposes it
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem', title='The first item')
        annex1 = self.addAnnex(item1)
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'proposeToServiceHead')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # the ServiceHead validation level
        self.changeUser('pmServiceHead1')
        self.failUnless(self.hasPermission('Modify portal content', (item1, annex1)))
        self.do(item1, 'proposeToOfficeManager')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # the OfficeManager validation level
        self.changeUser('pmOfficeManager1')
        self.failUnless(self.hasPermission('Modify portal content', (item1, annex1)))
        self.do(item1, 'proposeToDivisionHead')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # the DivisionHead validation level
        self.changeUser('pmDivisionHead1')
        self.failUnless(self.hasPermission('Modify portal content', (item1, annex1)))
        self.do(item1, 'propose')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # the Director validation level
        self.changeUser('pmReviewer1')
        self.failUnless(self.hasPermission('Modify portal content', (item1, annex1)))
        self.do(item1, 'validate')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # pmManager creates a meeting
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        self.addAnnex(item1, relatedTo='item_decision')
        # pmCreator2 creates and proposes an item
        self.changeUser('pmCreator2')
        item2 = self.create('MeetingItem', title='The second item',
                            preferredMeeting=meeting.UID())
        self.do(item2, 'proposeToServiceHead')
        # pmReviewer1 can not validate the item has not in the same proposing group
        self.changeUser('pmReviewer1')
        self.failIf(self.hasPermission('Modify portal content', item2))
        # even pmManagercan not see/validate an item in the validation queue
        self.changeUser('pmManager')
        self.failIf(self.hasPermission('Modify portal content', item2))
        # do the complete validation
        self.changeUser('admin')
        self.do(item2, 'proposeToOfficeManager')
        self.do(item2, 'proposeToDivisionHead')
        self.do(item2, 'propose')
        # pmManager inserts item1 into the meeting and publishes it
        self.changeUser('pmManager')
        managerAnnex = self.addAnnex(item1)
        self.portal.restrictedTraverse('@@delete_givenuid')(managerAnnex.UID())
        self.do(item1, 'present')
        # Now reviewers can't add annexes anymore
        self.changeUser('pmReviewer2')
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        # freeze the meeting
        self.changeUser('pmManager')
        self.do(meeting, 'validateByDG')
        self.do(meeting, 'freeze')
        # validate item2 after meeting freeze
        self.changeUser('pmReviewer2')
        self.do(item2, 'validate')
        self.changeUser('pmManager')
        self.do(item2, 'present')
        self.addAnnex(item2)
        # So now we should have 3 normal item (2 recurring + 1) and one late item in the meeting
        self.failUnless(len(meeting.getItems()) == 4)
        self.failUnless(len(meeting.getItems(listTypes='late')) == 1)
        self.do(meeting, 'decide')
        self.do(item1, 'accept')
        self.assertEquals(item1.queryState(), 'accepted')
        self.assertEquals(item2.queryState(), 'itemfrozen')
        self.do(meeting, 'close')
        self.assertEquals(item1.queryState(), 'accepted_closed')
        # every items without a decision are automatically accepted_closed
        self.assertEquals(item2.queryState(), 'accepted_closed')

    def test_pm_WorkflowPermissions(self):
        """Bypass this test..."""
        pass


    def test_pm_RecurringItems(self):
        """Bypass this test..."""
        pass


    def test_pm_MeetingExecuteActionOnLinkedItemsGiveAccessToAcceptedItemsOfAMeetingToPowerAdvisers(self):
        '''Test the MeetingConfig.onMeetingTransitionItemActionToExecute parameter :
           specific usecase, being able to give access to decided items of a meeting only when meeting
           is closed, even if item is decided before the meeting is closed.'''
        self.changeUser('siteadmin')
        cfg = self.meetingConfig
        # call updateLocalRoles on item only if it not already decided
        # as updateLocalRoles is called when item review_state changed
        self.assertTrue('accepted' in cfg.getItemDecidedStates())
        cfg.setOnMeetingTransitionItemActionToExecute(
            [{'meeting_transition': 'decide',
              'item_action': 'itemValidateByDG',
              'tal_expression': ''},
             {'meeting_transition': 'decide',
              'item_action': 'itemfreeze',
              'tal_expression': ''},

             {'meeting_transition': 'close',
              'item_action': 'itemValidateByDG',
              'tal_expression': ''},
             {'meeting_transition': 'close',
              'item_action': 'itemfreeze',
              'tal_expression': ''},
             {'meeting_transition': 'close',
              'item_action': EXECUTE_EXPR_VALUE,
              'tal_expression': 'python: item.queryState() in cfg.getItemDecidedStates() and '
                'item.updateLocalRoles()'},
             {'meeting_transition': 'close',
              'item_action': 'accept',
              'tal_expression': ''}, ])
        # configure access of powerobservers only access if meeting is 'closed'
        cfg.setPowerObservers([
            {'item_access_on': 'python: item.getMeeting().queryState() == "closed"',
             'item_states': ['accepted'],
             'label': 'Power observers',
             'meeting_access_on': '',
             'meeting_states': ['closed'],
             'row_id': 'powerobservers'}])
        self.changeUser('pmManager')
        item1 = self.create('MeetingItem')
        item1.setDecision(self.decisionText)
        item2 = self.create('MeetingItem', decision=self.decisionText)
        item2.setDecision(self.decisionText)
        meeting = self.create('Meeting', date=DateTime('2019/09/10'))
        self.presentItem(item1)
        self.presentItem(item2)
        self.decideMeeting(meeting)
        self.do(item1, 'accept')
        self.assertEqual(item1.queryState(), 'accepted')
        # power observer does not have access to item1/item2
        self.changeUser('powerobserver1')
        self.assertFalse(self.hasPermission(View, item1))
        self.assertFalse(self.hasPermission(View, item2))
        self.changeUser('pmManager')
        self.closeMeeting(meeting)
        # items are accepted
        self.assertEqual(item1.queryState(), 'accepted')
        self.assertEqual(item2.queryState(), 'accepted')
        # and powerobserver has also access to item1 that was already accepted before meeting was closed
        self.assertTrue(self.hasPermission(View, item1))
        self.assertTrue(self.hasPermission(View, item2))


    def test_pm_MeetingExecuteActionOnLinkedItemsCaseTALExpression(self):
        '''Test the MeetingConfig.onMeetingTransitionItemActionToExecute parameter :
           executing a TAL expression on every items.'''
        # when we freeze a meeting, we will append word '(frozen)' to the item title
        # first, wrong tal_expression, nothing is done
        self.changeUser('siteadmin')
        cfg = self.meetingConfig
        cfg.setOnMeetingTransitionItemActionToExecute(
            [{'meeting_transition': 'freeze',
              'item_action': EXECUTE_EXPR_VALUE,
              'tal_expression': 'item/unknown'},
             {'meeting_transition': 'freeze',
              'item_action': 'itemValidateByDG',
              'tal_expression': ''},
             {'meeting_transition': 'freeze',
              'item_action': 'itemfreeze',
              'tal_expression': ''}, ])
        self.changeUser('pmManager')
        # create a meeting with items
        meeting = self._createMeetingWithItems()
        # for now, every items are 'presented'
        for item in meeting.getItems():
            self.assertEqual(item.queryState(), 'presented')
        # freeze the meeting, nothing is done by the expression and the items are frozen
        self.freezeMeeting(meeting)
        for item in meeting.getItems():
            self.assertEqual(item.queryState(), 'itemfrozen')

        # now a valid config, append ('accepted') to item title when meeting is decided
        title_suffix = " (accepted)"
        cfg.setOnMeetingTransitionItemActionToExecute(
            [{'meeting_transition': 'decide',
              'item_action': EXECUTE_EXPR_VALUE,
              'tal_expression': 'python: item.setTitle(item.Title() + "{0}")'.format(title_suffix)},
             {'meeting_transition': 'decide',
              'item_action': 'accept',
              'tal_expression': ''}])
        for item in meeting.getItems():
            self.assertFalse(title_suffix in item.Title())
        self.decideMeeting(meeting)
        for item in meeting.getItems():
            self.assertTrue(title_suffix in item.Title())
            self.assertEqual(item.queryState(), 'accepted')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflows, prefix='test_pm_'))
    return suite
