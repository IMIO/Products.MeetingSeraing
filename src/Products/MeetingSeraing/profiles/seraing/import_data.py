# -*- coding: utf-8 -*-
from Products.PloneMeeting.config import MEETINGREVIEWERS
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import GroupDescriptor
from Products.PloneMeeting.profiles import ItemAnnexSubTypeDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import ItemTemplateDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import MeetingUserDescriptor
from Products.PloneMeeting.profiles import PloneGroupDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import RecurringItemDescriptor
from Products.PloneMeeting.profiles import UserDescriptor

# Annex types
overheadAnalysisSubtype = ItemAnnexSubTypeDescriptor(
    'overhead-analysis-sub-annex',
    'Overhead analysis sub annex',
    other_mc_correspondences=(
        'meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis', ))

overheadAnalysis = ItemAnnexTypeDescriptor(
    'overhead-analysis', 'Administrative overhead analysis',
    u'overheadAnalysis.png',
    subTypes=[overheadAnalysisSubtype],
    other_mc_correspondences=(
        'meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis_-_budget-analysis-sub-annex', ))

financialAnalysisSubAnnex = ItemAnnexSubTypeDescriptor(
    'financial-analysis-sub-annex',
    'Financial analysis sub annex')

financialAnalysis = ItemAnnexTypeDescriptor(
    'financial-analysis', 'Financial analysis', u'financialAnalysis.png',
    u'Predefined title for financial analysis', subTypes=[financialAnalysisSubAnnex])

legalAnalysis = ItemAnnexTypeDescriptor(
    'legal-analysis', 'Legal analysis', u'legalAnalysis.png')

budgetAnalysisCfg2Subtype = ItemAnnexSubTypeDescriptor(
    'budget-analysis-sub-annex',
    'Budget analysis sub annex')

budgetAnalysisCfg2 = ItemAnnexTypeDescriptor(
    'budget-analysis', 'Budget analysis', u'budgetAnalysis.png',
    subTypes=[budgetAnalysisCfg2Subtype])

budgetAnalysisCfg1Subtype = ItemAnnexSubTypeDescriptor(
    'budget-analysis-sub-annex',
    'Budget analysis sub annex',
    other_mc_correspondences=(
        'meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis_-_budget-analysis-sub-annex', ))

budgetAnalysisCfg1 = ItemAnnexTypeDescriptor(
    'budget-analysis', 'Budget analysis', u'budgetAnalysis.png',
    subTypes=[budgetAnalysisCfg1Subtype],
    other_mc_correspondences=('meeting-config-council_-_annexes_types_-_item_annexes_-_budget-analysis', ))

itemAnnex = ItemAnnexTypeDescriptor(
    'item-annex', 'Other annex(es)', u'itemAnnex.png')
# Could be used once we
# will digitally sign decisions ? Indeed, once signed, we will need to
# store them (together with the signature) as separate files.
decision = ItemAnnexTypeDescriptor(
    'decision', 'Decision', u'decision.png', relatedTo='item_decision')
decisionAnnex = ItemAnnexTypeDescriptor(
    'decision-annex', 'Decision annex(es)', u'decisionAnnex.png', relatedTo='item_decision')
# A vintage annex type
marketingAnalysis = ItemAnnexTypeDescriptor(
    'marketing-annex', 'Marketing annex(es)', u'legalAnalysis.png', relatedTo='item_decision',
    enabled=False)
# Advice annex types
adviceAnnex = AnnexTypeDescriptor(
    'advice-annex', 'Advice annex(es)', u'itemAnnex.png', relatedTo='advice')
adviceLegalAnalysis = AnnexTypeDescriptor(
    'advice-legal-analysis', 'Advice legal analysis', u'legalAnalysis.png', relatedTo='advice')
# Meeting annex types
meetingAnnex = AnnexTypeDescriptor(
    'meeting-annex', 'Meeting annex(es)', u'itemAnnex.png', relatedTo='meeting')

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.odt_file = 'Agenda.odt'
agendaTemplate.pod_portal_types = ['MeetingCollege']
agendaTemplate.tal_condition = 'python:(here.meta_type=="Meeting") and here.portal_plonemeeting.isManager()'


decisionsTemplate = PodTemplateDescriptor('decisionsTemplate', 'Meeting decisions')
decisionsTemplate.odt_file = 'Decisions.odt'
decisionsTemplate.pod_portal_types = ['MeetingCollege']
decisionsTemplate.tal_condition = 'python:here.adapted().isDecided()'

itemTemplate = PodTemplateDescriptor('itemTemplate', 'Meeting item')
itemTemplate.odt_file = 'Item.odt'
itemTemplate.pod_portal_types = ['MeetingItemCollege']
itemTemplate.tal_condition = ''

# item templates

# Categories -------------------------------------------------------------------

# Users and groups -------------------------------------------------------------
admin = UserDescriptor('admin', ['Manager', 'MeetingManager'])
# powerobserver1 is 'power observer' because in the meeting-config-college '_powerobservers' group

# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-college', 'College Communal',
    'College communal', isDefault=True)
collegeMeeting.meetingManagers = ['pmManager', ]
collegeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
collegeMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
collegeMeeting.certifiedSignatures = []
collegeMeeting.categories = []
collegeMeeting.classifiers = []
collegeMeeting.shortName = 'College'
collegeMeeting.annexTypes = [financialAnalysis, budgetAnalysisCfg1, overheadAnalysis,
                             itemAnnex, decisionAnnex, marketingAnalysis,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
collegeMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
collegeMeeting.maxShownListings = '100'
collegeMeeting.itemWorkflow = 'meetingitemseraing_workflow'
collegeMeeting.meetingWorkflow = 'meetingseraing_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowActions'
collegeMeeting.transitionsToConfirm = []
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
collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.recordItemHistoryStates = []
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'searchallitems'
collegeMeeting.itemDocFormats = ('odt', 'pdf')
collegeMeeting.meetingDocFormats = ('odt', 'pdf')
collegeMeeting.useAdvices = True
collegeMeeting.selectableAdvisers = []
collegeMeeting.itemAdviceStates = ['proposed', ]
collegeMeeting.itemAdviceEditStates = ['proposed', 'validated']
collegeMeeting.itemAdviceViewStates = ['presented', ]
collegeMeeting.transitionsReinitializingDelays = ('backToItemCreated', )
collegeMeeting.enforceAdviceMandatoriness = False
collegeMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed', )
collegeMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified', 'accepted_closed', 'delayed_closed', 'accepted_but_modified_closed', ]
collegeMeeting.workflowAdaptations = []
collegeMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                             'reverse': '0'}, )
collegeMeeting.useGroupsAsCategories = True
collegeMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
collegeMeeting.useCopies = True
collegeMeeting.itemCopyGroupsStates = []
collegeMeeting.selectableCopyGroups = []
collegeMeeting.podTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]
collegeMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'meeting-config-council',
                                           'trigger_workflow_transitions_until': '__nothing__'}, ]
collegeMeeting.itemAutoSentToOtherMCStates = ('accepted', 'accepted_but_modified', 'accepted_closed', 'accepted_but_modified_closed', )
collegeMeeting.recurringItems = []
collegeMeeting.itemTemplates = ()

# Conseil communal
councilMeeting = MeetingConfigDescriptor(
    'meeting-config-council', 'Conseil Communal',
    'Conseil Communal')
councilMeeting.meetingManagers = ['pmManager', ]
councilMeeting.assembly = 'Default assembly'
councilMeeting.signatures = 'Default signatures'
councilMeeting.certifiedSignatures = []
councilMeeting.categories = []
councilMeeting.shortName = 'Council'
councilMeeting.annexTypes = [financialAnalysis, legalAnalysis,
                             budgetAnalysisCfg2, itemAnnex, decisionAnnex,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
councilMeeting.usedItemAttributes = ['oralQuestion', 'itemInitiator', 'observations',
                                     'privacy', 'itemAssembly', 'itemIsSigned',
                                     'motivation', ]
councilMeeting.maxShownListings = '100'
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
councilMeeting.itemTopicStates = ('itemcreated', 'proposed_to_servicehead', 'proposed_to_officemanager',
                                  'proposed_to_divisionhead', 'proposed', 'validated',
                                  'presented', 'itemfrozen', 'accepted',
                                  'delayed', )
councilMeeting.meetingTopicStates = ('created', 'frozen')
councilMeeting.decisionTopicStates = ('decided', 'closed')
councilMeeting.recordItemHistoryStates = []
councilMeeting.maxShownMeetings = 5
councilMeeting.maxDaysDecisions = 60
councilMeeting.meetingAppDefaultView = 'searchallitems'
councilMeeting.itemDocFormats = ('odt', 'pdf')
councilMeeting.meetingDocFormats = ('odt', 'pdf')
councilMeeting.useAdvices = False
councilMeeting.selectableAdvisers = []
councilMeeting.itemAdviceStates = ['proposed', ]
councilMeeting.itemAdviceEditStates = ['proposed', 'validated']
councilMeeting.itemAdviceViewStates = ['presented', ]
councilMeeting.transitionsReinitializingDelays = 'backToItemCreated'
councilMeeting.enforceAdviceMandatoriness = False
councilMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed')
councilMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified', 'accepted_closed', 'delayed_closed', 'accepted_but_modified_closed', ]
councilMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_categories',
                                             'reverse': '0'}, )
councilMeeting.useGroupsAsCategories = False
councilMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
councilMeeting.useCopies = True
councilMeeting.selectableCopyGroups = [ ]
councilMeeting.itemCopyGroupsStates = []
councilMeeting.useVotes = True
councilMeeting.meetingUsers = []
councilMeeting.recurringItems = []
councilMeeting.itemTemplates = ()

# no recurring items for this meetingConfig, only for tests !!!
# so we can test a meetingConfig with recurring items (college) and without (council)

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes seances',
    meetingConfigs=(collegeMeeting, councilMeeting),
    groups=())
# necessary for testSetup.test_pm_ToolAttributesAreOnlySetOnFirstImportData
data.restrictUsers = False
data.usersOutsideGroups = []
# ------------------------------------------------------------------------------
