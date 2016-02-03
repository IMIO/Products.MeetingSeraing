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
from Products.Archetypes.atapi import DisplayList
from Products.CMFCore.permissions import ReviewPortalContent, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from imio.helpers.xhtml import xhtmlContentIsEmpty
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.model.adaptations import WF_DOES_NOT_EXIST_WARNING, \
    WF_APPLIED, RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE
from Products.PloneMeeting.utils import checkPermission, prepareSearchValue
from Products.PloneMeeting.Meeting import MeetingWorkflowActions, \
    MeetingWorkflowConditions, Meeting
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingGroup import MeetingGroup
from Products.PloneMeeting.interfaces import IMeetingCustom, IMeetingItemCustom, \
    IMeetingConfigCustom, IMeetingGroupCustom, IToolPloneMeetingCustom, IMeetingItem
from Products.MeetingSeraing.interfaces import \
    IMeetingItemCollegeSeraingWorkflowConditions, IMeetingItemCollegeSeraingWorkflowActions,\
    IMeetingCollegeSeraingWorkflowConditions, IMeetingCollegeSeraingWorkflowActions
from Products.MeetingSeraing.config import EDITOR_USECASES, POWEREDITORS_GROUP_SUFFIX
from zope.i18n import translate
from Products.PloneMeeting.ToolPloneMeeting import ToolPloneMeeting
from DateTime import DateTime
from Products.CMFCore.permissions import DeleteObjects


# disable most of wfAdaptations
customWfAdaptations = ('return_to_proposing_group', 'returned_to_advise')
MeetingConfig.wfAdaptations = customWfAdaptations
originalPerformWorkflowAdaptations = adaptations.performWorkflowAdaptations

# configure parameters for the returned_to_proposing_group wfAdaptation
# we keep also 'itemfrozen' and 'itempublished' in case this should be activated for meeting-config-college...

CUSTOM_RETURN_TO_PROPOSING_GROUP_MAPPINGS = {'backTo_presented_from_returned_to_proposing_group':
                                             ['created', ],
                                             'backTo_itempublished_from_returned_to_proposing_group':
                                             ['published', ],
                                             'backTo_itemfrozen_from_returned_to_proposing_group':
                                             ['frozen', 'decided', 'decisions_published', ],
                                             'backTo_presented_from_returned_to_advise':
                                             ['created', ],
                                             'backTo_itempublished_from_returned_to_advise':
                                             ['published', ],
                                             'backTo_itemfrozen_from_returned_to_advise':
                                             ['frozen', 'decided', 'decisions_published', ],
                                             'backTo_returned_to_proposing_group_from_returned_to_advise':
                                             ['frozen', 'decided', 'decisions_published', ],
                                             'NO_MORE_RETURNABLE_STATES': ['closed', 'archived', ]
                                             }
adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS = CUSTOM_RETURN_TO_PROPOSING_GROUP_MAPPINGS

RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'itemfrozen', 'itempublished',
                                              'item_in_committee', 'item_in_council', )
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES
RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {
    # view permissions
    'Access contents information':
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
    'PloneMeeting: Read optional advisers':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read decision annex':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read item observations':
    ('Manager', 'MeetingManager', ),
    'MeetingSeraing: Read commission transcript':
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
    'PloneMeeting: Add MeetingFile':
    ('Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', 'Editor', ),
    'PloneMeeting: Write decision annex':
    ('Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ),
    'PloneMeeting: Write optional advisers':
    ('Manager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager', ),
    # MeetingManagers edit permissions
    'Delete objects':
    ('Manager', 'MeetingManager', ),
    'PloneMeeting: Write item observations':
    ('Manager', 'MeetingManager', ),
    'MeetingSeraing: Write commission transcript':
    ('Manager', 'MeetingManager', ),
}
adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS

RETURN_TO_ADVISE_CUSTOM_PERMISSIONS = {
    # view permissions
    'Access contents information':
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
    'PloneMeeting: Read optional advisers':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read decision annex':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'PloneMeeting: Read item observations':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingServiceHead', 'MeetingOfficeManager',
     'MeetingDivisionHead', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', 'Editor', ),
    'MeetingSeraing: Read commission transcript':
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
    'PloneMeeting: Add MeetingFile':
    ('Manager', 'MeetingManager', ),
    'PloneMeeting: Write decision annex':
    ('Manager',  'MeetingManager', ),
    'PloneMeeting: Write optional advisers':
    ('Manager', 'MeetingManager', ),
    # MeetingManagers edit permissions
    'Delete objects':
    ('Manager', 'MeetingManager', ),
    'PloneMeeting: Write item observations':
    ('Manager', 'MeetingManager', ),
    'MeetingSeraing: Write commission transcript':
    ('Manager', 'MeetingManager', ),
}

from Products.PloneMeeting.MeetingItem import MeetingItem, \
    MeetingItemWorkflowConditions, MeetingItemWorkflowActions


def customPerformWorkflowAdaptations(site, meetingConfig, logger, specificAdaptation=None):
    '''This function applies workflow changes as specified by the
       p_meetingConfig.'''

    wfAdaptations = specificAdaptation and [specificAdaptation, ] or meetingConfig.getWorkflowAdaptations()

    #while reinstalling a separate profile, the workflow could not exist
    wfTool = getToolByName(site, 'portal_workflow')
    meetingWorkflow = getattr(wfTool, meetingConfig.getMeetingWorkflow(), None)
    if not meetingWorkflow:
        logger.warning(WF_DOES_NOT_EXIST_WARNING % meetingConfig.getMeetingWorkflow())
        return
    itemWorkflow = getattr(wfTool, meetingConfig.getItemWorkflow(), None)
    if not itemWorkflow:
        logger.warning(WF_DOES_NOT_EXIST_WARNING % meetingConfig.getItemWorkflow())
        return

    error = meetingConfig.validate_workflowAdaptations(wfAdaptations)
    if error:
        raise Exception(error)

    for wfAdaptation in wfAdaptations:

        if not wfAdaptation in ['returned_to_advise', ]:
            # call original perform of PloneMeeting
            originalPerformWorkflowAdaptations(site, meetingConfig, logger, specificAdaptation=wfAdaptation)
        # when an item is linked to a meeting, most of times, creators lose modify rights on it
        # with this, the item can be 'returned_to_proposing_group' when in a meeting then the creators
        # can modify it if necessary and send it back to the MeetingManagers when done
        elif wfAdaptation == 'returned_to_advise':
            itemStates = itemWorkflow.states
            if 'returned_to_advise' not in itemStates and 'returned_to_proposing_group' in itemStates:
                # add the 'returned_to_advise' state and clone the
                # permissions from RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE
                # and apply permissions defined in RETURN_TO_ADVISE_CUSTOM_PERMISSIONS
                return_to_advice_item_state = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES + \
                    ('returned_to_proposing_group', )
                itemWorkflow.states.addState('returned_to_advise')
                newState = getattr(itemWorkflow.states, 'returned_to_advise')
                # clone the permissions of the given RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE if it exists
                cloned_permissions_with_meetingmanager = {}
                if hasattr(itemWorkflow.states, RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE):
                    stateToClone = getattr(itemWorkflow.states, RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE)
                    # we must make sure the MeetingManagers still may access this item
                    # so add MeetingManager role to every cloned permissions
                    cloned_permissions = dict(stateToClone.permission_roles)
                    # we need to use an intermediate dict because roles are stored as a tuple and we need a list...
                    for permission in cloned_permissions:
                        # the acquisition is defined like this : if permissions is a tuple, it is not acquired
                        # if it is a list, it is acquired...  WTF???  So make sure we store the correct type...
                        acquired = isinstance(cloned_permissions[permission], list) and True or False
                        cloned_permissions_with_meetingmanager[permission] = list(cloned_permissions[permission])
                        if not 'MeetingManager' in cloned_permissions[permission]:
                            cloned_permissions_with_meetingmanager[permission].append('MeetingManager')
                        if not acquired:
                            cloned_permissions_with_meetingmanager[permission] = \
                                tuple(cloned_permissions_with_meetingmanager[permission])
                # now apply custom permissions defined in RETURN_TO_ADVISE_CUSTOM_PERMISSIONS
                cloned_permissions_with_meetingmanager.update(RETURN_TO_ADVISE_CUSTOM_PERMISSIONS)

                # if we are cloning an existing state permissions, make sure DeleteObjects
                # is only be availble to ['Manager', 'MeetingManager']
                # if custom permissions are defined, keep what is defined in it
                if not DeleteObjects in RETURN_TO_ADVISE_CUSTOM_PERMISSIONS:
                    del_obj_perm = stateToClone.getPermissionInfo(DeleteObjects)
                    if del_obj_perm['acquired']:
                        cloned_permissions_with_meetingmanager[DeleteObjects] = ['Manager', ]
                    else:
                        cloned_permissions_with_meetingmanager[DeleteObjects] = ('Manager', )

                # finally, apply computed permissions, aka cloned + custom
                newState.permission_roles = cloned_permissions_with_meetingmanager
                # now create the necessary transitions : one to go to 'returned_to_proposing_group' state
                # and x to go back to relevant state depending on current meeting state
                # first, the transition 'return_to_advise'
                itemWorkflow.transitions.addTransition('return_to_advise')
                transition = itemWorkflow.transitions['return_to_advise']
                #use same guard from ReturnToProposingGroup
                transition.setProperties(
                    title='return_to_advise',
                    new_state_id='returned_to_advise', trigger_type=1, script_name='',
                    actbox_name='return_to_advise', actbox_url='', actbox_category='workflow',
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
                    transition.setProperties(
                        title='return_to_meeting',
                        new_state_id=stateName, trigger_type=1, script_name='',
                        actbox_name=transitionName, actbox_url='', actbox_category='workflow',
                        props={'guard_expr': 'python:here.wfConditions().mayBackToMeeting("%s")' % transitionName})
                # now that we created back transitions, we can assign them to newState 'returned_to_advise'
                            # set properties for new 'returned_to_advise' state
                newState.setProperties(
                    title='returned_to_advise', description='',
                    transitions=newTransitionNames)
            logger.info(WF_APPLIED % ("return_to_proposing_group", meetingConfig.getId()))

adaptations.performWorkflowAdaptations = customPerformWorkflowAdaptations


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
                                    excludedCategories=[], groupIds=[], firstNumber=1, renumber=False,
                                    includeEmptyCategories=False, includeEmptyGroups=False, isToPrintInMeeting='both',
                                    forceCategOrderFromConfig=False):
        '''Returns a list of (late or normal or both) items (depending on p_late)
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
           In this case, the firstNumber value can be used.'''
        # The result is a list of lists, where every inner list contains:
        # - at position 0: the category object (MeetingCategory or MeetingGroup)
        # - at position 1 to n: the items in this category
        # If by_proposing_group is True, the structure is more complex.
        # late can be 'both' or False or True
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        # privacy can be '*' or 'public' or 'secret'
        # Every inner list contains:
        # - at position 0: the category object
        # - at positions 1 to n: inner lists that contain:
        #   * at position 0: the proposing group object
        #   * at positions 1 to n: the items belonging to this group.
        #work only for groups...
        def _comp(v1, v2):
            if v1[0].getOrder(onlyActive=False) < v2[0].getOrder(onlyActive=False):
                return -1
            elif v1[0].getOrder(onlyActive=False) > v2[0].getOrder(onlyActive=False):
                return 1
            else:
                return 0
        res = []
        items = []
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
                elif groupIds and not item.getProposingGroup() in groupIds:
                    continue
                elif categories and not item.getCategory() in categories:
                    continue
                elif excludedCategories and item.getCategory() in excludedCategories:
                    continue
                elif not (isToPrintInMeeting == 'both' or item.getIsToPrintInMeeting() == isToPrintInMeeting):
                    continue
                currentCat = item.getCategory(theObject=True)
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
        if forceCategOrderFromConfig or late == 'both':
            res.sort(cmp=_comp)
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

    security.declarePublic('getAllItemsToPrintingOrNot')

    def getAllItemsToPrintingOrNot(self, uids=[], ordered=False, toPrint='True'):
        res = []
        items = self.context.getAllItems(uids, ordered)
        for item in items:
            if (toPrint and item.getIsToPrintInMeeting()) or not(toPrint or item.getIsToPrintInMeeting()):
                res.append(item)
        return res

    security.declarePublic('getOJByCategory')

    def getOJByCategory(self, itemUids=[], late=False,
                        ignore_review_states=[], by_proposing_group=False, group_prefixes={},
                        privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                        excludedCategories=[], groupIds=[], firstNumber=1, renumber=False,
                        includeEmptyCategories=False, includeEmptyGroups=False, isToPrintInMeeting='both',
                        forceCategOrderFromConfig=False):
        lists = self.context.getPrintableItemsByCategory(itemUids, late, ignore_review_states, by_proposing_group,
                                                         group_prefixes, privacy, oralQuestion, toDiscuss, categories,
                                                         excludedCategories, groupIds, firstNumber, renumber,
                                                         includeEmptyCategories, includeEmptyGroups,
                                                         isToPrintInMeeting, forceCategOrderFromConfig)
        res = []
        for sub_list in lists:
            #we use by categories, first element of each obj is a category
            final_res = [sub_list[0]]
            find_late = False
            for obj in sub_list[1:]:
                final_items = []
                #obj contain list like this [(num1, item1), (num2, item2), (num3, item3), (num4, item4)]
                for sub_obj in obj:
                    #separate normal items and late items
                    if not find_late and IMeetingItem.providedBy(sub_obj) and sub_obj.isLate():
                        final_items.append('late')
                        find_late = True
                    final_items.append(sub_obj)
                final_res.append(final_items)
            res.append(final_res)
        return res

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

old_setTakenOverBy = MeetingItem.setTakenOverBy


class CustomMeetingItem(MeetingItem):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom.'''
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    security.declarePublic('itemPositiveDecidedStates')

    def itemPositiveDecidedStates(self):
        '''See doc in interfaces.py.'''
        return ('accepted', 'accepted_but_modified', )

    customItemDecidedStates = ('accepted', 'delayed', 'accepted_but_modified', )
    MeetingItem.itemDecidedStates = customItemDecidedStates

    customBeforePublicationStates = ('itemcreated',
                                     'proposed_to_servicehead',
                                     'proposed_to_officemanager',
                                     'proposed_to_divisionhead',
                                     'proposed',
                                     'validated', )
    MeetingItem.beforePublicationStates = customBeforePublicationStates
    #this list is used by doPresent defined in PloneMeeting
    customMeetingAlreadyFrozenStates = ('validated_by_dga', 'frozen', 'decided', )
    MeetingItem.meetingAlreadyFrozenStates = customMeetingAlreadyFrozenStates

    customMeetingNotClosedStates = ('validated_by_dga', 'frozen', 'decided', )
    MeetingItem.meetingNotClosedStates = customMeetingNotClosedStates

    customMeetingTransitionsAcceptingRecurringItems = ('_init_', 'validated_by_dga', 'freeze', 'decide', )
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
        elif itemState == 'validated_by_dga':
            res.append(('itemValidateByDGA.png', 'icon_help_validated_by_dga'))
        elif itemState == 'proposed_to_servicehead':
            res.append(('proposeToServiceHead.png', 'icon_help_proposed_to_servicehead'))
        elif itemState == 'accepted_but_modified_closed':
            res.append(('accepted_but_modified.png', 'icon_help_accepted_but_modified_closed'))
        elif itemState == 'delayed_closed':
            res.append(('delayed.png', 'icon_help_delayed_closed'))
        elif itemState == 'returned_to_advise':
            res.append(('returned_to_advise.png', 'icon_help_returned_to_advise'))
        if item.getIsToPrintInMeeting():
            res.append(('toPrint.png', 'icon_help_to_print'))
        return res

    def _initDecisionFieldIfEmpty(self):
        '''
          If decision field is empty, it will be initialized
          with data coming from title and description.
        '''
        # set keepWithNext to False as it will add a 'class' and so
        # xhtmlContentIsEmpty will never consider it empty...
        if xhtmlContentIsEmpty(self.getDeliberation(keepWithNext=False)):
            self.setDecision("<p>%s</p>%s" % (self.Title(),
                                              self.Description()))
            self.reindexObject()
    MeetingItem._initDecisionFieldIfEmpty = _initDecisionFieldIfEmpty

    security.declarePublic('updatePowerEditorsLocalRoles')

    def updatePowerEditorsLocalRoles(self):
        '''Give the 'power editors' local role to the corresponding
           MeetingConfig 'powereditors' group on self.'''
        item = self.getSelf()
        # First, remove 'power editor' local roles granted to powereditors.
        item.portal_plonemeeting.removeGivenLocalRolesFor(item,
                                                          role_to_remove=EDITOR_USECASES['power_editors'],
                                                          suffixes=[POWEREDITORS_GROUP_SUFFIX, ])
        # Then, add local roles for powereditors.
        cfg = item.portal_plonemeeting.getMeetingConfig(item)
        powerEditorsGroupId = "%s_%s" % (cfg.getId(), POWEREDITORS_GROUP_SUFFIX)
        item.manage_addLocalRoles(powerEditorsGroupId, (EDITOR_USECASES['power_editors'],))

    def getExtraFieldsToCopyWhenCloning(self, cloned_to_same_mc):
        '''
          Keep some new fields when item is cloned (to another mc or from itemtemplate).
        '''
        res = ['interventions', 'isToPrintInMeeting', 'pvNote', 'dgNote']
        if cloned_to_same_mc:
            res = res + []
        return res

    security.declarePublic('mayTakeOver')

    def mayTakeOver(self):
        '''Condition for editing 'takenOverBy' field.
           A member may take an item over if he is able to modify item.'''
        return checkPermission(ModifyPortalContent, self.context)

    security.declarePublic('setTakenOverBy')

    def setTakenOverBy(self, value, **kwargs):
        #call original method
        old_setTakenOverBy(self, value, **kwargs)
        item = self.getSelf()
        if not item._at_creation_flag:
            wf_states_to_keep = ['presented', 'validated_by_dga', 'itemfrozen', 'accepted_but_modified', 'accepted']
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

    security.declarePublic('listCdldProposingGroup')

    def listCdldProposingGroup(self):
        '''Returns a list of groups that can be selected for cdld synthesis field
        '''
        tool = getToolByName(self, 'portal_plonemeeting')
        res = []
        # add delay-aware optionalAdvisers
        customAdvisers = self.getSelf().getCustomAdvisers()
        for customAdviser in customAdvisers:
            groupId = customAdviser['group']
            groupDelay = customAdviser['delay']
            groupDelayLabel = customAdviser['delay_label']
            group = getattr(tool, groupId, None)
            groupKey = '%s__%s__(%s)' % (groupId, groupDelay, groupDelayLabel)
            groupValue = '%s - %s (%s)' % (group.Title(), groupDelay, groupDelayLabel)
            if group:
                res.append((groupKey, groupValue))
        # only let select groups for which there is at least one user in
        nonEmptyMeetingGroups = tool.getMeetingGroups(notEmptySuffix='advisers')
        if nonEmptyMeetingGroups:
            for mGroup in nonEmptyMeetingGroups:
                res.append(('%s____' % mGroup.getId(), mGroup.getName()))
        res = DisplayList(res)
        return res
    MeetingConfig.listCdldProposingGroup = listCdldProposingGroup

    security.declarePublic('searchCDLDItems')

    def searchCDLDItems(self, sortKey='', sortOrder='', filterKey='', filterValue='', **kwargs):
        '''Queries all items for cdld synthesis'''
        groups = []
        cdldProposingGroups = self.getSelf().getCdldProposingGroup()
        for cdldProposingGroup in cdldProposingGroups:
            groupId = cdldProposingGroup.split('__')[0]
            delay = ''
            if cdldProposingGroup.split('__')[1]:
                delay = 'delay__'
            groups.append('%s%s' % (delay, groupId))
        # advised items are items that has an advice in a particular review_state
        # just append every available meetingadvice state: we want "given" advices.
        # this search will only return 'delay-aware' advices
        wfTool = getToolByName(self, 'portal_workflow')
        adviceWF = wfTool.getWorkflowsFor('meetingadvice')[0]
        adviceStates = adviceWF.states.keys()
        groupIds = []
        advice_index__suffixs = ('advice_delay_exceeded', 'advice_not_given', 'advice_not_giveable')
        # advice given
        for adviceState in adviceStates:
            groupIds += [g + '_%s' % adviceState for g in groups]
        #advice not given
        for advice_index__suffix in advice_index__suffixs:
            groupIds += [g + '_%s' % advice_index__suffix for g in groups]
        # Create query parameters
        fromDate = DateTime(2013, 01, 01)
        toDate = DateTime(2017, 12, 31, 23, 59)
        params = {'portal_type': self.getItemTypeName(),
                  # KeywordIndex 'indexAdvisers' use 'OR' by default
                  'indexAdvisers': groupIds,
                  'created': {'query': [fromDate, toDate], 'range': 'minmax'},
                  'sort_on': sortKey,
                  'sort_order': sortOrder, }
        # Manage filter
        if filterKey:
            params[filterKey] = prepareSearchValue(filterValue)
        # update params with kwargs
        params.update(kwargs)
        # Perform the query in portal_catalog
        brains = self.portal_catalog(**params)
        res = []
        fromDate = DateTime(2014, 01, 01)  # redefine date to get advice in 2014
        for brain in brains:
            obj = brain.getObject()
            if obj.getMeeting() and obj.getMeeting().getDate() >= fromDate and obj.getMeeting().getDate() <= toDate:
                res.append(brain)
        return res
    MeetingConfig.searchCDLDItems = searchCDLDItems

    security.declarePublic('printCDLDItems')

    def printCDLDItems(self):
        '''
        Returns a list of advice for synthesis document (CDLD)
        '''
        meetingConfig = self.getSelf()
        brains = meetingConfig.context.searchCDLDItems()
        res = []
        groups = []
        cdldProposingGroups = meetingConfig.getCdldProposingGroup()
        for cdldProposingGroup in cdldProposingGroups:
            groupId = cdldProposingGroup.split('__')[0]
            delay = False
            if cdldProposingGroup.split('__')[1]:
                delay = True
            if not (groupId, delay) in groups:
                groups.append((groupId, delay))
        for brain in brains:
            item = brain.getObject()
            advicesIndex = item.adviceIndex
            for groupId, delay in groups:
                if groupId in advicesIndex:
                    advice = advicesIndex[groupId]
                    if advice['delay'] and not delay:
                        continue
                    if not (advice, item) in res:
                        res.append((advice, item))
        return res

    security.declarePublic('getMeetingsAcceptingItems')

    def getMeetingsAcceptingItems(self, review_states=('created', 'validated_by_dga', 'frozen'), inTheFuture=False):
        '''This returns meetings that are still accepting items.'''
        cfg = self.getSelf()
        tool = getToolByName(cfg, 'portal_plonemeeting')
        catalog = getToolByName(cfg, 'portal_catalog')
        # If the current user is a meetingManager (or a Manager),
        # he is able to add a meetingitem to a 'decided' meeting.
        # except if we specifically restricted given p_review_states.
        if review_states == ('created', 'validated_by_dga', 'frozen') and tool.isManager(cfg):
            review_states += ('decided', )

        query = {'portal_type': cfg.getMeetingTypeName(),
                 'review_state': review_states,
                 'sort_on': 'getDate'}

        if inTheFuture:
            query['getDate'] = {'query': DateTime(), 'range': 'min'}

        return catalog.unrestrictedSearchResults(**query)


class CustomMeetingGroup(MeetingGroup):
    '''Adapter that adapts a meeting group implementing IMeetingGroup to the
       interface IMeetingGroupCustom.'''

    implements(IMeetingGroupCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePublic('listEchevinServices')

    def listEchevinServices(self):
        '''Returns a list of groups that can be selected on an group (without isEchevin).'''
        res = []
        tool = getToolByName(self, 'portal_plonemeeting')
        # Get every Plone group related to a MeetingGroup
        for group in tool.getMeetingGroups():
            res.append((group.id, group.getProperty('title')))

        return DisplayList(tuple(res))
    MeetingGroup.listEchevinServices = listEchevinServices


class MeetingCollegeSeraingWorkflowActions(MeetingWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeWorkflowActions'''

    implements(IMeetingCollegeSeraingWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doBackToCreated')

    def doBackToCreated(self, stateChange):
        '''When a meeting go back to the "created" state, for example the
           meeting manager wants to add an item, we do not do anything.'''
        pass

    security.declarePrivate('doValidateByDGA')

    def doValidateByDGA(self, stateChange):
        '''When a meeting go to the "validatedByDGA" state, for example the
           meeting manager wants to add an item, we do not do anything.'''
        pass

    security.declarePrivate('doBackToValidatedByDGA')

    def doBackToValidatedByDGA(self, stateChange):
        '''When a meeting go back to the "validatedByDGA" state, for example the
           meeting manager wants to add an item, we do not do anything.'''
        pass


class MeetingCollegeSeraingWorkflowConditions(MeetingWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeWorkflowConditions'''

    implements(IMeetingCollegeSeraingWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting
        customAcceptItemsStates = ('created', 'validated_by_dga', 'frozen', 'decided')
        self.acceptItemsStates = customAcceptItemsStates

    security.declarePublic('mayValidateByDGA')

    def mayValidateByDGA(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            res = True  # At least at present
            if not self.context.getRawItems():
                res = No(translate('item_required_to_publish', domain='PloneMeeting', context=self.context.REQUEST))
        return res

    security.declarePublic('mayFreeze')

    def mayFreeze(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            res = True  # At least at present
            if not self.context.getRawItems():
                res = No(translate('item_required_to_publish', domain='PloneMeeting', context=self.context.REQUEST))
        return res

    security.declarePublic('mayDecide')

    def mayDecide(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

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
           self.context.queryState() not in ('closed'):
            res = True
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
        '''After cloned item, we validate this item'''
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

    security.declarePrivate('doItemValidateByDGA')

    def doItemValidateByDGA(self, stateChange):
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

    security.declarePrivate('doBackToItemValidatedByDGA')

    def doBackToItemValidatedByDGA(self, stateChange):
        pass

    security.declarePrivate('doReturn_to_advise')

    def doReturn_to_advise(self, stateChange):
        pass


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

    security.declarePublic('mayValidate')

    def mayValidate(self):
        """
          We must be reviewer
        """
        res = False
        #The user must have the 'Review portal content permission and be reviewer or manager'
        if checkPermission(ReviewPortalContent, self.context):
            res = True
            memnber = self.context.portal_membership.getAuthenticatedMember()
            tool = getToolByName(self.context, 'portal_plonemeeting')
            if not memnber.has_role('MeetingReviewer', self.context) and not tool.isManager(self.context):
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

    security.declarePublic('mayValidateByDGA')

    def mayValidateByDGA(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in ('created', 'validated_by_dga',
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

    security.declarePublic('mayClose')

    def mayClose(self):
        """
          Check that the user has the 'Review portal content' and meeting is closed (for automatic transitions)
        """
        res = False
        meeting = self.context.getMeeting()
        if checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['closed']):
                res = True
        return res

    security.declarePublic('mayBackToMeeting')

    def mayBackToMeeting(self, transitionName):
        """Specific guard for the 'return_to_proposing_group' wfAdaptation.
           As we have only one guard_expr for potentially several transitions departing
           from the 'returned_to_proposing_group' state, we receive the p_transitionName."""
        tool = getToolByName(self.context, 'portal_plonemeeting')
        if not checkPermission(ReviewPortalContent, self.context) and not \
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
            if not 'may_not_back_to_meeting_warned_by' in self.context.REQUEST:
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
InitializeClass(CustomToolPloneMeeting)
# ------------------------------------------------------------------------------
