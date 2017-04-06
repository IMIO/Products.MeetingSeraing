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
template1 = ItemTemplateDescriptor(id='template1',
                                   title='Tutelle CPAS',
                                   description='<p>Tutelle CPAS</p>',
                                   category='',
                                   proposingGroup='developers',
                                   templateUsingGroups=['developers', 'vendors'],
                                   decision="""<p>Vu la loi du 8 juillet 1976 organique des centres publics d'action sociale et plus particulièrement son article 111;</p>
<p>Vu l'Arrêté du Gouvernement Wallon du 22 avril 2004 portant codification de la législation relative aux pouvoirs locaux tel que confirmé par le décret du 27 mai 2004 du Conseil régional wallon;</p>
<p>Attendu que les décisions suivantes du Bureau permanent/du Conseil de l'Action sociale du XXX ont été reçues le XXX dans le cadre de la tutelle générale sur les centres publics d'action sociale :</p>
<p>- ...;</p>
<p>- ...;</p>
<p>- ...</p>
<p>Attendu que ces décisions sont conformes à la loi et à l'intérêt général;</p>
<p>Déclare à l'unanimité que :</p>
<p><strong>Article 1er :</strong></p>
<p>Les décisions du Bureau permanent/Conseil de l'Action sociale visées ci-dessus sont conformes à la loi et à l'intérêt général et qu'il n'y a, dès lors, pas lieu de les annuler.</p>
<p><strong>Article 2 :</strong></p>
<p>Copie de la présente délibération sera transmise au Bureau permanent/Conseil de l'Action sociale.</p>""")
template2 = ItemTemplateDescriptor(id='template2',
                                   title='Contrôle médical systématique agent contractuel',
                                   description='<p>Contrôle médical systématique agent contractuel</p>',
                                   category='',
                                   proposingGroup='vendors',
                                   templateUsingGroups=['vendors', ],
                                   decision="""<p>Vu la loi du 26 mai 2002 instituant le droit à l’intégration sociale;</p>
<p>Vu la délibération du Conseil communal du 29 juin 2009 concernant le cahier spécial des charges relatif au marché de services portant sur le contrôle des agents communaux absents pour raisons médicales;</p>
<p>Vu sa délibération du 17 décembre 2009 désignant le docteur XXX en qualité d’adjudicataire pour la mission de contrôle médical des agents de l’Administration communale;</p>
<p>Vu également sa décision du 17 décembre 2009 d’opérer les contrôles médicaux de manière systématique et pour une période d’essai d’un trimestre;</p>
<p>Attendu qu’un certificat médical a été  reçu le XXX concernant XXX la couvrant du XXX au XXX, avec la mention « XXX »;</p>
<p>Attendu que le Docteur XXX a transmis au service du Personnel, par fax, le même jour à XXX le rapport de contrôle mentionnant l’absence de XXX ce XXX à XXX;</p>
<p>Considérant que XXX avait été informée par le Service du Personnel de la mise en route du système de contrôle systématique que le médecin-contrôleur;</p>
<p>Considérant qu’ayant été absent(e) pour maladie la semaine précédente elle avait reçu la visite du médecin-contrôleur;</p>
<p>DECIDE :</p>
<p><strong>Article 1</strong> : De convoquer XXX devant  Monsieur le Secrétaire communal f.f. afin de lui rappeler ses obligations en la matière.</p>
<p><strong>Article 2</strong> :  De prévenir XXX, qu’en cas de récidive, il sera proposé par le Secrétaire communal au Collège de transformer les jours de congés de maladie en absence injustifiée (retenue sur traitement avec application de la loi du 26 mai 2002 citée ci-dessus).</p>
<p><strong>Article 3</strong> : De charger le service du personnel du suivi de ce dossier.</p>""")

# Categories -------------------------------------------------------------------
deployment = CategoryDescriptor('deployment', 'Deployment topics')
maintenance = CategoryDescriptor('maintenance', 'Maintenance topics')
development = CategoryDescriptor('development', 'Development topics')
events = CategoryDescriptor('events', 'Events')
research = CategoryDescriptor('research', 'Research topics')
projects = CategoryDescriptor('projects', 'Projects')
# A vintage category
marketing = CategoryDescriptor('marketing', 'Marketing', active=False)
# usingGroups category
subproducts = CategoryDescriptor('subproducts', 'Subproducts wishes', usingGroups=('vendors',))

# Classifiers
classifier1 = CategoryDescriptor('classifier1', 'Classifier 1')
classifier2 = CategoryDescriptor('classifier2', 'Classifier 2')
classifier3 = CategoryDescriptor('classifier3', 'Classifier 3')

# Users and groups -------------------------------------------------------------
admin = UserDescriptor('admin', ['Manager', 'MeetingManager'])
pmManager = UserDescriptor('pmManager', [])
pmCreator1 = UserDescriptor('pmCreator1', [])
pmCreator1b = UserDescriptor('pmCreator1b', [])
pmObserver1 = UserDescriptor('pmObserver1', [], email="pmobserver1@plonemeeting.org", fullname='M. PMObserver One')
pmReviewer1 = UserDescriptor('pmReviewer1', [])
pmServiceHead1 = UserDescriptor('pmServiceHead1', [])
pmOfficeManager1 = UserDescriptor('pmOfficeManager1', [])
pmDivisionHead1 = UserDescriptor('pmDivisionHead1', [])
pmReviewerLevel1 = UserDescriptor('pmReviewerLevel1', [],
                                  email="pmreviewerlevel1@plonemeeting.org", fullname='M. PMReviewer Level One')
pmCreator2 = UserDescriptor('pmCreator2', [])
pmReviewer2 = UserDescriptor('pmReviewer2', [])
pmReviewerLevel2 = UserDescriptor('pmReviewerLevel2', [],
                                  email="pmreviewerlevel2@plonemeeting.org", fullname='M. PMReviewer Level Two')
pmAdviser1 = UserDescriptor('pmAdviser1', [])
voter1 = UserDescriptor('voter1', [], fullname='M. Voter One')
voter2 = UserDescriptor('voter2', [], fullname='M. Voter Two')
powerobserver1 = UserDescriptor('powerobserver1',
                                [],
                                email="powerobserver1@plonemeeting.org",
                                fullname='M. Power Observer1')
# powerobserver1 is 'power observer' because in the meeting-config-college '_powerobservers' group
college_powerobservers = PloneGroupDescriptor('meeting-config-college_powerobservers',
                                              'meeting-config-college_powerobservers',
                                              [])
powerobserver1.ploneGroups = [college_powerobservers, ]
powerobserver2 = UserDescriptor('powerobserver2',
                                [],
                                email="powerobserver2@plonemeeting.org",
                                fullname='M. Power Observer2')

restrictedpowerobserver1 = UserDescriptor('restrictedpowerobserver1',
                                          [],
                                          email="restrictedpowerobserver1@plonemeeting.org",
                                          fullname='M. Restricted Power Observer 1')
college_restrictedpowerobservers = PloneGroupDescriptor('meeting-config-college_restrictedpowerobservers',
                                                        'meeting-config-college_restrictedpowerobservers',
                                                        [])
restrictedpowerobserver1.ploneGroups = [college_restrictedpowerobservers, ]
restrictedpowerobserver2 = UserDescriptor('restrictedpowerobserver2',
                                          [],
                                          email="restrictedpowerobserver2@plonemeeting.org",
                                          fullname='M. Restricted Power Observer 2')
council_restrictedpowerobservers = PloneGroupDescriptor('meeting-config-council_restrictedpowerobservers',
                                                        'meeting-config-council_restrictedpowerobservers',
                                                        [])
restrictedpowerobserver2.ploneGroups = [council_restrictedpowerobservers, ]

plonemeeting_assembly_powereditors = PloneGroupDescriptor('meeting-config-college_powereditors',
                                                          'meeting-config-council_powereditors', [])
powerEditor1 = UserDescriptor('powerEditor1', [])
powerEditor1.ploneGroups = [plonemeeting_assembly_powereditors, ]

developers = GroupDescriptor('developers', 'Developers', 'Devel')
developers.creators.append(pmCreator1)
developers.creators.append(pmCreator1b)
developers.creators.append(pmManager)
developers.observers.append(pmObserver1)
developers.serviceheads.append(pmReviewer1)
developers.serviceheads.append(pmServiceHead1)
developers.serviceheads.append(pmManager)
developers.officemanagers.append(pmOfficeManager1)
developers.officemanagers.append(pmManager)
developers.divisionheads.append(pmDivisionHead1)
developers.divisionheads.append(pmManager)
developers.reviewers.append(pmReviewer1)
developers.reviewers.append(pmManager)
developers.observers.append(pmReviewer1)
developers.observers.append(pmManager)
developers.advisers.append(pmAdviser1)
developers.advisers.append(pmManager)
setattr(developers, 'signatures', 'developers signatures')
setattr(developers, 'echevinServices', 'developers')

# put pmReviewerLevel1 in first level of reviewers from what is in MEETINGREVIEWERS
getattr(developers, MEETINGREVIEWERS.keys()[-1]).append(pmReviewerLevel1)
# put pmReviewerLevel2 in second level of reviewers from what is in MEETINGREVIEWERS
getattr(developers, MEETINGREVIEWERS.keys()[0]).append(pmReviewerLevel2)

# give an advice on recurring items
vendors = GroupDescriptor('vendors', 'Vendors', 'Devil')
vendors.creators.append(pmCreator2)
vendors.reviewers.append(pmReviewer2)
vendors.observers.append(pmReviewer2)
vendors.advisers.append(pmReviewer2)
vendors.advisers.append(pmManager)
setattr(vendors, 'signatures', '')

# Do voters able to see items to vote for
developers.observers.append(voter1)
developers.observers.append(voter2)
vendors.observers.append(voter1)
vendors.observers.append(voter2)

# Add a vintage group
endUsers = GroupDescriptor('endUsers', 'End users', 'EndUsers', active=False)

pmManager_observer = MeetingUserDescriptor('pmManager',
                                           duty='Secretaire de la Chancellerie',
                                           usages=['assemblyMember'])
cadranel_signer = MeetingUserDescriptor('cadranel', duty='Secretaire',
                                        usages=['assemblyMember', 'signer'],
                                        signatureImage='SignatureCadranel.jpg',
                                        signatureIsDefault=True)
# Add meeting users (voting purposes)
muser_voter1 = MeetingUserDescriptor('voter1', duty='Voter1',
                                     usages=['assemblyMember', 'voter', ])
muser_voter2 = MeetingUserDescriptor('voter2', duty='Voter2',
                                     usages=['assemblyMember', 'voter', ])

# budget impact editors
budgetimpacteditor = UserDescriptor('budgetimpacteditor',
                                    [],
                                    email="budgetimpacteditor@plonemeeting.org",
                                    fullname='M. Budget Impact Editor')
college_budgetimpacteditors = PloneGroupDescriptor('meeting-config-college_budgetimpacteditors',
                                                   'meeting-config-college_budgetimpacteditors',
                                                   [])
budgetimpacteditor.ploneGroups = [college_budgetimpacteditors,
                                  college_powerobservers]

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
collegeMeeting.categories = [development, research]
collegeMeeting.classifiers = [classifier1, classifier2, classifier3]
collegeMeeting.shortName = 'College'
collegeMeeting.annexTypes = [financialAnalysis, budgetAnalysisCfg1, overheadAnalysis,
                             itemAnnex, decisionAnnex, marketingAnalysis,
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
collegeMeeting.selectableAdvisers = ['developers', 'vendors']
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
collegeMeeting.selectableCopyGroups = [developers.getIdSuffixed('reviewers'), vendors.getIdSuffixed('reviewers'), ]
collegeMeeting.podTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]
collegeMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'meeting-config-council',
                                           'trigger_workflow_transitions_until': '__nothing__'}, ]
collegeMeeting.itemAutoSentToOtherMCStates = ('accepted', 'accepted_but_modified', 'accepted_closed', 'accepted_but_modified_closed', )
collegeMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recItem1',
        description='<p>This is the first recurring item.</p>',
        title='Recurring item #1',
        proposingGroup='developers',
        decision='First recurring item approved'),

    RecurringItemDescriptor(
        id='recItem2',
        title='Recurring item #2',
        description='<p>This is the second recurring item.</p>',
        proposingGroup='developers',
        decision='Second recurring item approved'),
]
collegeMeeting.itemTemplates = (template1, template2)

# Conseil communal
councilMeeting = MeetingConfigDescriptor(
    'meeting-config-council', 'Conseil Communal',
    'Conseil Communal')
councilMeeting.meetingManagers = ['pmManager', ]
councilMeeting.assembly = 'Default assembly'
councilMeeting.signatures = 'Default signatures'
councilMeeting.certifiedSignatures = []
councilMeeting.categories = [deployment, maintenance, development, events,
                             research, projects, marketing, subproducts]
councilMeeting.classifiers = [classifier1, classifier2, classifier3]
councilMeeting.shortName = 'Council'
councilMeeting.annexTypes = [financialAnalysis, legalAnalysis,
                             budgetAnalysisCfg2, itemAnnex, decisionAnnex,
                             adviceAnnex, adviceLegalAnalysis, meetingAnnex]
councilMeeting.usedItemAttributes = ['oralQuestion', 'itemInitiator', 'observations',
                                     'privacy', 'itemAssembly', 'itemIsSigned',
                                     'motivation', ]
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
councilMeeting.selectableCopyGroups = [developers.getIdSuffixed('reviewers'), vendors.getIdSuffixed('reviewers'), ]
councilMeeting.itemCopyGroupsStates = []
councilMeeting.useVotes = True
councilMeeting.meetingUsers = [muser_voter1, muser_voter2, ]
councilMeeting.recurringItems = []
councilMeeting.itemTemplates = (template1, template2)

# no recurring items for this meetingConfig, only for tests !!!
# so we can test a meetingConfig with recurring items (college) and without (council)

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes seances',
    meetingConfigs=(collegeMeeting, councilMeeting),
    groups=(developers, vendors, endUsers))
# necessary for testSetup.test_pm_ToolAttributesAreOnlySetOnFirstImportData
data.restrictUsers = False
data.usersOutsideGroups = [voter1, voter2, powerobserver1, powerobserver2, powerEditor1,
                           restrictedpowerobserver1, restrictedpowerobserver2, budgetimpacteditor]
# ------------------------------------------------------------------------------
