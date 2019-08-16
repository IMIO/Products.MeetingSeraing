# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import ItemAnnexSubTypeDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration

# Annex types

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

# Categories -------------------------------------------------------------------
categories = []

# Users and groups -------------------------------------------------------------

# Meeting configurations -------------------------------------------------------
# codir
codirMeeting = deepcopy(mc_import_data.collegeMeeting)
codirMeeting.id = 'meeting-config-codir'
codirMeeting.Title = 'Comité de direction'
codirMeeting.folderTitle = 'Comité de direction'
codirMeeting.shortName = 'CoDir'
codirMeeting.meetingManagers = ['pmManager', ]
codirMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                        'Charles Exemple - 1er Echevin,\n' \
                        'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                        'Jacqueline Exemple, Responsable du CPAS'
codirMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
codirMeeting.certifiedSignatures = []
codirMeeting.categories = categories
codirMeeting.annexTypes = [financialAnalysis, itemAnnex, decisionAnnex, marketingAnalysis,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
codirMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
codirMeeting.itemWorkflow = 'meetingitemseraing_workflow'
codirMeeting.meetingWorkflow = 'meetingseraing_workflow'
codirMeeting.itemConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowConditions'
codirMeeting.itemActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowActions'
codirMeeting.meetingConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowConditions'
codirMeeting.meetingActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowActions'
codirMeeting.transitionsToConfirm = []
codirMeeting.workflowAdaptations = []
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
                                'delayed',)
codirMeeting.meetingTopicStates = ('created', 'frozen')
codirMeeting.decisionTopicStates = ('decided', 'closed')
codirMeeting.recordItemHistoryStates = []
codirMeeting.maxShownMeetings = 5
codirMeeting.maxDaysDecisions = 60
codirMeeting.meetingAppDefaultView = 'searchallitems'
codirMeeting.itemDocFormats = ('odt', 'pdf')
codirMeeting.meetingDocFormats = ('odt', 'pdf')
codirMeeting.useAdvices = True
codirMeeting.itemAdviceStates = ['proposed', ]
codirMeeting.itemAdviceEditStates = ['proposed', 'validated']
codirMeeting.itemAdviceViewStates = ['presented', ]
codirMeeting.transitionReinitializingDelays = 'backToItemCreated'
codirMeeting.enforceAdviceMandatoriness = False
codirMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed')
codirMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified']
codirMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                           'reverse': '0'}, )
codirMeeting.useGroupsAsCategories = True
codirMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
codirMeeting.useCopies = True
codirMeeting.itemCopyGroupsStates = []
codirMeeting.selectableCopyGroups = []
codirMeeting.podTemplates = []
codirMeeting.meetingConfigsToCloneTo = []
codirMeeting.recurringItems = []
codirMeeting.itemTemplates = []


data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(codirMeeting, ), orgs=[])
# necessary for testSetup.test_pm_ToolAttributesAreOnlySetOnFirstImportData
data.restrictUsers = False
# ------------------------------------------------------------------------------
