# -*- coding: utf-8 -*-

from collections import OrderedDict
from Products.PloneMeeting import config as PMconfig


product_globals = globals()

PROJECTNAME = "MeetingSeraing"


# Roles
SERAINGROLES = {}
SERAINGROLES['serviceheads'] = 'MeetingServiceHead'
SERAINGROLES['officemanagers'] = 'MeetingOfficeManager'
SERAINGROLES['divisionheads'] = 'MeetingDivisionHead'
PMconfig.MEETINGROLES.update(SERAINGROLES)


POWEREDITORS_GROUP_SUFFIX = 'powereditors'
EDITOR_USECASES = {'power_editors': 'Editor', }

# group suffixes
PMconfig.EXTRA_GROUP_SUFFIXES = [
    {'fct_title': u'serviceheads', 'fct_id': u'serviceheads', 'fct_orgs': [], 'enabled': True},
    {'fct_title': u'officemanagers', 'fct_id': u'officemanagers', 'fct_orgs': [], 'enabled': True},
    {'fct_title': u'divisionheads', 'fct_id': u'divisionheads',  'fct_orgs': [], 'enabled': True},
]

SERAINGMEETINGREVIEWERS = {
    'meetingitemseraing_workflow': OrderedDict([('reviewers', ['proposed']),
                                     ('divisionheads', ['proposed_to_divisionhead']),
                                     ('officemanagers', ['proposed_to_officemanager']),
                                     ('serviceheads', ['proposed_to_servicehead']), ])}
PMconfig.MEETINGREVIEWERS.update(SERAINGMEETINGREVIEWERS)
