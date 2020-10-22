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
from AccessControl.class_init import InitializeClass
from appy.gen import No
from DateTime import DateTime
from plone import api
from Products.Archetypes.atapi import DisplayList
from Products.CMFCore.permissions import DeleteObjects
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.MeetingCommunes.adapters import CustomMeeting
from Products.MeetingCommunes.adapters import CustomMeetingConfig
from Products.MeetingCommunes.adapters import CustomMeetingItem
from Products.MeetingCommunes.adapters import CustomToolPloneMeeting
from Products.MeetingCommunes.adapters import MeetingCommunesWorkflowActions
from Products.MeetingCommunes.adapters import MeetingCommunesWorkflowConditions
from Products.MeetingCommunes.adapters import MeetingItemCommunesWorkflowActions
from Products.MeetingCommunes.adapters import MeetingItemCommunesWorkflowConditions
from Products.MeetingSeraing.config import EDITOR_USECASES
from Products.MeetingSeraing.config import POWEREDITORS_GROUP_SUFFIX
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCollegeWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCollegeWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCouncilWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCouncilWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCollegeWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCollegeWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCouncilWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCouncilWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingSeraingWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingSeraingWorkflowConditions
from Products.PloneMeeting.adapters import ItemPrettyLinkAdapter
from Products.PloneMeeting.config import PMMessageFactory as _
from Products.PloneMeeting.interfaces import IMeetingConfigCustom
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItem
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.PloneMeeting.interfaces import IToolPloneMeetingCustom
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.model.adaptations import WF_APPLIED
from Products.PloneMeeting.utils import sendMailIfRelevant
from zope.i18n import translate
from zope.interface import implements


# disable most of wfAdaptations
customWfAdaptations = ('return_to_proposing_group', 'return_to_proposing_group_with_last_validation',
                       'returned_to_advise')
MeetingConfig.wfAdaptations = customWfAdaptations
originalPerformWorkflowAdaptations = adaptations.performWorkflowAdaptations

# configure parameters for the returned_to_proposing_group wfAdaptation
# we keep also 'itemfrozen' and 'itempublished' in case this should be activated for meeting-config-college...
CUSTOM_RETURN_TO_PROPOSING_GROUP_VALIDATION_STATES = ('proposed_to_servicehead',
                                                      'proposed_to_officemanager',
                                                      'proposed_to_divisionhead',
                                                      'proposed')
adaptations.RETURN_TO_PROPOSING_GROUP_VALIDATION_STATES = CUSTOM_RETURN_TO_PROPOSING_GROUP_VALIDATION_STATES

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

RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'validated_by_dg', 'itemfrozen',)
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES

RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {'meetingitemseraing_workflow':
                                                # view permissions
                                                    {'Access contents information':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingServiceHead', 'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer',
                                                          'MeetingObserverLocal', 'Reader', 'Editor',),
                                                     'View':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingServiceHead', 'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer',
                                                          'MeetingObserverLocal', 'Reader', 'Editor',),
                                                     'PloneMeeting: Read budget infos':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingServiceHead', 'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer',
                                                          'MeetingObserverLocal', 'Reader', 'Editor',),
                                                     'PloneMeeting: Read decision':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingServiceHead', 'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer',
                                                          'MeetingObserverLocal', 'Reader', 'Editor',),
                                                     'PloneMeeting: Read item observations':
                                                         ('Manager', 'MeetingManager', 'MeetingMember',
                                                          'MeetingServiceHead', 'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer',
                                                          'MeetingObserverLocal', 'Reader', 'Editor',),
                                                     # edit permissions
                                                     'Modify portal content':
                                                         ('Manager', 'MeetingMember', 'MeetingServiceHead',
                                                          'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager',),
                                                     'PloneMeeting: Write budget infos':
                                                         ('Manager', 'MeetingMember', 'MeetingServiceHead',
                                                          'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager',
                                                          'MeetingBudgetImpactEditor',),
                                                     'PloneMeeting: Write decision':
                                                         ('Manager', 'MeetingMember', 'MeetingServiceHead',
                                                          'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager',),
                                                     'Review portal content':
                                                         ('Manager', 'MeetingMember', 'MeetingServiceHead',
                                                          'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager',),
                                                     'Add portal content':
                                                         ('Manager', 'MeetingMember', 'MeetingServiceHead',
                                                          'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager',),
                                                     'PloneMeeting: Add annex':
                                                         ('Manager', 'MeetingMember', 'MeetingServiceHead',
                                                          'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager',),
                                                     'PloneMeeting: Add annexDecision':
                                                         ('Manager', 'MeetingMember', 'MeetingServiceHead',
                                                          'MeetingOfficeManager',
                                                          'MeetingDivisionHead', 'MeetingReviewer', 'MeetingManager',),
                                                     # MeetingManagers edit permissions
                                                     'PloneMeeting: Write marginal notes':
                                                         ('Manager',),
                                                     'PloneMeeting: Write item MeetingManager reserved fields':
                                                         ('Manager', 'MeetingManager',),
                                                     'Delete objects':
                                                         ('Manager', 'MeetingManager',), }
                                                }

adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS

RETURN_TO_PROPOSING_GROUP_CUSTOM_STATE_TO_CLONE = {
    'meetingitemseraing_workflow': 'meetingitemseraing_workflow.itemcreated'}
adaptations.RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = RETURN_TO_PROPOSING_GROUP_CUSTOM_STATE_TO_CLONE

RETURN_TO_ADVISE_CUSTOM_PERMISSIONS = {
    'meetingitemseraing_workflow':
    {
        # edit permissions
        'Modify portal content':
            ('Manager', 'MeetingManager',)}
}

RETURN_TO_PROPOSING_GROUP_CUSTOM_STATE_TO_CLONE = {
    'meetingitemseraing_workflow': 'meetingitemseraing_workflow.itemcreated'}
adaptations.RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = RETURN_TO_PROPOSING_GROUP_CUSTOM_STATE_TO_CLONE


class CustomSeraingMeeting(CustomMeeting):
    """Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom."""

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting

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
            if (toPrint and item.getIsToPrintInMeeting()) or not (toPrint or item.getIsToPrintInMeeting()):
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
                                                         excludedCategories, groupIds, excludedGroupIds, firstNumber,
                                                         renumber,
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

    security.declarePublic('listSections')

    def listSections(self):
        """Vocabulary for column 'name_section' of Meeting.sections."""
        if self.portal_type == 'MeetingCouncil':
            res = [('oj', "Collège d'arrêt de l'OJ"),
                   ('tec', "Commission du développement territorial et économique"),
                   ('fin', "Commission des travaux, des marchés publics et des finances"),
                   ('env', "Commission de la jeunesse, de la citoyenneté et du bien-être animal"),
                   ('ag', "Commission de l'administration générale, du budget et des grands projets"),
                   ('ens', "Commission de l'enseignement et de l'enfance"),
                   ('as', "Commission des affaires sociales"),
                   ('prev', "Commission de la prévention, du tourisme, du logement et des nouvelles technologies"),
                   ('cul', "Commission de la culture et des sports"),
                   ('ec', "Commission de la population et de l'état civil")]
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


class CustomSeraingMeetingItem(CustomMeetingItem):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom."""
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    customItemDecidedStates = ('accepted', 'delayed', 'accepted_but_modified', 'accepted_closed', 'delayed_closed',
                               'accepted_but_modified_closed',)
    MeetingItem.itemDecidedStates = customItemDecidedStates

    customBeforePublicationStates = ('itemcreated',
                                     'proposed_to_servicehead',
                                     'proposed_to_officemanager',
                                     'proposed_to_divisionhead',
                                     'proposed',
                                     'validated',)
    MeetingItem.beforePublicationStates = customBeforePublicationStates

    customMeetingNotClosedStates = ('validated_by_dg', 'frozen', 'decided',)
    MeetingItem.meetingNotClosedStates = customMeetingNotClosedStates

    customMeetingTransitionsAcceptingRecurringItems = ('_init_', 'validated_by_dg', 'freeze', 'decide',)
    MeetingItem.meetingTransitionsAcceptingRecurringItems = customMeetingTransitionsAcceptingRecurringItems

    security.declarePublic('updatePowerEditorsLocalRoles')

    def updatePowerEditorsLocalRoles(self):
        """Give the 'power editors' local role to the corresponding
           MeetingConfig 'powereditors' group on self."""
        item = self.getSelf()
        # Then, add local roles for powereditors.
        cfg = item.portal_plonemeeting.getMeetingConfig(item)
        powerEditorsGroupId = "%s_%s" % (cfg.getId(), POWEREDITORS_GROUP_SUFFIX)
        item.manage_addLocalRoles(powerEditorsGroupId, (EDITOR_USECASES['power_editors'],))

    def getExtraFieldsToCopyWhenCloning(self, cloned_to_same_mc, cloned_from_item_template):
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
        if not self._at_creation_flag:
            # save takenOverBy to takenOverByInfos for current review_state
            # or check for a wf_state in kwargs
            tool = api.portal.get_tool('portal_plonemeeting')
            cfg = tool.getMeetingConfig(self)
            if 'wf_state' in kwargs:
                wf_state = kwargs['wf_state']
            else:
                wf_state = "%s__wfstate__%s" % (cfg.getItemWorkflow(), self.queryState())
            if value:
                self.takenOverByInfos[wf_state] = value
                # xxx for Seraing, in some states, we would keep the "Taken over" for some next states
                wf_states_service = ['itemcreated', 'proposed_to_servicehead', 'proposed_to_officemanager',
                                     'proposed_to_divisionhead', 'proposed']
                wf_state_gs = ['validated', 'presented', 'validated_by_dg', 'itemfrozen']
                wf_state_close = ['accepted', 'accepted_but_closed', 'accepted_but_modified',
                                  'accepted_but_modified_but_closed', 'delayed', 'delayed_closed']
                wf_states_to_use = []
                cpt = 0
                if self.queryState() in wf_states_service:
                    wf_states_to_use = wf_states_service
                elif self.queryState() in wf_state_gs:
                    wf_states_to_use = wf_state_gs
                elif self.queryState() in wf_state_close:
                    wf_states_to_use
                for wf_state_service in wf_states_to_use:
                    if self.queryState() == wf_state_service:
                        break
                    cpt += 1
                wf_states = wf_states_to_use[cpt:]
                # add for next states the taken over info
                for wf_state in wf_states:
                    wf_state = "%s__wfstate__%s" % (cfg.getItemWorkflow(), wf_state)
                    self.takenOverByInfos[wf_state] = value
            elif not value and wf_state in self.takenOverByInfos:
                del self.takenOverByInfos[wf_state]
        self.getField('takenOverBy').set(self, value, **kwargs)

    MeetingItem.setTakenOverBy = setTakenOverBy


class CustomSeraingMeetingConfig(CustomMeetingConfig):
    """Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom."""

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

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

    def getMeetingStatesAcceptingItem(self):
        """See doc in interfaces.py."""
        return ('created', 'validated_by_dg', 'frozen', 'decided')

    def extraItemEvents(self):
        """Override pm method"""
        return ("event_item_delayed-service_heads", "event_add_advice-service_heads")


class MeetingSeraingWorkflowActions(MeetingCommunesWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCommunesWorkflowActions"""

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


class MeetingSeraingWorkflowConditions(MeetingCommunesWorkflowConditions):
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


class MeetingSeraingCollegeWorkflowConditions(MeetingSeraingWorkflowConditions):
    """inherit class"""
    implements(IMeetingSeraingCollegeWorkflowConditions)


class MeetingSeraingCouncilWorkflowConditions(MeetingSeraingWorkflowConditions):
    """inherit class"""
    implements(IMeetingSeraingCouncilWorkflowConditions)


class MeetingItemSeraingWorkflowActions(MeetingItemCommunesWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCommunesWorkflowActions"""

    implements(IMeetingItemSeraingWorkflowActions)
    security = ClassSecurityInfo()

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
        super(MeetingItemSeraingWorkflowActions, self).doDelay(stateChange)
        # make sure we get freshly cloned item in case we delay self.context several times...
        clonedItem = [item for item in self.context.getBRefs('ItemPredecessor')
                      if item.queryState() == 'itemcreated'][0]
        wfTool = api.portal.get_tool('portal_workflow')
        # make sure item may be validated
        with api.env.adopt_roles(['Manager']):
            wfTool.doActionFor(clonedItem, 'validate')
        # Send, if configured, a mail to the person who created the item
        sendMailIfRelevant(clonedItem, 'event_item_delayed-service_heads', 'MeetingServiceHead', isRole=True)

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

    def _latePresentedItem(self):
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


class MeetingItemSeraingWorkflowConditions(MeetingItemCommunesWorkflowConditions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCommunesWorkflowConditions"""

    implements(IMeetingItemSeraingWorkflowConditions)
    security = ClassSecurityInfo()

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
            member = self.context.portal_membership.getAuthenticatedMember()
            tool = getToolByName(self.context, 'portal_plonemeeting')
            if not member.has_role('MeetingReviewer', self.context) and not tool.isManager(self.context):
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
        return self._check_review_and_required()

    security.declarePublic('mayProposeToOfficeManager')

    def mayProposeToOfficeManager(self):
        """
          Check that the user has the 'Review portal content'
        """
        return self._check_review_and_required()

    security.declarePublic('mayProposeToDivisionHead')

    def mayProposeToDivisionHead(self):
        """
          Check that the user has the 'Review portal content'
        """
        return self._check_review_and_required()

    security.declarePublic('mayPresent')

    def mayPresent(self):
        # only MeetingManagers may present an item, the 'Review portal content'
        # permission is not enough as MeetingReviewer may have the 'Review portal content'
        # when using the 'reviewers_take_back_validated_item' wfAdaptation
        tool = api.portal.get_tool('portal_plonemeeting')
        if not _checkPermission(ReviewPortalContent, self.context) or \
           not tool.isManager(self.context):
            return False
        # We may present the item if Plone currently publishes a meeting.
        # Indeed, an item may only be presented within a meeting.
        # if we are not on a meeting, try to get the next meeting accepting items
        if not self._publishedObjectIsMeeting():
            meeting = self.context.getMeetingToInsertIntoWhenNoCurrentMeetingObject()
            return bool(meeting)

        # here we are sure that we have a meeting that will accept the item
        # Verify if all automatic advices have been given on this item.
        res = True  # for now...
        if self.context.enforceAdviceMandatoriness() and \
           not self.context.mandatoryAdvicesAreOk():
            res = No(_('mandatory_advice_ko'))
        return res

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


class CustomSeraingToolPloneMeeting(CustomToolPloneMeeting):
    """Adapter that adapts a tool implementing ToolPloneMeeting to the
       interface IToolPloneMeetingCustom"""

    implements(IToolPloneMeetingCustom)
    security = ClassSecurityInfo()

    security.declarePublic('updatePowerEditors')

    def updatePowerEditors(self):
        """Update local_roles regarging the PowerEditors for every items."""
        if not self.context.isManager(realManagers=True):
            raise Unauthorized
        for b in self.context.portal_catalog(meta_type=('MeetingItem',)):
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
            itemTransitions = itemWorkflow.transitions
            if 'returned_to_advise' not in itemStates and 'returned_to_proposing_group' in itemStates:
                if 'returned_to_advise' not in itemStates:
                    # add the 'returned_to_proposing_group' state and clone the
                    # permissions from RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE
                    # and apply permissions defined in RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS
                    # RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS contains custom permissions by workflow
                    customPermissions = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS. \
                        get(meetingConfig.getItemWorkflow(), {})
                    itemStates.addState('returned_to_advise')
                    newState = getattr(itemStates, 'returned_to_advise')
                    # clone the permissions of the given RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE if it exists
                    cloned_permissions_with_meetingmanager = {}
                    # state to clone contains the state to clone and the workflow_id where this state is
                    stateToCloneInfos = adaptations.RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE.get(
                        meetingConfig.getItemWorkflow(), {})
                    stateToCloneWFId = ''
                    stateToCloneStateId = ''
                    if stateToCloneInfos:
                        # stateToCloneInfos is like 'meetingitem_workflow.itemcreated'
                        stateToCloneWFId, stateToCloneStateId = stateToCloneInfos.split('.')
                    stateToCloneWF = getattr(wfTool, stateToCloneWFId, None)
                    stateToClone = None
                    if stateToCloneWF and hasattr(stateToCloneWF.states, stateToCloneStateId):
                        stateToClone = getattr(stateToCloneWF.states, stateToCloneStateId)
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

                    # now apply custom permissions defined in customPermissions
                    cloned_permissions_with_meetingmanager.update(customPermissions)

                    # if we are cloning an existing state permissions, make sure DeleteObjects
                    # is only be availble to ['Manager', 'MeetingManager']
                    # if custom permissions are defined, keep what is defined in it
                    if DeleteObjects not in customPermissions and stateToClone:
                        del_obj_perm = stateToClone.getPermissionInfo(DeleteObjects)
                        if del_obj_perm['acquired']:
                            cloned_permissions_with_meetingmanager[DeleteObjects] = ['Manager', ]
                        else:
                            cloned_permissions_with_meetingmanager[DeleteObjects] = ('Manager',)

                    # finally, apply computed permissions, aka cloned + custom
                    newState.permission_roles = cloned_permissions_with_meetingmanager

                if 'return_to_advise' not in itemTransitions:
                    itemTransitions.addTransition('return_to_advise')

                transition = itemTransitions['return_to_advise']
                # use same guard from ReturnToProposingGroup
                transition.setProperties(
                    title='return_to_advise',
                    new_state_id='returned_to_advise', trigger_type=1, script_name='',
                    actbox_name='return_to_advise', actbox_url='', actbox_category='workflow',
                    actbox_icon='%(portal_url)s/return_to_advise.png',
                    props={'guard_expr': 'python:here.wfConditions().mayReturnToProposingGroup()'})

                returned_to_advise = itemStates['returned_to_advise']
                returned_to_advise.setProperties(
                    title='returned_to_advise', description='',
                    transitions=('backTo_returned_to_proposing_group_from_returned_to_proposing_group_proposed',
                                 'goTo_returned_to_proposing_group_proposed',))

                return_to_advice_item_state = [adaptations.getValidationReturnedStates(meetingConfig)[-1]] + \
                                              ['returned_to_proposing_group', 'presented', 'validated_by_dg',
                                               'itemfrozen']

                for state_id in return_to_advice_item_state:
                    new_trx = tuple(list(itemStates[state_id].getTransitions()) + ['return_to_advise'])
                    itemStates[state_id].transitions = new_trx

                # Initialize permission->roles mapping for new state "returned_to_advise",
                returned_to_advise = itemStates['returned_to_advise']
                for permission, roles in RETURN_TO_ADVISE_CUSTOM_PERMISSIONS['meetingitemseraing_workflow'].iteritems():
                    returned_to_advise.setPermission(permission, 0, roles)

            logger.info(WF_APPLIED % ("returned_to_advise", meetingConfig.getId()))
            return True
        return False


# ------------------------------------------------------------------------------
InitializeClass(CustomSeraingMeetingItem)
InitializeClass(CustomSeraingMeeting)
InitializeClass(CustomSeraingMeetingConfig)
InitializeClass(MeetingSeraingWorkflowActions)
InitializeClass(MeetingSeraingWorkflowConditions)
InitializeClass(MeetingItemSeraingWorkflowActions)
InitializeClass(MeetingItemSeraingWorkflowConditions)
InitializeClass(CustomSeraingToolPloneMeeting)


# ------------------------------------------------------------------------------

class MSItemPrettyLinkAdapter(ItemPrettyLinkAdapter):
    """
      Override to take into account MeetingLiege use cases...
    """

    def _leadingIcons(self):
        """
          Manage icons to display before the icons managed by PrettyLink._icons.
        """
        # Default PM item icons
        icons = super(MSItemPrettyLinkAdapter, self)._leadingIcons()

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
