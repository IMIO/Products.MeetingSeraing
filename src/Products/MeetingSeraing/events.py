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
from Products.PloneMeeting.utils import get_annexes
from Products.PloneMeeting.utils import forceHTMLContentTypeForEmptyRichFields


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
            newItem.queryState() not in ['delayed', ] and \
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
