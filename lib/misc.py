#
# misc
#
# Miscellaneous functions gathered here and waiting for some refactoring
# This allows incremental development. This is necessary to avoid multiple reload import
#
# Licence: GPL
# Author: jmfavre
#


#----- predicates -----------------------------------------------
def isEmpty(x):
  """ return True for empty strings, 0, empty lists, etc.
  """
  return not(x)
  
def notEmpty(x):
  """ return False for not empty things
  """
  return not isEmpty(x)
  
def isString(x):
  return isinstance(x,basestring)
  
def isNone(x):
  """ return True only for None value
  """
  return x is None

#----- String functions -----------------------------------------
  
def withCapital(s):
  if len(s)==0: return ""
  else: return s[0].capitalize()+s[1:]

#----- Collection function

def first(coll):
  """ get the first element of a list, of a tuple, etc. 
  """
  return coll[0]  
  
def second(coll):
   """ get the second element of a list, of a typle, etc.
   """
   return coll[1]
   
def rest(coll):
   """ tail of the collection, that is everything except the first element.
   """
   return coll[1:]
   
#----- List functions -------------------------------------------

from java.util import List as JavaList
from java.util import Collection as JavaCollection
def isList(x):
  # is it enough?
  return isinstance(x,list) \
         or isinstance(x,JavaCollection)
  
def excluding(list,elem):
  return [x for x in list if x != elem]

def flatten(colls):
  """ flatten a collection of collections
  """
  return [item for coll in colls for item in coll]  
  
def onlyOnce(coll):
  """ return a list where elements appear only once but in the
      same order as in the given list, that is in the order of
      the first occurence. The result is a list.
      onlyOnce[2,4,2,1,1] = {2,4,1]
  """
  result = []
  for e in coll:
    if not e in result:
      result=result+[e]
  return result
  
def _addItemToGroups(element,fun,groups):
  elementKey = apply(fun,[element])
  size = len(groups)
  if size==0:
    return [(elementKey,[element])]
  else:
    (firstGroupKey,groupElements)=groups[0]
    if elementKey == firstGroupKey:
      return [(elementKey,groupElements+[element])]+groups[1:]
    else:
      return [groups[0]]+_addItemToGroups(element,fun,groups[1:])
      
def _getGroups(fun,coll):
  # groupedBy(lambda x:x//10,[22,31,11,36,34]) = [(2, [22]), (3, [31, 36, 34]), (1, [11])]
  if len(coll)==0:
    return []
  else:
    r = _addItemToGroups(coll[-1],fun,groupedBy(fun,coll[:-1]),)
    return r
    
def groupedBy(fun,coll,style="nested"):
  groups = _getGroups(fun,coll)
  return groups if style is "nested" else flatten(map(second,groups))


# for sorting see https://wiki.python.org/moin/HowTo/Sorting/  
   
def reject(predicate,coll):
  result = []
  for e in coll:
    if not predicate(e):
      result = result + [e]
  return result
  
import operator
def forAll(predicate,coll):
  return reduce(operator.and_, map(predicate,coll), True)
  
def exists(predicate,coll):
  return reduce(operator.or_, map(predicate,coll), False)


#----- graphical user interface ---------------------------------------------------------

from org.eclipse.swt import SWT
from org.eclipse.swt.widgets import Shell,Display,Label,Button,Listener
from org.eclipse.swt.browser import Browser
from org.eclipse.swt.layout import GridData,GridLayout


import os    
from org.eclipse.swt.graphics import Color, Image
from org.eclipse.swt.widgets import Display

class ImageProvider(object):
  """ provide some images for given name (extension is added)
  """
  def __init__(self,resourcePath="",extension=".gif"):
    self.extension = extension
    if resourcePath != "":
      self.resourcePath = resourcePath
    else:
      self.resourcePath = os.path.join(os.path.dirname(__file__),'res')
    # imageMap contains a mapping   name -> image|None 
    # this mapping is built on demand
    self.imageMap = {}
  def getImageFromName(self,name):
    if name not in self.imageMap:
      try:
        image = Image(Display.getCurrent(),os.path.join(self.resourcePath,name+self.extension))
      except:
        image = None
      self.imageMap[name] = image
    return self.imageMap[name]




# see http://git.eclipse.org/c/platform/eclipse.platform.swt.git/tree/examples/org.eclipse.swt.snippets/src/org/eclipse/swt/snippets/Snippet128.java to improve this window with more feature
class HtmlWindow(object):
  def __init__(self, url=None, html=None,title="information",width=800,height=800,labeltext=""):      
    parent = Display.getDefault().getActiveShell()
    self.window = Shell(parent, SWT.CLOSE | SWT.RESIZE)
    # give minimum size, location and size
    self.window.setMinimumSize(width, height)
    parentBounds = parent.getBounds()
    self.window.setLocation( \
      (parentBounds.width-width)/2+parentBounds.x, \
      (parentBounds.height-height)/2+parentBounds.y )
    self.window.setSize(width, height)
    # layout
    gridLayout = GridLayout(1, 1)
    self.window.setLayout(gridLayout)
    self.window.setText(title)
    self._createLabel(labeltext)
    self._createBrowser(url=url,html=html)
    self._createOkButton()
    self._listenSelection()
    self.window.open()
  def _createLabel(self,labeltext):
    data = GridData(GridData.FILL_HORIZONTAL)
    data.verticalIndent = 5;
    self.label = Label(self.window, SWT.WRAP)
    self.label.setLayoutData(data)
    self.label.setText(labeltext)
    self.label.setLocation(10, 40)
  def _createBrowser(self,html=None,url=None):
    data = GridData(SWT.FILL,SWT.FILL,1,1)
    data.verticalIndent = 10;
    self.browser = Browser(self.window, SWT.BORDER)
    self.browser.setLayoutData(data)
    if url is not None:
      self.setURL(url)
    else:
      if html is not None:
        self.setText(html)
      else:
        pass
  def _createOkButton(self):    
    data = GridData(GridData.HORIZONTAL_ALIGN_END)
    data.widthHint = 50
    button = Button(self.window, SWT.FLAT)    
    button.setLayoutData(data)    
    button.setText("OK")        
    class MyListener(Listener):
       def handleEvent(self, event):        
        if (event.widget == button):
           button.getShell().close()
    button.addListener(SWT.Selection, MyListener())
    self.okButton = button
  def _listenSelection(self):
    thebrowser = self.browser
    from org.modelio.api.modelio import Modelio
    from org.modelio.api.app.navigation import INavigationListener
    class SelectionListener(INavigationListener):
      #def navigateTo(self):
      #  thebrowser.setText("selection is "+str(target.getName()))
      pass
    Modelio.getInstance().getNavigationService().addNavigationListener(SelectionListener())
  def setText(self,html):  
    self.browser.setText( \
      "<html><header></header><body>" + html + "</body></html>")
  def setURL(self,url):
    self.browser.setUrl(url)
  def setLabel(self,text):
    self.label.setText(text)
  

  
from org.eclipse.swt import *
from org.eclipse.swt.layout import FillLayout
#from org.eclipse.swt.graphics import *
from org.eclipse.swt.widgets import Tree,TreeItem



class TreeWindow(object):
  def __init__(self,rootDataObjects,getChildrenFun,isLeafFun,
                getImageFun=None,getTextFun=None,title="Explorer",
                getGrayedFun=None,getBackgroundFun=None,getForegroundFun=None,
                onSelectionFun=None
              ):
              
    def _addRootDataObjects():
      # add the roots to the tree
      for rootDataObject in rootDataObjects:
        node = TreeItem(self.tree, 0)
        _decorateTreeItem(node,rootDataObject)
        # add a dummy node if this is not a leaf
        if not isLeafFun(rootDataObject):
          TreeItem(node,0)   
    
    def _decorateTreeItem(node,dataObject):
      node.setData(dataObject)
      if getTextFun is not None:
        text = getTextFun(dataObject)
      else:
        text = unicode(dataObject)
      if text is not None:
        node.setText(text)
      if getImageFun is not None:
        image = getImageFun(dataObject)
        if image is not None:
          # print "not none"
          node.setImage(image)
      if getGrayedFun is not None:
        grayed = getGrayedFun(dataObject)
        if grayed is not None:
          node.setGrayed(grayed)
      if getBackgroundFun is not None:
        background = getBackgroundFun(dataObject)
        if background is not None:
          node.setBackground(background)
      if getForegroundFun is not None:
        foreground = getForegroundFun(dataObject)
        if foreground is not None:
          node.setForeground(foreground)

    class ThisTreeExpandListener(Listener):
      def handleEvent(self, event):         
        node = event.item
        # print "expanding node "+str(node.getData()),
        items = node.getItems()
        # print ": ",len(items),"children"
        # check if this subtree has already been expanded before
        # if so there is nothing to do, otherwise remove dummy nodes
        for item in items:
          # print "  object",item.getData(),type(item.getData()),
          if item.getData() is not None:
            # print "already visited. Stop"
            return
          else:
            # print "remove this node"
            item.dispose()
        # get the children and add them to the tree
        for childDataObject in getChildrenFun(node.getData()):
          item = TreeItem(node,0)
          _decorateTreeItem(item,childDataObject)
          if not isLeafFun(childDataObject):
            # create a dummy node 
            TreeItem(item, 0)
            
    class ThisTreeSelectionListener(Listener):
      def handleEvent(self, event):
        node = event.item
        # print "item selected",node,type(node)
        # print "details",event.detail
        if onSelectionFun is not None:
          onSelectionFun(node.getData())        
        
    parentShell = Display.getDefault().getActiveShell()
    self.window = Shell(parentShell, SWT.CLOSE | SWT.RESIZE)
    self.window.setText(title)
    self.window.setLayout(FillLayout())
    self.tree = Tree(self.window, SWT.BORDER)
    self.tree.addListener(SWT.Expand, ThisTreeExpandListener())
    self.tree.addListener(SWT.Selection,ThisTreeSelectionListener())
    _addRootDataObjects()
    size = self.tree.computeSize(300, SWT.DEFAULT)
    width = max (300, size.x)
    height = max (300, size.y)
    self.window.setSize (self.window.computeSize(width, height))
    self.window.open ()
    
        

#----- web  ---------------------------------------------------------


from encodings import iso8859_1
import urllib2
  
def getWebPage(url):
  """ read the content of the given url and throws an exception in case of error
  """
  return urllib2.urlopen(url).read()
  
  

  
print "module misc loaded from",__file__
