# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import FunctionalTesting
from Products.PloneMeeting.testing import PloneWithPackageLayer
import Products.MeetingSeraing
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE


MS_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                          package=Products.MeetingSeraing,
                          name='MS_ZCML')

MS_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MS_ZCML),
                              name='MS_Z2')

MS_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingSeraing,
    additional_z2_products=('imio.dashboard',
                            'Products.MeetingSeraing',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingSeraing:testing',
    name="MS_TESTING_PROFILE")


MS_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MS_TESTING_PROFILE,), name="MS_TESTING_PROFILE_FUNCTIONAL")


MS_TESTING_ROBOT = FunctionalTesting(
    bases=(
        MS_TESTING_PROFILE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="MS_TESTING_ROBOT",
)
