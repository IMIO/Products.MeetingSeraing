# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data
from Products.PloneMeeting.config import MEETINGREVIEWERS
from Products.PloneMeeting.profiles import PloneGroupDescriptor
from Products.PloneMeeting.profiles import UserDescriptor

data = deepcopy(mc_import_data.data)

# Users and groups -------------------------------------------------------------4
pmServiceHead1 = UserDescriptor('pmServiceHead1', [])
pmOfficeManager1 = UserDescriptor('pmOfficeManager1', [])
pmDivisionHead1 = UserDescriptor('pmDivisionHead1', [])

plonemeeting_assembly_powereditors = PloneGroupDescriptor('meeting-config-college_powereditors',
                                                          'meeting-config-council_powereditors', [])
powerEditor1 = UserDescriptor('powerEditor1', [])
powerEditor1.ploneGroups = [plonemeeting_assembly_powereditors, ]

# Inherited users
pmReviewer1 = deepcopy(pm_import_data.pmReviewer1)
pmReviewer2 = deepcopy(pm_import_data.pmReviewer2)
pmReviewerLevel1 = deepcopy(pm_import_data.pmReviewerLevel1)
pmReviewerLevel2 = deepcopy(pm_import_data.pmReviewerLevel2)
pmManager = deepcopy(pm_import_data.pmManager)

# Groups

developers = data.orgs[0]
developers.serviceheads.append(pmReviewer1)
developers.serviceheads.append(pmServiceHead1)
developers.serviceheads.append(pmManager)
developers.officemanagers.append(pmOfficeManager1)
developers.officemanagers.append(pmManager)
developers.divisionheads.append(pmDivisionHead1)
developers.divisionheads.append(pmManager)

# to serviceheads that is first reviewer level
developers.prereviewers = [descr for descr in developers.prereviewers if descr.id != 'pmReviewerLevel1']
getattr(developers, MEETINGREVIEWERS['meetingitemseraing_workflow'].keys()[-1]).append(pmReviewerLevel1)

vendors = data.orgs[1]
vendors.serviceheads.append(pmReviewer2)
vendors.officemanagers.append(pmReviewer2)
vendors.divisionheads.append(pmReviewer2)

# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)
collegeMeeting.id = 'meeting-config-college'
collegeMeeting.Title = 'Collège Communal'
collegeMeeting.folderTitle = 'Collège Communal'
collegeMeeting.shortName = 'TestCollege'
collegeMeeting.id = 'meeting-config-college'
collegeMeeting.isDefault = True
collegeMeeting.itemWorkflow = 'meetingitemseraing_workflow'
collegeMeeting.meetingWorkflow = 'meetingseraing_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowActions'
collegeMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified', 'pre_accepted']
collegeMeeting.itemPositiveDecidedStates = ['accepted', 'accepted_but_modified']
collegeMeeting.transitionsForPresentingAnItem = ('proposeToServiceHead',
                                                 'proposeToOfficeManager',
                                                 'proposeToDivisionHead',
                                                 'propose',
                                                 'validate',
                                                 'present', )
collegeMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'validateByDG',
                                                              'item_transition': 'itemValidateByDG'},

                                                             {'meeting_transition': 'freeze',
                                                              'item_transition': 'itemValidateByDG'},
                                                             {'meeting_transition': 'freeze',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'decide',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'itemValidateByDG'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'itemfreeze'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept_close'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept_but_modify_close'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'delay_close'},

                                                             {'meeting_transition': 'backToCreated',
                                                              'item_transition': 'backToItemValidatedByDG'},
                                                             {'meeting_transition': 'backToCreated',
                                                              'item_transition': 'backToPresented'},)
collegeMeeting.itemTopicStates = ('itemcreated', 'proposed_to_servicehead', 'proposed_to_officemanager',
                                  'proposed_to_divisionhead', 'proposed', 'validated',
                                  'presented', 'itemfrozen', 'accepted',
                                  'delayed', )
collegeMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified', 'accepted_closed', 'delayed_closed', 'accepted_but_modified_closed', ]
collegeMeeting.workflowAdaptations = []
collegeMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups', 'reverse': '0'}, )
collegeMeeting.itemAutoSentToOtherMCStates = ('accepted', 'accepted_but_modified', 'accepted_closed', 'accepted_but_modified_closed', )

# Conseil communal
councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.id = 'meeting-config-council'
councilMeeting.Title = 'Conseil Communal'
councilMeeting.folderTitle = 'Conseil Communal'
councilMeeting.shortName = 'TestCouncil'
councilMeeting.isDefault = False
councilMeeting.itemWorkflow = 'meetingitemseraing_workflow'
councilMeeting.meetingWorkflow = 'meetingseraing_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCouncilWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCouncilWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCouncilWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCouncilWorkflowActions'
councilMeeting.transitionsToConfirm = []
councilMeeting.transitionsForPresentingAnItem = ('proposeToServiceHead',
                                                 'proposeToOfficeManager',
                                                 'proposeToDivisionHead',
                                                 'propose',
                                                 'validate',
                                                 'present', )
councilMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_categories', 'reverse': '0'}, )
councilMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'validateByDG',
                                                              'item_transition': 'itemValidateByDG'},

                                                             {'meeting_transition': 'freeze',
                                                              'item_transition': 'itemValidateByDG'},
                                                             {'meeting_transition': 'freeze',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'decide',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'itemValidateByDG'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'itemfreeze'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept_close'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept_but_modify_close'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'delay_close'},

                                                             {'meeting_transition': 'backToCreated',
                                                              'item_transition': 'backToItemValidatedByDG'},
                                                             {'meeting_transition': 'backToCreated',
                                                              'item_transition': 'backToPresented'},)
councilMeeting.itemCopyGroupsStates = []
councilMeeting.itemTopicStates = ('itemcreated', 'proposed_to_servicehead', 'proposed_to_officemanager',
                                  'proposed_to_divisionhead', 'proposed', 'validated',
                                  'presented', 'itemfrozen', 'accepted',
                                  'delayed', )
councilMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified', 'accepted_closed', 'delayed_closed', 'accepted_but_modified_closed', ]

data.meetingConfigs = (collegeMeeting, councilMeeting)
data.usersOutsideGroups += [powerEditor1, pmServiceHead1, pmOfficeManager1, pmDivisionHead1]
