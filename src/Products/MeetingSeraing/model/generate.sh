#!/bin/sh
/srv/archgenxml/agx27/bin/archgenxml --cfg generate.conf MeetingSeraing.zargo -o ..
#we do some manual adaptations
#do not take generatedsubscribers into account
echo "Removing 'generatedsubscribers.zcml' include from configure.zcml"
#we remove the eleventh line : <include file="generatedsubscribers.zcml"/>
sed '/generatedsubscribers.zcml/d' ../configure.zcml >> ../tmp.zcml
# make workflow removed before re-adding them so wfAdaptations are ok, see #7692
sed -i '/<object name="portal_workflow" meta_type="Plone Workflow Tool">/a \ <object name="meetingitemcouncilSeraing_workflow" meta_type="Workflow" remove="True"/>' ../profiles/default/workflows.xml
sed -i '/<object name="portal_workflow" meta_type="Plone Workflow Tool">/a \ <object name="meetingitemcollegeSeraing_workflow" meta_type="Workflow" remove="True"/>' ../profiles/default/workflows.xml
sed -i '/<object name="portal_workflow" meta_type="Plone Workflow Tool">/a \ <object name="meetingcouncilSeraing_workflow" meta_type="Workflow" remove="True"/>' ../profiles/default/workflows.xml
sed -i '/<object name="portal_workflow" meta_type="Plone Workflow Tool">/a \ <object name="meetingcollegeSeraing_workflow" meta_type="Workflow" remove="True"/>' ../profiles/default/workflows.xml
sed -i '/<object name="portal_workflow" meta_type="Plone Workflow Tool">/a \ <!-- first remove then re-apply so workflows are correct regarding workflow adaptations... -->' ../profiles/default/workflows.xml ../configure.zcml
mv ../tmp.zcml ../configure.zcml
rm ../generatedsubscribers.zcml
rm ../wfsubscribers.py
echo "We do not use wf subsribers for now as PM implemented it differently"
