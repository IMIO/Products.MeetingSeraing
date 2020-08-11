# -*- coding: utf-8 -*-
#
# File: testColumns.py
#
# Copyright (c) 2016 by Imio.be
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

from collective.iconifiedcategory.interfaces import IIconifiedCategorySettings
from DateTime import DateTime
from plone import api
from Products.MeetingCommunes.tests.testColumns import testColumns as mctc
from Products.MeetingSeraing.tests.MeetingSeraingTestCase import MeetingSeraingTestCase
from Products.PloneMeeting.columns import PMAnnexActionsColumn
from Products.PloneMeeting.config import AddAnnex
from Products.PloneMeeting.config import AddAnnexDecision


class testColumns(MeetingSeraingTestCase, mctc):
    ''' '''

    def test_pm_AnnexActionsColumnShowArrows(self):
        """Arrows are only shown if annex or annexDecision are orderable.
           Only displayed on annexDecisions if only annexDecision addable and no more annex addable."""
        # avoid adding recurring items to created meeting
        self._removeConfigObjectsFor(self.meetingConfig, folders=['recurringitems'])

        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        item.setDecision('<p>Decision text</p>')
        annex1 = self.addAnnex(item)
        annex2 = self.addAnnex(item)

        annex1_brain = self.portal.portal_catalog(UID=annex1.UID())[0]
        annex2_brain = self.portal.portal_catalog(UID=annex2.UID())[0]
        meetingFolder = self.getMeetingFolder()
        faceted_table = meetingFolder.restrictedTraverse('faceted-table-view')
        column = PMAnnexActionsColumn(meetingFolder, self.portal.REQUEST, faceted_table)
        renderedColumnAnnex1 = column.renderCell(annex1_brain)
        renderedColumnAnnex2 = column.renderCell(annex2_brain)
        self.assertTrue(self.hasPermission(AddAnnex, item))
        # sort_categorized_tab must be False to show arrows
        sort_categorized_tab = api.portal.get_registry_record(
            'sort_categorized_tab',
            interface=IIconifiedCategorySettings,
        )
        self.assertTrue(sort_categorized_tab)
        self.assertFalse('folder_position_typeaware?position=down' in renderedColumnAnnex1)
        self.assertFalse('folder_position_typeaware?position=up' in renderedColumnAnnex2)
        api.portal.set_registry_record('sort_categorized_tab',
                                       False,
                                       interface=IIconifiedCategorySettings)
        renderedColumnAnnex1 = column.renderCell(annex1_brain)
        renderedColumnAnnex2 = column.renderCell(annex2_brain)
        self.assertTrue('folder_position_typeaware?position=down' in renderedColumnAnnex1)
        self.assertTrue('folder_position_typeaware?position=up' in renderedColumnAnnex2)

        # now test when both annex and annexDecision may be added
        self.validateItem(item)
        self.assertTrue(self.hasPermission(AddAnnex, item))
        self.assertTrue(self.hasPermission(AddAnnexDecision, item))
        annexDecision1 = self.addAnnex(item, relatedTo='item_decision')
        annexDecision2 = self.addAnnex(item, relatedTo='item_decision')
        annexDecision1_brain = self.portal.portal_catalog(UID=annexDecision1.UID())[0]
        annexDecision2_brain = self.portal.portal_catalog(UID=annexDecision2.UID())[0]
        renderedColumnAnnex1 = column.renderCell(annex1_brain)
        renderedColumnAnnex2 = column.renderCell(annex2_brain)
        renderedColumnDecisionAnnex1 = column.renderCell(annexDecision1_brain)
        renderedColumnDecisionAnnex2 = column.renderCell(annexDecision2_brain)
        self.assertTrue('folder_position_typeaware?position=down' in renderedColumnAnnex1)
        self.assertTrue('folder_position_typeaware?position=up' in renderedColumnAnnex2)
        self.assertTrue('folder_position_typeaware?position=down' in renderedColumnDecisionAnnex1)
        self.assertTrue('folder_position_typeaware?position=up' in renderedColumnDecisionAnnex2)
        # and it works
        item.folder_position_typeaware(position='down', id=annex1.getId())
        item.folder_position_typeaware(position='up', id=annex2.getId())
        item.folder_position_typeaware(position='down', id=annexDecision1.getId())
        item.folder_position_typeaware(position='up', id=annexDecision2.getId())

        # now when only annexDecision are addable
        meeting = self.create('Meeting', date=DateTime('2016/06/06'))
        self.presentItem(item)
        self.closeMeeting(meeting)
        self.assertFalse(self.hasPermission(AddAnnex, item))
        self.assertFalse(self.hasPermission(AddAnnexDecision, item))
        renderedColumnAnnex1 = column.renderCell(annex1_brain)
        renderedColumnAnnex2 = column.renderCell(annex2_brain)
        renderedColumnDecisionAnnex1 = column.renderCell(annexDecision1_brain)
        renderedColumnDecisionAnnex2 = column.renderCell(annexDecision2_brain)
        self.assertFalse('folder_position_typeaware?position=down' in renderedColumnAnnex1)
        self.assertFalse('folder_position_typeaware?position=up' in renderedColumnAnnex2)
        self.assertFalse('folder_position_typeaware?position=up' in renderedColumnDecisionAnnex1)
        self.assertFalse('folder_position_typeaware?position=down' in renderedColumnDecisionAnnex2)
        # and it works
        item.folder_position_typeaware(position='up', id=annexDecision1.getId())
        item.folder_position_typeaware(position='down', id=annexDecision2.getId())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testColumns, prefix='test_pm_'))
    return suite
