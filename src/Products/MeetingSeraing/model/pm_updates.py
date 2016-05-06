# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
# File: adapters.py
#
# Copyright (c) 2013 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# ------------------------------------------------------------------------------
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import TextField
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import MultiSelectionWidget
from Products.DataGridField import DataGridField
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingGroup import MeetingGroup
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.config import WriteRiskyConfig


def update_config_schema(baseSchema):
    specificSchema = Schema((
        BooleanField(
            name='initItemDecisionIfEmptyOnDecide',
            default=True,
            widget=BooleanField._properties['widget'](
                description="InitItemDecisionIfEmptyOnDecide",
                description_msgid="init_item_decision_if_empty_on_decide",
                label='Inititemdecisionifemptyondecide',
                label_msgid='MeetingCommunes_label_initItemDecisionIfEmptyOnDecide',
                i18n_domain='PloneMeeting'),
            write_permission=WriteRiskyConfig,
        ),

        # field used to define list of services for synthesis document for DF (legality advice)
        LinesField(
            name='cdldProposingGroup',
            widget=MultiSelectionWidget(
                size=10,
                label='CdldProposingGroup',
                label_msgid='MeetingCommunes_label_cdldProposingGroup',
                description='Choose proposing group for cdld advice',
                description_msgid='MeetingCommunes_descr_cdldProposingGroup',
                i18n_domain='PloneMeeting',
            ),
            enforceVocabulary=True,
            multiValued=1,
            vocabulary='listCdldProposingGroup',
            write_permission=WriteRiskyConfig,
        ),
    ),)

    completeConfigSchema = baseSchema + specificSchema.copy()
    return completeConfigSchema
MeetingConfig.schema = update_config_schema(MeetingConfig.schema)


def update_group_schema(baseSchema):
    specificSchema = Schema((

        # field used to define list of services for echevin for a MeetingGroup
        LinesField(
            name='echevinServices',
            widget=MultiSelectionWidget(
                size=10,
                label='EchevinServices',
                label_msgid='MeetingCommunes_label_echevinServices',
                description='Leave empty if he is not an echevin',
                description_msgid='MeetingCommunes_descr_echevinServices',
                i18n_domain='PloneMeeting',
            ),
            enforceVocabulary=True,
            multiValued=1,
            vocabulary='listEchevinServices',
        ),
    ),)

    completeSchema = baseSchema + specificSchema.copy()
    return completeSchema
MeetingGroup.schema = update_group_schema(MeetingGroup.schema)


def update_item_schema(baseSchema):

    specificSchema = Schema((
        #specific field for council added for MeetingManagers to transcribe interventions
        TextField(
            name='interventions',
            widget=RichWidget(
                rows=15,
                condition="python: here.portal_type == 'MeetingItemCouncil' \
                and (here.portal_plonemeeting.isManager(here) or here.portal_plonemeeting.userIsAmong('powerobservers')\
                or here.portal_plonemeeting.userIsAmong('restrictedpowerobservers'))",
                label='Interventions',
                label_msgid='MeetingSeraing_label_interventions',
                description='Transcription of interventions',
                description_msgid='MeetingSeraing_descr_interventions',
                i18n_domain='PloneMeeting',
            ),
            default_content_type="text/html",
            searchable=True,
            allowable_content_types=('text/html',),
            default_output_type="text/html",
        ),
        #specific field for mark if this item must be printing in meeting
        BooleanField(
            name='isToPrintInMeeting',
            default=False,
            widget=BooleanField._properties['widget'](
                description="IsToPrintInMeeting",
                description_msgid="item_print_in_meeting_descr",
                label='IsToPrintInMeeting',
                label_msgid='PloneMeeting_label_item_print_in_meeting',
                i18n_domain='PloneMeeting',
            ),
        ),
        #specific field for mark pv note
        TextField(
            name='pvNote',
            widget=RichWidget(
                rows=15,
                label='PvNote',
                label_msgid='MeetingSeraing_label_pvNote',
                description='PV Note',
                description_msgid='MeetingSeraing_descr_pvNote',
                i18n_domain='PloneMeeting',
            ),
            default_content_type="text/html",
            default="",
            searchable=True,
            allowable_content_types=('text/html',),
            default_output_type="text/html",
            write_permission="PloneMeeting: Write item observations",
            read_permission="PloneMeeting: Read item observations",
        ),
        #specific field for mark dg note
        TextField(
            name='dgNote',
            widget=RichWidget(
                rows=15,
                condition="python: here.portal_plonemeeting.isManager(here)",
                label='dgnote',
                label_msgid='MeetingSeraing_label_dgnote',
                description='DG Note',
                description_msgid='MeetingSeraing_descr_dgnote',
                i18n_domain='PloneMeeting',
            ),
            default_content_type="text/html",
            default="",
            searchable=True,
            allowable_content_types=('text/html',),
            default_output_type="text/html",
        ),
    ),)

    baseSchema['motivation'].widget.description_msgid = "MeetingSeraing_descr_motivation"

    completeItemSchema = baseSchema + specificSchema.copy()
    return completeItemSchema
MeetingItem.schema = update_item_schema(MeetingItem.schema)


def update_meeting_schema(baseSchema):
    specificSchema = Schema((

        DataGridField(
            name='sections',
            widget=DataGridField._properties['widget'](
                description="Sections",
                description_msgid="sections_descr",
                condition="python: here.portal_type == 'MeetingCouncil'",
                columns={'name_section': SelectColumn("Sections name", vocabulary="listSections",
                                                      col_description="Select the section name."),
                         'date_section': Column("Section date",
                                                col_description="Enter valid from date, "
                                                                "use following format : DD/MM/YYYY."), },
                label='Sections',
                label_msgid='MeetingSeraing_label_sections',
                i18n_domain='PloneMeeting',
            ),
            allow_oddeven=True,
            write_permission="Modify portal content",
            columns=('name_section', 'date_section'),
            allow_empty_rows=False,
        ),
    ),)

    completeSchema = baseSchema + specificSchema.copy()
    return completeSchema
Meeting.schema = update_meeting_schema(Meeting.schema)


# Classes have already been registered, but we register them again here
# because we have potentially applied some schema adaptations (see above).
# Class registering includes generation of accessors and mutators, for
# example, so this is why we need to do it again now.
from Products.PloneMeeting.config import registerClasses
registerClasses()
