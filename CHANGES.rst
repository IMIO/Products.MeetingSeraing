Products.MeetingSeraing Changelog
=================================

4.2.0a3 (2022-08-23)
--------------------

- Fixed a bug when an item was late (`_latePresentedItem`).
  [aduchene]
- Fixed broken tests as PowerEditors is now a WFA.
  [aduchene]

4.2.0a2 (2022-08-19)
--------------------

- Fixed issues with back transitions for WFA seraing_validated_by_DG.
  [aduchene]
- Add missing WFA translations.
  [aduchene]
- Refactored PowerEditors feature. Now it's a WFA's and PowerEditors may store item podtemplate as annex (SUP-16787).
  [aduchene]
- marginalNotes are now highlighted and displayed at the top when completed (SUP-16802).
  [aduchene]
- Renamed `returned_to_advise` to `seraing_returned_to_advise`.
  [aduchene]
- Improved demo import_data to ease testing.
  [aduchene]
- Add missing icons back.
  [aduchene]

4.2.0a1 (2022-08-11)
--------------------

- Compatible for PloneMeeting 4.2.
  [aduchene]
- meetingseraing_workflow and meetingitemseraing_workflow are now deprecated.
  Use PloneMeeting's default WF with itemWFValidationLevels set accordingly.
  [aduchene]
- Add two new WFA to have feature parity between old seraing_workflow and PloneMeeting's default WF.
  [aduchene]
- Adapted PowerEditors feature to use local roles correctly.
  [aduchene]
- Fixed broken tests.
  [aduchene]

4.1.6 (2022-04-01)
------------------

- Fixed typo getMeetingStatesAcceptingItem -> getMeetingStatesAcceptingItems.
  [aduchene]
- Fixed wrong permissions in `patch_return_to_proposing_group_with_last_validation`.
  [aduchene]


4.1.5 (2022-03-09)
------------------

- Fixed issue with mayPresent.
  [aduchene]
- SUP-18390: Fixed incorrect permissions in return_to_proposing_group_with_last_validation WFA
  [aduchene]


4.1.4 (2021-04-07)
------------------

- SUP-16268: refactored takenOverBy feature. Now takenOverBy is kept between transitions except for those defined in `MeetingConfig.transitionsReinitializingTakenOverBy`.
  [aduchene]


4.1.3 (2020-12-18)
------------------

- Renamed `testSearches.test_pm_SearchItemsToCorrectToValidateOfHighestHierarchicLevel`
  to `testSearches.test_pm_SearchItemsToCorrectToValidateOfHighestHierarchicLevel`
  as it was renamed in `Products.PloneMeeting` and we bypass it this way.
  [gbastien]
- Changed setTakenOverBy as it should not reinit itself
  when transitionning from itemfrozen to accepted. SUP-15933
  [aduchene]

4.1.2 (2020-10-22)
------------------

- Updated sections label to commissions label. SUP-15177
  [aduchene]


4.1.1 (2020-10-12)
------------------

- Fixed MANIFEST.in
  [aduchene]


4.1 (2020-10-12)
----------------
- Compatible for PloneMeeting 4.1
- Added two new mail's notification:
    - When item is delayed, send mail to service head;
    - When advice is added or modified, send mail to service head.
- Keep "Taken over" for severals states
- Fix sendMailIfRelevant.
  [odelaere]
- Adapted code and tests regarding DX meetingcategory.
  [gbastien]
- Adapted templates regarding last changes in Products.PloneMeeting.
  [gbastien]

4.02 (2019-05-02)
-----------------
- Change rules for keeping annexes and decision's annexes

4.0 (2017-01-01)
----------------
- Adapted workflows to define the icon to use for transitions
- Removed field MeetingConfig.cdldProposingGroup and use the 'indexAdvisers' value
  defined in the 'searchitemswithfinanceadvice' collection to determinate what are
  the finance adviser group ids
- 'getEchevinsForProposingGroup' does also return inactive MeetingGroups so when used
  as a TAL condition in a customAdviser, an inactive MeetingGroup/customAdviser does
  still behaves correctly when updating advices
- Use ToolPloneMeeting.performCustomWFAdaptations to manage our own WFAdaptation
  (override of the 'no_publication' WFAdaptation)
- Adapted tests, keep test... original PM files to overrides original PM tests and
  use testCustom... for every other tests, added a testCustomWorkflow.py
- Now that the same WF may be used in several MeetingConfig in PloneMeeting, removed the
  2 WFs meetingcollege and meetingcouncil and use only one meetingseraing where wfAdaptations
  'no_publication' and 'no_global_observation' are enabled
- Added profile 'financesadvice' to manage advanced finances advice using a particular
  workflow and a specific meetingadvicefinances portal_type
- Adapted profiles to reflect imio.annex integration
- Added new adapter method to ease financial advices management while generating documents
  printFinanceAdvice(self, case)
- Added parameter 'excludedGroupIds' to getPrintableItems and getPrintableItemsByCategory
- MeetingObserverLocal has every View-like permissions in every states

3.3 (2015-04-07)
----------------
- Updated regarding changes in PloneMeeting
- Removed profile 'examples' that loaded examples in english
- Removed dependencies already defined in PloneMeeting's setup.py
- Added parameter MeetingConfig.initItemDecisionIfEmptyOnDecide that let enable/disable
  items decision field initialization when meeting 'decide' transition is triggered
- Added MeetingConfig 'CoDir'
- Added MeetingConfig 'CA'
- Field 'MeetingGroup.signatures' was moved to PloneMeeting

3.2.0.1 (05-09-2014)
--------------------
- Original release
