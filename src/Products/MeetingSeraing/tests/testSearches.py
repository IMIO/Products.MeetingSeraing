# -*- coding: utf-8 -*-
#
# File: testMeetingConfig.py
#
# Copyright (c) 2015 by Imio.be
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

from collective.compoundcriterion.interfaces import ICompoundCriterionFilter
from Products.MeetingCommunes.tests.testSearches import testSearches as mcts
from Products.MeetingSeraing.tests.MeetingSeraingTestCase import MeetingSeraingTestCase
from zope.component import getAdapter


class testSearches(MeetingSeraingTestCase, mcts):
    """Test searches."""

    def test_pm_SearchItemsToCorrectToValidateHighestHierarchicLevel(self):
        '''Not used yet...'''
        pass

    def test_pm_SearchItemsToCorrectToValidateOfEveryReviewerGroups(self):
        '''Not used yet...'''
        pass

    def test_pm_SearchMyItemsTakenOver(self):
        '''Test the 'search-my-items-taken-over' method.  This should return
           a list of items a user has taken over.'''
        self.changeUser('admin')
        # specify that copyGroups can see the item when it is proposed
        cfg = self.meetingConfig
        cfg.setUseCopies(True)
        cfg.setItemCopyGroupsStates((self._stateMappingFor('proposed'), 'validated', ))

        itemTypeName = cfg.getItemTypeName()

        # first test the generated query
        adapter = getAdapter(cfg,
                             ICompoundCriterionFilter,
                             name='my-items-taken-over')
        # query is correct
        self.changeUser('pmManager')
        self.assertEqual(adapter.query,
                         {'portal_type': {'query': itemTypeName},
                          'getTakenOverBy': {'query': 'pmManager'}})

        # now do the query
        # this adapter is used by the "searchmyitemstakenover"
        collection = cfg.searches.searches_items.searchmyitemstakenover
        item = self.create('MeetingItem')
        # by default nothing is returned
        self.failIf(collection.results())
        # now take item over
        item.setTakenOverBy(self.member.getId())
        item.reindexObject(idxs=['getTakenOverBy', ])
        # now it is returned
        self.failUnless(collection.results())
        self.proposeItem(item)
        self.assertTrue(self.member.getId() in item.takenOverByInfos.values())
        self.failUnless(collection.results())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSearches, prefix='test_pm_'))
    return suite
