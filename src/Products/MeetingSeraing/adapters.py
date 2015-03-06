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
from appy.gen import No
from AccessControl import getSecurityManager, ClassSecurityInfo, Unauthorized
from Globals import InitializeClass
from zope.interface import implements
from Products.CMFCore.permissions import ReviewPortalContent, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from Products.PloneMeeting.MeetingItem import MeetingItem, \
    MeetingItemWorkflowConditions, MeetingItemWorkflowActions
from Products.PloneMeeting.utils import checkPermission, prepareSearchValue
from Products.PloneMeeting.config import ITEM_NO_PREFERRED_MEETING_VALUE
from Products.PloneMeeting.Meeting import MeetingWorkflowActions, \
    MeetingWorkflowConditions, Meeting
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingGroup import MeetingGroup
from Products.PloneMeeting.interfaces import IMeetingCustom, IMeetingItemCustom, \
    IMeetingConfigCustom, IMeetingGroupCustom, IToolPloneMeetingCustom
from Products.MeetingSeraing.interfaces import \
    IMeetingItemCollegeSeraingWorkflowConditions, IMeetingItemCollegeSeraingWorkflowActions,\
    IMeetingCollegeSeraingWorkflowConditions, IMeetingCollegeSeraingWorkflowActions, \
    IMeetingItemCouncilSeraingWorkflowConditions, IMeetingItemCouncilSeraingWorkflowActions,\
    IMeetingCouncilSeraingWorkflowConditions, IMeetingCouncilSeraingWorkflowActions
from Products.MeetingSeraing.config import COUNCIL_COMMISSION_IDS, \
    COUNCIL_COMMISSION_IDS_2013, COUNCIL_MEETING_COMMISSION_IDS_2013, COMMISSION_EDITORS_SUFFIX, \
    EDITOR_USECASES, POWEREDITORS_GROUP_SUFFIX
from Products.PloneMeeting import PloneMeetingError
from zope.i18n import translate
from Products.PloneMeeting.ToolPloneMeeting import ToolPloneMeeting

# disable most of wfAdaptations
customWfAdaptations = ('archiving', 'local_meeting_managers', 'return_to_proposing_group', )
MeetingConfig.wfAdaptations = customWfAdaptations

# configure parameters for the returned_to_proposing_group wfAdaptation
# we keep also 'itemfrozen' and 'itempublished' in case this should be activated for meeting-config-college...
from Products.PloneMeeting.model import adaptations
RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'itemfrozen', 'itempublished',
                                              'item_in_committee', 'item_in_council', )
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES
RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {
    # view permissions
    'Access contents information':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'View':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read budget infos':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read decision':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read optional advisers':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read decision annex':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'PloneMeeting: Read item observations':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    'MeetingSeraing: Read commission transcript':
    ['Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ],
    # edit permissions
    'Modify portal content':
    ['Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ],
    'PloneMeeting: Write budget infos':
    ['Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', 'MeetingBudgetImpactEditor'],
    'PloneMeeting: Write decision':
    ['Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ],
    'Review portal content':
    ['Manager', 'MeetingReviewer', 'MeetingManager', ],
    'Add portal content':
    ['Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ],
    'PloneMeeting: Add annex':
    ['Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ],
    'PloneMeeting: Add MeetingFile':
    ['Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ],
    'PloneMeeting: Write decision annex':
    ['Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ],
    'PloneMeeting: Write optional advisers':
    ['Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ],
    # MeetingManagers edit permissions
    'Delete objects':
    ['Manager', 'MeetingManager', ],
    'PloneMeeting: Write item observations':
    ['Manager', 'MeetingManager', ],
    'MeetingSeraing: Write commission transcript':
    ['Manager', 'MeetingManager', ],
}

adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS


class CustomMeeting(Meeting):
    '''Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom.'''

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    # define same validator for every preMeetingDate_X than the one used for preMeetingDate
    Meeting.validate_preMeetingDate_2 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_3 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_4 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_5 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_6 = Meeting.validate_preMeetingDate
    Meeting.validate_preMeetingDate_7 = Meeting.validate_preMeetingDate

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

    def getPrintableItems(self, itemUids, late=False, ignore_review_states=[],
                          privacy='*', oralQuestion='both', categories=[],
                          excludedCategories=[], firstNumber=1, renumber=False):
        '''Returns a list of items.
           An extra list of review states to ignore can be defined.
           A privacy can also be given, and the fact that the item is an
           oralQuestion or not (or both).
           Some specific categories can be given or some categories to exchude.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be returned with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'''
        # We just filter ignore_review_states here and privacy and call
        # getItemsInOrder(uids), passing the correct uids and removing empty
        # uids.
        # privacy can be '*' or 'public' or 'secret'
        # oralQuestion can be 'both' or False or True
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)
        #no filtering, returns the items ordered
        if not categories and not ignore_review_states and privacy == '*' and oralQuestion == 'both':
            return self.context.getItemsInOrder(late=late, uids=itemUids)
        # Either, we will have to filter the state here and check privacy
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
            elif excludedCategories and obj.getCategory() in excludedCategories:
                continue
            filteredItemUids.append(itemUid)
        #in case we do not have anything, we return an empty list
        if not filteredItemUids:
            return []
        else:
            items = self.context.getItemsInOrder(late=late, uids=filteredItemUids)
            if renumber:
                #returns a list of tuple with first element the number
                #and second element the item itself
                i = firstNumber
                res = []
                for item in items:
                    res.append((i, item))
                    i = i + 1
                items = res
            return items

    security.declarePublic('getAvailableItems')

    def getAvailableItems(self):
        '''Items are available to the meeting no matter the meeting state (except 'closed').
           In the 'created' state, every validated items are availble, in other states, only items
           for wich the specific meeting is selected as preferred will appear.'''
        meeting = self.getSelf()
        if meeting.queryState() not in ('created', 'frozen', 'in_committee', 'in_council', 'decided'):
            return []
        tool = getToolByName(meeting, 'portal_plonemeeting')
        meetingConfig = tool.getMeetingConfig(meeting)
        # First, get meetings accepting items for which the date is lower or
        # equal to the date of this meeting (self)
        catalog = getToolByName(meeting, 'portal_catalog')
        meetings = catalog(portal_type=meetingConfig.getMeetingTypeName(),
                           getDate={'query': meeting.getDate(), 'range': 'max'})
        meetingUids = [b.getObject().UID() for b in meetings]
        # if the meeting is 'in_committee' or 'in_council'
        # we only accept items for wich the preferredMeeting is the current meeting
        if not meeting.queryState() in ('in_committee', 'in_council', ):
            meetingUids.append(ITEM_NO_PREFERRED_MEETING_VALUE)
        # Then, get the items whose preferred meeting is None or is among
        # those meetings.
        itemsUids = catalog(portal_type=meetingConfig.getItemTypeName(),
                            review_state='validated',
                            getPreferredMeeting=meetingUids,
                            sort_on="modified")
        if meeting.queryState() in ('frozen', 'decided'):
            # Oups. I can only take items which are "late" items.
            res = []
            for uid in itemsUids:
                if uid.getObject().wfConditions().isLateFor(meeting):
                    res.append(uid)
        else:
            res = itemsUids
        return res

    def _getAcronymPrefix(self, group, groupPrefixes):
        '''This method returns the prefix of the p_group's acronym among all
           prefixes listed in p_groupPrefixes. If group acronym does not have a
           prefix listed in groupPrefixes, this method returns None.'''
        res = None
        groupAcronym = group.getAcronym()
        for prefix in groupPrefixes.iterkeys():
            if groupAcronym.startswith(prefix):
                res = prefix
                break
        return res

    def _getGroupIndex(self, group, groups, groupPrefixes):
        '''Is p_group among the list of p_groups? If p_group is not among
           p_groups but another group having the same prefix as p_group
           (the list of prefixes is given by p_groupPrefixes), we must conclude
           that p_group is among p_groups. res is -1 if p_group is not
           among p_group; else, the method returns the index of p_group in
           p_groups.'''
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
        '''Inserts a group list corresponding to p_meetingGroup in the given
           p_categoryList, following meeting group order as defined in the
           main configuration (groups from the config are in p_groups).
           If p_item is specified, the item is appended to the group list.'''
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
                        categoryList.insert(i+1, [meetingGroup, item])
                    else:
                        categoryList.insert(i+1, [meetingGroup])
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
                categoryList[groupIndex+1].append(item)

    def _insertItemInCategory(self, categoryList, item, byProposingGroup, groupPrefixes, groups):
        '''This method is used by the next one for inserting an item into the
           list of all items of a given category. if p_byProposingGroup is True,
           we must add it in a sub-list containing items of a given proposing
           group. Else, we simply append it to p_category.'''
        if not byProposingGroup:
            categoryList.append(item)
        else:
            group = item.getProposingGroup(True)
            self._insertGroupInCategory(categoryList, group, groupPrefixes, groups, item)

    security.declarePublic('getPrintableItemsByCategory')

    def getPrintableItemsByCategory(self, itemUids=[], late=False,
                                    ignore_review_states=[], by_proposing_group=False, group_prefixes={},
                                    privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                                    excludedCategories=[], firstNumber=1, renumber=False,
                                    includeEmptyCategories=False, includeEmptyGroups=False, isToPrintInMeeting='both'):
        '''Returns a list of (late-)items (depending on p_late) ordered by
           category. Items being in a state whose name is in
           p_ignore_review_state will not be included in the result.
           If p_by_proposing_group is True, items are grouped by proposing group
           within every category. In this case, specifying p_group_prefixes will
           allow to consider all groups whose acronym starts with a prefix from
           this param prefix as a unique group. p_group_prefixes is a dict whose
           keys are prefixes and whose values are names of the logical big
           groups. A privacy,A toDiscuss, isToPrintInMeeting and oralQuestion can also be given, the item is a
           toDiscuss (oralQuestion) or not (or both) item.
           If p_includeEmptyCategories is True, categories for which no
           item is defined are included nevertheless. If p_includeEmptyGroups
           is True, proposing groups for which no item is defined are included
           nevertheless.Some specific categories can be given or some categories to exclude.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'''
        # The result is a list of lists, where every inner list contains:
        # - at position 0: the category object (MeetingCategory or MeetingGroup)
        # - at position 1 to n: the items in this category
        # If by_proposing_group is True, the structure is more complex.
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        # privacy can be '*' or 'public' or 'secret'
        # Every inner list contains:
        # - at position 0: the category object
        # - at positions 1 to n: inner lists that contain:
        #   * at position 0: the proposing group object
        #   * at positions 1 to n: the items belonging to this group.
        res = []
        items = []
        previousCatId = None
        tool = getToolByName(self.context, 'portal_plonemeeting')
        # Retrieve the list of items
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)
        if late == 'both':
            items = self.context.getItemsInOrder(late=False, uids=itemUids)
            items += self.context.getItemsInOrder(late=True, uids=itemUids)
        else:
            items = self.context.getItemsInOrder(late=late, uids=itemUids)
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
                elif categories and not item.getCategory() in categories:
                    continue
                elif excludedCategories and item.getCategory() in excludedCategories:
                    continue
                elif not (isToPrintInMeeting == 'both' or item.getIsToPrintInMeeting() == isToPrintInMeeting):
                    continue
                currentCat = item.getCategory(theObject=True)
                currentCatId = currentCat.getId()
                if currentCatId != previousCatId:
                    # Add the item to a new category, excepted if the
                    # category already exists.
                    catExists = False
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
                    previousCatId = currentCatId
                else:
                    # Append the item to the same category
                    self._insertItemInCategory(res[-1], item,
                                               by_proposing_group, group_prefixes, groups)
        if includeEmptyCategories:
            meetingConfig = tool.getMeetingConfig(
                self.context)
            allCategories = meetingConfig.getCategories()
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
            #return a list of tuple with first element the number and second
            #element the item itself
            final_res = []
            for elts in res:
                final_items = [elts[0]]
                item_num = 1
                # we received a list of tuple (cat, items_list)
                for item in elts[1:]:
                    # we received a list of items
                    final_items.append((item_num, item))
                    item_num = item_num + 1
                final_res.append(final_items)
            res = final_res
        return res

    #helper methods used in templates
    security.declarePublic('getNormalCategories')

    def getNormalCategories(self):
        '''Returns the 'normal' categories'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        categories = mc.getCategories(onlySelectable=False)
        res = []
        firstSupplCatIds = self.getFirstSupplCategories()
        secondSupplCatIds = self.getSecondSupplCategories()
        thirdSupplCatIds = self.getThirdSupplCategories()
        for cat in categories:
            catId = cat.getId()
            if not catId in firstSupplCatIds and \
               not catId in secondSupplCatIds and \
               not catId in thirdSupplCatIds:
                res.append(catId)
        return res
    Meeting.getNormalCategories = getNormalCategories

    security.declarePublic('getFirstSupplCategories')

    def getFirstSupplCategories(self):
        '''Returns the '1er-supplement' categories'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        categories = mc.getCategories(onlySelectable=False)
        res = []
        for cat in categories:
            catId = cat.getId()
            if catId.endswith('1er-supplement'):
                res.append(catId)
        return res
    Meeting.getFirstSupplCategories = getFirstSupplCategories

    security.declarePublic('getSecondSupplCategories')

    def getSecondSupplCategories(self):
        '''Returns the '2eme-supplement' categories'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        categories = mc.getCategories(onlySelectable=False)
        res = []
        for cat in categories:
            catId = cat.getId()
            if catId.endswith('2eme-supplement'):
                res.append(catId)
        return res
    Meeting.getSecondSupplCategories = getSecondSupplCategories

    security.declarePublic('getThirdSupplCategories')

    def getThirdSupplCategories(self):
        '''Returns the '3eme-supplement' categories'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        categories = mc.getCategories(onlySelectable=False)
        res = []
        for cat in categories:
            catId = cat.getId()
            if catId.endswith('3eme-supplement'):
                res.append(catId)
        return res
    Meeting.getThirdSupplCategories = getThirdSupplCategories

    security.declarePublic('getNumberOfItems')

    def getNumberOfItems(self, itemUids, privacy='*', categories=[], late=False):
        '''Returns the number of items depending on parameters.
           This is used in templates'''
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)
        #no filtering, return the items ordered
        if not categories and privacy == '*':
            return self.getItemsInOrder(late=late, uids=itemUids)
        # Either, we will have to filter the state here and check privacy
        filteredItemUids = []
        uid_catalog = self.uid_catalog
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (categories == [] or obj.getCategory() in categories):
                continue
            filteredItemUids.append(itemUid)
        return len(filteredItemUids)
    Meeting.getNumberOfItems = getNumberOfItems

    def getItemsFirstSuppl(self, itemUids, privacy='public'):
        '''Returns the items presented as first supplement'''
        normalCategories = self.getNormalCategories()
        firstSupplCategories = self.getFirstSupplCategories()
        firstNumber = self.getNumberOfItems(itemUids,
                                            privacy=privacy,
                                            categories=normalCategories) + 1
        return self.adapted().getPrintableItems(itemUids,
                                                privacy=privacy,
                                                categories=firstSupplCategories,
                                                firstNumber=firstNumber,
                                                renumber=True)
    Meeting.getItemsFirstSuppl = getItemsFirstSuppl

    def getItemsSecondSuppl(self, itemUids, privacy='public'):
        '''Returns the items presented as second supplement'''
        normalCategories = self.getNormalCategories()
        firstSupplCategories = self.getFirstSupplCategories()
        secondSupplCategories = self.getSecondSupplCategories()
        firstNumber = self.getNumberOfItems(itemUids,
                                            privacy=privacy,
                                            categories=normalCategories+firstSupplCategories) + 1
        return self.adapted().getPrintableItems(itemUids,
                                                privacy=privacy,
                                                categories=secondSupplCategories,
                                                firstNumber=firstNumber,
                                                renumber=True)
    Meeting.getItemsSecondSuppl = getItemsSecondSuppl

    def getItemsThirdSuppl(self, itemUids, privacy='public'):
        '''Returns the items presented as third supplement'''
        normalCategories = self.getNormalCategories()
        firstSupplCategories = self.getFirstSupplCategories()
        secondSupplCategories = self.getSecondSupplCategories()
        thirdSupplCategories = self.getThirdSupplCategories()
        firstNumber = self.getNumberOfItems(itemUids,
                                            privacy=privacy,
                                            categories=normalCategories+firstSupplCategories+secondSupplCategories) + 1
        return self.adapted().getPrintableItems(itemUids,
                                                privacy=privacy,
                                                categories=thirdSupplCategories,
                                                firstNumber=firstNumber,
                                                renumber=True)
    Meeting.getItemsThirdSuppl = getItemsThirdSuppl

    security.declarePublic('getLabelDescription')

    def getLabelDescription(self):
        '''Returns the label to use for field MeetingItem.description
          The label is different between college and council'''
        if self.portal_type == 'MeetingItemCouncil':
            return self.utranslate("MeetingSeraing_label_councildescription", domain="PloneMeeting")
        else:
            return self.utranslate("PloneMeeting_label_description", domain="PloneMeeting")
    MeetingItem.getLabelDescription = getLabelDescription

    security.declarePublic('getLabelCategory')

    def getLabelCategory(self):
        '''Returns the label to use for field MeetingItem.category
          The label is different between college and council'''
        if self.portal_type == 'MeetingItemCouncil':
            return self.utranslate("MeetingSeraing_label_councilcategory", domain="PloneMeeting")
        else:
            return self.utranslate("PloneMeeting_label_category", domain="PloneMeeting")
    MeetingItem.getLabelCategory = getLabelCategory

    security.declarePublic('getLabelObservations')

    def getLabelObservations(self):
        '''Returns the label to use for field Meeting.observations
           The label is different between college and council'''
        if self.portal_type == 'MeetingCouncil':
            return self.utranslate("MeetingSeraing_label_meetingcouncilobservations", domain="PloneMeeting")
        else:
            return self.utranslate("PloneMeeting_label_meetingObservations", domain="PloneMeeting")
    Meeting.getLabelObservations = getLabelObservations

    security.declarePublic('getCommissionTitle')

    def getCommissionTitle(self, commissionNumber=1):
        '''
          Given a commissionNumber, return the commission title depending on corresponding categories
        '''
        meeting = self.getSelf()
        commissionCategories = meeting.getCommissionCategories()
        if not len(commissionCategories) >= commissionNumber:
            return ''
        commissionCat = commissionCategories[commissionNumber-1]
        # build title
        if isinstance(commissionCat, tuple):
            res = 'Commission ' + '/'.join([subcat.Title().replace('Commission ', '') for subcat in commissionCat])
        else:
            res = commissionCat.Title()
        return res

    security.declarePublic('getCommissionCategories')

    def getCommissionCategories(self):
        '''Returns the list of categories used for Commissions.
           Since june 2013, some commission are aggregating several categories, in this case,
           a sublist of categories is returned...'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        # creating a new Meeting or editing an existing meeting with date >= june 2013
        if not self.getDate() or \
           (self.getDate().year() >= 2013 and self.getDate().month() > 5) or \
           (self.getDate().year() > 2013):
            # since 2013 commissions does NOT correspond to commission as MeetingItem.category
            # several MeetingItem.category are taken for one single commission...
            commissionCategoryIds = COUNCIL_MEETING_COMMISSION_IDS_2013
        else:
            commissionCategoryIds = COUNCIL_COMMISSION_IDS

        res = []
        for categoryId in commissionCategoryIds:
            # check if we have subcategories, aka a commission made of several categories
            if isinstance(categoryId, tuple):
                res2 = []
                for subcatId in categoryId:
                    res2.append(getattr(mc.categories, subcatId))
                res.append(tuple(res2))
            else:
                res.append(getattr(mc.categories, categoryId))
        return tuple(res)
    Meeting.getCommissionCategories = getCommissionCategories

    security.declarePublic('showAllItemsAtOnce')

    def showAllItemsAtOnce(self):
        '''Monkeypatch for hiding the allItemsAtOnce field.'''
        return False
    Meeting.showAllItemsAtOnce = showAllItemsAtOnce

    security.declarePrivate('getDefaultPreMeetingAssembly')

    def getDefaultPreMeetingAssembly(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly = getDefaultPreMeetingAssembly

    security.declarePrivate('getDefaultPreMeetingAssembly_2')

    def getDefaultPreMeetingAssembly_2(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_2_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_2 = getDefaultPreMeetingAssembly_2

    security.declarePrivate('getDefaultPreMeetingAssembly_3')

    def getDefaultPreMeetingAssembly_3(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_3_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_3 = getDefaultPreMeetingAssembly_3

    security.declarePrivate('getDefaultPreMeetingAssembly_4')

    def getDefaultPreMeetingAssembly_4(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_4_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_4 = getDefaultPreMeetingAssembly_4

    security.declarePrivate('getDefaultPreMeetingAssembly_5')

    def getDefaultPreMeetingAssembly_5(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_5_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_5 = getDefaultPreMeetingAssembly_5

    security.declarePrivate('getDefaultPreMeetingAssembly_6')

    def getDefaultPreMeetingAssembly_6(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_6_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_6 = getDefaultPreMeetingAssembly_6

    security.declarePrivate('getDefaultPreMeetingAssembly_7')

    def getDefaultPreMeetingAssembly_7(self):
        '''Returns the default value for field 'preMeetingAssembly.'''
        if self.attributeIsUsed('preMeetingAssembly'):
            tool = getToolByName(self, 'portal_plonemeeting')
            return tool.getMeetingConfig(self).getPreMeetingAssembly_7_default()
        return ''
    Meeting.getDefaultPreMeetingAssembly_7 = getDefaultPreMeetingAssembly_7


class CustomMeetingItem(MeetingItem):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom.'''
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    customItemPositiveDecidedStates = ('accepted', 'accepted_but_modified', )
    MeetingItem.itemPositiveDecidedStates = customItemPositiveDecidedStates
    customItemDecidedStates = ('accepted', 'delayed', 'accepted_but_modified', 'removed', )
    MeetingItem.itemDecidedStates = customItemDecidedStates
    customBeforePublicationStates = ('itemcreated',
                                     'proposed_to_servicehead',
                                     'proposed_to_officemanager',
                                     'proposed_to_divisionhead',
                                     'proposed',
                                     'validated', )
    MeetingItem.beforePublicationStates = customBeforePublicationStates
    #this list is used by doPresent defined in PloneMeeting
    #for the Council, there is no "frozen" functionnality
    customMeetingAlreadyFrozenStates = ('frozen', 'decided', )
    MeetingItem.meetingAlreadyFrozenStates = customMeetingAlreadyFrozenStates

    customMeetingNotClosedStates = ('frozen', 'in_committee', 'in_council', 'decided', )
    MeetingItem.meetingNotClosedStates = customMeetingNotClosedStates

    customMeetingTransitionsAcceptingRecurringItems = ('_init_', 'freeze', 'decide', 'setInCommittee', 'setInCouncil', )
    MeetingItem.meetingTransitionsAcceptingRecurringItems = customMeetingTransitionsAcceptingRecurringItems

    def __init__(self, item):
        self.context = item

    security.declarePublic('mayBeLinkedToTasks')

    def mayBeLinkedToTasks(self):
        '''See doc in interfaces.py.'''
        item = self.getSelf()
        res = False
        if (item.queryState() in ('accepted', 'delayed', 'accepted_but_modified', )):
            res = True
        return res

    security.declarePublic('onDuplicatedFromConfig')

    def onDuplicatedFromConfig(self, usage):
        '''Hook when a recurring item is added to a meeting'''
        # Recurring items added when the meeting is 'in_council' need
        # to be set in council also.  By default they are just 'presented'
        if not self.context.portal_type == 'MeetingItemCouncil':
            return

        if usage == 'as_recurring_item' and self.context.getMeeting().queryState() == 'in_committee':
            wfTool = getToolByName(self.context, 'portal_workflow')
            item = self.getSelf()
            if item.queryState() == 'presented':
                wfTool.doActionFor(item, 'setItemInCommittee')
            if item.queryState() == 'item_in_committee':
                wfTool.doActionFor(item, 'setItemInCouncil')

    security.declarePublic('onDuplicated')

    def onDuplicated(self, original):
        '''Hook when a item is duplicated (called by MeetingItem.clone).'''
        # while an item is cloned to the meeting-config-council,
        # add the council specific 'motivation' at the top of existing 'motivation'
        item = self.getSelf()
        # only apply if we are actually creating a MeetingItemCouncil from another MeetingConfig
        if not (item.portal_type == 'MeetingItemCouncil' and original.portal_type != 'MeetingItemCouncil'):
            return
        existingMotivation = item.getMotivation()
        defaultCouncilMotivation = item.Schema()['motivation'].getDefault(item)
        item.setMotivation(defaultCouncilMotivation + '<p>&nbsp;</p><p>&nbsp;</p>' + existingMotivation)

    security.declareProtected('Modify portal content', 'onEdit')

    def onEdit(self, isCreated):
        '''Depending on the selected Council commission (category),
           give the 'MeetingCommissionEditor' role to the relevant Plone group'''
        # if the current category id startswith a given Plone group, this is the correspondance
        # for example, category 'commission-travaux' correspond to Plone
        # group 'commission-travaux_COMMISSION_EDITORS_SUFFIX'
        # category 'commission-travaux-1er-supplement' correspond to Plone
        # group 'commission-travaux_COMMISSION_EDITORS_SUFFIX'
        # first, remove previously set local roles for the Plone group commission
        # this is only done for MeetingItemCouncil
        # update power editor for this item
        if not self.context.portal_type == 'MeetingItemCouncil':
            return
        #existing commission Plone groups
        commissionEditorsGroupIds = [(commissionId + COMMISSION_EDITORS_SUFFIX) for commissionId in
                                     set(COUNCIL_COMMISSION_IDS).union(set(COUNCIL_COMMISSION_IDS_2013))]
        groupsTool = getToolByName(self.context, 'portal_groups')
        commissionPloneGroupIds = [groupId for groupId in groupsTool.getGroupIds()
                                   if groupId in commissionEditorsGroupIds]
        toRemove = []
        for principalId, localRoles in self.context.get_local_roles():
            if (principalId in commissionPloneGroupIds):
                toRemove.append(principalId)
        self.context.manage_delLocalRoles(toRemove)
        #now add the new local roles
        for groupId in commissionPloneGroupIds:
            if self.context.getCategory().startswith(groupId[:-len(COMMISSION_EDITORS_SUFFIX)]):
                #we found the relevant group
                self.context.manage_addLocalRoles(groupId, ('MeetingCommissionEditor',))

    security.declarePublic('getCertifiedSignatures')

    def getCertifiedSignatures(self):
        '''Returns certified signatures taking delegations into account.'''
        tool = getToolByName(self, 'portal_plonemeeting')
        mc = tool.getMeetingConfig(self)
        globalCertifiedSignatures = mc.getCertifiedSignatures().split('\n')
        # we need to return 6 values but by default, certifiedSignatures contains 4 values...
        if len(globalCertifiedSignatures) == 4:
            globalCertifiedSignatures = globalCertifiedSignatures[0:1] + [''] + globalCertifiedSignatures[1:3] + \
                [''] + globalCertifiedSignatures[3:4]
        specificSignatures = self.getProposingGroup(theObject=True).getSignatures().split('\n')
        specificSignaturesLength = len(specificSignatures)
        # just take specific/delegation signatures into account if there are 3 (just redefined the first signatory) or
        # 6 (redefined at least second signatory) available values
        if not specificSignaturesLength == 12:
            return globalCertifiedSignatures
        else:
            res = []
            for elt in enumerate(specificSignatures):
                index = elt[0]
                line = elt[1]
                if not line.strip() == '-':
                    res.append(line)
                else:
                    if index > 5:
                        index = index - 6
                    res.append(globalCertifiedSignatures[index])
            return res
    MeetingItem.getCertifiedSignatures = getCertifiedSignatures

    security.declarePublic('getCollegeItem')

    def getCollegeItem(self):
        '''Returns the predecessor item that was in the college.'''
        item = self.getSelf()
        predecessor = item.getPredecessor()
        collegeItem = None
        while predecessor:
            if predecessor.portal_type == 'MeetingItemCollege':
                collegeItem = predecessor
                break
        return collegeItem

    security.declarePublic('isPrivacyViewable')

    def isPrivacyViewable(self):
        '''Override so privacy is not taken into account while accessing an item.
           We just need privacy to be an information here, not an access management.'''
        return True
    MeetingItem.isPrivacyViewable = isPrivacyViewable

    security.declarePublic('getMeetingsAcceptingItems')

    def getMeetingsAcceptingItems(self):
        '''Overrides the default method so we only display meetings that are
           in the 'created' or 'frozen' state.'''
        tool = getToolByName(self.context, 'portal_plonemeeting')
        catalog = getToolByName(self.context, 'portal_catalog')
        meetingPortalType = tool.getMeetingConfig(self.context).getMeetingTypeName()
        # If the current user is a meetingManager (or a Manager),
        # he is able to add a meetingitem to a 'decided' meeting.
        review_state = ['created', 'frozen', ]
        if tool.isManager():
            review_state.extend(('decided', 'in_committee', 'in_council', ))
        res = catalog.unrestrictedSearchResults(
            portal_type=meetingPortalType,
            review_state=review_state,
            sort_on='getDate')
        # Frozen meetings may still accept "late" items.
        return res

    security.declarePublic('getIcons')

    def getIcons(self, inMeeting, meeting):
        '''Check docstring in PloneMeeting interfaces.py.'''
        item = self.getSelf()
        res = []
        itemState = item.queryState()
        # Default PM item icons
        res = res + MeetingItem.getIcons(item, inMeeting, meeting)
        # Add our icons for wf states
        if itemState == 'accepted_but_modified':
            res.append(('accepted_but_modified.png', 'icon_help_accepted_but_modified'))
        elif itemState == 'proposed':
            res.append(('proposeToDirector.png', 'icon_help_proposed_to_director'))
        elif itemState == 'proposed_to_divisionhead':
            res.append(('proposeToDivisionHead.png', 'icon_help_proposed_to_divisionhead'))
        elif itemState == 'proposed_to_officemanager':
            res.append(('proposeToOfficeManager.png', 'icon_help_proposed_to_officemanager'))
        elif itemState == 'item_in_council':
            res.append(('item_in_council.png', 'icon_help_item_in_council'))
        elif itemState == 'item_in_committee':
            res.append(('item_in_committee.png', 'icon_help_item_in_committee'))
        elif itemState == 'proposed_to_servicehead':
            res.append(('proposeToServiceHead.png', 'icon_help_proposed_to_servicehead'))
        elif itemState == 'removed':
            res.append(('removed.png', 'icon_help_removed'))
        return res

    security.declarePublic('updatePowerEditorsLocalRoles')

    def updatePowerEditorsLocalRoles(self):
        '''Give the 'power editors' local role to the corresponding
           MeetingConfig 'powereditors' group on self.'''
        item = self.getSelf()
        # First, remove 'power editor' local roles granted to powereditors.
        item.portal_plonemeeting.removeGivenLocalRolesFor(item,
                                                          role_to_remove=EDITOR_USECASES['power_editors'],
                                                          suffixes=[POWEREDITORS_GROUP_SUFFIX, ])
        # Then, add local roles for powereditors if itemState is itemfrozen.
        itemState = item.queryState()
        if itemState != 'itemfrozen':
            return
        cfg = item.portal_plonemeeting.getMeetingConfig(item)
        powerEditorsGroupId = "%s_%s" % (cfg.getId(), POWEREDITORS_GROUP_SUFFIX)
        item.manage_addLocalRoles(powerEditorsGroupId, (EDITOR_USECASES['power_editors'],))


class CustomMeetingConfig(MeetingConfig):
    '''Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom.'''

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePublic('searchReviewableItems')

    def searchReviewableItems(self, sortKey, sortOrder, filterKey, filterValue, **kwargs):
        '''Returns a list of items that the user could review.'''
        membershipTool = getToolByName(self, 'portal_membership')
        member = membershipTool.getAuthenticatedMember()
        groupsTool = getToolByName(self, 'portal_groups')
        groups = groupsTool.getGroupsForPrincipal(member)
        # the logic is :
        # a user is reviewer for his level of hierarchy and every levels below in a group
        # so find the different groups (a user could be divisionhead in groupA and director in groupB)
        # and find the different states we have to search for this group (proposingGroup of the item)
        reviewSuffixes = ('_reviewers', '_divisionheads', '_officemanagers', '_serviceheads', )
        statesMapping = {'_reviewers': ('proposed_to_servicehead',
                                        'proposed_to_officemanager',
                                        'proposed_to_divisionhead',
                                        'proposed'),
                         '_divisionheads': ('proposed_to_servicehead',
                                            'proposed_to_officemanager',
                                            'proposed_to_divisionhead'),
                         '_officemanagers': ('proposed_to_servicehead',
                                             'proposed_to_officemanager'),
                         '_serviceheads': 'proposed_to_servicehead'}
        foundGroups = {}
        # check that we have a real PM group, not "echevins", or "Administrators"
        for group in groups:
            realPMGroup = False
            for reviewSuffix in reviewSuffixes:
                if group.endswith(reviewSuffix):
                    realPMGroup = True
                    break
            if not realPMGroup:
                continue
            # remove the suffix
            groupPrefix = '_'.join(group.split('_')[:-1])
            if not groupPrefix in foundGroups:
                foundGroups[groupPrefix] = ''
        # now we have the differents services (equal to the MeetingGroup id) the user is in
        strgroups = str(groups)
        for foundGroup in foundGroups:
            for reviewSuffix in reviewSuffixes:
                if "%s%s" % (foundGroup, reviewSuffix) in strgroups:
                    foundGroups[foundGroup] = reviewSuffix
                    break
        # now we have in the dict foundGroups the group the user is in, in the key and the highest level in the value
        res = []
        for foundGroup in foundGroups:
            params = {'Type': unicode(self.getItemTypeName(), 'utf-8'),
                      'getProposingGroup': foundGroup,
                      'review_state': statesMapping[foundGroups[foundGroup]],
                      'sort_on': sortKey,
                      'sort_order': sortOrder}
            # Manage filter
            if filterKey:
                params[filterKey] = prepareSearchValue(filterValue)
            # update params with kwargs
            params.update(kwargs)
            # Perform the query in portal_catalog
            catalog = getToolByName(self, 'portal_catalog')
            brains = catalog(**params)
            res.extend(brains)
        return res
    MeetingConfig.searchReviewableItems = searchReviewableItems

    security.declarePublic('searchItemsOfCommission')

    def searchItemsOfMyCommissions(self, sortKey, sortOrder, filterKey, filterValue, **kwargs):
        '''Return a list of items i'm commissionTranscript writer of
           (user is in Plone group with id 'commission-foo_COMMISSION_EDITORS_SUFFIX)'''
        #get every commission I'm transcript editor for
        commissionEditorsGroupIds = [(commissionId + COMMISSION_EDITORS_SUFFIX) for commissionId in
                                     set(COUNCIL_COMMISSION_IDS).union(set(COUNCIL_COMMISSION_IDS_2013))]
        res = []
        membershipTool = getToolByName(self, 'portal_membership')
        member = membershipTool.getAuthenticatedMember()
        for groupId in member.getGroups():
            if groupId in commissionEditorsGroupIds:
                res.append(groupId)
        #a commission groupId correspond to a category but with an additional suffix (COMMISSION_EDITORS_SUFFIX)
        cats = [cat[:-len(COMMISSION_EDITORS_SUFFIX)] for cat in res]
        #we add the corresponding '1er-supplement' suffixed cat too
        cats = cats + [cat+'-1er-supplement' for cat in cats]
        params = {'Type': unicode(self.getItemTypeName(), 'utf-8'),
                  'getCategory': cats,
                  'sort_on': sortKey,
                  'sort_order': sortOrder
                  }
        # Manage filter
        if filterKey:
            params[filterKey] = prepareSearchValue(filterValue)
        # update params with kwargs
        params.update(kwargs)
        # Perform the query in portal_catalog
        catalog = getToolByName(self, 'portal_catalog')
        return catalog(**params)
    MeetingConfig.searchItemsOfMyCommissions = searchItemsOfMyCommissions

    security.declarePublic('searchItemsOfCommission')

    def searchItemsOfMyCommissionsToEdit(self, sortKey, sortOrder, filterKey, filterValue, **kwargs):
        '''Return a list of items i'm commissionTranscript writer of
           (user is in Plone group with id 'commission-foo_COMMISSION_EDITORS_SUFFIX)
           and I can actually edit (in state 'in_committee')'''
        #get every commission I'm transcript editor for
        commissionEditorsGroupIds = [(commissionId + COMMISSION_EDITORS_SUFFIX) for commissionId in
                                     set(COUNCIL_COMMISSION_IDS).union(set(COUNCIL_COMMISSION_IDS_2013))]
        res = []
        membershipTool = getToolByName(self, 'portal_membership')
        member = membershipTool.getAuthenticatedMember()
        for groupId in member.getGroups():
            if groupId in commissionEditorsGroupIds:
                res.append(groupId)
        #a commission groupId correspond to a category but with an additional suffix (COMMISSION_EDITORS_SUFFIX)
        cats = [cat[:-len(COMMISSION_EDITORS_SUFFIX)] for cat in res]
        #we add the corresponding '1er-supplement' suffixed cat too
        cats = cats + [cat+'-1er-supplement' for cat in cats]
        params = {'Type': unicode(self.getItemTypeName(), 'utf-8'),
                  'getCategory': cats,
                  'review_state': 'item_in_committee',
                  'sort_on': sortKey,
                  'sort_order': sortOrder
                  }
        # Manage filter
        if filterKey:
            params[filterKey] = prepareSearchValue(filterValue)
        # update params with kwargs
        params.update(kwargs)
        # Perform the query in portal_catalog
        catalog = getToolByName(self, 'portal_catalog')
        return catalog(**params)
    MeetingConfig.searchItemsOfMyCommissionsToEdit = searchItemsOfMyCommissionsToEdit

    security.declarePrivate('createPowerObserversGroup')

    def createPowerEditorsGroup(self):
        '''Creates a Plone group that will be used to apply the 'Editor'
           local role on every items in itemFrozen state.'''
        meetingConfig = self.getSelf()
        groupId = "%s_%s" % (meetingConfig.getId(), POWEREDITORS_GROUP_SUFFIX)
        if not groupId in meetingConfig.portal_groups.listGroupIds():
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

    def onEdit(self, isCreated):
        self.context.createPowerEditorsGroup()


class CustomMeetingGroup(MeetingGroup):
    '''Adapter that adapts a meetingGroup implementing IMeetingGroup to the
       interface IMeetingGroupCustom.'''

    implements(IMeetingGroupCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePrivate('validate_signatures')

    def validate_signatures(self, value):
        '''Validate the MeetingGroup.signatures field.'''
        if value.strip() and not len(value.split('\n')) == 12:
            return self.utranslate('signatures_length_error', domain='PloneMeeting')
    MeetingGroup.validate_signatures = validate_signatures


class MeetingCollegeSeraingWorkflowActions(MeetingWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeWorkflowActions'''

    implements(IMeetingCollegeSeraingWorkflowActions)
    security = ClassSecurityInfo()

    def _adaptEveryItemsOnMeetingClosure(self):
        """Helper method for accepting every items."""
        # Every item that is not decided will be automatically set to "accepted"
        wfTool = getToolByName(self.context, 'portal_workflow')
        for item in self.context.getAllItems():
            if item.queryState() == 'presented':
                wfTool.doActionFor(item, 'itemfreeze')
            if item.queryState() in ['itemfrozen', ]:
                wfTool.doActionFor(item, 'accept')

    security.declarePrivate('doDecide')

    def doDecide(self, stateChange):
        '''We pass every item that is 'presented' in the 'itemfrozen'
           state.  It is the case for late items.'''
        wfTool = getToolByName(self.context, 'portal_workflow')
        for item in self.context.getAllItems(ordered=False):
            if item.queryState() == 'presented':
                wfTool.doActionFor(item, 'itemfreeze')

    security.declarePrivate('doFreeze')

    def doFreeze(self, stateChange):
        '''When freezing the meeting, every items must be automatically set to
           "itemfrozen".'''
        wfTool = getToolByName(self.context, 'portal_workflow')
        for item in self.context.getAllItems(ordered=True):
            if item.queryState() == 'presented':
                wfTool.doActionFor(item, 'itemfreeze')
        #manage meeting number
        self.initSequenceNumber()

    security.declarePrivate('doBackToCreated')

    def doBackToCreated(self, stateChange):
        '''When a meeting go back to the "created" state, for example the
           meeting manager wants to add an item, we do not do anything.'''
        pass


class MeetingCollegeSeraingWorkflowConditions(MeetingWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeWorkflowConditions'''

    implements(IMeetingCollegeSeraingWorkflowConditions)
    security = ClassSecurityInfo()

    security.declarePublic('mayFreeze')

    def mayFreeze(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            res = True  # At least at present
            if not self.context.getRawItems():
                res = No(self.context.utranslate('item_required_to_publish'))
        return res

    security.declarePublic('mayClose')

    def mayClose(self):
        res = False
        # The user just needs the "Review portal content" permission on the
        # object to close it.
        if checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayDecide')

    def mayDecide(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context) and \
           (not self._allItemsAreDelayed()):
            res = True
        return res

    security.declarePublic('mayChangeItemsOrder')

    def mayChangeItemsOrder(self):
        '''We can change the order if the meeting is not closed'''
        res = False
        if checkPermission(ModifyPortalContent, self.context) and \
           self.context.queryState() not in ('closed'):
            res = True
        return res

    def mayCorrect(self):
        '''Take the default behaviour except if the meeting is frozen
           we still have the permission to correct it.'''
        from Products.PloneMeeting.Meeting import MeetingWorkflowConditions
        res = MeetingWorkflowConditions.mayCorrect(self)
        currentState = self.context.queryState()
        if res is not True and currentState == "frozen":
            # Change the behaviour for being able to correct a frozen meeting
            # back to created.
            if checkPermission(ReviewPortalContent, self.context):
                return True
        return res


class MeetingItemCollegeSeraingWorkflowActions(MeetingItemWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCollegeWorkflowActions'''

    implements(IMeetingItemCollegeSeraingWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doAccept_but_modify')

    def doAccept_but_modify(self, stateChange):
        pass

    security.declarePrivate('doRemove')

    def doRemove(self, stateChange):
        pass

    security.declarePrivate('doProposeToServiceHead')

    def doProposeToServiceHead(self, stateChange):
        pass

    security.declarePrivate('doPropose')

    def doPropose(self, stateChange):
        pass

    security.declarePrivate('doProposeToOfficeManager')

    def doProposeToOfficeManager(self, stateChange):
        pass

    security.declarePrivate('doProposeToDivisionHead')

    def doProposeToDivisionHead(self, stateChange):
        pass

    security.declarePrivate('doDelay')

    def doDelay(self, stateChange):
        '''When an item is delayed, we will duplicate it: the copy is back to
           the validate state and will be linked to this one.
           After, we replace decision for initial items'''
        creator = self.context.Creator()
        # We create a copy in the initial item state, in the folder of creator.
        clonedItem = self.context.clone(copyAnnexes=True, newOwnerId=creator,
                                        cloneEventAction='create_from_predecessor')
        clonedItem.setPredecessor(self.context)
        # Send, if configured, a mail to the person who created the item
        clonedItem.sendMailIfRelevant('itemDelayed', 'Owner', isRole=True)
        meetingConfig = self.context.portal_plonemeeting.getMeetingConfig(self.context)
        itemDecisionReportText = meetingConfig.getItemDecisionReportText()
        if itemDecisionReportText.strip():
            from Products.CMFCore.Expression import Expression, createExprContext
            portal = self.context.portal_url.getPortalObject()
            ctx = createExprContext(self.context.getParentNode(), portal, self.context)
            try:
                res = Expression(itemDecisionReportText)(ctx)
            except Exception, e:
                self.context.portal_plonemeeting.plone_utils.addPortalMessage(PloneMeetingError('%s' % str(e)))
                return
            self.context.setDecision(res)
        self.context.portal_workflow.doActionFor(clonedItem, 'validate')


class MeetingItemCollegeSeraingWorkflowConditions(MeetingItemWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCollegeWorkflowConditions'''

    implements(IMeetingItemCollegeSeraingWorkflowConditions)
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
        self.sm = getSecurityManager()

    security.declarePublic('mayDecide')

    def mayDecide(self):
        '''We may decide an item if the linked meeting is in the 'decided'
           state.'''
        res = False
        meeting = self.context.getMeeting()
        if checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['decided', 'closed', 'decisions_published', ]):
            res = True
        return res

    security.declarePublic('mayDelay')

    def mayDelay(self):
        '''Only 'Manager' may delay an item, it is for history reasons because now this is not
           used anymore but some old items were 'delayed'...'''
        tool = getToolByName(self.context, 'portal_plonemeeting')
        if tool.isManager(realManagers=True):
            return True
        return False

    security.declarePublic('mayValidate')

    def mayValidate(self):
        """
          Either the Director or the MeetingManager can validate
          The MeetingManager can bypass the validation process and validate an item
          that is in the state 'itemcreated'
        """
        res = False
        #first of all, the use must have the 'Review portal content permission'
        if checkPermission(ReviewPortalContent, self.context):
            res = True
            #if the current item state is 'itemcreated', only the MeetingManager can validate
            tool = getToolByName(self.context, 'portal_plonemeeting')
            if self.context.queryState() in ('itemcreated',) and not tool.isManager():
                res = False
        return res

    security.declarePublic('mayFreeze')

    def mayFreeze(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in ('frozen', 'decided', 'closed')):
                res = True
        return res

    security.declarePublic('mayCorrect')

    def mayCorrect(self):
        # Check with the default PloneMeeting method and our test if res is
        # False. The diffence here is when we correct an item from itemfrozen to
        # presented, we have to check if the Meeting is in the "created" state
        # and not "published".
        res = MeetingItemWorkflowConditions.mayCorrect(self)
        # Manage our own behaviour now when the item is linked to a meeting,
        # a MeetingManager can correct anything except if the meeting is closed
        if res is not True:
            if checkPermission(ReviewPortalContent, self.context):
                # Get the meeting
                meeting = self.context.getMeeting()
                if meeting:
                    # Meeting can be None if there was a wf problem leading
                    # an item to be in a "presented" state with no linked
                    # meeting.
                    meetingState = meeting.queryState()
                    # A user having ReviewPortalContent permission can correct
                    # an item in any case except if the meeting is closed.
                    if meetingState != 'closed':
                        res = True
                else:
                    res = True
        return res

    security.declarePublic('mayProposeToServiceHead')

    def mayProposeToServiceHead(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToOfficeManager')

    def mayProposeToOfficeManager(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToDivisionHead')

    def mayProposeToDivisionHead(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeT')

    def mayPropose(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayRemove')

    def mayRemove(self):
        """
          We may remove an item if the linked meeting is in the 'decided'
          state.  For now, this is the same behaviour as 'mayDecide'
        """
        res = False
        meeting = self.context.getMeeting()
        if checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['decided', 'closed']):
            res = True
        return res


class MeetingCouncilSeraingWorkflowActions(MeetingWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCouncilWorkflowActions'''

    implements(IMeetingCouncilSeraingWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doSetInCommittee')

    def doSetInCommittee(self, stateChange):
        '''When setting the meeting in committee, every items must be automatically
           set to "item_in_committee".'''
        wfTool = getToolByName(self.context, 'portal_workflow')
        for item in self.context.getAllItems(ordered=True):
            if item.queryState() == 'presented':
                wfTool.doActionFor(item, 'setItemInCommittee')
        #manage meeting number
        self.initSequenceNumber()

    security.declarePrivate('doSetInCouncil')

    def doSetInCouncil(self, stateChange):
        '''When setting the meeting in council, every items must be automatically
           set to "item_in_council".'''
        wfTool = getToolByName(self.context, 'portal_workflow')
        for item in self.context.getAllItems(ordered=True):
            if item.queryState() == 'presented':
                wfTool.doActionFor(item, 'setItemInCommittee')
            if item.queryState() == 'item_in_committee':
                wfTool.doActionFor(item, 'setItemInCouncil')

    def _adaptEveryItemsOnMeetingClosure(self):
        """Helper method for accepting every items."""
        # Every item that is not decided will be automatically set to "accepted"
        wfTool = getToolByName(self.context, 'portal_workflow')
        for item in self.context.getAllItems():
            if item.queryState() == 'presented':
                wfTool.doActionFor(item, 'setItemInCommittee')
            if item.queryState() == 'item_in_committee':
                wfTool.doActionFor(item, 'setItemInCouncil')
            if item.queryState() == 'item_in_council':
                wfTool.doActionFor(item, 'accept')

    security.declarePrivate('doBackToCreated')

    def doBackToCreated(self, stateChange):
        '''When a meeting go back to the "created" state, for example the
           meeting manager wants to add an item, we do not do anything.'''
        pass

    security.declarePrivate('doBackToInCommittee')

    def doBackToInCommittee(self, stateChange):
        '''When a meeting go back to the "in_committee" we set every items 'in_council' back to 'in_committee'.'''
        wfTool = getToolByName(self.context, 'portal_workflow')
        for item in self.context.getAllItems():
            if item.queryState() == 'item_in_council':
                wfTool.doActionFor(item, 'backToItemInCommittee')

    security.declarePrivate('doBackToInCouncil')

    def doBackToInCouncil(self, stateChange):
        '''When a meeting go back to the "in_council" we do not do anything.'''
        pass


class MeetingCouncilSeraingWorkflowConditions(MeetingWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCouncilWorkflowConditions'''

    implements(IMeetingCouncilSeraingWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting
        customAcceptItemsStates = ('created', 'in_committee', 'in_council', )
        self.acceptItemsStates = customAcceptItemsStates

    security.declarePublic('maySetInCommittee')

    def maySetInCommittee(self):
        res = False
        # The user just needs the "Review portal content" permission
        if checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('maySetInCouncil')

    def maySetInCouncil(self):
        # The user just needs the "Review portal content" permission
        if not checkPermission(ReviewPortalContent, self.context):
            return False
        return True

    security.declarePublic('mayClose')

    def mayClose(self):
        res = False
        # The user just needs the "Review portal content" permission on the
        # object to close it.
        if checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayChangeItemsOrder')

    def mayChangeItemsOrder(self):
        '''We can change the order if the meeting is not closed'''
        res = False
        if checkPermission(ModifyPortalContent, self.context) and \
           self.context.queryState() not in ('closed', ):
            res = True
        return res

    def mayCorrect(self):
        '''Take the default behaviour except if the meeting is frozen
           we still have the permission to correct it.'''
        from Products.PloneMeeting.Meeting import MeetingWorkflowConditions
        res = MeetingWorkflowConditions.mayCorrect(self)
        currentState = self.context.queryState()
        if res is not True and currentState in ('in_committee', 'in_council', ):
            # Change the behaviour for being able to correct a frozen meeting
            # back to created.
            if checkPermission(ReviewPortalContent, self.context):
                return True
        return res


class MeetingItemCouncilSeraingWorkflowActions(MeetingItemWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCouncilWorkflowActions'''

    implements(IMeetingItemCouncilSeraingWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doPropose')

    def doPropose(self, stateChange):
        pass

    security.declarePrivate('doSetItemInCommittee')

    def doSetItemInCommittee(self, stateChange):
        pass

    security.declarePrivate('doSetItemInCouncil')

    def doSetItemInCouncil(self, stateChange):
        pass

    security.declarePrivate('doReturn_to_proposing_group')

    def doReturn_to_proposing_group(self, stateChange):
        '''Send an email to the creator and to the officemanagers'''
        self.context.sendMailIfRelevant('returnedToProposingGroup', 'MeetingMember', isRole=True)
        self.context.sendMailIfRelevant('returnedToProposingGroup', 'MeetingOfficeManager', isRole=True)

    security.declarePrivate('doBackToItemInCommittee')

    def doBackToItemInCommittee(self, stateChange):
        pass

    security.declarePrivate('doBackToItemInCouncil')

    def doBackToItemInCouncil(self, stateChange):
        pass

    security.declarePrivate('doAccept_but_modify')

    def doAccept_but_modify(self, stateChange):
        pass

    security.declarePrivate('doDelay')

    def doDelay(self, stateChange):
        '''When an item is delayed, by default it is duplicated but we do not
           duplicate it here'''
        pass


class MeetingItemCouncilSeraingWorkflowConditions(MeetingItemWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCouncilWorkflowConditions'''

    implements(IMeetingItemCouncilSeraingWorkflowConditions)
    security = ClassSecurityInfo()

    useHardcodedTransitionsForPresentingAnItem = True
    transitionsForPresentingAnItem = ('propose', 'validate', 'present')

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem
        self.sm = getSecurityManager()

    security.declarePublic('mayPropose')

    def mayPropose(self):
        """
          Check that the user has the 'Review portal content'
          If the item comes from the college, check that it has a defined
          'category'
        """
        # In the case the item comes from the college
        if not self.context.getCategory():
            return False
        if checkPermission(ReviewPortalContent, self.context) and \
           (not self.context.isDefinedInTool()):
            return True
        return False

    security.declarePublic('isLateFor')

    def isLateFor(self, meeting):
        """
          No late functionnality for Council
        """
        return False

    security.declarePublic('maySetItemInCommittee')

    def maySetItemInCommittee(self):
        """
          Check that the user has the 'Review portal content'
          And that the linked meeting is in the correct state
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in
               ('in_committee', 'in_council', 'closed')):
                res = True
        return res

    security.declarePublic('maySetItemInCouncil')

    def maySetItemInCouncil(self):
        """
          Check that the user has the 'Review portal content'
          And that the linked meeting is in the correct state
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in
               ('in_council', 'closed')):
                res = True
        return res

    security.declarePublic('mayDecide')

    def mayDecide(self):
        '''We may decide an item if the linked meeting is in the 'decided'
           state.'''
        res = False
        meeting = self.context.getMeeting()
        if checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['in_council', 'closed']):
            res = True
        return res

    security.declarePublic('mayCorrect')

    def mayCorrect(self):
        # Check with the default PloneMeeting method and our test if res is
        # False. The diffence here is when we correct an item from itemfrozen to
        # presented, we have to check if the Meeting is in the "created" state
        # and not "published".
        res = MeetingItemWorkflowConditions.mayCorrect(self)
        # Manage our own behaviour now when the item is linked to a meeting,
        # a MeetingManager can correct anything except if the meeting is closed
        if res is not True:
            if checkPermission(ReviewPortalContent, self.context):
                # Get the meeting
                meeting = self.context.getMeeting()
                if meeting:
                    # Meeting can be None if there was a wf problem leading
                    # an item to be in a "presented" state with no linked
                    # meeting.
                    meetingState = meeting.queryState()
                    # A user having ReviewPortalContent permission can correct
                    # an item in any case except if the meeting is closed.
                    if meetingState != 'closed':
                        res = True
                else:
                    res = True
        return res


class CustomToolPloneMeeting(ToolPloneMeeting):
    '''Adapter that adapts a tool implementing ToolPloneMeeting to the
       interface IToolPloneMeetingCustom'''

    implements(IToolPloneMeetingCustom)
    security = ClassSecurityInfo()

    security.declarePublic('updatePowerEditors')

    def updatePowerEditors(self):
        '''Update local_roles regarging the PowerEditors for every items.'''
        if not self.context.isManager(realManagers=True):
            raise Unauthorized
        for b in self.context.portal_catalog(meta_type=('MeetingItem')):
            obj = b.getObject()
            obj.updatePowerEditorsLocalRoles()
            # Update security
            obj.reindexObject(idxs=['allowedRolesAndUsers', ])
        self.context.plone_utils.addPortalMessage('Done.')
        self.context.gotoReferer()

# ------------------------------------------------------------------------------
InitializeClass(CustomMeetingItem)
InitializeClass(CustomMeeting)
InitializeClass(CustomMeetingConfig)
InitializeClass(CustomMeetingGroup)
InitializeClass(MeetingCollegeSeraingWorkflowActions)
InitializeClass(MeetingCollegeSeraingWorkflowConditions)
InitializeClass(MeetingItemCollegeSeraingWorkflowActions)
InitializeClass(MeetingItemCollegeSeraingWorkflowConditions)
InitializeClass(MeetingCouncilSeraingWorkflowActions)
InitializeClass(MeetingCouncilSeraingWorkflowConditions)
InitializeClass(MeetingItemCouncilSeraingWorkflowActions)
InitializeClass(MeetingItemCouncilSeraingWorkflowConditions)
InitializeClass(CustomToolPloneMeeting)
# ------------------------------------------------------------------------------
