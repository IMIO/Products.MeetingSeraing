# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import GroupDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import MeetingFileTypeDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import RecurringItemDescriptor
from Products.PloneMeeting.profiles import UserDescriptor

today = DateTime().strftime('%Y/%m/%d')

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgétaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
annexeRemarks = MeetingFileTypeDescriptor('annexeRemarks', 'Remarques secrétaires',
                                          'secretary_remarks.png', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision',
                                           'attach.png', '', 'item_decision')
annexeAvis = MeetingFileTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                       'attach.png', '', 'advice')
annexeAvisLegal = MeetingFileTypeDescriptor('annexeAvisLegal', 'Extrait article de loi',
                                            'legalAdvice.png', '', 'advice')
# Pod templates ----------------------------------------------------------------
# MeetingItem
collegeDelibTemplate = PodTemplateDescriptor('college-deliberation', 'Délibération')
collegeDelibTemplate.podTemplate = 'college_deliberation.odt'
collegeDelibTemplate.podCondition = 'python:(here.meta_type=="MeetingItem") and ' \
                                    'here.queryState() in ["accepted", "refused", "delayed", "accepted_but_modified",]'
collegeRapportTemplate = PodTemplateDescriptor('college-rapport', 'Rapport')
collegeRapportTemplate.podTemplate = 'college_rapport.odt'
collegeRapportTemplate.podCondition = ' python: here.meta_type == "MeetingItem" and ' \
                                      'not (here.portal_membership.getAuthenticatedMember().has_role("MeetingManager"))'
collegeOJADiscTemplate = PodTemplateDescriptor('college-oj-a-discuter', 'OJ (à discuter)')
collegeOJADiscTemplate.podTemplate = 'college_oj_a_discuter.odt'
collegeOJADiscTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                      'here.portal_plonemeeting.isManager()'
collegeOJPasADiscTemplate = PodTemplateDescriptor('college-oj-pas-a-discuter', 'OJ (pas à discuter)')
collegeOJPasADiscTemplate.podTemplate = 'college_oj_pas_a_discuter.odt'
collegeOJPasADiscTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                         'here.portal_plonemeeting.isManager()'
collegePVTemplate = PodTemplateDescriptor('college-pv', 'PV')
collegePVTemplate.podTemplate = 'college_pv.odt'
collegePVTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager()'
councilDelibTemplate = PodTemplateDescriptor('conseil-deliberation', 'Délibération')
councilDelibTemplate.podTemplate = 'conseil_deliberation.odt'
councilDelibTemplate.podCondition = 'python:(here.meta_type=="MeetingItem") and ' \
                                    'here.queryState() in ["accepted", "refused", "delayed", "accepted_but_modified",]'
councilProjetDelibTemplate = PodTemplateDescriptor('conseil-projet-deliberation', 'Projet délibération')
councilProjetDelibTemplate.podTemplate = 'conseil_projet_deliberation.odt'
councilProjetDelibTemplate.podCondition = 'python:(here.meta_type=="MeetingItem")'

councilNoteExplTemplate = PodTemplateDescriptor('conseil-note-explicative', 'Note explicative')
councilNoteExplTemplate.podTemplate = 'conseil_note_explicative.odt'
councilNoteExplTemplate.podCondition = 'python:(here.meta_type=="MeetingItem")'

# Meeting
councilOJExplanatoryTemplate = PodTemplateDescriptor('conseil-oj-notes-explicatives', 'OJ (notes explicatives)')
councilOJExplanatoryTemplate.podTemplate = 'conseil_oj_notes_explicatives.odt'
councilOJExplanatoryTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                            'here.portal_plonemeeting.isManager()'
councilFardesTemplate = PodTemplateDescriptor('conseil-fardes', 'Fardes')
councilFardesTemplate.podTemplate = 'conseil_fardes.odt'
councilFardesTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                     'here.portal_plonemeeting.isManager()'
councilAvisTemplate = PodTemplateDescriptor('conseil-avis', 'Avis')
councilAvisTemplate.podTemplate = 'conseil_avis_affiche_aux_valves.odt'
councilAvisTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                   'here.portal_plonemeeting.isManager()'
councilOJConvPresseTemplate = PodTemplateDescriptor('conseil-convocation-presse', 'Convocation presse')
councilOJConvPresseTemplate.podTemplate = 'conseil_convocation_presse.odt'
councilOJConvPresseTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                           'here.portal_plonemeeting.isManager()'
councilOJConvConsTemplate = PodTemplateDescriptor('conseil-convocation-conseillers', 'Convocation conseillers')
councilOJConvConsTemplate.podTemplate = 'conseil_convocation_conseillers.odt'
councilOJConvConsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                         'here.portal_plonemeeting.isManager()'
councilOJConvConsPremSupplTemplate = PodTemplateDescriptor('conseil-convocation-conseillers-1er-supplement',
                                                           'Convocation conseillers (1er supplément)')
councilOJConvConsPremSupplTemplate.podTemplate = 'conseil_convocation_conseillers_1er_supplement.odt'
councilOJConvConsPremSupplTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                                  'here.portal_plonemeeting.isManager()'
councilOJConvConsDeuxSupplTemplate = PodTemplateDescriptor('conseil-convocation-conseillers-2eme-supplement',
                                                           'Convocation conseillers (2ème supplément)')
councilOJConvConsDeuxSupplTemplate.podTemplate = 'conseil_convocation_conseillers_2eme_supplement.odt'
councilOJConvConsDeuxSupplTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                                  'here.portal_plonemeeting.isManager()'
councilOJConvConsTroisSupplTemplate = PodTemplateDescriptor('conseil-convocation-conseillers-3eme-supplement',
                                                            'Convocation conseillers (3ème supplément)')
councilOJConvConsTroisSupplTemplate.podTemplate = 'conseil_convocation_conseillers_3eme_supplement.odt'
councilOJConvConsTroisSupplTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                                   'here.portal_plonemeeting.isManager()'
councilOJConvCommTravTemplate = PodTemplateDescriptor('conseil-oj-commission-travaux', 'Comm. Trav.')
councilOJConvCommTravTemplate.podTemplate = 'conseil_oj_commission_travaux.odt'
councilOJConvCommTravTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                             'here.portal_plonemeeting.isManager()'
councilOJConvCommEnsTemplate = PodTemplateDescriptor('conseil-oj-commission-enseignement', 'Comm. Ens.')
councilOJConvCommEnsTemplate.podTemplate = 'conseil_oj_commission_enseignement.odt'
councilOJConvCommEnsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                            'here.portal_plonemeeting.isManager()'
councilOJConvCommLogTemplate = PodTemplateDescriptor('conseil-oj-commission-logement', 'Comm. Log.')
councilOJConvCommLogTemplate.podTemplate = 'conseil_oj_commission_logement.odt'
councilOJConvCommLogTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                            'here.portal_plonemeeting.isManager()'
councilOJConvCommAGTemplate = PodTemplateDescriptor('conseil-oj-commission-ag', 'Comm. AG.')
councilOJConvCommAGTemplate.podTemplate = 'conseil_oj_commission_ag.odt'
councilOJConvCommAGTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                           'here.portal_plonemeeting.isManager()'
councilOJConvCommAGSupplTemplate = PodTemplateDescriptor('conseil-oj-commission-ag-suppl', 'Comm. AG. (Suppl.)')
councilOJConvCommAGSupplTemplate.podTemplate = 'conseil_oj_commission_ag_supplement.odt'
councilOJConvCommAGSupplTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                                'here.portal_plonemeeting.isManager()'
councilOJConvCommFinTemplate = PodTemplateDescriptor('conseil-oj-commission-finances', 'Comm. Fin.')
councilOJConvCommFinTemplate.podTemplate = 'conseil_oj_commission_finances.odt'
councilOJConvCommFinTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                            'here.portal_plonemeeting.isManager()'
councilOJConvCommPolTemplate = PodTemplateDescriptor('conseil-oj-commission-police', 'Comm. Pol.')
councilOJConvCommPolTemplate.podTemplate = 'conseil_oj_commission_police.odt'
councilOJConvCommPolTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                            'here.portal_plonemeeting.isManager()'
councilOJConvCommSpecTemplate = PodTemplateDescriptor('conseil-oj-commission-speciale', 'Comm. Spec.')
councilOJConvCommSpecTemplate.podTemplate = 'conseil_oj_commission_speciale.odt'
councilOJConvCommSpecTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                             'here.portal_plonemeeting.isManager()'
councilPVConvCommTravTemplate = PodTemplateDescriptor('conseil-pv-commission-travaux', 'PV Comm. Trav.')
councilPVConvCommTravTemplate.podTemplate = 'conseil_pv_commission_travaux.odt'
councilPVConvCommTravTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                             'here.portal_plonemeeting.isManager()'
councilPVConvCommEnsTemplate = PodTemplateDescriptor('conseil-pv-commission-enseignement', 'PV Comm. Ens.')
councilPVConvCommEnsTemplate.podTemplate = 'conseil_pv_commission_enseignement.odt'
councilPVConvCommEnsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                            'here.portal_plonemeeting.isManager()'
councilPVConvCommLogTemplate = PodTemplateDescriptor('conseil-pv-commission-logement', 'PV Comm. Log.')
councilPVConvCommLogTemplate.podTemplate = 'conseil_pv_commission_logement.odt'
councilPVConvCommLogTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                            'here.portal_plonemeeting.isManager()'
councilPVConvCommAgTemplate = PodTemplateDescriptor('conseil-pv-commission-ag', 'PV Comm. AG.')
councilPVConvCommAgTemplate.podTemplate = 'conseil_pv_commission_ag.odt'
councilPVConvCommAgTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                           'here.portal_plonemeeting.isManager()'
councilPVConvCommFinTemplate = PodTemplateDescriptor('conseil-pv-commission-fin', 'PV Comm. Fin.')
councilPVConvCommFinTemplate.podTemplate = 'conseil_pv_commission_finances.odt'
councilPVConvCommFinTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                            'here.portal_plonemeeting.isManager()'
councilPVConvCommPolTemplate = PodTemplateDescriptor('conseil-pv-commission-police', 'PV Comm. Pol.')
councilPVConvCommPolTemplate.podTemplate = 'conseil_pv_commission_police.odt'
councilPVConvCommPolTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                            'here.portal_plonemeeting.isManager()'
councilPVConvCommSpecTemplate = PodTemplateDescriptor('conseil-pv-commission-speciale', 'PV Comm. Spec.')
councilPVConvCommSpecTemplate.podTemplate = 'conseil_pv_commission_speciale.odt'
councilPVConvCommSpecTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                             'here.portal_plonemeeting.isManager()'
councilPVTemplate = PodTemplateDescriptor('conseil-pv', 'PV')
councilPVTemplate.podTemplate = 'conseil_pv.odt'
councilPVTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager()'

collegeTemplates = [collegeDelibTemplate, collegeRapportTemplate, collegeOJADiscTemplate,
                    collegeOJPasADiscTemplate, collegePVTemplate]
councilTemplates = [councilOJExplanatoryTemplate, councilFardesTemplate,
                    councilAvisTemplate, councilOJConvPresseTemplate,
                    councilOJConvConsTemplate, councilOJConvConsPremSupplTemplate,
                    councilOJConvConsDeuxSupplTemplate, councilOJConvConsTroisSupplTemplate,
                    councilOJConvCommTravTemplate,
                    councilOJConvCommEnsTemplate, councilOJConvCommLogTemplate,
                    councilOJConvCommAGTemplate, councilOJConvCommFinTemplate,
                    councilOJConvCommPolTemplate, councilOJConvCommSpecTemplate,
                    councilPVConvCommTravTemplate, councilPVConvCommEnsTemplate,
                    councilPVConvCommLogTemplate, councilPVConvCommAgTemplate,
                    councilPVConvCommFinTemplate, councilPVConvCommPolTemplate,
                    councilPVConvCommSpecTemplate, councilPVTemplate,
                    councilNoteExplTemplate, councilProjetDelibTemplate, councilDelibTemplate]


# Users and groups -------------------------------------------------------------
dgen = UserDescriptor('dgen', ['MeetingManager'], email="test@test.be", fullname="Henry Directeur")
dfin = UserDescriptor('dfin', [], email="test@test.be", fullname="Directeur Financier")
secretaire = UserDescriptor('secretaire', ['MeetingManager'], email="test@test.be")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be")
agentPers = UserDescriptor('agentPers', [], email="test@test.be")
agentTrav = UserDescriptor('agentTrav', [], email="test@test.be")
chefPers = UserDescriptor('chefPers', [], email="test@test.be")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be")
chefBureauCompta = UserDescriptor('chefBureauCompta', [], email="test@test.be")
echevinPers = UserDescriptor('echevinPers', [], email="test@test.be")
emetteuravisPers = UserDescriptor('emetteuravisPers', [], email="test@test.be")

groups = [GroupDescriptor('dirgen', 'Directeur Général', 'DG'),
          GroupDescriptor('secretariat', 'Secretariat communal', 'Secr',
                          asCopyGroupOn="python: item.getProposingGroup()=='informatique' and ['reviewers',] or []"),
          GroupDescriptor('informatique', 'Service informatique', 'Info'),
          GroupDescriptor('personnel', 'Service du personnel', 'Pers'),
          GroupDescriptor('dirfin', 'Directeur Financier', 'DF'),
          GroupDescriptor('comptabilite', 'Service comptabilité', 'Compt'),
          GroupDescriptor('travaux', 'Service travaux', 'Trav'),
          GroupDescriptor('conseillers', 'Conseillers', 'Conseillers'),
          GroupDescriptor('secretaire-communal', 'Secrétaire communal', 'SecrComm'),
          GroupDescriptor('secretaire-communal-adj', 'Secrétaire communal ADJ', 'SecrCommAdj')]

# MeetingManager
groups[0].creators.append(secretaire)
groups[0].officemanagers.append(secretaire)
groups[0].observers.append(secretaire)
groups[0].advisers.append(secretaire)
groups[0].creators.append(dgen)
groups[0].officemanagers.append(dgen)
groups[0].observers.append(dgen)
groups[0].advisers.append(dgen)

groups[1].creators.append(agentInfo)
groups[1].creators.append(secretaire)
groups[1].creators.append(dgen)
groups[1].officemanagers.append(agentInfo)
groups[1].officemanagers.append(secretaire)
groups[1].officemanagers.append(dgen)
groups[1].observers.append(agentInfo)
groups[1].advisers.append(agentInfo)

groups[2].creators.append(agentPers)
groups[2].observers.append(agentPers)
groups[2].creators.append(secretaire)
groups[2].officemanagers.append(secretaire)
groups[2].creators.append(dgen)
groups[2].officemanagers.append(dgen)
groups[2].creators.append(chefPers)
groups[2].officemanagers.append(chefPers)
groups[2].observers.append(chefPers)
groups[2].observers.append(echevinPers)
groups[2].advisers.append(emetteuravisPers)

groups[3].creators.append(agentCompta)
groups[3].creators.append(chefCompta)
groups[3].creators.append(chefBureauCompta)
groups[3].creators.append(secretaire)
groups[3].creators.append(dgen)
groups[3].serviceheads.append(chefCompta)
groups[3].officemanagers.append(chefBureauCompta)
groups[3].officemanagers.append(secretaire)
groups[3].officemanagers.append(dgen)
groups[3].observers.append(agentCompta)
groups[3].advisers.append(chefCompta)
groups[3].advisers.append(chefBureauCompta)

groups[4].creators.append(agentTrav)
groups[4].creators.append(secretaire)
groups[4].creators.append(dgen)
groups[4].reviewers.append(agentTrav)
groups[4].reviewers.append(secretaire)
groups[4].reviewers.append(dgen)
groups[4].observers.append(agentTrav)
groups[4].advisers.append(agentTrav)

# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-college', 'Collège Communal',
    'Collège communal', isDefault=True)
collegeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
collegeMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
collegeMeeting.categories = []
collegeMeeting.shortName = 'College'
collegeMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier,
                                   annexeDecision, annexeAvis, annexeAvisLegal]
collegeMeeting.usedItemAttributes = ['budgetInfos', 'observations', 'toDiscuss',
                                     'motivation', ]
collegeMeeting.xhtmlTransformFields = ('MeetingItem.description', 'MeetingItem.detailedDescription',
                                       'MeetingItem.decision', 'MeetingItem.observations',
                                       'MeetingItem.interventions', 'MeetingItem.commissionTranscript')
collegeMeeting.xhtmlTransformTypes = ('removeBlanks',)
collegeMeeting.itemWorkflow = 'meetingitemcollegeseraing_workflow'
collegeMeeting.meetingWorkflow = 'meetingcollegeseraing_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemCollegeSeraingWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemCollegeSeraingWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingCollegeSeraingWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingCollegeSeraingWorkflowActions'
collegeMeeting.itemTopicStates = ('itemcreated', 'proposedToServiceHead', 'proposedToOfficeManager',
                                  'proposedToDivisionHead', 'proposed', 
                                  'validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'delayed',
                                  'pre_accepted', 'removed', 'accepted_but_modified', )
collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.itemBudgetInfosStates = ('proposed_to_budgetimpact_reviewer', )
collegeMeeting.itemAdviceStates = ('validated',)
collegeMeeting.itemAdviceEditStates = ('validated',)
collegeMeeting.recordItemHistoryStates = ['']
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'topic_searchmyitems'
collegeMeeting.itemDocFormats = ('odt', 'pdf')
collegeMeeting.meetingDocFormats = ('odt', 'pdf')
collegeMeeting.useAdvices = True
collegeMeeting.customAdvisers = [
    {'row_id': 'unique_id_001',
     'group': 'comptabilite',
     'gives_auto_advice_on': 'item/getBudgetRelated',
     'for_item_created_from': today, },
    {'row_id': 'unique_id_002',
     'group': 'dirfin',
     'for_item_created_from': today,
     'delay': '5',
     'delay_left_alert': '2',
     'delay_label': 'Incidence financière >= 22.000€', },
    {'row_id': 'unique_id_003',
     'group': 'dirfin',
     'for_item_created_from': today,
     'delay': '10',
     'delay_left_alert': '4',
     'delay_label': 'Incidence financière >= 22.000€', },
    {'row_id': 'unique_id_004',
     'group': 'dirfin',
     'for_item_created_from': today,
     'delay': '20',
     'delay_left_alert': '4',
     'delay_label': 'Incidence financière >= 22.000€', }, ]
collegeMeeting.enforceAdviceMandatoriness = False
collegeMeeting.enableAdviceInvalidation = False
collegeMeeting.useCopies = True
collegeMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                       groups[1].getIdSuffixed('reviewers'),
                                       groups[2].getIdSuffixed('reviewers'),
                                       groups[4].getIdSuffixed('reviewers')]
collegeMeeting.podTemplates = collegeTemplates
collegeMeeting.meetingConfigsToCloneTo = ['meeting-config-council']
collegeMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
collegeMeeting.useGroupsAsCategories = True
collegeMeeting.defaultMeetingItemMotivation = ""
collegeMeeting.recurringItems = []
collegeMeeting.meetingUsers = []

# Conseil communal
# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('recurrent', 'Point récurrent',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-travaux', 'Commission Travaux'),
              CategoryDescriptor('commission-enseignement-culture-sport-sante',
                                 'Commission Enseignement/Culture/Sport/Santé'),
              CategoryDescriptor('commission-cadre-de-vie', 'Commission Cadre de Vie'),
              CategoryDescriptor('commission-ag', 'Commission AG'),
              CategoryDescriptor('commission-finances', 'Commission Finances'),
              CategoryDescriptor('commission-patrimoine', 'Commission Patrimoine'),
              CategoryDescriptor('commission-police', 'Commission Police'),
              CategoryDescriptor('commission-speciale', 'Commission Spéciale',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),

              CategoryDescriptor('commission-travaux-1er-supplement', 'Commission Travaux (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-enseignement-culture-sport-sante-1er-supplement',
                                 'Commission Enseignement/Culture/Sport/Santé (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-cadre-de-vie-1er-supplement', 'Commission Cadre de Vie (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-ag-1er-supplement', 'Commission AG (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-finances-1er-supplement', 'Commission Finances (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-patrimoine-1er-supplement', 'Commission Patrimoine (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-police-1er-supplement', 'Commission Police (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('commission-speciale-1er-supplement', 'Commission Spéciale (1er supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),

              CategoryDescriptor('points-conseillers-2eme-supplement', 'Points conseillers (2ème supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen')),
              CategoryDescriptor('points-conseillers-3eme-supplement', 'Points conseillers (3ème supplément)',
                                 usingGroups=('secretaire-communal', 'secretaire-communal-adj',
                                              'secretariat', 'dirgen'))]

councilMeeting = MeetingConfigDescriptor(
    'meeting-config-council', 'Conseil Communal',
    'Conseil Communal')
councilMeeting.assembly = """Assemblée du Conseil"""
councilMeeting.categories = categories
councilMeeting.shortName = 'Council'
councilMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeRemarks,
                                   annexeDecision, annexeAvis, annexeAvisLegal]
councilMeeting.xhtmlTransformFields = ('MeetingItem.description', 'MeetingItem.detailedDescription',
                                       'MeetingItem.decision', 'MeetingItem.observations',
                                       'MeetingItem.interventions', 'MeetingItem.commissionTranscript')
councilMeeting.xhtmlTransformTypes = ('removeBlanks',)
councilMeeting.usedItemAttributes = ['oralQuestion', 'itemInitiator', 'observations',
                                     'privacy', 'itemAssembly', 'motivation']
councilMeeting.usedMeetingAttributes = ('place', 'observations', 'signatures', 'assembly', 'preMeetingDate',
                                        'preMeetingPlace', 'preMeetingAssembly', 'preMeetingDate_2',
                                        'preMeetingPlace_2', 'preMeetingAssembly_2', 'preMeetingDate_3',
                                        'preMeetingPlace_3', 'preMeetingAssembly_3', 'preMeetingDate_4',
                                        'preMeetingPlace_4', 'preMeetingAssembly_4', 'preMeetingDate_5',
                                        'preMeetingPlace_5', 'preMeetingAssembly_5', 'preMeetingDate_6',
                                        'preMeetingPlace_6', 'preMeetingAssembly_6', 'preMeetingDate_7',
                                        'preMeetingPlace_7', 'preMeetingAssembly_7', 'startDate', 'endDate', )
councilMeeting.recordMeetingHistoryStates = []
councilMeeting.workflowAdaptations = ['return_to_proposing_group', ]
councilMeeting.itemWorkflow = 'meetingitemcouncilseraing_workflow'
councilMeeting.meetingWorkflow = 'meetingcouncilseraing_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemCouncilSeraingWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingItemCouncilSeraingWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingCouncilSeraingWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingSeraing.interfaces.IMeetingCouncilSeraingWorkflowActions'
#show every items states
councilMeeting.itemTopicStates = ('itemcreated',
                                  'proposed_to_officemanager',
                                  'validated',
                                  'presented',
                                  'itemfrozen',
                                  'item_in_committee',
                                  'item_in_council',
                                  'returned_to_service',
                                  'accepted',
                                  'accepted_but_modified',
                                  'refused',
                                  'delayed')
councilMeeting.meetingTopicStates = ('created',
                                     'frozen',
                                     'in_committee')
councilMeeting.decisionTopicStates = ('in_council',
                                      'closed')
councilMeeting.itemAdviceStates = ('itemcreated',)
councilMeeting.itemAdviceEditStates = ('itemcreated',)
councilMeeting.recordItemHistoryStates = ['']
councilMeeting.maxShownMeetings = 5
councilMeeting.maxDaysDecisions = 60
councilMeeting.meetingAppDefaultView = 'topic_searchmyitems'
councilMeeting.itemDocFormats = ('odt', 'pdf')
councilMeeting.meetingDocFormats = ('odt', 'pdf')
councilMeeting.useAdvices = True
councilMeeting.enforceAdviceMandatoriness = False
councilMeeting.enableAdviceInvalidation = False
councilMeeting.useCopies = True
councilMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                       groups[1].getIdSuffixed('reviewers'),
                                       groups[2].getIdSuffixed('reviewers'),
                                       groups[4].getIdSuffixed('reviewers')]
councilMeeting.podTemplates = councilTemplates
councilMeeting.transitionsToConfirm = ['MeetingItem.return_to_service']
councilMeeting.sortingMethodOnAddItem = 'on_privacy_then_categories'
councilMeeting.useGroupsAsCategories = False
councilMeeting.defaultMeetingItemMotivation = ""
councilMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurrent-approuve-pv',
        title='Approbation du procès-verbal du Conseil communal du ...',
        description='',
        category='recurrent',
        proposingGroup='secretariat',
        decision='',
        meetingTransitionInsertingMe='setInCouncil'),
    RecurringItemDescriptor(
        id='recurrent-questions-actualite',
        title='Questions d\'actualités',
        description='',
        category='recurrent',
        proposingGroup='secretariat',
        decision='',
        meetingTransitionInsertingMe='setInCouncil'),
]
councilMeeting.meetingUsers = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(collegeMeeting, councilMeeting),
                                 groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
# ------------------------------------------------------------------------------
