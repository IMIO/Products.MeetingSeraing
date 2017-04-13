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

from imio.actionspanel.utils import unrestrictedRemoveGivenObject
from Products.PloneMeeting.utils import get_annexes
from Products.PloneMeeting.utils import forceHTMLContentTypeForEmptyRichFields


def onItemLocalRolesUpdated(item, event):
    """Called after localRoles have been updated on the item."""
    item.adapted().updatePowerEditorsLocalRoles()


def onItemDuplicated(original, event):
    """After item's cloning, we removed decision annexe.
    """
    newItem = event.newItem
    # Delete the decision annexes that have been copied.
    for annex in get_annexes(newItem, portal_types=['annexDecision']):
        unrestrictedRemoveGivenObject(annex)
    # clear some fields linked to meeting
    newDescri = _removeTypistNote(newItem.Description())
    newItem.setDescription(newDescri)
    newItem.setPvNote('')
    newItem.setDgNote('')
    newItem.setObservations('')
    # Make sure we have 'text/html' for every Rich fields
    forceHTMLContentTypeForEmptyRichFields(newItem)


def _removeTypistNote(field):
    """ Remove typist's note find with highlight-purple class"""
    import re
    return re.sub('<span class="highlight-purple">.*?</span>', '', field)
