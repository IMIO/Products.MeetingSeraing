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
from Products.PloneMeeting.interfaces import IAnnexable


def onItemAfterTransition(item, event):
    '''Called whenever a transition has been fired on an item.'''
    if not event.transition or (item != event.object):
        return
    item.adapted().updatePowerEditorsLocalRoles()


def onItemDuplicated(original, event):
    '''After item's cloning, we removed decision annexe.
    '''
    newItem = event.newItem
    # Delete the decision annexes that have been copied.
    for annex in IAnnexable(newItem).getAnnexes(relatedTo='item_decision'):
        unrestrictedRemoveGivenObject(annex)
