#
# AdvancedSearch 
#
# Description:
# This script searches for elements.
# Applicable on: Anything
#
# Licence: GPL
#
# Author:  Modeliosoft, jmfavre
#
# Applicable on:
# - IModelElement
#
# Version history:
# 1.2  28 Oct 2013    
#    - Support to Modelio 3.0 (and 2.x at the same time)
#    - Refactoring and comments
#    - Results are now sorted by name
# 1.1  19 Feb 2012    
#    - Regular expression search option added
#    - Catching exception if regular exception is incorrect
#    - IModelElement metaclass selected by default
# 1.0  08 Feb 2012    
#    - Creation
#

# check if this is modelio 3 because the API has changed
try:
  from org.modelio.api.modelio import Modelio
  orgVersion = True
except:
  from com.modeliosoft.modelio.api.modelio import Modelio
  orgVersion = False
# The proper way to get version in general is as below
# version = Modelio.getInstance().getContext().getVersion()

from java.lang import *
from java.lang import Integer
from java.util import ArrayList
from java.util import List
from java.util import HashSet
from java.util import Comparator
from java.util.regex import Pattern
from java.util.regex import PatternSyntaxException
from org.eclipse.swt.widgets import MessageBox
from org.eclipse.swt import SWT
from org.eclipse.swt.events import SelectionAdapter
from org.eclipse.swt.browser import Browser
from org.eclipse.swt.widgets import Shell
from org.eclipse.swt.widgets import Display
from org.eclipse.swt.widgets import Label
from org.eclipse.swt.widgets import Button
from org.eclipse.swt.widgets import Listener
from org.eclipse.swt.widgets import Group
from org.eclipse.swt.widgets import Text
from org.eclipse.swt.widgets import List
from org.eclipse.swt.widgets import Composite
from org.eclipse.swt.layout import GridData
from org.eclipse.swt.layout import FormData
from org.eclipse.swt.layout import FormAttachment
from org.eclipse.swt.layout import GridLayout
from org.eclipse.jface.viewers import TableViewer
from org.eclipse.jface.viewers import ISelectionChangedListener
from org.eclipse.jface.viewers import IStructuredContentProvider
from org.eclipse.jface.viewers import LabelProvider
from org.eclipse.jface.viewers import ListViewer
from org.eclipse.jface.viewers import ViewerSorter
if orgVersion:
  from org.modelio.api.ui.text import TextWrapperForIElement
  from org.modelio.api.meta import IMetamodelService
  from org.modelio.metamodel.uml.infrastructure import ModelElement
  MODELELEMENT_METACLASS = ModelElement
  from org.modelio.metamodel.uml.infrastructure import ModelTree
  MODELTREE_METACLASS = ModelTree
  from org.modelio.metamodel.uml.statik import NameSpace
  NAMESPACE_METACLASS = NameSpace  
else:
  from com.modeliosoft.modelio.api.ui.text import TextWrapperForIElement
  from com.modeliosoft.modelio.api.meta import IMetamodelService
  from com.modeliosoft.modelio.api.model.uml.statik import IModelTree
  MODELELEMENT_METACLASS = IModelElement
  MODELTREE_METACLASS = IModelTree
  NAMESPACE_METACLASS = INameSpace
  
METAMODEL_SERVICE = Modelio.getInstance().getMetamodelService()
IMAGE_SERVICE = Modelio.getInstance().getImageService()


def getMetaclassFromElement(element):
  if orgVersion:
    name = element.getMClass().getName()
  else:
    name = element.metaclassName
  return METAMODEL_SERVICE.getMetaclass(name)

def getMetaclassImageFromMetaclass(metaclass):
  return IMAGE_SERVICE.getMetaclassImage(metaclass)

def getMetaclassImageFromElement(element):
  metaclass = getMetaclassFromElement(element)
  return getMetaclassImageFromMetaclass(metaclass)
  
# Returns the full path of given element by browsing its parent hierarchy.

def getFullName(element):
  name = element.getName()
  if (isinstance(element,MODELTREE_METACLASS)):
    owner = element.getOwner()
    if (owner is not None):
      name = getFullName(owner) + "." + name
  return name
  
# The "Search" window allows to select metaclasses with two lists
# The list on the left contains unselected metaclasses
# The list on the right contains the metaclasses used for filterning
# In the GUI << and >> buttons allows to update the variables below
# These lists contains "Metaclass" objects (this class is defined below)
unselectedMetaclasses = []   # list of Metaclass objects (see below)
selectedMetaclasses = []

# The root of all metaclasses. (I)ModelElement depending on API version.
ROOT_METACLASS = MODELELEMENT_METACLASS

# Function used to sort metaclass by name
def key_name(mc):
  return mc.name
  
# Build the lists of metaclass (unselectedMetaclasses/right)
# with the root on the right as the only one selected and all other
# on the left
def initmetaclasses():
  # get all metaclass under the root metaclass including the root itself
  metaclasses = METAMODEL_SERVICE.getInheritingMetaclasses(ROOT_METACLASS)
  # necessary on version 3 as the method now exclude the element
  if ROOT_METACLASS not in metaclasses:
    metaclasses = metaclasses + [ROOT_METACLASS]
  # Create Metaclass objects and store in the proper list
  # Note that only the root is selected at the begining
  for metaclass in metaclasses:
    if metaclass is not ROOT_METACLASS:
      unselectedMetaclasses.append(MetaclassWrapper(metaclass))
    else:
      selectedMetaclasses.append(MetaclassWrapper(metaclass))
  # Sort the unselected metaclass by alphabetic order
  # (necessary on version 3 as getInheritingMetaclasses no longer do it)
  unselectedMetaclasses.sort(key=key_name)
  
class MetaclassWrapper:
  def __init__(self, metaclass):
    self.metaclass = metaclass
    self.name = metaclass.getSimpleName()


#=== Search Engine ================================================================= 
import re
def search(metaclasses, regexp, options):
  print "Searching ..."
  rawResults = HashSet()
  session = Modelio.getInstance().getModelingSession()
  
  #--- (1) Add all instances of selected metaclasses 
  for metaclass in metaclasses:
    print "  searching for instance of metaclass ",metaclass.getSimpleName()," ... ",
    metaclassInstances = session.findByClass(metaclass)
    print unicode(len(metaclassInstances)),"elements found"
    rawResults.addAll(metaclassInstances)
  # remove predefined types
  predefTypes = Modelio.getInstance().getModelingSession().getModel().getUmlTypes().getBOOLEAN().getOwner()
  rawResults.remove(predefTypes)
  rawResults.remove(predefTypes.getOwner())
  print "  ==>",unicode(len(rawResults)),"elements found (primitive types excluded)"
  
  #--- (2) Check for name matching
  filteredResults = []
  try:
    if options[0] == 1:
      p = Pattern.compile(regexp)
      for result in rawResults:
        name = result.getName()
        if (p.matcher(name).matches()):
          filteredResults.append(result)
    else:
      for result in rawResults:
        if result.getName().find(regexp) != -1:
          filteredResults.append(result)
  except PatternSyntaxException:
    messageBox("The entered regular expression: '"+regexp+"' has a syntax error.")
  except IllegalArgumentException:
    messageBox("Illegal Argument Exception.")
  print "  "+unicode(len(filteredResults))+" elements selected after name filtering"
  
  #--- (3) sort results by name
  filteredResults.sort(key=lambda x:x.getName())
  return filteredResults





  
#=== GUI : message Box =====================================================

def messageBox(s):
  parent = Display.getDefault().getActiveShell()
  child = Shell(parent, SWT.OK)
  mb = MessageBox (child, SWT.OK | SWT.ERROR)
  mb.setMessage(s)
  mb.open()

    
#===== GUI : Search Results window ==================================
# The interface has three components:
# (1) an introduction text
# (2) a "Objects found" panel containing a table listing the objects found
# (3) a close button
# The table is not present if no objects are found
# Note that if a object is selected in the list of objects found, 
# then it will be selected in modelio explorer.
class SearchResultsWindow:
  def __init__(self, parentWindow, metaclasses, wordtosearch, options):
    # do the search
    results = HashSet()
    listMC = ArrayList()
    for mc in metaclasses:
      listMC.add(mc.metaclass)
    results = search(listMC, wordtosearch, options)

    # build the interface
    childW = 420
    if (len(results)==0):
      childH=100
    else:
      childH = 400
    child = Shell(parentWindow, SWT.CLOSE | SWT.RESIZE)
    child.setMinimumSize(childW, childH)
    child.setText("Search Results")
    self.createContent(child, results, wordtosearch)
    x = (parentWindow.getBounds().width-childW)/2+parentWindow.getBounds().x
    y = (parentWindow.getBounds().height-childH)/2+parentWindow.getBounds().y
    child.setLocation(x, y)
    child.setSize(childW, childH)
    child.open()

  def createContent(self, child, results, wordtosearch):
    resultsCount = len(results)
    gridLayout = GridLayout(1, 1)
    child.setLayout(gridLayout)

    #-- Introduction text
    introdata = GridData(GridData.FILL_HORIZONTAL) ; introdata.verticalIndent = 5
    introlabel = Label(child, SWT.WRAP)            ; introlabel.setLayoutData(introdata)
    if (resultsCount==0):
      introlabel.setText("No element matching your search request '"+wordtosearch+"' has been found.")
    else:
      if not orgVersion:
        introlabel.setText("Click on each element to select it directly from the UML model explorer.")
    introlabel.setLocation(10, 40)

    #-- "Objects found" panel containing a table (if the results is not empty)
    if (resultsCount!=0):
      resultsGroup = Group(child, SWT.NONE)
      fd_resultsGroup = GridData(SWT.FILL, SWT.FILL, 1,1)
      resultsGroup.setLayoutData(fd_resultsGroup)
      if resultsCount == 1:
        text = "1 element found"
      else:
        text = str(resultsCount)+" elements found"
      resultsGroup.setText(text)
      gridLayout2 = GridLayout()
      gridLayout2.numColumns = 1
      resultsGroup.setLayout(gridLayout)
      table = TableViewer(resultsGroup, SWT.NONE);
      table.getControl().setLayoutData(GridData(GridData.FILL_BOTH))
      # When a element in the list is selected then select it in modelio explorer
      # This is achieved with fireNavigate method of the NavigationService
      # FIXME this feature is currently not working on V3 because of fireNavigate
      class SCListener(ISelectionChangedListener):
        def __init__(self, app):
          self.app = app
        def selectionChanged(self, event):
          selection = event.getSelection()
          element = selection.getFirstElement()
          print element
          if (element != None):
            Modelio.getInstance().getNavigationService().fireNavigate(element)

      sclistener = SCListener(self)
      table.setContentProvider(self.SearchResultsContentProvider(results))
      table.setLabelProvider(self.SearchResultsLabelProvider())
      table.addSelectionChangedListener(sclistener)
      table.setInput(results)

    #-- "Close" Button
    closeBtn = Button(child, SWT.FLAT)
    closeBtn.setText("Close")
    class MyListener(Listener):
     def handleEvent(self, event):
      if (event.widget == closeBtn):
         closeBtn.getShell().close()
    listener = MyListener()
    closeBtn.addListener(SWT.Selection, listener)
    btndata = GridData(GridData.HORIZONTAL_ALIGN_END) ;    btndata.widthHint = 50
    closeBtn.setLayoutData(btndata)
    
  #-- Content Provider for the table  
  class SearchResultsContentProvider(IStructuredContentProvider):
    def __init__(self, results):
      self.results = results
    def getElements(self, element):
      return self.results
    def dispose(self):
      pass

  #-- Label provider for each element in the table
  class SearchResultsLabelProvider(LabelProvider):
    def getImage(self, element):
      try:
        image = getMetaclassImageFromElement(element)
      except:
        image = None
      return image
    def getText(self, element):
      # print "getText(",element,")",
      text = ""
      if (isinstance(element, NAMESPACE_METACLASS)):
        ns = element
        parentStr = ""
        parent = ns.getOwner()
        while (parent != None):
          parentStr = parent.getName() + "." + parentStr
          parent = parent.getOwner()
        text = parentStr + ns.getName()
      else:
        text = getFullName(element)
      # print text
      return text


    
#====== Main search window ======================================================
# This main window allows to define the search criteria and launch the search
# It is composed as following:
# (1) A "Name filter" panel
# (2) A "Metaclass filter" panel
# (3) "Search" and "Close" buttons at the bottom
class SearchWindow:

  class _MCContentProvider(IStructuredContentProvider):
    def getElements(self, metaclassWrapper):
      return metaclassWrapper
    def dispose(self):
      pass
    def inputChanged(self, viewer, oldInput, newInput):
      pass
        
  class _MCLabelProvider(LabelProvider):
    def getImage(self, metaclassWrapper):
      return getMetaclassImageFromMetaclass(metaclassWrapper.metaclass)
    def getText(self, metaclassWrapper):
      return metaclassWrapper.name
      
  def __init__(self):
    childW = 500
    childH = 400
    parent = Display.getDefault().getActiveShell()
    child = Shell(parent, SWT.CLOSE | SWT.RESIZE)
    child.setMinimumSize(childW, childH)
    child.setText("Advanced Search")
    self._createContent(child)
    parentW = parent.getBounds().width
    parentH = parent.getBounds().height
    parentX = parent.getBounds().x
    parentY = parent.getBounds().y
    child.setLocation((parentW-childW)/2+parentX, (parentH-childH)/2+parentY)
    child.setSize(childW, childH)
    child.open()

  def _createContent(self, child):
    gridLayout = GridLayout(1, 1)
    child.setLayout(gridLayout)

    #---- (1) "Name filter" group
    # This group contains:
    # - a text area with a filter label
    # - regexpr check box with its label
    nameFilterGroup = Group(child, SWT.NONE)
    fd_resultsGroup = GridData(GridData.FILL_HORIZONTAL)
    nameFilterGroup.setLayoutData(fd_resultsGroup)
    nameFilterGroup.setText("Name filter")
    gridLayout2 = GridLayout()
    gridLayout2.numColumns = 2
    nameFilterGroup.setLayout(gridLayout2)
    filterlabel = Label(nameFilterGroup, SWT.NULL)
    filterlabel.setText("Filter: ")
    filterTxt = Text(nameFilterGroup, SWT.SINGLE | SWT.BORDER)
    gridData = GridData(SWT.FILL, SWT.DEFAULT, 1, 0)
    filterTxt.setLayoutData(gridData)
    regexpCheckBox = Button(nameFilterGroup, SWT.CHECK)
    regexpCheckBox.setText("Use regular expression")

    #---- (2) "Metaclass filter" group
    # This group contains:
    # (2.1) a table on the left for unselected metaclasses
    # (2.2) two buttons on the center: ">>" and "<<" 
    # (2.3) a table on the right for selected metaclasses
    mcFilterGroup = Group(child, SWT.NONE)
    gd_mcFilterGroup = GridData(SWT.FILL, SWT.FILL, 1,1)
    mcFilterGroup.setLayoutData(gd_mcFilterGroup)
    mcFilterGroup.setText("Metaclass filter")
    gridLayout3 = GridLayout() ; gridLayout3.numColumns = 3
    mcFilterGroup.setLayout(gridLayout3)
    # (2.1) table for unselected metaclasses
    unselectedMetaclassesTable = TableViewer(mcFilterGroup, SWT.BORDER | SWT.MULTI | SWT.V_SCROLL)
    unselectedMetaclassesTable.setLabelProvider(self._MCLabelProvider())
    unselectedMetaclassesTable.setContentProvider(self._MCContentProvider())
    gdata = GridData(SWT.FILL, SWT.FILL, 1, 1)
    gdata.minimumWidth = 200;
    unselectedMetaclassesTable.getControl().setLayoutData(gdata)
    unselectedMetaclassesTable.setInput(unselectedMetaclasses)

    # (2.2) Add (">>") and Remove ("<<") buttons
    # They allow to change the list of metaclasses selected
    # The buttons are in a composite
    compositeButtons = Composite(mcFilterGroup, SWT.NONE)
    gdLayout = GridLayout()
    gdLayout.numColumns = 1;
    compositeButtons.setLayout(gdLayout)
    gdata2 = GridData(SWT.DEFAULT, SWT.CENTER, 0, 1)
    gdata2.widthHint = 50
    compositeButtons.setLayoutData(gdata2)
    # ">>" button
    addBtn = Button(compositeButtons, SWT.FLAT)
    addBtn.setText(">>")
    gd_addData = GridData(GridData.FILL_HORIZONTAL)
    gd_addData.widthHint = 20
    addBtn.setLayoutData(gd_addData)
    # "<<" button
    removeBtn = Button(compositeButtons, SWT.FLAT)
    removeBtn.setText("<<")
    gd_removeData = GridData(GridData.FILL_HORIZONTAL)
    gd_removeData.widthHint = 20
    removeBtn.setLayoutData(gd_removeData)

    # (2.3) Table on the right for selected metaclasses
    selectedMetaclassTable = TableViewer(mcFilterGroup, SWT.BORDER | SWT.MULTI | SWT.V_SCROLL)
    selectedMetaclassTable.setLabelProvider(self._MCLabelProvider())
    selectedMetaclassTable.setContentProvider(self._MCContentProvider())
    gdata3 = GridData(SWT.FILL, SWT.FILL, 1, 1)
    gdata3.minimumWidth = 200;
    selectedMetaclassTable.getControl().setLayoutData(gdata3)
    selectedMetaclassTable.setInput(selectedMetaclasses)

    #---- (3) Bottom buttons : "Search" and "Close"
    compositeBottomButtons = Composite(child, SWT.NONE)
    gdLayout = GridLayout()
    gdLayout.numColumns = 2;
    compositeBottomButtons.setLayout(gdLayout)
    compositeBottomButtons.setLayoutData(GridData(SWT.END, SWT.BOTTOM, 0, 0 ))
    searchBtn = Button(compositeBottomButtons, SWT.FLAT)
    searchBtn.setText("Search")
    closeBtn = Button(compositeBottomButtons, SWT.FLAT)
    closeBtn.setText("Close")
    btndata = GridData(GridData.HORIZONTAL_ALIGN_END)
    btndata.widthHint = 50
    closeBtn.setLayoutData(btndata)
    btndata = GridData(GridData.HORIZONTAL_ALIGN_END)
    btndata.widthHint = 50
    searchBtn.setLayoutData(btndata)
    
    #---- Install a listener shared by all buttons
    class _ButtonsListener(Listener):
      def handleEvent(self, event):
        if (event.widget == closeBtn):
          # "Close" button handler
          closeBtn.getShell().close()
        elif (event.widget == searchBtn):
          # "Search" button handler
          wordtosearch = filterTxt.getText().strip()
          if (wordtosearch != ""):
            options = [regexpCheckBox.getSelection()]
            SearchResultsWindow(child, selectedMetaclasses, wordtosearch, options)
        elif (event.widget == addBtn):
          #  ">>" button handler
          indices = unselectedMetaclassesTable.getControl().getSelectionIndices()
          i = 0
          for indice in indices:
            mc = unselectedMetaclasses[indice-i]
            selectedMetaclasses.append(mc)
            unselectedMetaclasses.remove(mc)
            i = i+1
          selectedMetaclasses.sort(key=key_name)
          unselectedMetaclassesTable.refresh()
          selectedMetaclassTable.refresh()
        elif (event.widget == removeBtn):
          #  "<<" button handler
          indices = selectedMetaclassTable.getControl().getSelectionIndices()
          i = 0
          for indice in indices:
            mc = selectedMetaclasses[indice-i]
            unselectedMetaclasses.append(mc)
            selectedMetaclasses.remove(mc)
            i = i+1
          unselectedMetaclasses.sort(key=key_name)
          unselectedMetaclassesTable.refresh()
          selectedMetaclassTable.refresh()
    listener = _ButtonsListener()
    addBtn.addListener(SWT.Selection, listener)
    removeBtn.addListener(SWT.Selection, listener)
    closeBtn.addListener(SWT.Selection, listener)
    searchBtn.addListener(SWT.Selection, listener)
    
    #---- Install a table listener for both tables
    class _TableSelectionChangedListener(ISelectionChangedListener):
      def selectionChanged(self, e):
        selection = e.getSelection()
    unselectedMetaclassesTable.addSelectionChangedListener(_TableSelectionChangedListener())
    selectedMetaclassTable.addSelectionChangedListener(_TableSelectionChangedListener())


    

#
# The macro execution starts here
#
initmetaclasses()
searchwindow = SearchWindow()
