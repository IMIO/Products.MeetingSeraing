# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data

data = deepcopy(mc_import_data.data)

# Remove persons -------------------------------------------------
data.persons = []

# Meeting configurations -------------------------------------------------------
# college
codirMeeting = deepcopy(mc_import_data.collegeMeeting)
codirMeeting.id = 'meeting-config-codir'
codirMeeting.Title = 'Comité de direction'
codirMeeting.folderTitle = 'Comité de direction'
codirMeeting.shortName = 'CoDir'
codirMeeting.isDefault = True
codirMeeting.itemWorkflow = 'meetingitemseraing_workflow'
codirMeeting.meetingWorkflow = 'meetingseraing_workflow'
codirMeeting.itemConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowConditions'
codirMeeting.itemActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowActions'
codirMeeting.meetingConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowConditions'
codirMeeting.meetingActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowActions'
codirMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified', 'pre_accepted']
codirMeeting.itemPositiveDecidedStates = ['accepted', 'accepted_but_modified']
codirMeeting.transitionsForPresentingAnItem = ('proposeToServiceHead',
                                                 'proposeToOfficeManager',
                                                 'proposeToDivisionHead',
                                                 'propose',
                                                 'validate',
                                                 'present', )
codirMeeting.meetingConfigsToCloneTo = []
codirMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'validateByDG',
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
codirMeeting.itemTopicStates = ('itemcreated', 'proposed_to_servicehead', 'proposed_to_officemanager',
                                  'proposed_to_divisionhead', 'proposed', 'validated',
                                  'presented', 'itemfrozen', 'accepted',
                                  'delayed', )
codirMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified', 'accepted_closed', 'delayed_closed', 'accepted_but_modified_closed', ]
codirMeeting.workflowAdaptations = []
codirMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups', 'reverse': '0'}, )
codirMeeting.itemAutoSentToOtherMCStates = ('accepted', 'accepted_but_modified', 'accepted_closed', 'accepted_but_modified_closed', )


data.meetingConfigs = (codirMeeting, )
data.usersOutsideGroups = []
