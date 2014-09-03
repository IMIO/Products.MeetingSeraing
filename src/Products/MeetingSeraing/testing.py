# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting
import Products.MeetingSeraing


MLL_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                           package=Products.MeetingSeraing,
                           name='MLL_ZCML')

MLL_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MLL_ZCML),
                               name='MLL_Z2')

MLL_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingSeraing,
    additional_z2_products=('Products.MeetingSeraing',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow'),
    gs_profile_id='Products.MeetingSeraing:testing',
    name="MLL_TESTING_PROFILE")

MLL_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MLL_TESTING_PROFILE,), name="MLL_TESTING_PROFILE_FUNCTIONAL")
