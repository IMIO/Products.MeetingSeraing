# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
# File: adapters.py
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
# ------------------------------------------------------------------------------
from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from appy.gen import No
from collections import OrderedDict
from DateTime import DateTime
from Globals import InitializeClass
from zope.interface import implements
from zope.i18n import translate

from Products.CMFCore.permissions import DeleteObjects
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import DisplayList
from plone import api

from imio.helpers.xhtml import xhtmlContentIsEmpty
from Products.PloneMeeting.adapters import ItemPrettyLinkAdapter
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItem
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.PloneMeeting.interfaces import IMeetingGroupCustom
from Products.PloneMeeting.interfaces import IMeetingConfigCustom
from Products.PloneMeeting.interfaces import IToolPloneMeetingCustom
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.Meeting import MeetingWorkflowActions
from Products.PloneMeeting.Meeting import MeetingWorkflowConditions
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingGroup import MeetingGroup
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowActions
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowConditions
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.model.adaptations import WF_APPLIED
from Products.PloneMeeting.ToolPloneMeeting import ToolPloneMeeting
from Products.MeetingSeraing import logger
from Products.MeetingSeraing.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingSeraingWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingSeraingWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCollegeWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCollegeWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCollegeWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCollegeWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCouncilWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCouncilWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCouncilWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCouncilWorkflowActions
from Products.MeetingSeraing.config import EDITOR_USECASES
from Products.MeetingSeraing.config import POWEREDITORS_GROUP_SUFFIX


# disable most of wfAdaptations
customWfAdaptations = ('return_to_proposing_group', 'returned_to_advise')
MeetingConfig.wfAdaptations = customWfAdaptations
originalPerformWorkflowAdaptations = adaptations.performWorkflowAdaptations

# configure parameters for the returned_to_proposing_group wfAdaptation
# we keep also 'itemfrozen' and 'itempublished' in case this should be activated for meeting-config-college...

CUSTOM_RETURN_TO_PROPOSING_GROUP_MAPPINGS = {'backTo_presented_from_returned_to_proposing_group':
                                             ['created', ],
                                             'backTo_validated_by_dg_from_returned_to_proposing_group':
                                             ['validated_by_dg', ],
                                             'backTo_itemfrozen_from_returned_to_proposing_group':
                                             ['frozen', 'decided', 'decisions_published', ],
                                             'backTo_presented_from_returned_to_advise':
                                             ['created', ],
                                             'backTo_validated_by_dg_from_returned_to_advise':
                                             ['validated_by_dg', ],
                                             'backTo_itemfrozen_from_returned_to_advise':
                                             ['frozen', 'decided', 'decisions_published', ],
                                             'backTo_returned_to_proposing_group_from_returned_to_advise':
                                             ['created', 'validated_by_dg', 'frozen', 'decided',
                                              'decisions_published', ],
                                             'NO_MORE_RETURNABLE_STATES': ['closed', 'archived', ]
                                             }
adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS = CUSTOM_RETURN_TO_PROPOSING_GROUP_MAPPINGS

RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'validated_by_dg', 'itemfrozen', )
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES
RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {'meetingitemseraing_workflow':
    # view permissions
    {'Access contents information':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'View':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read budget infos':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read decision':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read item observations':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    # edit permissions
    'Modify portal content':
    ('Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Write budget infos':
    ('Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', 'MeetingBudgetImpactEditor', ),
    'PloneMeeting: Write decision':
    ('Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ),
    'Review portal content':
    ('Manager', 'MeetingReviewer', 'MeetingManager', ),
    'Add portal content':
    ('Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Add annex':
    ('Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Add annexDecision':
    ('Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ),
    # MeetingManagers edit permissions
     'PloneMeeting: Write marginal notes':
     ('Manager',),
     'PloneMeeting: Write item MeetingManager reserved fields':
     ('Manager', 'MeetingManager',),
    'Delete objects':
    ('Manager', 'MeetingManager', ), }
}
adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS

RETURN_TO_ADVISE_CUSTOM_PERMISSIONS = {'meetingitemseraing_workflow':
    # view permissions
    {'Access contents information':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'View':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read budget infos':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read decision':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read item observations':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    # edit permissions
    'Modify portal content':
    ('Manager', 'MeetingManager', ),
    'PloneMeeting: Write budget infos':
    ('Manager', 'MeetingManager', 'MeetingBudgetImpactEditor'),
    'PloneMeeting: Write decision':
    ('Manager', 'MeetingManager', ),
    'Review portal content':
    ('Manager', 'MeetingReviewer', 'MeetingManager', ),
    'Add portal content':
    ('Manager', 'MeetingManager', ),
    'PloneMeeting: Add annex':
    ('Manager', 'MeetingManager', ),
    'PloneMeeting: Add annexDecision':
    ('Manager',  'MeetingManager', ),
    # MeetingManagers edit permissions
     'PloneMeeting: Write marginal notes':
    ('Manager',),
     'PloneMeeting: Write item MeetingManager reserved fields':
     ('Manager', 'MeetingManager',),
    'Delete objects':
    ('Manager', 'MeetingManager', ), }
}

RETURN_TO_PROPOSING_GROUP_CUSTOM_STATE_TO_CLONE = {'meetingitemseraing_workflow':
                                                       'meetingitemseraing_workflow.itemcreated'}
adaptations.RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = RETURN_TO_PROPOSING_GROUP_CUSTOM_STATE_TO_CLONE


class CustomMeeting(Meeting):
    """Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom."""

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePublic('isDecided')

    def isDecided(self):
        """
          The meeting is supposed 'decided', if at least in state :
          - 'in_council' for MeetingCouncil
          - 'decided' for MeetingCollege
        """
        meeting = self.getSelf()
        return meeting.queryState() in ('in_council', 'decided', 'closed', 'archived')

    # Implements here methods that will be used by templates
    security.declarePublic('getPrintableItems')

    def getPrintableItems(self, itemUids, listTypes=['normal'], ignore_review_states=[],
                          privacy='*', oralQuestion='both', categories=[],
                          excludedCategories=[], groupIds=[], excludedGroupIds=[],
                          firstNumber=1, renumber=False):
        """Returns a list of items.
           An extra list of review states to ignore can be defined.
           A privacy can also be given, and the fact that the item is an
           oralQuestion or not (or both).
           Some specific categories can be given or some categories to exchude.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be returned with first element the number and second element, the item.
           In this case, the firstNumber value can be used."""
        # We just filter ignore_review_states here and privacy and call
        # getItems(uids), passing the correct uids and removing empty uids.
        # privacy can be '*' or 'public' or 'secret' or 'public_heading' or 'secret_heading'
        # oralQuestion can be 'both' or False or True
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)

        # check filters
        filteredItemUids = []
        uid_catalog = self.context.uid_catalog
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if obj.queryState() in ignore_review_states:
                continue
            elif not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (oralQuestion == 'both' or obj.getOralQuestion() == oralQuestion):
                continue
            elif categories and not obj.getCategory() in categories:
                continue
            elif groupIds and not obj.getProposingGroup() in groupIds:
                continue
            elif excludedCategories and obj.getCategory() in excludedCategories:
                continue
            elif excludedGroupIds and obj.getProposingGroup() in excludedGroupIds:
                continue
            filteredItemUids.append(itemUid)
        # in case we do not have anything, we return an empty list
        if not filteredItemUids:
            return []
        else:
            items = self.context.getItems(uids=filteredItemUids, listTypes=listTypes, ordered=True)
            if renumber:
                # returns a list of tuple with first element the number
                # and second element the item itself
                i = firstNumber
                res = []
                for item in items:
                    res.append((i, item))
                    i += 1
                items = res
            return items

    def _getAcronymPrefix(self, group, groupPrefixes):
        """This method returns the prefix of the p_group's acronym among all
           prefixes listed in p_groupPrefixes. If group acronym does not have a
           prefix listed in groupPrefixes, this method returns None."""
        res = None
        groupAcronym = group.getAcronym()
        for prefix in groupPrefixes.iterkeys():
            if groupAcronym.startswith(prefix):
                res = prefix
                break
        return res

    def _getGroupIndex(self, group, groups, groupPrefixes):
        """Is p_group among the list of p_groups? If p_group is not among
           p_groups but another group having the same prefix as p_group
           (the list of prefixes is given by p_groupPrefixes), we must conclude
           that p_group is among p_groups. res is -1 if p_group is not
           among p_group; else, the method returns the index of p_group in
           p_groups."""
        prefix = self._getAcronymPrefix(group, groupPrefixes)
        if not prefix:
            if group not in groups:
                return -1
            else:
                return groups.index(group)
        else:
            for gp in groups:
                if gp.getAcronym().startswith(prefix):
                    return groups.index(gp)
            return -1

    def _insertGroupInCategory(self, categoryList, meetingGroup, groupPrefixes, groups, item=None):
        """Inserts a group list corresponding to p_meetingGroup in the given
           p_categoryList, following meeting group order as defined in the
           main configuration (groups from the config are in p_groups).
           If p_item is specified, the item is appended to the group list."""
        usedGroups = [g[0] for g in categoryList[1:]]
        groupIndex = self._getGroupIndex(meetingGroup, usedGroups, groupPrefixes)
        if groupIndex == -1:
            # Insert the group among used groups at the right place.
            groupInserted = False
            i = -1
            for usedGroup in usedGroups:
                i += 1
                if groups.index(meetingGroup) < groups.index(usedGroup):
                    if item:
                        categoryList.insert(i + 1, [meetingGroup, item])
                    else:
                        categoryList.insert(i + 1, [meetingGroup])
                    groupInserted = True
                    break
            if not groupInserted:
                if item:
                    categoryList.append([meetingGroup, item])
                else:
                    categoryList.append([meetingGroup])
        else:
            # Insert the item into the existing group.
            if item:
                categoryList[groupIndex + 1].append(item)

    def _insertItemInCategory(self, categoryList, item, byProposingGroup, groupPrefixes, groups):
        """This method is used by the next one for inserting an item into the
           list of all items of a given category. if p_byProposingGroup is True,
           we must add it in a sub-list containing items of a given proposing
           group. Else, we simply append it to p_category."""
        if not byProposingGroup:
            categoryList.append(item)
        else:
            group = item.getProposingGroup(True)
            self._insertGroupInCategory(categoryList, group, groupPrefixes, groups, item)

    security.declarePublic('getPrintableItemsByCategory')

    def getPrintableItemsByCategory(self, itemUids=[], listTypes=['normal'],
                                    ignore_review_states=[], by_proposing_group=False, group_prefixes={},
                                    privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                                    excludedCategories=[], groupIds=[], excludedGroupIds=[],
                                    firstNumber=1, renumber=False, includeEmptyCategories=False,
                                    includeEmptyGroups=False, isToPrintInMeeting='both',
                                    forceCategOrderFromConfig=False, unrestricted=False):
        """Returns a list of (late or normal or both) items (depending on p_listTypes)
           ordered by category. Items being in a state whose name is in
           p_ignore_review_state will not be included in the result.
           If p_by_proposing_group is True, items are grouped by proposing group
           within every category. In this case, specifying p_group_prefixes will
           allow to consider all groups whose acronym starts with a prefix from
           this param prefix as a unique group. p_group_prefixes is a dict whose
           keys are prefixes and whose values are names of the logical big
           groups. A privacy,A toDiscuss, isToPrintInMeeting and oralQuestion can also be given, the item is a
           toDiscuss (oralQuestion) or not (or both) item.
           If p_forceCategOrderFromConfig is True, the categories order will be
           the one in the config and not the one from the meeting.
           If p_groupIds are given, we will only consider these proposingGroups.
           If p_includeEmptyCategories is True, categories for which no
           item is defined are included nevertheless. If p_includeEmptyGroups
           is True, proposing groups for which no item is defined are included
           nevertheless.Some specific categories can be given or some categories to exclude.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used."""
        # The result is a list of lists, where every inner list contains:
        # - at position 0: the category object (MeetingCategory or MeetingGroup)
        # - at position 1 to n: the items in this category
        # If by_proposing_group is True, the structure is more complex.
        # listTypes is a list that can be filled with 'normal' and/or 'late'
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        # privacy can be '*' or 'public' or 'secret'
        # Every inner list contains:
        # - at position 0: the category object
        # - at positions 1 to n: inner lists that contain:
        #   * at position 0: the proposing group object
        #   * at positions 1 to n: the items belonging to this group.
        # work only for groups...
        def _comp(v1, v2):
            if v1[0].getOrder(onlyActive=False) < v2[0].getOrder(onlyActive=False):
                return -1
            elif v1[0].getOrder(onlyActive=False) > v2[0].getOrder(onlyActive=False):
                return 1
            else:
                return 0
        res = []
        tool = getToolByName(self.context, 'portal_plonemeeting')
        # Retrieve the list of items
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)
        try:
             items = self.context.getItems(uids=itemUids, listTypes=listTypes, ordered=True, unrestricted=unrestricted)
        except Unauthorized:
            return res
        if by_proposing_group:
            groups = tool.getMeetingGroups()
        else:
            groups = None
        if items:
            for item in items:
                # Check if the review_state has to be taken into account
                if item.queryState() in ignore_review_states:
                    continue
                elif not (privacy == '*' or item.getPrivacy() == privacy):
                    continue
                elif not (oralQuestion == 'both' or item.getOralQuestion() == oralQuestion):
                    continue
                elif not (toDiscuss == 'both' or item.getToDiscuss() == toDiscuss):
                    continue
                elif groupIds and not item.getProposingGroup() in groupIds:
                    continue
                elif categories and not item.getCategory() in categories:
                    continue
                elif excludedCategories and item.getCategory() in excludedCategories:
                    continue
                elif excludedGroupIds and item.getProposingGroup() in excludedGroupIds:
                    continue
                elif not (isToPrintInMeeting == 'both' or item.getIsToPrintInMeeting() == isToPrintInMeeting):
                    continue
                currentCat = item.getCategory(theObject=True)
                # Add the item to a new category, excepted if the
                # category already exists.
                catExists = False
                catList = []
                for catList in res:
                    if catList[0] == currentCat:
                        catExists = True
                        break
                if catExists:
                    self._insertItemInCategory(catList, item,
                                               by_proposing_group, group_prefixes, groups)
                else:
                    res.append([currentCat])
                    self._insertItemInCategory(res[-1], item,
                                               by_proposing_group, group_prefixes, groups)
        if forceCategOrderFromConfig or cmp(listTypes.sort(), ['late', 'normal']) == 0:
            res.sort(cmp=_comp)
        if includeEmptyCategories:
            meetingConfig = tool.getMeetingConfig(
                self.context)
            # onlySelectable = False will also return disabled categories...
            allCategories = [cat for cat in meetingConfig.getCategories(onlySelectable=False)
                             if api.content.get_state(cat) == 'active']
            usedCategories = [elem[0] for elem in res]
            for cat in allCategories:
                if cat not in usedCategories:
                    # Insert the category among used categories at the right
                    # place.
                    categoryInserted = False
                    for i in range(len(usedCategories)):
                        if allCategories.index(cat) < \
                           allCategories.index(usedCategories[i]):
                            usedCategories.insert(i, cat)
                            res.insert(i, [cat])
                            categoryInserted = True
                            break
                    if not categoryInserted:
                        usedCategories.append(cat)
                        res.append([cat])
        if by_proposing_group and includeEmptyGroups:
            # Include, in every category list, not already used groups.
            # But first, compute "macro-groups": we will put one group for
            # every existing macro-group.
            macroGroups = []  # Contains only 1 group of every "macro-group"
            consumedPrefixes = []
            for group in groups:
                prefix = self._getAcronymPrefix(group, group_prefixes)
                if not prefix:
                    group._v_printableName = group.Title()
                    macroGroups.append(group)
                else:
                    if prefix not in consumedPrefixes:
                        consumedPrefixes.append(prefix)
                        group._v_printableName = group_prefixes[prefix]
                        macroGroups.append(group)
            # Every category must have one group from every macro-group
            for catInfo in res:
                for group in macroGroups:
                    self._insertGroupInCategory(catInfo, group, group_prefixes,
                                                groups)
                    # The method does nothing if the group (or another from the
                    # same macro-group) is already there.
        if renumber:
            # return a list of tuple with first element the number and second
            # element the item itself
            final_res = []
            for elts in res:
                final_items = [elts[0]]
                item_num = 1
                # we received a list of tuple (cat, items_list)
                for item in elts[1:]:
                    # we received a list of items
                    final_items.append((item_num, item))
                    item_num += 1
                final_res.append(final_items)
            res = final_res
        return res

    security.declarePublic('getAllItemsToPrintingOrNot')

    def getAllItemsToPrintingOrNot(self, uids=[], ordered=False, toPrint='True'):
        res = []
        items = self.context.getItems(uids)
        for item in items:
            if (toPrint and item.getIsToPrintInMeeting()) or not(toPrint or item.getIsToPrintInMeeting()):
                res.append(item)
        return res

    security.declarePublic('getOJByCategory')

    def getOJByCategory(self, itemUids=[], listTypes=['normal'],
                        ignore_review_states=[], by_proposing_group=False, group_prefixes={},
                        privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                        excludedCategories=[], groupIds=[], excludedGroupIds=[],
                        firstNumber=1, renumber=False, includeEmptyCategories=False,
                        includeEmptyGroups=False, isToPrintInMeeting='both',
                        forceCategOrderFromConfig=False, unrestricted=False):
        lists = self.context.getPrintableItemsByCategory(itemUids, listTypes, ignore_review_states, by_proposing_group,
                                                         group_prefixes, privacy, oralQuestion, toDiscuss, categories,
                                                         excludedCategories, groupIds, excludedGroupIds, firstNumber, renumber,
                                                         includeEmptyCategories, includeEmptyGroups,
                                                         isToPrintInMeeting, forceCategOrderFromConfig, unrestricted)
        res = []
        for sub_list in lists:
            # we use by categories, first element of each obj is a category
            final_res = [sub_list[0]]
            find_late = False
            for obj in sub_list[1:]:
                final_items = []
                # obj contain list like this [(num1, item1), (num2, item2), (num3, item3), (num4, item4)]
                for sub_obj in obj:
                    # separate normal items and late items
                    if not find_late and IMeetingItem.providedBy(sub_obj) and sub_obj.isLate():
                        final_items.append('late')
                        find_late = True
                    final_items.append(sub_obj)
                final_res.append(final_items)
            res.append(final_res)
        return res

    security.declarePublic('getNumberOfItems')

    def getNumberOfItems(self, itemUids, privacy='*', categories=[], listTypes=['normal']):
        """Returns the number of items depending on parameters.
           This is used in templates"""
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)
        if not categories and privacy == '*':
            return len(self.context.getItems(uids=itemUids, listTypes=listTypes))
        # Either, we will have to filter the state here and check privacy
        filteredItemUids = []
        uid_catalog = self.uid_catalog
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (categories == [] or obj.getCategory() in categories):
                continue
            elif not obj.isLate() == bool(listTypes == ['late']):
                continue
            filteredItemUids.append(itemUid)
        return len(filteredItemUids)
    Meeting.getNumberOfItems = getNumberOfItems

    security.declarePublic('listSections')

    def listSections(self):
        """Vocabulary for column 'name_section' of Meeting.sections."""
        if self.portal_type == 'MeetingCouncil':
            res = [('oj', "Collège d'arrêt de l'OJ"),
                   ('tec', "Section du développement territorial, économique et du commerce"),
                   ('fin', "Section des finances et des marchés publics"),
                   ('env', "Section de la propreté, de l'environnement, du développement durable et des travaux"),
                   ('ag', "Section de l'administration générale"),
                   ('ens', "Section de l'enseignement"),
                   ('as', "Section des affaires sociales"),
                   ('prev', "Section de la prévention de la citoyenneté et de la jeunesse"),
                   ('cul', "Section de la culture et des sports"),
                   ('ec', "Section de l'état civil")]
        else:
            res = [('oj', "Collège d'arrêt de l'OJ"), ]
        return DisplayList(tuple(res))
    Meeting.listSections = listSections

    security.declarePublic('getSectionDate')

    def getSectionDate(self, section_name):
        """Used in template."""
        dt = None
        for section in self.getSelf().getSections():
            if section['name_section'].upper() == section_name:
                dt = DateTime(section['date_section'], datefmt='international')
                break
        if not dt:
            return ''

        day = '%s %s' % (translate('weekday_%s' % dt.strftime('%a').lower(), domain='plonelocales',
                                  context=self.getSelf().REQUEST).lower(), dt.strftime('%d'))
        month = translate('month_%s' % dt.strftime('%b').lower(), domain='plonelocales',
                          context=self.getSelf().REQUEST).lower()
        year = dt.strftime('%Y')
        res = '%s %s %s' % (day, month, year)
        return res

old_setTakenOverBy = MeetingItem.setTakenOverBy


class CustomMeetingItem(MeetingItem):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom."""
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    def getFinanceAdviceId(self):
        """ """
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        usedFinanceGroupIds = cfg.adapted().getUsedFinanceGroupIds(self.context)
        adviserIds = self.context.adviceIndex.keys()
        financeAdvisersIds = set(usedFinanceGroupIds).intersection(set(adviserIds))
        if financeAdvisersIds:
            return list(financeAdvisersIds)[0]
        else:
            return None

    customItemDecidedStates = ('accepted', 'delayed', 'accepted_but_modified', 'accepted_closed', 'delayed_closed', 'accepted_but_modified_closed',)
    MeetingItem.itemDecidedStates = customItemDecidedStates

    customBeforePublicationStates = ('itemcreated',
                                     'proposed_to_servicehead',
                                     'proposed_to_officemanager',
                                     'proposed_to_divisionhead',
                                     'proposed',
                                     'validated', )
    MeetingItem.beforePublicationStates = customBeforePublicationStates

    customMeetingNotClosedStates = ('validated_by_dg', 'frozen', 'decided', )
    MeetingItem.meetingNotClosedStates = customMeetingNotClosedStates

    customMeetingTransitionsAcceptingRecurringItems = ('_init_', 'validated_by_dg', 'freeze', 'decide', )
    MeetingItem.meetingTransitionsAcceptingRecurringItems = customMeetingTransitionsAcceptingRecurringItems

    security.declarePublic('mayBeLinkedToTasks')

    def mayBeLinkedToTasks(self):
        """See doc in interfaces.py."""
        item = self.getSelf()
        res = False
        if item.queryState() in ('accepted', 'delayed', 'accepted_but_modified', ):
            res = True
        return res

    def _initDecisionFieldIfEmpty(self):
        """
          If decision field is empty, it will be initialized
          with data coming from title and description.
        """
        # set keepWithNext to False as it will add a 'class' and so
        # xhtmlContentIsEmpty will never consider it empty...
        if xhtmlContentIsEmpty(self.getDecision(keepWithNext=False)):
            self.setDecision("<p>%s</p>%s" % (self.Title(),
                                              self.Description()))
            self.reindexObject()
    MeetingItem._initDecisionFieldIfEmpty = _initDecisionFieldIfEmpty

    security.declarePublic('updatePowerEditorsLocalRoles')

    def updatePowerEditorsLocalRoles(self):
        """Give the 'power editors' local role to the corresponding
           MeetingConfig 'powereditors' group on self."""
        item = self.getSelf()
        # Then, add local roles for powereditors.
        cfg = item.portal_plonemeeting.getMeetingConfig(item)
        powerEditorsGroupId = "%s_%s" % (cfg.getId(), POWEREDITORS_GROUP_SUFFIX)
        item.manage_addLocalRoles(powerEditorsGroupId, (EDITOR_USECASES['power_editors'],))

    def getExtraFieldsToCopyWhenCloning(self, cloned_to_same_mc):
        """
          Keep some new fields when item is cloned (to another mc or from itemtemplate).
        """
        res = ['isToPrintInMeeting']
        if cloned_to_same_mc:
            res = res + []
        return res

    security.declarePublic('mayTakeOver')

    def mayTakeOver(self):
        """Condition for editing 'takenOverBy' field.
           A member may take an item over if he is able to modify item."""
        return _checkPermission(ModifyPortalContent, self.context)

    security.declarePublic('setTakenOverBy')

    def setTakenOverBy(self, value, **kwargs):
        # call original method
        old_setTakenOverBy(self, value, **kwargs)
        item = self.getSelf()
        if not item._at_creation_flag:
            wf_states_to_keep = ['presented', 'validated_by_dg', 'itemfrozen', 'accepted_but_modified', 'accepted']
            if item.queryState() in wf_states_to_keep:
                tool = getToolByName(item, 'portal_plonemeeting')
                cfg = tool.getMeetingConfig(item)
                for wf_state_to_keep in wf_states_to_keep:
                    wf_state = "%s__wfstate__%s" % (cfg.getItemWorkflow(), wf_state_to_keep)
                    if value:
                        item.takenOverByInfos[wf_state] = value
                    elif not value and wf_state in item.takenOverByInfos:
                        del item.takenOverByInfos[wf_state]
        item.getField('takenOverBy').set(item, value, **kwargs)
    MeetingItem.setTakenOverBy = setTakenOverBy

    def adviceDelayIsTimedOutWithRowId(self, groupId, rowIds=[]):
        """ Check if advice with delay from a certain p_groupId and with
            a row_id contained in p_rowIds is timed out."""
        item = self.getSelf()
        if item.getAdviceDataFor(item) and groupId in item.getAdviceDataFor(item):
            adviceRowId = item.getAdviceDataFor(item, groupId)['row_id']
        else:
            return False

        if not rowIds or adviceRowId in rowIds:
            return item._adviceDelayIsTimedOut(groupId)
        else:
            return False

    def showFinanceAdviceTemplate(self):
        """ """
        item = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(item)
        return bool(set(cfg.adapted().getUsedFinanceGroupIds(item)).
                    intersection(set(item.adviceIndex.keys())))


class CustomMeetingConfig(MeetingConfig):
    """Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom."""

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePublic('getUsedFinanceGroupIds')

    def getUsedFinanceGroupIds(self, item=None):
        """Possible finance advisers group ids are defined on
           the FINANCE_ADVICES_COLLECTION_ID collection."""
        cfg = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        collection = getattr(cfg.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID, None)
        if not collection:
            logger.warn(
                "Method 'getUsedFinanceGroupIds' could not find the '{0}' collection!".format(
                    FINANCE_ADVICES_COLLECTION_ID))
            return []
        # get the indexAdvisers value defined on the collection
        # and find the relevant group, indexAdvisers form is :
        # 'delay_real_group_id__2014-04-16.9996934488', 'real_group_id_directeur-financier'
        # it is either a customAdviser row_id or a MeetingGroup id
        values = [term['v'] for term in collection.getRawQuery()
                  if term['i'] == 'indexAdvisers'][0]
        res = []
        for v in values:
            rowIdOrGroupId = v.replace('delay_real_group_id__', '').replace('real_group_id__', '')
            if hasattr(tool, rowIdOrGroupId):
                groupId = rowIdOrGroupId
                # append it only if not already into res and if
                # we have no 'row_id' for this adviser in adviceIndex
                if item and groupId not in res and \
                   (groupId in item.adviceIndex and not item.adviceIndex[groupId]['row_id']):
                    res.append(groupId)
                elif not item:
                    res.append(groupId)
            else:
                groupId = cfg._dataForCustomAdviserRowId(rowIdOrGroupId)['group']
                # append it only if not already into res and if
                # we have a 'row_id' for this adviser in adviceIndex
                if item and groupId not in res and \
                    (groupId in item.adviceIndex and
                     item.adviceIndex[groupId]['row_id'] == rowIdOrGroupId):
                    res.append(groupId)
                elif not item:
                    res.append(groupId)
        # remove duplicates
        return list(set(res))

    security.declarePrivate('createPowerObserversGroup')

    def createPowerEditorsGroup(self):
        """Creates a Plone group that will be used to apply the 'Editor'
           local role on every items in itemFrozen state."""
        meetingConfig = self.getSelf()
        groupId = "%s_%s" % (meetingConfig.getId(), POWEREDITORS_GROUP_SUFFIX)
        if groupId not in meetingConfig.portal_groups.listGroupIds():
            enc = meetingConfig.portal_properties.site_properties.getProperty(
                'default_charset')
            groupTitle = '%s (%s)' % (
                meetingConfig.Title().decode(enc),
                translate(POWEREDITORS_GROUP_SUFFIX, domain='PloneMeeting', context=meetingConfig.REQUEST))
            # a default Plone group title is NOT unicode.  If a Plone group title is
            # edited TTW, his title is no more unicode if it was previously...
            # make sure we behave like Plone...
            groupTitle = groupTitle.encode(enc)
            meetingConfig.portal_groups.addGroup(groupId, title=groupTitle)
        # now define local_roles on the tool so it is accessible by this group
        tool = getToolByName(meetingConfig, 'portal_plonemeeting')
        tool.manage_addLocalRoles(groupId, (EDITOR_USECASES['power_editors'],))
        # but we do not want this group to access every MeetingConfigs so
        # remove inheritance on self and define these local_roles for self too
        meetingConfig.__ac_local_roles_block__ = True
        meetingConfig.manage_addLocalRoles(groupId, (EDITOR_USECASES['power_editors'],))

    security.declareProtected('Modify portal content', 'onEdit')

    def onEdit(self, isCreated):  # noqa
        self.context.createPowerEditorsGroup()

    security.declarePublic('getMeetingsAcceptingItems')

    def getMeetingsAcceptingItems(self, review_states=('created', 'validated_by_dg', 'frozen'), inTheFuture=False):
        """This returns meetings that are still accepting items."""
        cfg = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        catalog = api.portal.get_tool('portal_catalog')
        # If the current user is a meetingManager (or a Manager),
        # he is able to add a meetingitem to a 'decided' meeting.
        # except if we specifically restricted given p_review_states.
        if review_states == ('created', 'validated_by_dg', 'frozen') and tool.isManager(cfg):
            review_states += ('decided', )

        query = {'portal_type': cfg.getMeetingTypeName(),
                 'review_state': review_states,
                 'sort_on': 'getDate'}

        # querying empty review_state will return nothing
        if not review_states:
            query.pop('review_state')

        if inTheFuture:
            query['getDate'] = {'query': DateTime(), 'range': 'min'}

        return catalog.unrestrictedSearchResults(**query)

    def _extraSearchesInfo(self, infos):
        """Add some specific searches."""
        cfg = self.getSelf()
        itemType = cfg.getItemTypeName()
        extra_infos = OrderedDict(
            [
                # Items in state 'proposed'
                ('searchproposeditems',
                 {
                     'subFolderId': 'searches_items',
                     'active': True,
                     'query':
                         [
                             {'i': 'portal_type',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': [itemType, ]},
                             {'i': 'review_state',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': ['proposed']}
                         ],
                     'sort_on': u'created',
                     'sort_reversed': True,
                     'showNumberOfItems': False,
                     'tal_condition': "python: not tool.userIsAmong(['reviewers'])",
                     'roles_bypassing_talcondition': ['Manager', ]
                 }
                 ),
                # Items in state 'validated'
                ('searchvalidateditems',
                 {
                     'subFolderId': 'searches_items',
                     'active': True,
                     'query':
                         [
                             {'i': 'portal_type',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': [itemType, ]},
                             {'i': 'review_state',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': ['validated']}
                         ],
                     'sort_on': u'created',
                     'sort_reversed': True,
                     'showNumberOfItems': False,
                     'tal_condition': "",
                     'roles_bypassing_talcondition': ['Manager', ]
                 }
                 ),
            ]
        )
        infos.update(extra_infos)
        return infos

    def extraAdviceTypes(self):
        """See doc in interfaces.py."""
        typesTool = api.portal.get_tool('portal_types')
        if 'meetingadvicefinances' in typesTool:
            return ['positive_finance', 'positive_with_remarks_finance',
                    'cautious_finance', 'negative_finance', 'not_given_finance',
                    'not_required_finance']
        return []


class CustomMeetingGroup(MeetingGroup):
    """Adapter that adapts a meeting group implementing IMeetingGroup to the
       interface IMeetingGroupCustom."""

    implements(IMeetingGroupCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePublic('listEchevinServices')

    def listEchevinServices(self):
        """Returns a list of groups that can be selected on an group (without isEchevin)."""
        res = []
        tool = getToolByName(self, 'portal_plonemeeting')
        # Get every Plone group related to a MeetingGroup
        for group in tool.getMeetingGroups():
            res.append((group.id, group.getProperty('title')))

        return DisplayList(tuple(res))
    MeetingGroup.listEchevinServices = listEchevinServices


class MeetingSeraingWorkflowActions(MeetingWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeWorkflowActions"""

    implements(IMeetingSeraingWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doValidateByDG')

    def doValidateByDG(self, stateChange):
        """When a meeting go to the "validatedByDG" state, for example the
           meeting manager wants to add an item, we do not do anything."""
        pass

    security.declarePrivate('doBackToValidatedByDG')

    def doBackToValidatedByDG(self, stateChange):
        """When a meeting go back to the "validatedByDG" state, for example the
           meeting manager wants to add an item, we do not do anything."""
        pass


class MeetingSeraingCollegeWorkflowActions(MeetingSeraingWorkflowActions):
    """inherit class"""
    implements(IMeetingSeraingCollegeWorkflowActions)


class MeetingSeraingCouncilWorkflowActions(MeetingSeraingWorkflowActions):
    """inherit class"""
    implements(IMeetingSeraingCouncilWorkflowActions)


class MeetingSeraingWorkflowConditions(MeetingWorkflowConditions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeWorkflowConditions"""

    implements(IMeetingSeraingWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting
        customAcceptItemsStates = ('created', 'validated_by_dg', 'frozen', 'decided')
        self.acceptItemsStates = customAcceptItemsStates

    security.declarePublic('mayValidateByDG')

    def mayValidateByDG(self):
        if _checkPermission(ReviewPortalContent, self.context):
            return True

    security.declarePublic('mayDecide')

    def mayDecide(self):
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res


class MeetingSeraingCollegeWorkflowConditions(MeetingSeraingWorkflowConditions):
    """inherit class"""
    implements(IMeetingSeraingCollegeWorkflowConditions)


class MeetingSeraingCouncilWorkflowConditions(MeetingSeraingWorkflowConditions):
    """inherit class"""
    implements(IMeetingSeraingCouncilWorkflowConditions)


class MeetingItemSeraingWorkflowActions(MeetingItemWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCollegeWorkflowActions"""

    implements(IMeetingItemSeraingWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doAccept_but_modify')

    def doAccept_but_modify(self, stateChange):
        pass

    security.declarePrivate('doProposeToServiceHead')

    def doProposeToServiceHead(self, stateChange):
        pass

    security.declarePrivate('doProposeToOfficeManager')

    def doProposeToOfficeManager(self, stateChange):
        pass

    security.declarePrivate('doProposeToDivisionHead')

    def doProposeToDivisionHead(self, stateChange):
        pass

    security.declarePrivate('doDelay')

    def doDelay(self, stateChange):
        """After cloned item, we validate this item"""
        MeetingItemWorkflowActions(self.context).doDelay(stateChange)
        clonedItem = self.context.getBRefs('ItemPredecessor')[0]
        self.context.portal_workflow.doActionFor(clonedItem, 'validate')

    security.declarePrivate('doAccept_close')

    def doAccept_close(self, stateChange):
        pass

    security.declarePrivate('doAccept_but_modify_close')

    def doAccept_but_modify_close(self, stateChange):
        pass

    security.declarePrivate('doDelay_close')

    def doDelay_close(self, stateChange):
        pass

    security.declarePrivate('doItemValidateByDG')

    def doItemValidateByDG(self, stateChange):
        pass

    security.declarePrivate('doBackToItemAcceptedButModified')

    def doBackToItemAcceptedButModified(self, stateChange):
        pass

    security.declarePrivate('doBackToItemAccepted')

    def doBackToItemAccepted(self, stateChange):
        pass

    security.declarePrivate('doBackToItemDelayed')

    def doBackToItemDelayed(self, stateChange):
        pass

    security.declarePrivate('doBackToItemValidatedByDG')

    def doBackToItemValidatedByDG(self, stateChange):
        pass

    security.declarePrivate('doReturn_to_advise')

    def doReturn_to_advise(self, stateChange):
        pass

    security.declarePrivate('_freezePresentedItem')

    def _freezePresentedItem(self):
        """Presents an item into a frozen meeting. """
        wTool = getToolByName(self.context, 'portal_workflow')
        wTool.doActionFor(self.context, 'itemValidateByDG')
        wTool.doActionFor(self.context, 'itemfreeze')


class MeetingItemSeraingCollegeWorkflowActions(MeetingItemSeraingWorkflowActions):
    """inherit class"""
    implements(IMeetingItemSeraingCollegeWorkflowActions)


class MeetingItemSeraingCouncilWorkflowActions(MeetingItemSeraingWorkflowActions):
    """inherit class"""
    implements(IMeetingItemSeraingCouncilWorkflowActions)


class MeetingItemSeraingWorkflowConditions(MeetingItemWorkflowConditions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCollegeWorkflowConditions"""

    implements(IMeetingItemSeraingWorkflowConditions)
    security = ClassSecurityInfo()

    useHardcodedTransitionsForPresentingAnItem = True
    transitionsForPresentingAnItem = ('proposeToServiceHead',
                                      'proposeToOfficeManager',
                                      'proposeToDivisionHead',
                                      'propose',
                                      'validate',
                                      'present')

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem

    security.declarePublic('mayDecide')

    def mayDecide(self):
        """We may decide an item if the linked meeting is in the 'decided'
           state."""
        res = False
        meeting = self.context.getMeeting()
        if _checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['decided', 'closed', 'decisions_published', ]):
            res = True
        return res

    security.declarePublic('mayValidate')

    def mayValidate(self):
        """
          We must be reviewer
        """
        res = False
        # The user must have the 'Review portal content permission and be reviewer or manager'
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
            memnber = self.context.portal_membership.getAuthenticatedMember()
            tool = getToolByName(self.context, 'portal_plonemeeting')
            if not memnber.has_role('MeetingReviewer', self.context) and not tool.isManager(self.context):
                res = False
        return res

    security.declarePublic('mayValidateByDG')

    def mayValidateByDG(self):
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in ('created', 'validated_by_dg',
                                                           'frozen', 'decided', 'closed')):
                res = True
        return res

    security.declarePublic('mayProposeToServiceHead')

    def mayProposeToServiceHead(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if not self.context.getCategory():
            return No(translate('required_category_ko',
                                domain="PloneMeeting",
                                context=self.context.REQUEST))
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToOfficeManager')

    def mayProposeToOfficeManager(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToDivisionHead')

    def mayProposeToDivisionHead(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayBackToMeeting')

    def mayBackToMeeting(self, transitionName):
        """Specific guard for the 'return_to_proposing_group' wfAdaptation.
           As we have only one guard_expr for potentially several transitions departing
           from the 'returned_to_proposing_group' state, we receive the p_transitionName."""
        tool = getToolByName(self.context, 'portal_plonemeeting')
        if not _checkPermission(ReviewPortalContent, self.context) and not \
           tool.isManager(self.context):
            return
        # get the linked meeting
        meeting = self.context.getMeeting()
        meetingState = meeting.queryState()
        # use RETURN_TO_PROPOSING_GROUP_MAPPINGS to know in wich meetingStates
        # the given p_transitionName can be triggered
        authorizedMeetingStates = adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS[transitionName]
        if meetingState in authorizedMeetingStates:
            return True
        # if we did not return True, then return a No(...) message specifying that
        # it can no more be returned to the meeting because the meeting is in some
        # specifig states (like 'closed' for example)
        if meetingState in adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS['NO_MORE_RETURNABLE_STATES']:
            # avoid to display No(...) message for each transition having the 'mayBackToMeeting'
            # guard expr, just return the No(...) msg for the first transitionName checking this...
            if 'may_not_back_to_meeting_warned_by' not in self.context.REQUEST:
                self.context.REQUEST.set('may_not_back_to_meeting_warned_by', transitionName)
            if self.context.REQUEST.get('may_not_back_to_meeting_warned_by') == transitionName:
                return No(translate('can_not_return_to_meeting_because_of_meeting_state',
                                    mapping={'meetingState': translate(meetingState,
                                                                       domain='plone',
                                                                       context=self.context.REQUEST),
                                             },
                                    domain="PloneMeeting",
                                    context=self.context.REQUEST))
        return False


    security.declarePublic('mayClose')

    def mayClose(self):
        """
          Check that the user has the 'Review portal content' and meeting is closed (for automatic transitions)
        """
        res = False
        meeting = self.context.getMeeting()
        if _checkPermission(ReviewPortalContent, self.context) and meeting and (meeting.queryState() in ['closed']):
            res = True
        return res


class MeetingItemSeraingCollegeWorkflowConditions(MeetingItemSeraingWorkflowConditions):
    """inherit class"""
    implements(IMeetingItemSeraingCollegeWorkflowConditions)


class MeetingItemSeraingCouncilWorkflowConditions(MeetingItemSeraingWorkflowConditions):
    """inherit class"""
    implements(IMeetingItemSeraingCouncilWorkflowConditions)


class CustomToolPloneMeeting(ToolPloneMeeting):
    """Adapter that adapts a tool implementing ToolPloneMeeting to the
       interface IToolPloneMeetingCustom"""

    implements(IToolPloneMeetingCustom)
    security = ClassSecurityInfo()

    security.declarePublic('updatePowerEditors')

    def updatePowerEditors(self):
        """Update local_roles regarging the PowerEditors for every items."""
        if not self.context.isManager(realManagers=True):
            raise Unauthorized
        for b in self.context.portal_catalog(meta_type=('MeetingItem', )):
            obj = b.getObject()
            obj.updatePowerEditorsLocalRoles()
            # Update security
            obj.reindexObject(idxs=['allowedRolesAndUsers', ])
        self.context.plone_utils.addPortalMessage('Done.')
        self.context.gotoReferer()

    def performCustomWFAdaptations(self, meetingConfig, wfAdaptation, logger, itemWorkflow, meetingWorkflow):
        """This function applies workflow changes as specified by the
           p_meetingConfig."""
        if wfAdaptation == 'returned_to_advise':
            wfTool = api.portal.get_tool('portal_workflow')
            itemStates = itemWorkflow.states
            stateToClone = None
            if 'returned_to_advise' not in itemStates and 'returned_to_proposing_group' in itemStates:
                # add the 'returned_to_advise' state and clone the
                # permissions from RETURN_TO_PROPOSING_GROUP_CUSTOM_STATE_TO_CLONE
                # and apply permissions defined in RETURN_TO_ADVISE_CUSTOM_PERMISSIONS
                return_to_advice_item_state = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES + \
                                              ('returned_to_proposing_group',)
                itemWorkflow.states.addState('returned_to_advise')
                newState = getattr(itemWorkflow.states, 'returned_to_advise')
                # clone the permissions of the given RETURN_TO_PROPOSING_GROUP_CUSTOM_STATE_TO_CLONE if it exists
                cloned_permissions_with_meetingmanager = {}
                stateToCloneInfos = RETURN_TO_PROPOSING_GROUP_CUSTOM_STATE_TO_CLONE.get(meetingConfig.getItemWorkflow(), {})
                stateToCloneWFId = ''
                stateToCloneStateId = ''
                if stateToCloneInfos:
                    # stateToCloneInfos is like 'meetingitem_workflow.itemcreated'
                    stateToCloneWFId, stateToCloneStateId = stateToCloneInfos.split('.')
                stateToCloneWF = getattr(wfTool, stateToCloneWFId, None)
                stateToClone = None
                if stateToCloneWF and hasattr(stateToCloneWF.states, stateToCloneStateId):
                    stateToClone = getattr(itemWorkflow.states, stateToCloneStateId)
                    # we must make sure the MeetingManagers still may access this item
                    # so add MeetingManager role to every cloned permissions
                    cloned_permissions = dict(stateToClone.permission_roles)
                    # we need to use an intermediate dict because roles are stored as a tuple and we need a list...
                    for permission in cloned_permissions:
                        # the acquisition is defined like this : if permissions is a tuple, it is not acquired
                        # if it is a list, it is acquired...  WTF???  So make sure we store the correct type...
                        acquired = isinstance(cloned_permissions[permission], list) and True or False
                        cloned_permissions_with_meetingmanager[permission] = list(cloned_permissions[permission])
                        if 'MeetingManager' not in cloned_permissions[permission]:
                            cloned_permissions_with_meetingmanager[permission].append('MeetingManager')
                        if not acquired:
                            cloned_permissions_with_meetingmanager[permission] = \
                                tuple(cloned_permissions_with_meetingmanager[permission])
                # now apply custom permissions defined in RETURN_TO_ADVISE_CUSTOM_PERMISSIONS
                cloned_permissions_with_meetingmanager.update(RETURN_TO_ADVISE_CUSTOM_PERMISSIONS.get(meetingConfig.getItemWorkflow(), {}))

                # if we are cloning an existing state permissions, make sure DeleteObjects
                # is only be availble to ['Manager', 'MeetingManager']
                # if custom permissions are defined, keep what is defined in it
                if DeleteObjects not in RETURN_TO_ADVISE_CUSTOM_PERMISSIONS.get(meetingConfig.getItemWorkflow(), {}):
                    del_obj_perm = stateToClone.getPermissionInfo(DeleteObjects)
                    if del_obj_perm['acquired']:
                        cloned_permissions_with_meetingmanager[DeleteObjects] = ['Manager', ]
                    else:
                        cloned_permissions_with_meetingmanager[DeleteObjects] = ('Manager',)

                # finally, apply computed permissions, aka cloned + custom
                newState.permission_roles = cloned_permissions_with_meetingmanager
                # now create the necessary transitions : one to go to 'returned_to_proposing_group' state
                # and x to go back to relevant state depending on current meeting state
                # first, the transition 'return_to_advise'
                itemWorkflow.transitions.addTransition('return_to_advise')
                transition = itemWorkflow.transitions['return_to_advise']
                # use same guard from ReturnToProposingGroup
                transition.setProperties(
                    title='return_to_advise',
                    new_state_id='returned_to_advise', trigger_type=1, script_name='',
                    actbox_name='return_to_advise', actbox_url='', actbox_category='workflow',
                    actbox_icon='%(portal_url)s/return_to_advise.png', 
                    props={'guard_expr': 'python:here.wfConditions().mayReturnToProposingGroup()'})
                # Update connections between states and transitions and create new transitions
                newTransitionNames = []
                for stateName in return_to_advice_item_state:
                    if stateName not in itemWorkflow.states:
                        continue
                    # first specify that we can go to 'return_to_advise' from this state
                    currentTransitions = list(itemWorkflow.states[stateName].transitions)
                    currentTransitions.append('return_to_advise')
                    itemWorkflow.states[stateName].transitions = tuple(currentTransitions)
                    # then build a back transition name with given stateName
                    transitionName = 'backTo_%s_from_returned_to_advise' % stateName
                    newTransitionNames.append(transitionName)
                    itemWorkflow.transitions.addTransition(transitionName)
                    transition = itemWorkflow.transitions[transitionName]
                    # use a specific guard_expr 'mayBackToMeeting'
                    if stateName in ('returned_to_proposing_group',):
                        transition_title = 'return_to_proposing_group'
                    else:
                        transition_title = 'return_to_meeting'
                    icon_url = '%s%s.png' % ('%(portal_url)s/', transitionName)
                    transition.setProperties(
                        title=transition_title,
                        new_state_id=stateName, trigger_type=1, script_name='',
                        actbox_name=transitionName, actbox_url='',
                        actbox_icon=icon_url, actbox_category='workflow',
                        props={'guard_expr': 'python:here.wfConditions().mayBackToMeeting("%s")' % transitionName})
                # now that we created back transitions, we can assign them to newState 'returned_to_advise'
                # set properties for new 'returned_to_advise' state
                newState.setProperties(
                    title='returned_to_advise', description='',
                    transitions=newTransitionNames)
            logger.info(WF_APPLIED % ("return_to_proposing_group", meetingConfig.getId()))
            return True
        return False

# ------------------------------------------------------------------------------
InitializeClass(CustomMeetingItem)
InitializeClass(CustomMeeting)
InitializeClass(CustomMeetingConfig)
InitializeClass(CustomMeetingGroup)
InitializeClass(MeetingSeraingWorkflowActions)
InitializeClass(MeetingSeraingWorkflowConditions)
InitializeClass(MeetingItemSeraingWorkflowActions)
InitializeClass(MeetingItemSeraingWorkflowConditions)
InitializeClass(CustomToolPloneMeeting)
# ------------------------------------------------------------------------------

class MLItemPrettyLinkAdapter(ItemPrettyLinkAdapter):
    """
      Override to take into account MeetingLiege use cases...
    """

    def _leadingIcons(self):
        """
          Manage icons to display before the icons managed by PrettyLink._icons.
        """
        # Default PM item icons
        icons = super(MLItemPrettyLinkAdapter, self)._leadingIcons()

        if self.context.isDefinedInTool():
            return icons

        itemState = self.context.queryState()
        # Add our icons for some review states
        if itemState == 'proposed':
            icons.append(('proposeToDirector.png',
                          translate('icon_help_proposed_to_director',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'proposed_to_divisionhead':
            icons.append(('proposeToDivisionHead.png',
                          translate('icon_help_proposed_to_divisionhead',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'proposed_to_officemanager':
            icons.append(('proposeToOfficeManager.png',
                          translate('icon_help_proposed_to_officemanager',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'validated_by_dg':
            icons.append(('itemValidateByDG.png',
                          translate('icon_help_validated_by_dg',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'proposed_to_servicehead':
            icons.append(('proposeToServiceHead.png',
                          translate('icon_help_proposed_to_servicehead',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'accepted_but_modified_closed':
            icons.append(('accepted_but_modified.png',
                          translate('icon_help_accepted_but_modified_closed',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'delayed_closed':
            icons.append(('delayed.png',
                          translate('icon_help_delayed_closed',
                                    domain="PloneMeeting",
                                    context=self.request)))
        elif itemState == 'returned_to_advise':
            icons.append(('returned_to_advise.png',
                          translate('icon_help_returned_to_advise',
                                    domain="PloneMeeting",
                                    context=self.request)))

        # add an icon if item is down the workflow from the finances
        # if item was ever gone the the finances and now it is down to the
        # services, then it is considered as down the wf from the finances
        # so take into account every states before 'validated/proposed_to_finance'
        if self.context.getIsToPrintInMeeting():
            icons.append(('toPrint.png',
                          translate('icon_help_to_print',
                                    domain="PloneMeeting",
                                    context=self.request)))
        return icons
