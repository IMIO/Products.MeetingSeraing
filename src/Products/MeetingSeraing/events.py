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


def onItemTransition(item, event):
    '''Called whenever a transition has been fired on an item.'''
    if not event.transition or (item != event.object):
        return
    item.adapted().updatePowerEditorsLocalRoles()
