# -*- coding: utf-8 -*-
#
# File: MeetingSeraing.py
#
# Copyright (c) 2016 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre NUYENS <andre.nuyens@imio.be>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
##code-section config-head #fill in your manual code here
from collections import OrderedDict
##/code-section config-head


PROJECTNAME = "MeetingSeraing"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
from Products.PloneMeeting import config as PMconfig
SERAINGROLES = {}
SERAINGROLES['serviceheads'] = 'MeetingServiceHead'
SERAINGROLES['officemanagers'] = 'MeetingOfficeManager'
SERAINGROLES['divisionheads'] = 'MeetingDivisionHead'
PMconfig.MEETINGROLES.update(SERAINGROLES)
PMconfig.MEETING_GROUP_SUFFIXES = PMconfig.MEETINGROLES.keys()

POWEREDITORS_GROUP_SUFFIX = 'powereditors'

EDITOR_USECASES = {
    'power_editors': 'Editor',
}

# see doc in Products.PloneMeeting.config.py

SERAINGMEETINGREVIEWERS = OrderedDict([('reviewers', 'proposed'),
                                     ('divisionheads', 'proposed_to_divisionhead'),
                                     ('officemanagers', 'proposed_to_officemanager'),
                                     ('serviceheads', 'proposed_to_servicehead'), ])
PMconfig.MEETINGREVIEWERS = SERAINGMEETINGREVIEWERS

# Load custom configuration not managed by archgenxml
try:
    from Products.MeetingSeraing.AppConfig import *
except ImportError:
    pass
