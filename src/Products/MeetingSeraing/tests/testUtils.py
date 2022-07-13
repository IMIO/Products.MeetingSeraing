# -*- coding: utf-8 -*-
#
# File: testUtils.py
#
# Copyright (c) 2017 by Imio.be
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

from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import View
from Products.PloneMeeting.utils import sendMailIfRelevant

from Products.MeetingCommunes.tests.testUtils import testUtils as mctu
from Products.MeetingSeraing.tests.MeetingSeraingTestCase import MeetingSeraingTestCase


class testUtils(MeetingSeraingTestCase, mctu):
    ''' '''
    def test_pm_SendMailIfRelevantIsPermission(self):
        """ """
        cfg = self.meetingConfig
        cfg.setMailMode("activated")
        cfg.setMailItemEvents(("item_state_changed_validate", ))

        self.changeUser('pmManager')
        item = self.create("MeetingItem", title="My item")
        params = {"obj": item,
                  "event": "item_state_changed_validate",
                  "value": View,
                  "isPermission": True,
                  "debug": True}

        recipients, subject, body = sendMailIfRelevant(**params)
        # not sent to action triggerer
        self.assertEqual(sorted(recipients),
                         [u'M. Budget Impact Editor <budgetimpacteditor@plonemeeting.org>',
                          u'M. PMCreator One <pmcreator1@plonemeeting.org>',
                          u'M. PMCreator One bee <pmcreator1b@plonemeeting.org>',
                          u'M. PMObserver One <pmobserver1@plonemeeting.org>',
                          u'M. PMReviewer One <pmreviewer1@plonemeeting.org>',
                          u'M. Power Observer1 <powerobserver1@plonemeeting.org>',
                          u'Site administrator <siteadmin@plonemeeting.org>'])
        # check for editors
        params["value"] = ModifyPortalContent
        recipients, subject, body = sendMailIfRelevant(**params)
        self.assertEqual(sorted(recipients),  # XXX Specific MeetingSeraing for super editors
                         [u'M. PMCreator One <pmcreator1@plonemeeting.org>',
                          u'M. PMCreator One bee <pmcreator1b@plonemeeting.org>',
                          u'Site administrator <siteadmin@plonemeeting.org>',
                          u'powerEditor1 <user@plonemeeting.org>'
                          ])

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testUtils, prefix='test_pm_'))
    return suite
