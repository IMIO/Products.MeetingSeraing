# -*- coding: utf-8 -*-

import logging

from imio.helpers.xhtml import _turnToLxmlTree

import lxml

logger = logging.getLogger('MeetingSeraing')

from plone import api

from Products.PloneMeeting.migrations.migrate_to_4_0 import Migrate_To_4_0 as PMMigrate_To_4_0


# The migration class ----------------------------------------------------------
class Migrate_To_4_0(PMMigrate_To_4_0):

    wfs_to_delete = []

    def _cleanCDLD(self):
        """We removed things related to 'CDLD' finance advice, so:
           - remove the 'cdld-document-generate' from document_actions;
           - remove the MeetingConfig.CdldProposingGroup attribute.
        """
        logger.info('Removing CDLD related things...')
        doc_actions = self.portal.portal_actions.document_actions
        # remove the action from document_actions
        if 'cdld-document-generate' in doc_actions:
            doc_actions.manage_delObjects(ids=['cdld-document-generate', ])
        # clean the MeetingConfigs
        for cfg in self.tool.objectValues('MeetingConfig'):
            if hasattr(cfg, 'cdldProposingGroup'):
                delattr(cfg, 'cdldProposingGroup')
        logger.info('Done.')

    def _migrateItemPositiveDecidedStates(self):
        """Before, the states in which an item was auto sent to
           selected other meetingConfig was defined in a method
           'itemPositiveDecidedStates' now it is stored in MeetingConfig.itemAutoSentToOtherMCStates.
           We store these states in the MeetingConfig.itemPositiveDecidedStates, it is used
           to display the 'sent from' leading icon on items sent from another MeetingConfig."""
        logger.info('Defining values for MeetingConfig.itemAutoSentToOtherMCStates...')
        for cfg in self.tool.objectValues('MeetingConfig'):
            cfg.setItemAutoSentToOtherMCStates(('accepted', 'accepted_but_modified', ))
            cfg.setItemPositiveDecidedStates(('accepted', 'accepted_but_modified', ))
        logger.info('Done.')

    def _after_reinstall(self):
        """Use that hook that is called just after the profile has been reinstalled by
           PloneMeeting, this way, we may launch some steps before PloneMeeting ones.
           Here we will update used workflows before letting PM do his job."""
        logger.info('Replacing old no more existing workflows...')
        PMMigrate_To_4_0._after_reinstall(self)
        for cfg in self.tool.objectValues('MeetingConfig'):
            # MeetingItem workflow
            if cfg.getItemWorkflow() == 'meetingitemseraingcollege_workflow':
                cfg.setItemWorkflow('meetingitemseraing_workflow')
                cfg._v_oldItemWorkflow = 'meetingitemseraingcollege_workflow'
                wfAdaptations = list(cfg.getWorkflowAdaptations())
                cfg.setWorkflowAdaptations(wfAdaptations)
            if cfg.getItemWorkflow() == 'meetingitemseraingcouncil_workflow':
                cfg.setItemWorkflow('meetingitemseraing_workflow')
                cfg._v_oldItemWorkflow = 'meetingitemseraingcouncil_workflow'
            # Meeting workflow
            if cfg.getMeetingWorkflow() == 'meetingseraingcollege_workflow':
                cfg.setMeetingWorkflow('meetingseraing_workflow')
                cfg._v_oldMeetingWorkflow = 'meetingseraingcollege_workflow'
            if cfg.getMeetingWorkflow() == 'meetingseraingcouncil_workflow':
                cfg.setMeetingWorkflow('meetingseraing_workflow')
                cfg._v_oldMeetingWorkflow = 'meetingseraingcouncil_workflow'
        # delete old unused workflows, aka every workflows containing 'college' or 'council'
        wfTool = api.portal.get_tool('portal_workflow')
        self.wfs_to_delete = [wfId for wfId in wfTool.listWorkflows()
                              if wfId.endswith(('meetingitemseraingcollege_workflow',
                                                'meetingitemseraingcouncil_workflow',
                                                'meetingseraingcollege_workflow',
                                                'meetingseraingcouncil_workflow'))]
        logger.info('Done.')

    def _deleteUselessWorkflows(self):
        """Finally, remove useless workflows."""
        logger.info('Removing useless workflows...')
        if self.wfs_to_delete:
            wfTool = api.portal.get_tool('portal_workflow')
            wfTool.manage_delObjects(self.wfs_to_delete)
        logger.info('Done.')

    def addFirstLineIndentToMotivation(self):
        """Add css class attribute p_css_class to every CONTENT_TAGS of p_xhtmlContent."""
        logger.info('Replace praragraph indent in motivation ...')
        brains = self.portal.portal_catalog(meta_type='MeetingItem')

        for brain in brains:
            item = brain.getObject()
            xhtml_content = item.getMotivation()

            if xhtml_content:
                if isinstance(xhtml_content, lxml.html.HtmlElement):
                    children = [xhtml_content]
                else:
                    tree = _turnToLxmlTree(xhtml_content)
                    if not isinstance(tree, lxml.html.HtmlElement):
                        continue
                    children = tree.getchildren()

                for child in children:
                    if child.tag == 'p':
                        child.attrib['style'] = 'text-indent: 55px;'
                        if 'class' in child.attrib:
                            del child.attrib['class']

                # use encoding to 'ascii' so HTML entities are translated to something readable
                xhtml_content = ''.join([lxml.html.tostring(x,
                                                        encoding='ascii',
                                                        pretty_print=False,
                                                        method='xml') for x in children])
                item.setMotivation(xhtml_content)

        logger.info('Done.')

    def cleanup_all_rich_text_fields(self):
        """Add css class attribute p_css_class to every CONTENT_TAGS of p_xhtmlContent."""
        logger.info('Replace styles for ticket #17185 ...')
        brains = self.portal.portal_catalog(meta_type='MeetingItem')
        for brain in brains:
            item = brain.getObject()
            # check every RichText fields
            for field in item.Schema().filterFields(default_content_type='text/html'):
                content = field.get(item)
                if content.find(' style="text-align:justify"') != -1 \
                        or content.find('font-size:85%') \
                        or content.find('class="stab"') \
                        or content.find('border="0"')\
                        or content.find('style="border-collapse:collapse; border:undefined"'):
                    content = content.replace(' style="text-align:justify"', '')
                    content = content.replace('font-size:85%', 'font-size:80%')
                    content = content.replace('class="stab"', 'style="font-size:80%"')
                    content = content.replace('border="0"', 'border="1"')
                    content = content.replace('style="border-collapse:collapse; border:undefined"', 'border="1"')

                    field.set(item, content)

        logger.info('Done.')

    def run(self):
        # # change self.profile_name that is reinstalled at the beginning of the PM migration
        # self.profile_name = u'profile-Products.MeetingSeraing:default'
        # # call steps from Products.PloneMeeting
        # PMMigrate_To_4_0.run(self)
        # # now MeetingLiege specific steps
        # logger.info('Migrating to MeetingSeraing 4.0...')
        # self._cleanCDLD()
        # self._migrateItemPositiveDecidedStates()
        # self._addSampleAnnexTypeForMeetings()
        # self._deleteUselessWorkflows()
        self.cleanup_all_rich_text_fields()
        self.addFirstLineIndentToMotivation()



# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstall Products.MeetingSeraing and execute the Products.PloneMeeting migration;
       2) Clean CDLD attributes;
       3) Add an annex type for Meetings;
       4) Remove useless workflows;
       5) Migrate positive decided states.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run()
    migrator.finish()
# ------------------------------------------------------------------------------
