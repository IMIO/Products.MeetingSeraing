# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2015 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre NUYENS <andre.nuyens@imio.be>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('MeetingSeraing: setuphandlers')
from Products.MeetingSeraing.config import PROJECTNAME
from Products.MeetingSeraing.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.config import TOPIC_TYPE, TOPIC_SEARCH_SCRIPT, TOPIC_TAL_EXPRESSION
from Products.MeetingSeraing.config import COUNCIL_COMMISSION_IDS, \
    COUNCIL_COMMISSION_IDS_2013, COMMISSION_EDITORS_SUFFIX
##/code-section HEAD

def isNotMeetingSeraingProfile(context):
    return context.readDataFile("MeetingSeraing_marker.txt") is None



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotMeetingSeraingProfile(context): return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotMeetingSeraingProfile(context):
        return
    site = context.getSite()
    # Reinstall PloneMeeting
    reinstallPloneMeeting(context, site)
    # Add groups for council commissions that will contain MeetingCommissionEditors
    addCommissionEditorGroups(context, site)
    # Make sure the 'home' tab is shown
    showHomeTab(context, site)
    # Reinstall the skin
    reinstallPloneMeetingSkin(context, site)
    # reorder skins so we are sure that the meetingSeraing_xxx skins are just under custom
    reorderSkinsLayers(context, site)



##code-section FOOT
def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" % (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isNotMeetingSeraingSeraingProfile(context):
    return context.readDataFile("MeetingSeraing_seraing_marker.txt") is None


def installMeetingSeraing(context):
    """ Run the default profile before bing able to run the Seraing profile"""
    if isNotMeetingSeraingSeraingProfile(context):
        return

    logStep("installMeetingSeraing", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingSeraing:default')


def reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    if isNotMeetingSeraingProfile(context):
        return

    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context)
    # launch skins step for MeetingSeraing so MeetingSeraing skin layers are before PM ones
    site.portal_setup.runImportStepFromProfile('profile-Products.MeetingSeraing:default', 'skins')


def _installPloneMeeting(context):
    site = context.getSite()
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)

def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current
       profile.'''
    if isNotMeetingSeraingSeraingProfile(context):
        return

    logStep("initializeTool", context)
    _installPloneMeeting(context)
    return ToolInitializer(context, PROJECTNAME).run()


def addCommissionEditorGroups(context, portal):
    '''
       Add groups for council commissions that will contain MeetingCommissionEditors
    '''
    if isNotMeetingSeraingProfile(context):
        return

    logStep("addCommissionEditorGroups", context)
    existingPloneGroupIds = portal.portal_groups.getGroupIds()
    for commissionId in COUNCIL_COMMISSION_IDS+COUNCIL_COMMISSION_IDS_2013:
        groupId = commissionId + COMMISSION_EDITORS_SUFFIX
        if not groupId in existingPloneGroupIds:
            #add the Plone group
            groupTitle = groupId.replace('-', ' ').capitalize() + u' (RÃ©dacteurs PV)'.encode('utf-8')
            portal.portal_groups.addGroup(groupId, title=groupTitle)


def showHomeTab(context, site):
    """
       Make sure the 'home' tab is shown...
    """
    if isNotMeetingSeraingProfile(context):
        return

    logStep("showHomeTab", context)

    index_html = getattr(site.portal_actions.portal_tabs, 'index_html', None)
    if index_html:
        index_html.visible = True
    else:
        logger.info("The 'Home' tab does not exist !!!")


def reinstallPloneMeetingSkin(context, site):
    """
       Reinstall Products.plonemeetingskin as the reinstallation of MeetingCommunes
       change the portal_skins layers order
    """
    if isNotMeetingSeraingProfile(context):
        return

    logStep("reinstallPloneMeetingSkin", context)
    try:
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:default')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin')
    except KeyError:
        # if the Products.plonemeetingskin profile is not available
        # (not using plonemeetingskin or in testing?) we pass...
        pass


def reorderSkinsLayers(context, site):
    """
       Reinstall Products.plonemeetingskin and re-apply MeetingSeraing skins.xml step
       as the reinstallation of MeetingSeraing and PloneMeeting changes the portal_skins layers order
    """
    if isNotMeetingSeraingProfile(context) and isNotMeetingSeraingSeraingProfile(context):
        return

    logStep("reorderSkinsLayers", context)
    try:
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:default')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin')
        site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingSeraing:default', 'skins')
    except KeyError:
        # if the Products.plonemeetingskin profile is not available
        # (not using plonemeetingskin or in testing?) we pass...
        pass


def finalizeInstance(context):
    """
      Called at the very end of the installation process (after PloneMeeting).
    """
    reorderSkinsLayers(context, context.getSite())
    reorderCss(context)


def reorderCss(context):
    """
       Make sure CSS are correctly reordered in portal_css so things
       work as expected...
    """
    if isNotMeetingSeraingProfile(context) and isNotMeetingSeraingSeraingProfile(context):
        return

    site = context.getSite()

    logStep("reorderCss", context)
    portal_css = site.portal_css
    css = ['plonemeeting.css',
           'meeting.css',
           'meetingitem.css',
           'meetingSeraing.css',
           'imioapps.css',
           'plonemeetingskin.css',
           'imioapps_IEFixes.css',
           'ploneCustom.css']
    for resource in css:
        portal_css.moveResourceToBottom(resource)

##/code-section FOOT
