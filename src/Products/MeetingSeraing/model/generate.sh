#!/bin/sh
/srv/archgenxml/archgenxml-2.7/bin/archgenxml --cfg generate.conf MeetingSeraing.zargo -o tmp

# only keep workflows
cp -rf tmp/profiles/default/workflows/meetingseraing_workflow ../profiles/default/workflows
cp -rf tmp/profiles/default/workflows/meetingitemseraing_workflow ../profiles/default/workflows
rm -rf tmp