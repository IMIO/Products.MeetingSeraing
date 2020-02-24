# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 by Imio.be
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
from Products.MeetingCommunes.tests.helpers import MeetingCommunesTestingHelpers


class MeetingSeraingTestingHelpers(MeetingCommunesTestingHelpers):
    """Override some values of PloneMeetingTestingHelpers."""

    TRANSITIONS_FOR_PROPOSING_ITEM_1 = TRANSITIONS_FOR_PROPOSING_ITEM_2 = ('proposeToServiceHead',
                                                                           'proposeToOfficeManager',
                                                                           'proposeToDivisionHead',
                                                                           'propose', )
    TRANSITIONS_FOR_VALIDATING_ITEM_1 = TRANSITIONS_FOR_VALIDATING_ITEM_2 = ('proposeToServiceHead',
                                                                             'proposeToOfficeManager',
                                                                             'proposeToDivisionHead',
                                                                             'propose',
                                                                             'validate', )
    TRANSITIONS_FOR_PRESENTING_ITEM_1 = TRANSITIONS_FOR_PRESENTING_ITEM_2 = ('proposeToServiceHead',
                                                                             'proposeToOfficeManager',
                                                                             'proposeToDivisionHead',
                                                                             'propose',
                                                                             'validate',
                                                                             'present', )

    TRANSITIONS_FOR_ACCEPTING_ITEMS_MEETING_1 = TRANSITIONS_FOR_ACCEPTING_ITEMS_MEETING_2 = ('validateByDG', 'freeze',
                                                                                             'decide', )
    TRANSITIONS_FOR_FREEZING_MEETING_1 = TRANSITIONS_FOR_FREEZING_MEETING_2 = ('validateByDG', 'freeze', )
    TRANSITIONS_FOR_PUBLISHING_MEETING_1 = TRANSITIONS_FOR_PUBLISHING_MEETING_2 = ('validateByDG', 'freeze', )
    TRANSITIONS_FOR_DECIDING_MEETING_1 = TRANSITIONS_FOR_DECIDING_MEETING_2 = ('validateByDG', 'freeze', 'decide', )
    TRANSITIONS_FOR_CLOSING_MEETING_1 = TRANSITIONS_FOR_CLOSING_MEETING_2 = ('validateByDG', 'freeze', 'decide',
                                                                             'close', )
    BACK_TO_WF_PATH_1 = BACK_TO_WF_PATH_2 = {
        # Meeting
        'created': ('backToDecided',
                    'backToFrozen',
                    'backToValidatedByDG',
                    'backToCreated',),
        # MeetingItem
        'itemcreated': ('backToItemFrozen',
                        'backToItemValidatedByDG',
                        'backToPresented',
                        'backToValidated',
                        'backToProposed',
                        'backToProposedToDivisionHead',
                        'backToProposedToOfficeManager',
                        'backToProposedToServiceHead',
                        'backToItemCreated'),
        'proposed': ('backToItemFrozen',
                     'backToItemValidatedByDG',
                     'backToPresented',
                     'backToValidated',
                     'backToProposed', ),
        'validated': ('backToItemFrozen',
                      'backToItemValidatedByDG',
                      'backToPresented',
                      'backToValidated', ),
        'presented': ('backToItemFrozen',
                      'backToItemValidatedByDG',
                      'backToPresented', )}

    WF_STATE_NAME_MAPPINGS = {'itemcreated': 'itemcreated',
                              'proposed': 'proposed',
                              'validated': 'validated',
                              'presented': 'presented',
                              'itemfrozen': 'itemfrozen'}

    # in which state an item must be after a particular meeting transition?
    ITEM_WF_STATE_AFTER_MEETING_TRANSITION = {'close': 'accepted_closed', }
