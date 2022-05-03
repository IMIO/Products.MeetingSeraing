# Migration pm4.2

## TODO 

- Remove specific MeetingItem validation WF and migrate it into the new field on MeetingConfig.
- Remove specific MeetingItem last states and use custom WF adaptation instead.
- Remove specific MeetingWF and use a WF adaptation instead.
- Override proper methods in adapters.py. Currently, it's not working as Meeting is now using snake case for the method's names.
- Migrate commission into the Plonemeeting's new commission field.
- Verify and adapt import_data.py as it's a bit hacky at the moment
- Handle custom WF adaptations properly - removed the pathed WF adaptation
- Fix imports in the tests
- Fix the tests
- Rename state returned_to_advise -> returned_to_proposing_group_waiting_advice
  - Use adaptations.WAITING_ADVICES_FROM_STATES instead of a custom WF adaptation
  - Use WF adaptation 'waiting_advices'


## Done 
- Ensure tests are running