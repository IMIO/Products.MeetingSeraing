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

def test_suite():
    from unittest import TestSuite, makeSuite

    suite = TestSuite()
    suite.addTest(makeSuite(testColumns, prefix='test_pm_'))
    return suite
