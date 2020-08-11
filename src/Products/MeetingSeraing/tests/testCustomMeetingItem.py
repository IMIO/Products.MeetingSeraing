# -*- coding: utf-8 -*-
#
# File: testCustomMeetingItem.py
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

from DateTime import DateTime
from Products.MeetingCommunes.tests.testCustomMeetingItem import testCustomMeetingItem as mctcmi
from Products.MeetingSeraing.tests.MeetingSeraingTestCase import MeetingSeraingTestCase
from zope.annotation import IAnnotations


class testCustomMeetingItem(MeetingSeraingTestCase, mctcmi):
    """
        Tests the MeetingItem adapted methods
    """
    def test_onDuplicated(self):
        """
          When a college item is duplicated to the council meetingConfig,
          some fields must be cleaning (fields linked to the real meeting)
        """
        # by default, college items are sendable to council
        destMeetingConfigId = self.meetingConfig2.getId()
        self.assertTrue(self.meetingConfig.getMeetingConfigsToCloneTo() == (
            {'meeting_config': '%s' % destMeetingConfigId,
             'trigger_workflow_transitions_until': '__nothing__'},))
        # create an item in college, set a motivation, send it to council and check
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        item.setDecision('<p>A decision</p>')
        item.setDescription('<p>Lorem ipsum dolor sit amet <span class="highlight-purple">consectetur adipiscing '
                            'elit</span>. Nulla fermentum diam vel justo tincidunt aliquam.</p>')
        item.setPvNote('<p>A PV Note</p>')
        item.setDgNote('<p>A DG Note</p>')
        item.setObservations('<p>An intervention during meeting</p>')
        item.setOtherMeetingConfigsClonableTo((destMeetingConfigId,))
        meeting = self.create('Meeting', date=DateTime('2013/05/05'))
        self.presentItem(item)
        # now close the meeting so the item is automatically accepted and sent to meetingConfig2
        self.closeMeeting(meeting)
        cfg = self.meetingConfig

        self.assertTrue(item.queryState() in cfg.getItemAutoSentToOtherMCStates())
        self.assertTrue(item._checkAlreadyClonedToOtherMC(destMeetingConfigId))
        # get the item that was sent to meetingConfig2 and check his motivation field
        annotation_key = item._getSentToOtherMCAnnotationKey(destMeetingConfigId)
        newItem = self.portal.uid_catalog(UID=IAnnotations(item)[annotation_key])[0].getObject()
        self.assertTrue(newItem.getPvNote() == '')
        self.assertTrue(newItem.getDgNote() == '')
        self.assertTrue(newItem.getObservations() == '')
        self.assertTrue(newItem.Description() == '<p>Lorem ipsum dolor sit amet . Nulla fermentum diam vel '
                        'justo tincidunt aliquam.</p>')

    def test_powerEditor(self):
        """
           The power editor can modified frozen items
        """
        # create an item and a meeting and check locals roles
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        self.changeUser('powerEditor1')
        self.failIf(self.hasPermission('Modify portal content', item))
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date=DateTime('2013/05/05'))
        self.presentItem(item)
        self.failUnless(self.hasPermission('Modify portal content', item))
        self.do(meeting, 'validateByDG')
        self.changeUser('powerEditor1')
        self.failUnless(self.hasPermission('Modify portal content', item))
        self.changeUser('pmManager')
        self.do(meeting, 'freeze')
        self.changeUser('powerEditor1')
        self.failUnless(self.hasPermission('Modify portal content', item))
        self.closeMeeting(meeting)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomMeetingItem, prefix='test_'))
    return suite
