#!/bin/sh
/srv/archgenxml/agxtrunk/bin/archgenxml --cfg generate.conf MeetingCommunes.zargo -o ..
#we do some manual adaptations
#do not take generatedsubscribers into account
echo "Removing 'generatedsubscribers.zcml' include from configure.zcml"
#we remove the eleventh line : <include file="generatedsubscribers.zcml"/>
sed '/generatedsubscribers.zcml/d' ../configure.zcml >> ../tmp.zcml
rm ../configure.zcml
mv ../tmp.zcml ../configure.zcml
rm ../generatedsubscribers.zcml
rm ../wfsubscribers.py
echo "We do not use wf subsribers for now as PM implemented it differently"
