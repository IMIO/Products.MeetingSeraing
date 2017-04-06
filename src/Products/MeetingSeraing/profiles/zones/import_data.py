# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
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
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-zcollege', 'Collège',
    'Collège', isDefault=False)
collegeMeeting.meetingManagers = ['dgen', ]
collegeMeeting.assembly = 'Marie Curie - Présidente,\n' \
                          'Isaac Newton(ville de Physique),\n' \
                          'Pythagore (ville de Mathématiques),\n' \
                          'Louis Pasteur (ville de Chimie), Bourgmestres\n' \
                          'Archimède, Secrétaire du Collège,\n' \
                          'Albert Einstein, Commandant de zone'
collegeMeeting.signatures = 'Le Commandant de zone\nAlbert Einstein\nLa présidente\nMarie Curie'
collegeMeeting.certifiedSignatures = []
collegeMeeting.categories = categories
collegeMeeting.shortName = 'ZCollege'
collegeMeeting.annexTypes = [financialAnalysis, itemAnnex, decisionAnnex, marketingAnalysis,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
collegeMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
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
collegeMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
collegeMeeting.itemTopicStates = ('itemcreated', 'proposed_to_servicehead', 'proposed_to_officemanager',
                                'proposed_to_divisionhead', 'proposed', 'validated',
                                'presented', 'itemfrozen', 'accepted',
                                'delayed',)
collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.recordItemHistoryStates = []
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'searchallitems'
collegeMeeting.itemDocFormats = ('odt', 'pdf')
collegeMeeting.meetingDocFormats = ('odt', 'pdf')
collegeMeeting.useAdvices = True
collegeMeeting.itemAdviceStates = ['proposed', ]
collegeMeeting.itemAdviceEditStates = ['proposed', 'validated']
collegeMeeting.itemAdviceViewStates = ['presented', ]
collegeMeeting.transitionReinitializingDelays = 'backToItemCreated'
collegeMeeting.enforceAdviceMandatoriness = False
collegeMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed')
collegeMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified']
collegeMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                           'reverse': '0'}, )
collegeMeeting.useGroupsAsCategories = True
collegeMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
collegeMeeting.useCopies = True
collegeMeeting.itemCopyGroupsStates = []
collegeMeeting.selectableCopyGroups = []
collegeMeeting.podTemplates = []
collegeMeeting.meetingConfigsToCloneTo = []
collegeMeeting.recurringItems = []
collegeMeeting.itemTemplates = []

# ------------------------------------------------------------------------------

# Conseil
councilMeeting = MeetingConfigDescriptor(
    'meeting-config-zcouncil', 'Conseil',
    'Conseil')
councilMeeting.meetingManagers = ['dgen', ]
councilMeeting.assembly = 'Marie Curie - Présidente,\n' \
                          'Isaac Newton(ville de Physique),\n' \
                          'Pythagore (ville de Mathématiques),\n' \
                          'Louis Pasteur (ville de Chimie), Bourgmestres\n' \
                          'Archimède, Secrétaire du Collège,\n' \
                          'Albert Einstein, Commandant de zone'
councilMeeting.signatures = 'Le Commandant de zone\nAlbert Einstein\nLa présidente\nMarie Curie'
councilMeeting.certifiedSignatures = []
councilMeeting.categories = categories
councilMeeting.shortName = 'ZCouncil'
councilMeeting.annexTypes = [financialAnalysis, itemAnnex, decisionAnnex, marketingAnalysis,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
councilMeeting.usedItemAttributes = ('toDiscuss', 'associatedGroups', 'itemIsSigned',)
councilMeeting.itemWorkflow = 'meetingitemseraing_workflow'
councilMeeting.meetingWorkflow = 'meetingseraing_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemSeraingCollegeWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingSeraingCollegeWorkflowActions'
councilMeeting.transitionsToConfirm = []
councilMeeting.transitionsForPresentingAnItem = ('proposeToServiceHead',
                                               'proposeToOfficeManager',
                                               'proposeToDivisionHead',
                                               'propose',
                                               'validate',
                                               'present', )
councilMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
councilMeeting.itemTopicStates = ('itemcreated', 'proposed_to_servicehead', 'proposed_to_officemanager',
                                'proposed_to_divisionhead', 'proposed', 'validated',
                                'presented', 'itemfrozen', 'accepted',
                                'delayed',)
councilMeeting.meetingTopicStates = ('created', 'frozen')
councilMeeting.decisionTopicStates = ('decided', 'closed')
councilMeeting.recordItemHistoryStates = []
councilMeeting.maxShownMeetings = 5
councilMeeting.maxDaysDecisions = 60
councilMeeting.meetingAppDefaultView = 'searchallitems'
councilMeeting.itemDocFormats = ('odt', 'pdf')
councilMeeting.meetingDocFormats = ('odt', 'pdf')
councilMeeting.useAdvices = True
councilMeeting.itemAdviceStates = ['proposed', ]
councilMeeting.itemAdviceEditStates = ['proposed', 'validated']
councilMeeting.itemAdviceViewStates = ['presented', ]
councilMeeting.transitionReinitializingDelays = 'backToItemCreated'
councilMeeting.enforceAdviceMandatoriness = False
councilMeeting.itemPowerObserversStates = ('itemcreated', 'presented', 'accepted', 'delayed')
councilMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified']
councilMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                           'reverse': '0'}, )
councilMeeting.useGroupsAsCategories = True
councilMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
councilMeeting.useCopies = True
councilMeeting.itemCopyGroupsStates = []
councilMeeting.selectableCopyGroups = []
councilMeeting.podTemplates = []
councilMeeting.meetingConfigsToCloneTo = []
councilMeeting.recurringItems = []
councilMeeting.itemTemplates = []

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes seances',
    meetingConfigs=(collegeMeeting, councilMeeting),
    groups=([]))
# necessary for testSetup.test_pm_ToolAttributesAreOnlySetOnFirstImportData
data.restrictUsers = False
# ------------------------------------------------------------------------------
