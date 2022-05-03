# Migration pm4.2

## TODO 

- Remove specific MeetingItem WF and migrate it into the new field on MeetingConfig.
- Remove specific MeetingWF and use a WF adapation instead.
- Override proper methods in adapter.py. Currently, it's not working as Meeting is now using snake case for the method's names.
- Migrate commission into the Plonemeeting's new commission field.
- Verify and adapt import_data.py as it's a bit hacky a the moment
- Handle custom WF adaptations properly
- Fix imports in the tests
- Fix the tests

## Done 
- Ensure tests are running