from org.modelio.metamodel.mda import ModuleComponent
from org.modelio.metamodel.uml.infrastructure import Profile

#
# generateprofile 2.0
#  This script generates a part of the 'module.xml' file used for the module development.
#  It displays the complete description of a profile.
#
# Author:  tma
#
# Applicable on: Module, Profile
#
# Version history:
# 1.0   16th March 2012 - creation
# 2.0   10th October 2013 - update for Modelio 3
#

#
# Convert a boolean to string
# Example:
#    False --> false
#    True  --> true
#
def booleanToString (value):
    return str(value).lower()
    
#
# Returns the description of an XML attribute
# Example:
#    name="value"
#
def xmlAttribute (name,value):
    return name + "=\"" + value + "\""

#
# Note type description
# Example:
#    <notetype uid="38cfed8d-6a06-11e1-b50d-0027103f347d" name="summary" label="Summary" is-hidden="false"/>
#
def generateNoteType (notetype):
    print "            <notetype " + xmlAttribute ("uid", notetype.getUuid().toString()) + " " + xmlAttribute ("name", notetype.getName()) + " " + xmlAttribute("label", notetype.getLabelKey()) + " " + xmlAttribute ("is-hidden", booleanToString(notetype.isIsHidden())) + "/>"

#
# ExternDocument type description
# Example:
#    <externdocumenttype uid="38cfed8d-6a06-11e1-b50d-0027103f347d" name="summary" label="Summary" is-hidden="false"/>
#
def generateExternDocType (doctype):
    print "            <externdocumenttype " + xmlAttribute ("uid", doctype.getUuid().toString()) + " " + xmlAttribute ("name", doctype.getName()) + " " + xmlAttribute("label", doctype.getLabelKey()) + " " + xmlAttribute ("is-hidden", booleanToString(doctype.isIsHidden())) + "/>"

#
# Tag type description
# Example:
#    <taggedvalues uid="38cfed8d-6a06-11e1-b50d-0027103f347d" name="implementation" label="implementation" parameter-card="1" is-hidden="false" is-signed="false" />
#
def generateTagType (tagtype):
    print "            <taggedvalues " + xmlAttribute ("uid", tagtype.getUuid().toString()) + " " + xmlAttribute ("name", tagtype.getName()) + " " + xmlAttribute("label", tagtype.getLabelKey()) + " " + xmlAttribute ("parameter-card", tagtype.getParamNumber()) + " " + xmlAttribute ("is-hidden", booleanToString(tagtype.isIsHidden())) + " " + xmlAttribute ("is-signed", booleanToString(tagtype.isIsQualified())) + "/>"

#
# Stereotype description
# Example:
#    <stereotype uid="38cda39d-6a06-11e1-b50d-0027103f347d" name="Application" label="Application" metaclass="Package" is-hidden="false">
#        <icons>
#            <explorer path="res/icons/application.png" />
#            <diagram path="res/icons/application.png" />
#        </icons>
#        ...
#    </stereotype>
#
def generateStereotype (stereotype):
    owner = ""
    if stereotype.getParent() != None:
        owner = " " + xmlAttribute ("owner-stereotype", stereotype.getParent().getName())
    print "        <stereotype " + xmlAttribute ("uid", stereotype.getUuid().toString()) + " " + xmlAttribute ("name", stereotype.getName()) + " " + xmlAttribute("label", stereotype.getLabelKey()) + " " + xmlAttribute ("metaclass", stereotype.getBaseClassName()) + owner + " " + xmlAttribute ("is-hidden", booleanToString(stereotype.isIsHidden())) + ">"
    print "            <icons>"
    print "                <explorer " + xmlAttribute ("path", stereotype.getIcon()) + "/>"
    print "                <diagram " + xmlAttribute ("path", stereotype.getImage()) + "/>"
    print "            </icons>"
    for notetype in stereotype.getDefinedNoteType():
        generateNoteType(notetype)
    for tagtype in stereotype.getDefinedTagType():
        generateTagType(tagtype)
    for externDocType in stereotype.getDefinedExternDocumentType():
        generateExternDocType(externDocType)
    print "        </stereotype>"

#
# Metaclass description
# Example:
#    <anonymous-stereotype uid="38cda39d-6a06-11e1-b50d-0027103f347d" metaclass="Package">
#        ...
#    </anonymous-stereotype>
#
def generateMetaclassRef (metaclass):
    print "        <anonymous-stereotype " + xmlAttribute ("uid", metaclass.getUuid().toString()) + " " + xmlAttribute ("metaclass", metaclass.getReferencedClassName()) + ">"
    for notetype in metaclass.getDefinedNoteType():
        generateNoteType(notetype)
    for tagtype in metaclass.getDefinedTagType():
        generateTagType(tagtype)
    for externDocType in metaclass.getDefinedExternDocumentType():
        generateExternDocType(externDocType)
    print "        </anonymous-stereotype>"

#
# Profile description
# Example:
#    <profile uid="38cda39d-6a06-11e1-b50d-0027103f347d" name="JavaProfile">
#        ...
#    </profile>
#
def generateProfile(profile):
    print "    <profile " + xmlAttribute ("uid", profile.getUuid().toString()) + " " + xmlAttribute ("name", profile.getName()) + ">"
    for metaclass in profile.getOwnedReference():
        generateMetaclassRef (metaclass)
    for stereotype in profile.getDefinedStereotype():
        generateStereotype (stereotype)
    print "    </profile>"

#
# Module description
# Example:
#    <module uid="38cda39d-6a06-11e1-b50d-0027103f347d" name="JavaDesigner" class="org.modelio.javadesigner.impl.JavaDesignerModule">
#        ...
#    </module>
#
def generateModule (module):
    print "<module " + xmlAttribute ("uid", metaclass.getUuid().toString()) + " " + xmlAttribute ("name", module.getName()) + " " + xmlAttribute ("class", module.getjavaClassName()) + ">"
    for profile in module.getOwnedProfile():
        generateProfile(profile)

#
# The macro execution starts here
#
for element in selectedElements:
    if (isinstance(element, ModuleComponent)):
        for profile in element.getOwnedProfile():
            generateProfile (profile)
    if (isinstance(element, Profile)):
        generateProfile (element)