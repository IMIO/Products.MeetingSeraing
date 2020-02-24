# -*- coding: utf-8 -*-

from Products.MeetingCommunes.migrations.migrate_to_4_1 import Migrate_To_4_1 as MCMigrate_to_4_1

import logging


logger = logging.getLogger('MeetingSeraing')


class Migrate_To_4_1(MCMigrate_to_4_1):

    def run(self,
            profile_name=u'profile-Products.MeetingSeraing:default',
            extra_omitted=[]):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = profile_name

        # call steps from Products.MeetingCommunes
        super(Migrate_To_4_1, self).run(extra_omitted=extra_omitted)

        # now MeetingCommunes specific steps
        logger.info('Migrating to MeetingSeraing 4.1...')


# The migration function -------------------------------------------------------
def migrate(context):
    """This migration function:

       1) Reinstall Products.MeetingCommunes and execute the Products.PloneMeeting migration;
       2) Define default values for 'contacts' directory.position_types;
       3) Define default ftw.labels labels.
    """
    migrator = Migrate_To_4_1(context)
    migrator.run()
    migrator.finish()