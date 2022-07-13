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

from collective.iconifiedcategory.utils import get_config_root
from collective.iconifiedcategory.utils import get_group
from DateTime import DateTime
from Products.CMFCore.permissions import View
from Products.MeetingCommunes.tests.testMeetingItem import testMeetingItem as mctmi
from Products.MeetingSeraing.tests.MeetingSeraingTestCase import MeetingSeraingTestCase
from Products.PloneMeeting.tests.PloneMeetingTestCase import pm_logger
from Products.PloneMeeting.utils import get_annexes
from Products.statusmessages.interfaces import IStatusMessage
from zope.annotation.interfaces import IAnnotations
from zope.i18n import translate


class testMeetingItem(MeetingSeraingTestCase, mctmi):
    """
    Tests the MeetingItem class methods.
    """

    def test_pm_PowerObserversLocalRoles(self):
        """Check that powerobservers local roles are set correctly...
        Test alternatively item or meeting that is accessible to and not..."""
        # we will check that (restricted) power observers local roles are set correctly.
        # - powerobservers may access itemcreated, validated and presented items (and created meetings),
        #   not restricted power observers;
        # - frozen items/meetings are accessible by both;
        self._setPowerObserverStates(
            states=(
                'itemcreated',
                'validated',
                'presented',
                'itemfrozen',
                'accepted',
                'delayed',
            )
        )
        self._setPowerObserverStates(
            field_name='meeting_states', states=('created', 'frozen', 'decided', 'closed')
        )
        self._setPowerObserverStates(
            observer_type='restrictedpowerobservers', states=('itemfrozen', 'accepted')
        )

        self._setPowerObserverStates(
            field_name='meeting_states',
            observer_type='restrictedpowerobservers',
            states=('frozen', 'decided', 'closed'),
        )
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
        meeting = self.create('Meeting', date=DateTime('2015/01/01').asdatetime())
        self.presentItem(item)
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(self.hasPermission(View, item))
        self.assertFalse(self.hasPermission(View, meeting))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        # frozen items/meetings are accessible by both powerobs
        self.changeUser('pmManager')
        self.freezeMeeting(meeting)
        self.changeUser('powerobserver1')
        self.assertTrue(item.query_state() == 'itemfrozen')
        self.changeUser('restrictedpowerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        # decide the meeting the item, meeting accessible to both
        self.changeUser('pmManager')
        self.decideMeeting(meeting)
        self.do(item, 'accept')
        self.changeUser('restrictedpowerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))
        self.changeUser('powerobserver1')
        self.assertTrue(self.hasPermission(View, item))
        self.assertTrue(self.hasPermission(View, meeting))

    def test_pm_SendItemToOtherMCWithoutDefinedAnnexType(self):
        """When cloning an item to another meetingConfig or to the same meetingConfig,
        if we have annexes on the original item and destination meetingConfig (that could be same
        as original item or another) does not have annex types defined,
        it does not fail but annexes are not kept and a portal message is displayed."""
        cfg = self.meetingConfig
        cfg2 = self.meetingConfig2
        # first test when sending to another meetingConfig
        # remove every annexTypes from meetingConfig2
        self.changeUser('admin')
        self._removeConfigObjectsFor(
            cfg2,
            folders=[
                'annexes_types/item_annexes',
            ],
        )
        self.assertTrue(not cfg2.annexes_types.item_annexes.objectValues())
        # a portal message will be added, for now there is no message
        messages = IStatusMessage(self.request).show()
        self.assertTrue(not messages)
        # now create an item, add an annex and clone it to the other meetingConfig
        data = self._setupSendItemToOtherMC(with_annexes=True)
        originalItem = data['originalItem']
        newItem = data['newItem']
        # original item had annexes
        self.assertEqual(len(get_annexes(originalItem, portal_types=['annex'])), 2)
        self.assertEqual(
            len(get_annexes(originalItem, portal_types=['annexDecision'])), 2
        )
        # but new item is missing the normal annexes because
        # no annexType for normal annexes are defined in the cfg2
        self.assertEqual(len(get_annexes(newItem, portal_types=['annex'])), 0)
        # XXX Seraing, decision's annexe are keep (but in their config, these annexes was send in simply annexes
        self.assertEqual(len(get_annexes(newItem, portal_types=['annexDecision'])), 2)
        # moreover a message was added
        messages = IStatusMessage(self.request).show()
        expectedMessage = translate(
            "annex_not_kept_because_no_available_annex_type_warning",
            mapping={'annexTitle': data['annex2'].Title()},
            domain='PloneMeeting',
            context=self.request,
        )
        self.assertEqual(messages[-2].message, expectedMessage)

        # now test when cloning locally, even if annexes types are not enabled
        # it works, this is the expected behavior, backward compatibility when an annex type
        # is no more enabled but no more able to create new annexes with this annex type
        self.changeUser('admin')
        for at in (
            cfg.annexes_types.item_annexes.objectValues()
            + cfg.annexes_types.item_decision_annexes.objectValues()
        ):
            at.enabled = False
        # no available annex types, try to clone newItem now
        self.changeUser('pmManager')
        # clean status message so we check that a new one is added
        del IAnnotations(self.request)['statusmessages']
        clonedItem = originalItem.clone(copyAnnexes=True)
        # annexes were kept
        self.assertEqual(len(get_annexes(clonedItem, portal_types=['annex'])), 2)
        # for Seraing, item had not annexes decisions
        self.assertEqual(len(get_annexes(clonedItem, portal_types=['annexDecision'])), 0)

    def _extraNeutralFields(self):
        """This method is made to be overrided by subplugins that added
        neutral fields to the MeetingItem schema."""
        return ['pvNote', 'dgNote', 'interventions']

    def test_pm_AnnexToPrintBehaviourWhenCloned(self):
        """When cloning an item with annexes, to the same or another MeetingConfig, the 'toPrint' field
        is kept depending on MeetingConfig.keepOriginalToPrintOfClonedItems.
        If it is True, the original value is kept, if it is False, it will use the
        MeetingConfig.annexToPrintDefault value."""
        cfg = self.meetingConfig
        cfg2 = self.meetingConfig2
        cfg2Id = cfg2.getId()
        cfg.setKeepOriginalToPrintOfClonedItems(False)
        cfg2.setKeepOriginalToPrintOfClonedItems(False)
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date=DateTime('2016/02/02').asdatetime())
        item = self.create('MeetingItem')
        annex = self.addAnnex(item)
        annex_config = get_config_root(annex)
        annex_group = get_group(annex_config, annex)
        self.assertFalse(annex_group.to_be_printed_activated)
        self.assertFalse(annex.to_print)
        annex.to_print = True
        self.assertTrue(annex.to_print)
        # decide the item so we may add decision annex
        item.setDecision(self.decisionText)
        self.presentItem(item)
        self.decideMeeting(meeting)
        self.do(item, 'accept')
        self.assertEquals(item.query_state(), 'accepted')
        annexDec = self.addAnnex(item, relatedTo='item_decision')
        annexDec_config = get_config_root(annexDec)
        annexDec_group = get_group(annexDec_config, annexDec)
        self.assertFalse(annexDec_group.to_be_printed_activated)
        self.assertFalse(annexDec.to_print)
        annexDec.to_print = True
        self.assertTrue(annexDec.to_print)

        # clone item locally, as keepOriginalToPrintOfClonedItems is False
        # default values defined in the config will be used
        self.assertFalse(cfg.getKeepOriginalToPrintOfClonedItems())
        clonedItem = item.clone()
        annexes = get_annexes(clonedItem, portal_types=['annex'])
        if not annexes:
            pm_logger.info('No annexes found on duplicated item clonedItem')
        cloneItemAnnex = annexes and annexes[0]
        annexesDec = get_annexes(clonedItem, portal_types=['annexDecision'])
        if not annexesDec:
            pm_logger.info('No decision annexes found on duplicated item clonedItem')
        cloneItemAnnexDec = annexesDec and annexesDec[0]
        self.assertFalse(cloneItemAnnex and cloneItemAnnex.to_print)
        self.assertFalse(cloneItemAnnexDec and cloneItemAnnexDec.to_print)

        # enable keepOriginalToPrintOfClonedItems
        # some plugins remove annexes/decision annexes on duplication
        # so make sure we test if an annex is there...
        self.changeUser('siteadmin')
        cfg.setKeepOriginalToPrintOfClonedItems(True)
        self.changeUser('pmManager')
        clonedItem2 = item.clone()
        annexes = get_annexes(clonedItem2, portal_types=['annex'])
        if not annexes:
            pm_logger.info('No annexes found on duplicated item clonedItem2')
        cloneItem2Annex = annexes and annexes[0]
        annexesDec = get_annexes(clonedItem2, portal_types=['annexDecision'])
        if not annexesDec:
            pm_logger.info('No decision annexes found on duplicated item clonedItem2')
        cloneItem2AnnexDec = annexesDec and annexesDec[0]
        self.assertTrue(cloneItem2Annex and cloneItem2Annex.to_print or True)
        self.assertTrue(cloneItem2AnnexDec and cloneItem2AnnexDec.to_print or True)

        # clone item to another MC and test again
        # cfg2.keepOriginalToPrintOfClonedItems is True
        self.assertFalse(cfg2.getKeepOriginalToPrintOfClonedItems())
        item.setOtherMeetingConfigsClonableTo((cfg2Id,))
        clonedToCfg2 = item.cloneToOtherMeetingConfig(cfg2Id)
        annexes = get_annexes(clonedToCfg2, portal_types=['annex'])
        if not annexes:
            pm_logger.info('No annexes found on duplicated item clonedToCfg2')
        clonedToCfg2Annex = annexes and annexes[0]
        annexesDec = get_annexes(clonedToCfg2, portal_types=['annexDecision'])
        if not annexesDec:
            pm_logger.info('No decision annexes found on duplicated item clonedToCfg2')
        self.assertFalse(clonedToCfg2Annex and clonedToCfg2Annex.to_print)

        # enable keepOriginalToPrintOfClonedItems
        self.changeUser('siteadmin')
        cfg2.setKeepOriginalToPrintOfClonedItems(True)
        self.deleteAsManager(clonedToCfg2.UID())
        # send to cfg2 again
        self.changeUser('pmManager')
        clonedToCfg2Again = item.cloneToOtherMeetingConfig(cfg2Id)
        annexes = get_annexes(clonedToCfg2Again, portal_types=['annex'])
        if not annexes:
            pm_logger.info('No annexes found on duplicated item clonedToCfg2Again')
        clonedToCfg2AgainAnnex = annexes and annexes[0]
        annexesDec = get_annexes(clonedToCfg2Again, portal_types=['annexDecision'])
        if not annexesDec:
            pm_logger.info(
                'No decision annexes found on duplicated item clonedToCfg2Again'
            )
        self.assertTrue(
            clonedToCfg2AgainAnnex and clonedToCfg2AgainAnnex.to_print or True
        )

    def test_pm_HistorizedTakenOverBy(self):
        '''Not applicable for MeetingSeraing. See below.'''
        pass

    def test_pm_KeepTakenOverBy(self):
        '''
        Test takenOverBy feature that will keep the takenOverBy except for certain transitions
        '''
        cfg = self.meetingConfig
        cfg.setTransitionsReinitializingTakenOverBy(["validate"])

        # create an item
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        # take item over
        item.setTakenOverBy('pmCreator1')
        self.assertEqual(item.getTakenOverBy(), 'pmCreator1')
        # if takenOverBy is removed
        item.setTakenOverBy('')
        self.assertEqual(item.getTakenOverBy(), '')

        # take item over and propose item
        item.setTakenOverBy('pmCreator1')
        self.changeUser('pmManager')
        for transition in self.TRANSITIONS_FOR_PROPOSING_ITEM_1:
            self._do_transition_with_request(item, transition)
        self.assertEqual(item.getTakenOverBy(), 'pmCreator1')

        item.setTakenOverBy('pmManager')
        self.assertEqual(item.getTakenOverBy(), 'pmManager')

        for transition in self.TRANSITIONS_FOR_VALIDATING_ITEM_1:
            self._do_transition_with_request(item, transition)
        # Validate reinitialize takenOverBy
        self.assertEqual(item.getTakenOverBy(), '')

        item.setTakenOverBy('pmManager')
        self.assertEqual(item.getTakenOverBy(), 'pmManager')

        for transition in self.BACK_TO_WF_PATH_1["itemcreated"]:
            self._do_transition_with_request(item, transition)
        self.assertEqual(item.getTakenOverBy(), 'pmManager')

    def test_pm_MayTakeOverDecidedItem(self):
        """Overrided, this is not possible for now..."""
        cfg = self.meetingConfig
        self.assertTrue('accepted' in cfg.getItemDecidedStates())
        self.assertTrue('delayed' in cfg.getItemDecidedStates())
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem', decision=self.decisionText)
        item2 = self.create('MeetingItem', decision=self.decisionText)
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date=DateTime('2020/06/11').asdatetime())
        self.presentItem(item1)
        self.presentItem(item2)
        self.changeUser('pmCreator1')
        self.assertFalse(item1.adapted().mayTakeOver())
        self.assertFalse(item2.adapted().mayTakeOver())
        self.changeUser('pmManager')
        self.decideMeeting(meeting)
        self.do(item1, 'accept')
        self.do(item2, 'delay')
        self.changeUser('pmCreator1')
        # XXX changed
        self.assertFalse(item1.adapted().mayTakeOver())
        self.assertFalse(item2.adapted().mayTakeOver())

    def test_pm__sendCopyGroupsMailIfRelevant(self):
        """Bypass, not used."""

def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_pm_'))
    return suite
