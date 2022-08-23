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
from Products.PloneMeeting.browser.overrides import PMDocumentGeneratorLinksViewlet
from Products.PloneMeeting.browser.views import MeetingStoreItemsPodTemplateAsAnnexBatchActionForm
from Products.PloneMeeting.config import AddAnnex
from appy.gen import No
from copy import deepcopy
from DateTime import DateTime
from plone import api
from Products.Archetypes.atapi import DisplayList
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
from Products.MeetingSeraing.config import POWEREDITORS_GROUP_SUFFIX
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCollegeWorkflowActions
from Products.MeetingSeraing.interfaces import (
    IMeetingItemSeraingCollegeWorkflowConditions,
)
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingCouncilWorkflowActions
from Products.MeetingSeraing.interfaces import (
    IMeetingItemSeraingCouncilWorkflowConditions,
)
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingItemSeraingWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCollegeWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCollegeWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCouncilWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingSeraingCouncilWorkflowConditions
from Products.MeetingSeraing.interfaces import IMeetingSeraingWorkflowActions
from Products.MeetingSeraing.interfaces import IMeetingSeraingWorkflowConditions
from Products.PloneMeeting.adapters import ItemPrettyLinkAdapter
from Products.PloneMeeting.interfaces import IMeetingConfigCustom
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItem
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.PloneMeeting.interfaces import IToolPloneMeetingCustom
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.model.adaptations import WF_APPLIED, _addIsolatedState, _getValidationReturnedStates
from Products.PloneMeeting.utils import sendMailIfRelevant
from zope.i18n import translate
from zope.interface import implements

# disable most of wfAdaptations
customWfAdaptations = (
    'item_validation_shortcuts',
    'item_validation_no_validate_shortcuts',
    'only_creator_may_delete',
    # first define meeting workflow state removal
    'no_freeze',
    'no_publication',
    'no_decide',
    # then define added item decided states
    'accepted_but_modified',
    'postpone_next_meeting',
    'mark_not_applicable',
    'removed',
    'removed_and_duplicated',
    'refused',
    'delayed',
    'pre_accepted',
    "seraing_add_item_closed_state",
    "seraing_validated_by_DG",
    "seraing_powereditors",
    "return_to_proposing_group",
    "return_to_proposing_group_with_last_validation",
    "seraing_returned_to_advise"
)
MeetingConfig.wfAdaptations = customWfAdaptations

CUSTOM_RETURN_TO_PROPOSING_GROUP_MAPPINGS = {
    "backTo_presented_from_returned_to_proposing_group": [
        "created",
    ],
    "backTo_validated_by_dg_from_returned_to_proposing_group": [
        "validated_by_dg",
    ],
    "backTo_itempublished_from_returned_to_proposing_group": {
        "published"
    },
    "backTo_itemfrozen_from_returned_to_proposing_group": [
        "frozen",
        "decided",
        "decisions_published",
    ],
    "backTo_presented_from_returned_to_advise": [
        "created",
    ],
    "backTo_validated_by_dg_from_returned_to_advise": [
        "validated_by_dg",
    ],
    "backTo_itemfrozen_from_returned_to_advise": [
        "frozen",
        "decided",
        "decisions_published",
    ],
    "backTo_returned_to_proposing_group_from_returned_to_advise": [
        "created",
        "validated_by_dg",
        "frozen",
        "decided",
        "decisions_published",
    ],
    "NO_MORE_RETURNABLE_STATES": [
        "closed",
        "archived",
    ],
}
adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS = CUSTOM_RETURN_TO_PROPOSING_GROUP_MAPPINGS

CUSTOM_RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = (
    "validated_by_dg",
)
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES \
                                                         + CUSTOM_RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES

POWEREDITORS_EDITABLE_STATES = (
"validated_by_dg", "itemfrozen", "accepted", "delayed", "accepted_but_modified", "pre_accepted"
)


class CustomSeraingMeeting(CustomMeeting):
    """Adapter that adapts a meeting implementing IMeeting to the
    interface IMeetingCustom."""

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting

    security.declarePublic("isDecided")

    def is_decided(self):
        """
        The meeting is supposed 'decided', if at least in state :
        - 'in_council' for MeetingCouncil
        - 'decided' for MeetingCollege
        """
        meeting = self.getSelf()
        return meeting.query_state() in ("in_council", "decided", "closed", "archived")

    # Implements here methods that will be used by templates

    security.declarePublic("getPrintableItemsByCategory")

    def getPrintableItemsByCategory(
            self,
            itemUids=[],
            listTypes=["normal"],
            ignore_review_states=[],
            by_proposing_group=False,
            group_proposing_group=False,
            group_prefixes={},
            privacy="*",
            oralQuestion="both",
            toDiscuss="both",
            categories=[],
            excludedCategories=[],
            groupIds=[],
            excludedGroupIds=[],
            firstNumber=1,
            renumber=False,
            includeEmptyCategories=False,
            includeEmptyGroups=False,
            isToPrintInMeeting="both",
            forceCategOrderFromConfig=False,
            unrestricted=False,
    ):
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
        tool = getToolByName(self.context, "portal_plonemeeting")
        # Retrieve the list of items
        for elt in itemUids:
            if elt == "":
                itemUids.remove(elt)
        try:
            items = self.context.get_items(
                uids=itemUids,
                list_types=listTypes,
                ordered=True,
                unrestricted=unrestricted,
            )
        except Unauthorized:
            return res
        if by_proposing_group:
            groups = tool.getMeetingGroups()
        else:
            groups = None
        if items:
            for item in items:
                # Check if the review_state has to be taken into account
                if item.query_state() in ignore_review_states:
                    continue
                elif not (privacy == "*" or item.getPrivacy() == privacy):
                    continue
                elif not (
                        oralQuestion == "both" or item.getOralQuestion() == oralQuestion
                ):
                    continue
                elif not (toDiscuss == "both" or item.getToDiscuss() == toDiscuss):
                    continue
                elif groupIds and not item.getProposingGroup() in groupIds:
                    continue
                elif categories and not item.getCategory() in categories:
                    continue
                elif excludedCategories and item.getCategory() in excludedCategories:
                    continue
                elif excludedGroupIds and item.getProposingGroup() in excludedGroupIds:
                    continue
                elif not (
                        isToPrintInMeeting == "both"
                        or item.getIsToPrintInMeeting() == isToPrintInMeeting
                ):
                    continue
                if group_proposing_group:
                    currentCat = item.getProposingGroup(theObject=True)
                else:
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
                    self._insertItemInCategory(
                        catList, item, by_proposing_group, group_prefixes, groups
                    )
                else:
                    res.append([currentCat])
                    self._insertItemInCategory(
                        res[-1], item, by_proposing_group, group_prefixes, groups
                    )
        if forceCategOrderFromConfig or cmp(listTypes.sort(), ["late", "normal"]) == 0:
            res.sort(cmp=_comp)
        if includeEmptyCategories:
            meetingConfig = tool.getMeetingConfig(self.context)
            # onlySelectable = False will also return disabled categories...
            allCategories = [
                cat
                for cat in meetingConfig.getCategories(onlySelectable=False)
                if api.content.get_state(cat) == "active"
            ]
            usedCategories = [elem[0] for elem in res]
            for cat in allCategories:
                if cat not in usedCategories:
                    # Insert the category among used categories at the right
                    # place.
                    categoryInserted = False
                    for i in range(len(usedCategories)):
                        if allCategories.index(cat) < allCategories.index(
                                usedCategories[i]
                        ):
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
                    self._insertGroupInCategory(catInfo, group, group_prefixes, groups)
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

    security.declarePublic("getAllItemsToPrintingOrNot")

    def getAllItemsToPrintingOrNot(self, uids=[], ordered=False, toPrint="True"):
        res = []
        items = self.context.getItems(uids)
        for item in items:
            if (toPrint and item.getIsToPrintInMeeting()) or not (
                    toPrint or item.getIsToPrintInMeeting()
            ):
                res.append(item)
        return res

    security.declarePublic("getOJByCategory")

    def getOJByCategory(
            self,
            itemUids=[],
            listTypes=["normal"],
            ignore_review_states=[],
            by_proposing_group=False,
            group_prefixes={},
            privacy="*",
            oralQuestion="both",
            toDiscuss="both",
            categories=[],
            excludedCategories=[],
            groupIds=[],
            excludedGroupIds=[],
            firstNumber=1,
            renumber=False,
            includeEmptyCategories=False,
            includeEmptyGroups=False,
            isToPrintInMeeting="both",
            forceCategOrderFromConfig=False,
            unrestricted=False,
    ):
        lists = self.context.getPrintableItemsByCategory(
            itemUids,
            listTypes,
            ignore_review_states,
            by_proposing_group,
            group_prefixes,
            privacy,
            oralQuestion,
            toDiscuss,
            categories,
            excludedCategories,
            groupIds,
            excludedGroupIds,
            firstNumber,
            renumber,
            includeEmptyCategories,
            includeEmptyGroups,
            isToPrintInMeeting,
            forceCategOrderFromConfig,
            unrestricted,
        )
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
                    if (
                            not find_late
                            and IMeetingItem.providedBy(sub_obj)
                            and sub_obj.isLate()
                    ):
                        final_items.append("late")
                        find_late = True
                    final_items.append(sub_obj)
                final_res.append(final_items)
            res.append(final_res)
        return res

    security.declarePublic("listSections")

    def listSections(self):
        """Vocabulary for column 'name_section' of Meeting.sections."""
        if self.portal_type == "MeetingCouncil":
            res = [
                ("oj", "Collège d'arrêt de l'OJ"),
                ("tec", "Commission du développement territorial et économique"),
                ("fin", "Commission des travaux, des marchés publics et des finances"),
                (
                    "env",
                    "Commission de la jeunesse, de la citoyenneté et du bien-être animal",
                ),
                (
                    "ag",
                    "Commission de l'administration générale, du budget et des grands projets",
                ),
                ("ens", "Commission de l'enseignement et de l'enfance"),
                ("as", "Commission des affaires sociales"),
                (
                    "prev",
                    "Commission de la prévention, du tourisme, du logement et des nouvelles technologies",
                ),
                ("cul", "Commission de la culture et des sports"),
                ("ec", "Commission de la population et de l'état civil"),
            ]
        else:
            res = [
                ("oj", "Collège d'arrêt de l'OJ"),
            ]
        return DisplayList(tuple(res))

    Meeting.listSections = listSections

    security.declarePublic("getSectionDate")

    def getSectionDate(self, section_name):
        """Used in template."""
        dt = None
        for section in self.getSelf().getSections():
            if section["name_section"].upper() == section_name:
                dt = DateTime(section["date_section"], datefmt="international")
                break
        if not dt:
            return ""

        day = "%s %s" % (
            translate(
                "weekday_%s" % dt.strftime("%a").lower(),
                domain="plonelocales",
                context=self.getSelf().REQUEST,
            ).lower(),
            dt.strftime("%d"),
        )
        month = translate(
            "month_%s" % dt.strftime("%b").lower(),
            domain="plonelocales",
            context=self.getSelf().REQUEST,
        ).lower()
        year = dt.strftime("%Y")
        res = "%s %s %s" % (day, month, year)
        return res


class CustomSeraingMeetingItem(CustomMeetingItem):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
    interface IMeetingItemCustom."""

    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    customItemDecidedStates = (
        "accepted",
        "delayed",
        "accepted_but_modified",
        "accepted_closed",
        "delayed_closed",
        "accepted_but_modified_closed",
    )
    MeetingItem.itemDecidedStates = customItemDecidedStates

    customBeforePublicationStates = (
        "itemcreated",
        "proposed_to_servicehead",
        "proposed_to_officemanager",
        "proposed_to_divisionhead",
        "proposed",
        "validated",
    )
    MeetingItem.beforePublicationStates = customBeforePublicationStates

    customMeetingNotClosedStates = (
        "validated_by_dg",
        "frozen",
        "decided",
    )
    MeetingItem.meetingNotClosedStates = customMeetingNotClosedStates

    customMeetingTransitionsAcceptingRecurringItems = (
        "_init_",
        "validated_by_dg",
        "freeze",
        "decide",
    )
    MeetingItem.meetingTransitionsAcceptingRecurringItems = (
        customMeetingTransitionsAcceptingRecurringItems
    )

    security.declarePublic("updatePowerEditorsLocalRoles")

    def updatePowerEditorsLocalRoles(self):
        """Give the 'power editors' local role to the corresponding
        MeetingConfig 'powereditors' group on self."""
        item = self.getSelf()
        # Then, add local roles for powereditors.
        cfg = item.portal_plonemeeting.getMeetingConfig(item)
        powerEditorsGroupId = "%s_%s" % (cfg.getId(), POWEREDITORS_GROUP_SUFFIX)
        if item.query_state() in POWEREDITORS_EDITABLE_STATES:
            item.manage_addLocalRoles(
                powerEditorsGroupId, ("Editor", "Contributor")
            )

    def getExtraFieldsToCopyWhenCloning(
            self, cloned_to_same_mc, cloned_from_item_template
    ):
        """
        Keep some new fields when item is cloned (to another mc or from itemtemplate).
        """
        res = ["isToPrintInMeeting"]
        if cloned_to_same_mc:
            res = res + []
        return res

    security.declarePublic("mayTakeOver")

    def mayTakeOver(self):
        """Condition for editing 'takenOverBy' field.
        A member may take an item over if he is able to modify item."""
        return _checkPermission(ModifyPortalContent, self.context)

    security.declarePublic("setTakenOverBy")

    def setTakenOverBy(self, value, **kwargs):
        def _is_transitioning():
            return (
                    self.REQUEST
                    and hasattr(self.REQUEST, "form")
                    and "transition" in self.REQUEST.form
            )

        def _get_current_transition():
            if not _is_transitioning():
                return None
            return self.REQUEST.form["transition"]

        tool = api.portal.get_tool("portal_plonemeeting")
        cfg = tool.getMeetingConfig(self)
        if _is_transitioning():
            if _get_current_transition() in cfg.getTransitionsReinitializingTakenOverBy():
                # If transition should reinitialize TakenOverBy
                self.getField("takenOverBy").set(self, "", **kwargs)
            else:
                # Else keep the old value when transitioning
                self.getField("takenOverBy").set(self, self.getTakenOverBy(), **kwargs)
        else:
            # If it's not transitioning set the value
            self.getField("takenOverBy").set(self, value, **kwargs)

    MeetingItem.setTakenOverBy = setTakenOverBy


class CustomSeraingMeetingConfig(CustomMeetingConfig):
    """Adapter that adapts a meetingConfig implementing IMeetingConfig to the
    interface IMeetingConfigCustom."""

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePrivate("createPowerObserversGroup")

    def _custom_createOrUpdateGroups(self, force_update_access=False, dry_run_return_group_ids=False):
        """Creates a Plone group that will be used to apply the 'Editor'
        local role on every items in itemFrozen state."""
        meetingConfig = self.getSelf()
        groupId = "%s_%s" % (meetingConfig.getId(), POWEREDITORS_GROUP_SUFFIX)
        if groupId not in meetingConfig.portal_groups.listGroupIds():
            enc = meetingConfig.portal_properties.site_properties.getProperty(
                "default_charset"
            )
            groupTitle = "%s (%s)" % (
                meetingConfig.Title().decode(enc),
                translate(
                    POWEREDITORS_GROUP_SUFFIX,
                    domain="PloneMeeting",
                    context=meetingConfig.REQUEST,
                ),
            )
            # a default Plone group title is NOT unicode.  If a Plone group title is
            # edited TTW, his title is no more unicode if it was previously...
            # make sure we behave like Plone...
            groupTitle = groupTitle.encode(enc)
            meetingConfig.portal_groups.addGroup(groupId, title=groupTitle)
        # now define local_roles on the tool so it is accessible by this group
        tool = getToolByName(meetingConfig, "portal_plonemeeting")
        tool.manage_addLocalRoles(groupId, ("Editor",))
        # but we do not want this group to access every MeetingConfigs so
        # remove inheritance on self and define these local_roles for self too
        meetingConfig.__ac_local_roles_block__ = True
        meetingConfig.manage_addLocalRoles(groupId, ("Editor",))
        return [groupId]

    security.declareProtected("Modify portal content", "onEdit")

    def getMeetingStatesAcceptingItems(self):
        """See doc in interfaces.py."""
        return ("created", "validated_by_dg", "frozen", "decided")

    def extraItemEvents(self):
        """Override pm method"""
        return ("event_item_delayed-service_heads", "event_add_advice-service_heads")

    def get_item_corresponding_state_to_assign_local_roles(self, item_state):
        '''See doc in interfaces.py.'''
        cfg = self.getSelf()
        corresponding_item_state = None
        # XXX returned_to_proposing_group_xxx is special in MeetingSeraing
        # returned_to_proposing_group_proposed is equivalent to proposed state
        # (see patch_return_to_proposing_group_with_last_validation WFA in MeetingSeraing 4.1)
        # BUT returned_to_proposing_group has no equivalent,
        # everybody from the proposing group can edit
        if item_state == 'returned_to_proposing_group_proposed':
            corresponding_item_state = 'proposed'
        # waiting_advices WFAdaptation
        elif item_state.endswith('_waiting_advices'):
            corresponding_item_state = item_state.split('_waiting_advices')[0]
        return corresponding_item_state

    def get_item_custom_suffix_roles(self, item_state):
        suffix_roles = None
        if item_state == 'returned_to_proposing_group':
            SUFFIXES_THAT_MAY_EDIT_IN_RETURNED_TO_PROPOSING_GROUP = [
                "creators", "serviceheads", "officemanagers", "divisionheads", "reviewers"
            ]
            EDIT_ROLES = ['Reader', 'Contributor', 'Editor', 'Reviewer']
            suffix_roles = {'observers': ['Reader']}
            for suffix in SUFFIXES_THAT_MAY_EDIT_IN_RETURNED_TO_PROPOSING_GROUP:
                suffix_roles[suffix] = EDIT_ROLES
        if item_state == 'returned_to_advise':
            SUFFIXES_THAT_MAY_REVIEW_IN_RETURNED_TO_ADVISE = [
                "creators", "serviceheads", "officemanagers", "divisionheads", "reviewers"
            ]
            REVIEW_ROLES = ['Reader', 'Reviewer']
            suffix_roles = {'observers': ['Reader']}
            for suffix in SUFFIXES_THAT_MAY_REVIEW_IN_RETURNED_TO_ADVISE:
                suffix_roles[suffix] = REVIEW_ROLES
        return True, suffix_roles


class MeetingSeraingWorkflowActions(MeetingCommunesWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
    interface IMeetingCommunesWorkflowActions"""

    implements(IMeetingSeraingWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate("doValidateByDG")

    def doValidateByDG(self, stateChange):
        """When a meeting go to the "validatedByDG" state, for example the
        meeting manager wants to add an item, we do not do anything."""
        pass

    security.declarePrivate("doBackToValidatedByDG")

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
        customAcceptItemsStates = ("created", "validated_by_dg", "frozen", "decided")
        self.acceptItemsStates = customAcceptItemsStates

    security.declarePublic("mayValidateByDG")

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

    security.declarePrivate("doProposeToServiceHead")

    def doProposeToServiceHead(self, stateChange):
        pass

    security.declarePrivate("doProposeToOfficeManager")

    def doProposeToOfficeManager(self, stateChange):
        pass

    security.declarePrivate("doProposeToDivisionHead")

    def doProposeToDivisionHead(self, stateChange):
        pass

    security.declarePrivate("doDelay")

    def doDelay(self, stateChange):
        """After cloned item, we validate this item"""
        super(MeetingItemSeraingWorkflowActions, self).doDelay(stateChange)
        # make sure we get freshly cloned item in case we delay self.context several times...
        clonedItem = self.context.get_successors()[0]
        wfTool = api.portal.get_tool("portal_workflow")

        if clonedItem.query_state() != 'validated':
            # make sure item may be validated
            with api.env.adopt_roles(["Manager"]):
                wfTool.doActionFor(clonedItem, "validate")
        # Send, if configured, a mail to the person who created the item
        sendMailIfRelevant(
            clonedItem,
            "event_item_delayed-service_heads",
            "MeetingServiceHead",
            isRole=True,
        )

    security.declarePrivate("doAccept_close")

    def doAccept_close(self, stateChange):
        pass

    security.declarePrivate("doAccept_but_modify_close")

    def doAccept_but_modify_close(self, stateChange):
        pass

    security.declarePrivate("doDelay_close")

    def doDelay_close(self, stateChange):
        pass

    security.declarePrivate("doItemValidateByDG")

    def doItemValidateByDG(self, stateChange):
        pass

    security.declarePrivate("doBackToItemAcceptedButModified")

    def doBackToItemAcceptedButModified(self, stateChange):
        pass

    security.declarePrivate("doBackToItemAccepted")

    def doBackToItemAccepted(self, stateChange):
        pass

    security.declarePrivate("doBackToItemDelayed")

    def doBackToItemDelayed(self, stateChange):
        pass

    security.declarePrivate("doBackToItemValidatedByDG")

    def doBackToItemValidatedByDG(self, stateChange):
        pass

    security.declarePrivate("doReturn_to_advise")

    def doReturn_to_advise(self, stateChange):
        pass

    security.declarePrivate("_freezePresentedItem")

    def _latePresentedItem(self):
        """Presents an item into a frozen meeting."""
        wTool = getToolByName(self.context, "portal_workflow")
        wTool.doActionFor(self.context, "itemValidateByDG")
        wTool.doActionFor(self.context, "itemfreeze")


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

    security.declarePublic("mayDecide")

    def mayDecide(self):
        """We may decide an item if the linked meeting is in the 'decided'
        state."""
        res = False
        meeting = self.context.getMeeting()
        if (
                _checkPermission(ReviewPortalContent, self.context)
                and meeting
                and (
                meeting.query_state()
                in [
                    "decided",
                    "closed",
                    "decisions_published",
                ]
        )
        ):
            res = True
        return res

    security.declarePublic("mayValidateByDG")

    def mayValidateByDG(self):
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and (
                    self.context.getMeeting().query_state()
                    in ("created", "validated_by_dg", "frozen", "decided", "closed")
            ):
                res = True
        return res

    security.declarePublic("mayPropose")

    def mayPropose(self):
        """
        Check that the user has the 'Review portal content'
        """
        return _checkPermission(ReviewPortalContent, self.context)

    security.declarePublic("mayProposeToServiceHead")

    def mayProposeToServiceHead(self):
        """
        Check that the user has the 'Review portal content'
        """
        return _checkPermission(ReviewPortalContent, self.context)

    security.declarePublic("mayProposeToOfficeManager")

    def mayProposeToOfficeManager(self):
        """
        Check that the user has the 'Review portal content'
        """
        return _checkPermission(ReviewPortalContent, self.context)

    security.declarePublic("mayProposeToDivisionHead")

    def mayProposeToDivisionHead(self):
        """
        Check that the user has the 'Review portal content'
        """
        return _checkPermission(ReviewPortalContent, self.context)

    security.declarePublic("mayBackToMeeting")

    def mayBackToMeeting(self, transitionName):
        """Specific guard for the 'return_to_proposing_group' wfAdaptation.
        As we have only one guard_expr for potentially several transitions departing
        from the 'returned_to_proposing_group' state, we receive the p_transitionName."""
        tool = getToolByName(self.context, "portal_plonemeeting")
        if not _checkPermission(
                ReviewPortalContent, self.context
        ) and not self.tool.isManager(self.cfg):
            return
        # get the linked meeting
        meeting = self.context.getMeeting()
        meetingState = meeting.query_state()
        # use RETURN_TO_PROPOSING_GROUP_MAPPINGS to know in wich meetingStates
        # the given p_transitionName can be triggered
        authorizedMeetingStates = adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS[
            transitionName
        ]
        if meetingState in authorizedMeetingStates:
            return True
        # if we did not return True, then return a No(...) message specifying that
        # it can no more be returned to the meeting because the meeting is in some
        # specifig states (like 'closed' for example)
        if (
                meetingState
                in adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS["NO_MORE_RETURNABLE_STATES"]
        ):
            # avoid to display No(...) message for each transition having the 'mayBackToMeeting'
            # guard expr, just return the No(...) msg for the first transitionName checking this...
            if "may_not_back_to_meeting_warned_by" not in self.context.REQUEST:
                self.context.REQUEST.set(
                    "may_not_back_to_meeting_warned_by", transitionName
                )
            if (
                    self.context.REQUEST.get("may_not_back_to_meeting_warned_by")
                    == transitionName
            ):
                return No(
                    translate(
                        "can_not_return_to_meeting_because_of_meeting_state",
                        mapping={
                            "meetingState": translate(
                                meetingState,
                                domain="plone",
                                context=self.context.REQUEST,
                            ),
                        },
                        domain="PloneMeeting",
                        context=self.context.REQUEST,
                    )
                )
        return False

    security.declarePublic("mayClose")

    def mayClose(self):
        """
        Check that the user has the 'Review portal content' and meeting is closed (for automatic transitions)
        """
        res = False
        meeting = self.context.getMeeting()
        if (
                _checkPermission(ReviewPortalContent, self.context)
                and meeting
                and (meeting.query_state() in ["closed"])
        ):
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

    security.declarePublic("updatePowerEditors")

    def updatePowerEditors(self):
        """Update local_roles regarging the PowerEditors for every items."""
        if not self.context.isManager(realManagers=True):
            raise Unauthorized
        for b in self.context.portal_catalog(meta_type=("MeetingItem",)):
            obj = b.getObject()
            obj.updatePowerEditorsLocalRoles()
            # Update security
            obj.reindexObject(
                idxs=[
                    "allowedRolesAndUsers",
                ]
            )
        self.context.plone_utils.addPortalMessage("Done.")
        self.context.gotoReferer()

    def performCustomWFAdaptations(
            self, meetingConfig, wfAdaptation, logger, itemWorkflow, meetingWorkflow
    ):
        """This function applies workflow changes as specified by the
        p_meetingConfig."""
        itemStates = itemWorkflow.states
        itemTransitions = itemWorkflow.transitions

        if wfAdaptation == "seraing_add_item_closed_state":
            _addIsolatedState(
                new_state_id='accepted_closed',
                origin_state_id='accepted',
                origin_transition_id='accept_close',
                origin_transition_guard_expr_name='mayClose()',
                back_transition_guard_expr_name="mayCorrect()",
                back_transition_id='backToItemAccepted',
                itemWorkflow=itemWorkflow,
                base_state_id='accepted', )
            if "delayed" in itemStates:
                _addIsolatedState(
                    new_state_id='delayed_closed',
                    origin_state_id='delayed',
                    origin_transition_id='delay_close',
                    origin_transition_guard_expr_name='mayClose()',
                    back_transition_guard_expr_name="mayCorrect()",
                    back_transition_id='backToItemDelayed',
                    itemWorkflow=itemWorkflow,
                    base_state_id='delayed', )
            if "accepted_but_modified" in itemStates:
                _addIsolatedState(
                    new_state_id='accepted_but_modified_closed',
                    origin_state_id='accepted_but_modified',
                    origin_transition_id='accept_but_modify_close',
                    origin_transition_guard_expr_name='mayClose()',
                    back_transition_guard_expr_name="mayCorrect()",
                    back_transition_id='backToItemAcceptedButModified',
                    itemWorkflow=itemWorkflow,
                    base_state_id='accepted_but_modified', )
        if wfAdaptation == "seraing_validated_by_DG":
            # add state from itemfrozen? itempublished? presented? ...
            # same origin as mandatory transition 'accept'
            new_state = _addIsolatedState(
                new_state_id='validated_by_dg',
                origin_state_id='presented',
                origin_transition_id='itemValidateByDG',
                origin_transition_guard_expr_name='mayValidateByDG()',
                back_transition_guard_expr_name="mayCorrect()",
                back_transition_id='backToPresented',
                itemWorkflow=itemWorkflow,
                base_state_id='presented', )
            new_state.transitions = new_state.transitions + ('itemfreeze',)
            itemWorkflow.states['presented'].transitions = ('backToValidated', 'itemValidateByDG')

            itemWorkflow.transitions.addTransition("backToItemValidatedByDG")
            transition = itemWorkflow.transitions["backToItemValidatedByDG"]
            transition.setProperties(
                title="backToItemValidatedByDG",
                new_state_id="validated_by_dg", trigger_type=1, script_name='',
                actbox_name="backToItemValidatedByDG", actbox_url='',
                actbox_icon='%(portal_url)s/{0}.png'.format("backToItemValidatedByDG"),
                actbox_category='workflow',
                props={'guard_expr': 'python:here.wfConditions().{0}'.format("mayCorrect()")})
            itemfrozen = itemWorkflow.states['itemfrozen']
            itemfrozen.transitions = tuple(
                t for t in itemfrozen.transitions if t != 'backToPresented'
            ) + ("backToItemValidatedByDG",)

            new_meeting_state = _addIsolatedState(
                new_state_id='validated_by_dg',
                origin_state_id='created',
                origin_transition_id='validateByDG',
                origin_transition_guard_expr_name='mayValidateByDG()',
                back_transition_guard_expr_name="mayCorrect()",
                back_transition_id='backToCreated',
                itemWorkflow=meetingWorkflow,
                base_state_id='created', )
            new_meeting_state.transitions = new_meeting_state.transitions + ('freeze',)

            meetingWorkflow.states['created'].transitions = ('validateByDG',)
            meetingWorkflow.transitions.addTransition("backToValidatedByDG")
            transition = meetingWorkflow.transitions["backToValidatedByDG"]
            transition.setProperties(
                title="backToValidatedByDG",
                new_state_id="validated_by_dg", trigger_type=1, script_name='',
                actbox_name="backToValidatedByDG", actbox_url='',
                actbox_icon='%(portal_url)s/{0}.png'.format("backToValidatedByDG"),
                actbox_category='workflow',
                props={'guard_expr': 'python:here.wfConditions().{0}'.format("mayCorrect()")})
            frozen = meetingWorkflow.states['frozen']
            frozen.transitions = tuple(
                t for t in frozen.transitions if t != 'backToCreated'
            ) + ("backToValidatedByDG",)

        if wfAdaptation == "seraing_powereditors":
            # change permission for PloneMeeting: add annex for states in which
            # powereditors may edit
            for state_id in POWEREDITORS_EDITABLE_STATES:
                if state_id in itemWorkflow.states:
                    state = itemWorkflow.states[state_id]
                    state.permission_roles[AddAnnex] = state.permission_roles[AddAnnex] + ("Editor",)
        if wfAdaptation == "seraing_returned_to_advise":
            if "returned_to_proposing_group" not in itemStates:
                raise ValueError("returned_to_proposing_group should be in itemStates for this WFA")

            if "returned_to_advise" not in itemStates:
                itemStates.addState("returned_to_advise")
            returned_to_advise = getattr(itemStates, "returned_to_advise")
            returned_to_advise.permission_roles = deepcopy(itemStates.returned_to_proposing_group.permission_roles)

            if "return_to_advise" not in itemTransitions:
                itemTransitions.addTransition("return_to_advise")

            transition = itemTransitions["return_to_advise"]
            # use same guard from ReturnToProposingGroup
            transition.setProperties(
                title="return_to_advise",
                new_state_id="returned_to_advise",
                trigger_type=1,
                script_name="",
                actbox_name="return_to_advise",
                actbox_url="",
                actbox_category="workflow",
                actbox_icon="%(portal_url)s/return_to_advise.png",
                props={
                    "guard_expr": "python:here.wfConditions().mayReturnToProposingGroup()"
                },
            )
            returned_to_advise.setProperties(
                title="returned_to_advise",
                description="",
                transitions=(
                    "backTo_returned_to_proposing_group_from_returned_to_proposing_group_proposed",
                    "goTo_returned_to_proposing_group_proposed",
                ),
            )
            return_to_advice_item_state = [
                                              "presented",
                                              "validated_by_dg",
                                              "itemfrozen",
                                          ]
            if "returned_to_proposing_group_proposed" in itemStates:
                return_to_advice_item_state.append("returned_to_proposing_group_proposed")
            if "returned_to_proposing_group" in itemStates:
                return_to_advice_item_state.append("returned_to_proposing_group")
            for state_id in return_to_advice_item_state:
                new_trx = tuple(
                    list(itemStates[state_id].getTransitions()) + ["return_to_advise"]
                )
                itemStates[state_id].transitions = new_trx

            logger.info(WF_APPLIED % ("seraing_returned_to_advise", meetingConfig.getId()))
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

        itemState = self.context.query_state()
        # Add our icons for some review states
        if itemState == "proposed":
            icons.append(
                (
                    "proposeToDirector.png",
                    translate(
                        "icon_help_proposed_to_director",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "proposed_to_divisionhead":
            icons.append(
                (
                    "proposeToDivisionHead.png",
                    translate(
                        "icon_help_proposed_to_divisionhead",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "proposed_to_officemanager":
            icons.append(
                (
                    "proposeToOfficeManager.png",
                    translate(
                        "icon_help_proposed_to_officemanager",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "validated_by_dg":
            icons.append(
                (
                    "itemValidateByDG.png",
                    translate(
                        "icon_help_validated_by_dg",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "proposed_to_servicehead":
            icons.append(
                (
                    "proposeToServiceHead.png",
                    translate(
                        "icon_help_proposed_to_servicehead",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "accepted_but_modified_closed":
            icons.append(
                (
                    "accepted_but_modified.png",
                    translate(
                        "icon_help_accepted_but_modified_closed",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "delayed_closed":
            icons.append(
                (
                    "delayed.png",
                    translate(
                        "icon_help_delayed_closed",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        elif itemState == "returned_to_advise":
            icons.append(
                (
                    "returned_to_advise.png",
                    translate(
                        "icon_help_returned_to_advise",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )

        # add an icon if item is down the workflow from the finances
        # if item was ever gone the the finances and now it is down to the
        # services, then it is considered as down the wf from the finances
        # so take into account every states before 'validated/proposed_to_finance'
        if self.context.getIsToPrintInMeeting():
            icons.append(
                (
                    "toPrint.png",
                    translate(
                        "icon_help_to_print",
                        domain="PloneMeeting",
                        context=self.request,
                    ),
                )
            )
        return icons


# Power editors may store podtemplate as annex
def may_store_podtemplate_as_annex(self, pod_template):
    """By default only (Meeting)Managers are able to store a generated document as annex."""
    if not pod_template.store_as_annex:
        return False
    tool = api.portal.get_tool('portal_plonemeeting')
    cfg = tool.getMeetingConfig(self.context)
    return tool.isManager(cfg) or tool.userIsAmong(["powereditors"])


PMDocumentGeneratorLinksViewlet.may_store_as_annex = may_store_podtemplate_as_annex


def store_podtemplate_as_annex_batch_action_available(self):
    tool = api.portal.get_tool('portal_plonemeeting')
    """ """
    if self.cfg.getMeetingItemTemplatesToStoreAsAnnex() and \
            _checkPermission(ModifyPortalContent, self.context) or tool.userIsAmong(["powereditors"]):
        return True


MeetingStoreItemsPodTemplateAsAnnexBatchActionForm.available = store_podtemplate_as_annex_batch_action_available