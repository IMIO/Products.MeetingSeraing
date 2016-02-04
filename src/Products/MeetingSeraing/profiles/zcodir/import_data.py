# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import MeetingFileTypeDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration

# File types -------------------------------------------------------------------

annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgetaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
itemAnnex = MeetingFileTypeDescriptor('item-annex', 'Other annex(es)', 'attach.png', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe a la decision', 'attach.png', '', 'item_decision')
# Some type of annexes taken from the default PloneMeeting test profile
marketingAnalysis = MeetingFileTypeDescriptor(
    'marketing-annex', 'Marketing annex(es)', 'attach.png', '', 'item_decision',
    active=False)
overheadAnalysis = MeetingFileTypeDescriptor(
    'overhead-analysis', 'Administrative overhead analysis',
    'attach.png', '')
# Advice annexes types
adviceAnnex = MeetingFileTypeDescriptor(
    'advice-annex', 'Advice annex(es)', 'attach.png', '', 'advice')
adviceLegalAnalysis = MeetingFileTypeDescriptor(
    'advice-legal-analysis', 'Advice legal analysis', 'attach.png', '', 'advice')

# Categories -------------------------------------------------------------------
categories = []

# Users and groups -------------------------------------------------------------

# Meeting configurations -------------------------------------------------------
# codir
codirMeeting = MeetingConfigDescriptor(
    'codir', 'Comité de Direction',
    'Comité de Direction')
codirMeeting.meetingManagers = ['pmManager', ]
codirMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                        'Charles Exemple - 1er Echevin,\n' \
                        'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                        'Jacqueline Exemple, Responsable du CPAS'
codirMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
codirMeeting.certifiedSignatures = []
codirMeeting.categories = categories
codirMeeting.shortName = 'CoDir'
codirMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, itemAnnex,
                                 annexeDecision, overheadAnalysis, marketingAnalysis,
                                 adviceAnnex, adviceLegalAnalysis]
codirMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
codirMeeting.itemWorkflow = 'meetingitemcollegeseraing_workflow'
codirMeeting.meetingWorkflow = 'meetingcollegeseraing_workflow'
codirMeeting.itemConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemCollegeSeraingWorkflowConditions'
codirMeeting.itemActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemCollegeSeraingWorkflowActions'
codirMeeting.meetingConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingCollegeSeraingWorkflowConditions'
codirMeeting.meetingActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingCollegeSeraingWorkflowActions'
codirMeeting.transitionsToConfirm = []
codirMeeting.transitionsForPresentingAnItem = ('proposeToServiceHead',
                                               'proposeToOfficeManager',
                                               'proposeToDivisionHead',
                                               'propose',
                                               'validate',
                                               'present', )
codirMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
                                                            'item_transition': 'itemfreeze'},
                                                           {'meeting_transition': 'decide',
                                                            'item_transition': 'itemfreeze'},

                                                           {'meeting_transition': 'publish_decisions',
                                                            'item_transition': 'itemfreeze'},
                                                           {'meeting_transition': 'publish_decisions',
                                                            'item_transition': 'accept'},

                                                           {'meeting_transition': 'close',
                                                            'item_transition': 'itemfreeze'},
                                                           {'meeting_transition': 'close',
                                                            'item_transition': 'accept'},

                                                           {'meeting_transition': 'backToCreated',
                                                            'item_transition': 'backToPresented'},)
codirMeeting.itemTopicStates = ('itemcreated', 'proposed_to_servicehead', 'proposed_to_officemanager',
                                'proposed_to_divisionhead', 'proposed', 'validated',
                                'presented', 'itemfrozen', 'accepted',
                                'delayed', 'pre_accepted', 'removed',)
codirMeeting.meetingTopicStates = ('created', 'frozen')
codirMeeting.decisionTopicStates = ('decided', 'closed')
codirMeeting.recordItemHistoryStates = []
codirMeeting.maxShownMeetings = 5
codirMeeting.maxDaysDecisions = 60
codirMeeting.meetingAppDefaultView = 'topic_searchmyitems'
codirMeeting.itemDocFormats = ('odt', 'pdf')
codirMeeting.meetingDocFormats = ('odt', 'pdf')
codirMeeting.useAdvices = True
codirMeeting.itemAdviceStates = ['proposed', ]
codirMeeting.itemAdviceEditStates = ['proposed', 'validated']
codirMeeting.itemAdviceViewStates = ['presented', ]
codirMeeting.transitionReinitializingDelays = 'backToItemCreated'
codirMeeting.enforceAdviceMandatoriness = False
codirMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', 'refused')
codirMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
codirMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                           'reverse': '0'}, )
codirMeeting.useGroupsAsCategories = True
codirMeeting.meetingPowerObserversStates = ('frozen', 'published', 'decided', 'closed')
codirMeeting.useCopies = True
codirMeeting.selectableCopyGroups = []
codirMeeting.podTemplates = []
codirMeeting.meetingConfigsToCloneTo = []
codirMeeting.recurringItems = []
codirMeeting.itemTemplates = []


data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(codirMeeting, ),
                                 groups=[])
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
