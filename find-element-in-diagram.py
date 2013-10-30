#
# Search elements
#
# Description:
# This script searches the diagrams displaying the selected elements.
#
# Author:  Modeliosoft,jmfavre
#
# Applicable on:
# - (I)ModelElement
#
# Compatibility 2.x, 3.x
#
# Version history:
# 1.1  30 Oct 2013   
#    - Port to Modelio 3.0
#    - Refactoring and some comments
# 1.0  03 Jun 2013   
#    - Creation
#

# these imports with renamings allows to cope with Modelio 2.x and 3.x API changes
try:
  from org.modelio.api.modelio import Modelio
  from org.modelio.metamodel.uml.infrastructure import Element as ModelioElement
  from org.modelio.metamodel.diagrams import AbstractDiagram as ModelioAbstractDiagram
  from org.modelio.metamodel.uml.infrastructure import ModelTree as ModelioModelTree
  orgVersion = True
except:
  from com.modeliosoft.modelio.api.model.uml.infrastructure import Element as ModelioElement
  from com.modeliosoft.modelio.api.model.diagrams import IAbstractDiagram as ModelioAbstractDiagram
  from com.modeliosoft.modelio.api.model.uml.statik import IModelTree as ModelioModelTree
  orgVersion = False

def getMetaClassName(element):
  """ The way to get metaclass name of an element has changed from Modelio 2.x to 3.x
  """
  if orgVersion:
    name = element.getMClass().getName()
  else:
    name = element.metaclassName
  return name
      
def getFullName(element):
  """ Return full qualified name of an element
  """
  name = element.getName()
  if (isinstance(element,ModelioModelTree)):
    owner = element.getOwner()
    if (owner is not None):
      name = getFullName(owner) + "." + name
  elif (isinstance(element, ModelioElement)):
    owner = element.getCompositionOwner()
    if (owner is not None):
      name = getFullName(owner) + "." + name
  return name

DIAGRAM_SERVICE = Modelio.getInstance().getDiagramService()
ALL_DIAGRAMS = Modelio.getInstance().getModelingSession().findByClass(ModelioAbstractDiagram)

def getDiagramsContainingElement(element):
  """ Return all diagrams containing the element
  """
  selectedDiagrams = []
  for diagram in ALL_DIAGRAMS:
    graphicElements = DIAGRAM_SERVICE.getDiagramHandle(diagram).getDiagramGraphics(element)
    if len(graphicElements)!=0:
      selectedDiagrams.append(diagram)
  return selectedDiagrams

def getDiagramSignature(diagram):
  return getFullName(diagram)+" : "+getMetaClassName(diagram)

  
for element in selectedElements:
  diagrams = getDiagramsContainingElement(element)
  nbDiagrams = len(diagrams)
  if nbDiagrams != 0:
    print '"'+getFullName(element)+'"',"found in",nbDiagrams,"diagram"+("s" if nbDiagrams>1 else "")
    for diagram in diagrams:
      print "      ==>  "+getDiagramSignature(diagram)
      Modelio.getInstance().getEditionService().openEditor(diagram)
    print
