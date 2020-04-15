# -*- coding: utf-8 -*-
#
# File: events.py
#
# Copyright (c) 2013 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre NUYENS <a.nuyens@imio.be>"""
__docformat__ = 'plaintext'

from imio.actionspanel.interfaces import IContentDeletable
from Products.PloneMeeting.events import _advice_update_item
from Products.PloneMeeting.events import storeImagesLocallyDexterity
from Products.PloneMeeting.utils import _addManagedPermissions
from Products.PloneMeeting.utils import AdviceAfterAddEvent
from Products.PloneMeeting.utils import forceHTMLContentTypeForEmptyRichFields
from Products.PloneMeeting.utils import get_annexes
from zope.event import notify


def onItemLocalRolesUpdated(item, event):
    """Called after localRoles have been updated on the item."""
    item.adapted().updatePowerEditorsLocalRoles()


def onItemDuplicated(original, event):
    """After item's cloning, we removed decision annexe.
    """
    newItem = event.newItem
    # make sure we do not keep decision annexes
    decisionAnnexes = get_annexes(newItem, portal_types=['annexDecision', ])
    # if new state of item is "delayed", we keep simply the Annex Decision
    # if item is sent to Council, we keep annexDecision, but it's transfer in simple annex type (do it in config)
    if decisionAnnexes and IContentDeletable(newItem).mayDelete() and \
            original.queryState() not in ['delayed', ] and \
            newItem.portal_plonemeeting.getMeetingConfig(newItem) == \
            original.portal_plonemeeting.getMeetingConfig(original):
        toDelete = [annex.getId() for annex in decisionAnnexes]
        newItem.manage_delObjects(ids=toDelete)
    # clear some fields linked to meeting
    newRawDescri = _removeTypistNote(newItem.getRawDescription())
    newItem.setDescription(newRawDescri)
    # Make sure we have 'text/html' for every Rich fields
    forceHTMLContentTypeForEmptyRichFields(newItem)


def _removeTypistNote(field):
    """ Remove typist's note find with highlight-purple class"""
    import re
    return re.sub('<span class="highlight-purple">.*?</span>', '', field)

def onAdviceAdded(advice, event):
    '''Called when a meetingadvice is added so we can warn parent item.'''
    # if advice is added because we are pasting, pass as we will remove the advices...
    if advice.REQUEST.get('currentlyPastingItems', False):
        return

    # update advice_row_id if it was not already done before
    # for example in a onAdviceTransition event handler that is called
    # before the onAdviceAdded...
    if not advice.advice_row_id:
        advice._updateAdviceRowId()

    item = advice.getParentNode()
    item.updateLocalRoles()

    _addManagedPermissions(advice)

    # make sure external images used in RichText fields are stored locally
    storeImagesLocallyDexterity(advice)

    # notify our own PM event so we are sure that this event is called
    # after the onAviceAdded event
    notify(AdviceAfterAddEvent(advice))

    # redirect to referer after add if it is not the edit form
    http_referer = item.REQUEST['HTTP_REFERER']
    if not http_referer.endswith('/edit') and not http_referer.endswith('/@@edit'):
        advice.REQUEST.RESPONSE.redirect(http_referer + '#adviceAndAnnexes')

    # update item
    _advice_update_item(item)

    # Send mail if relevant
    item.sendMailIfRelevant('adviceEdited', 'MeetingMember', isRole=True)
    item.sendMailIfRelevant('event_add_advice-service_heads', 'MeetingServiceHead', isRole=True)