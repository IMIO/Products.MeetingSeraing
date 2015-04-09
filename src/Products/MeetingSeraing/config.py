# -*- coding: utf-8 -*-
#
# File: MeetingSeraing.py
#
# Copyright (c) 2015 by Imio.be
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
from Products.PloneMeeting.model import adaptations
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
RETURN_TO_PROPOSING_GROUP_MAPPINGS = {'backTo_item_in_committee_from_returned_to_proposing_group': ['in_committee', ],
                                      'backTo_item_in_council_from_returned_to_proposing_group': ['in_council', ],
                                      }
adaptations.RETURN_TO_PROPOSING_GROUP_MAPPINGS.update(RETURN_TO_PROPOSING_GROUP_MAPPINGS)


# ids of commissions used as categories for MeetingItemCouncil
# before 2013, commission ids were :
COUNCIL_COMMISSION_IDS = ('commission-travaux', 'commission-enseignement',
                          'commission-cadre-de-vie-et-logement', 'commission-ag',
                          'commission-finances-et-patrimoine', 'commission-police',
                          'commission-speciale',)
# until 2013, commission ids are :
# changes are about 'commission-enseignement', 'commission-cadre-de-vie-et-logement' and
# 'commission-finances-et-patrimoine' that are splitted in smaller commissions
COUNCIL_COMMISSION_IDS_2013 = ('commission-ag', 'commission-finances', 'commission-enseignement',
                               'commission-culture', 'commission-sport', 'commission-sante',
                               'commission-police', 'commission-cadre-de-vie', 'commission-patrimoine',
                               'commission-travaux', 'commission-speciale',)
# commissions taken into account on the Meeting
# since 2013, some commissions are made of several categories...
COUNCIL_MEETING_COMMISSION_IDS_2013 = ('commission-travaux',
                                       ('commission-ag', 'commission-finances', 'commission-enseignement',
                                        'commission-culture', 'commission-sport', 'commission-sante',),
                                       ('commission-cadre-de-vie', 'commission-patrimoine',),
                                       'commission-police',
                                       'commission-speciale',)


# suffix of specific groups containing commission transcript editors
COMMISSION_EDITORS_SUFFIX = '_commissioneditors'
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.MeetingSeraing.AppConfig import *
except ImportError:
    pass
