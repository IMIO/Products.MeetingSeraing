# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data

data = deepcopy(mc_import_data.data)

# Remove persons -------------------------------------------------
data.persons = []

# No Users and groups -----------------------------------------------

# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)
collegeMeeting.id = 'meeting-config-college'
collegeMeeting.title = 'Collège Communal'
collegeMeeting.folderTitle = 'Collège Communal'
collegeMeeting.shortName = 'College'
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
councilMeeting.title = 'Conseil Communal'
councilMeeting.folderTitle = 'Conseil Communal'
councilMeeting.shortName = 'Council'
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
data.usersOutsideGroups = []
