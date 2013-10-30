#
# CoExplorer
#
# Model/Metamodel co-explorer for Modelio.
#
# Author: jmfavre
#
# Compatibility: Modelio 2.x, Modelio 3.x
#
# Purpose:
#   This macro allows to explore the set of selected elements by navigating at the
#   same time in the model and the metamodel.
#   The set of all (non empty) features associated with each element is displayed,
#   allowing the navigation to continue. Note that the tree is virtually infinite and
#   that there is currently no indication that an element has been already visited.
#   The methods followed are those of the form getXXX(), isXXX() and toString() with no
#   parameters. A few "virtual" methods which do not have direct correspondance in modelio
#   are also added, in particular to enable navigation to and within diagrams.
#   The co-explorer allows to navigate at the same time the model
#   and discover a slice of the metamodel, the slice that is useful for the model at hand.
#   The explorer not only allow to explore ModelElement, but also other Java entities,
#   and interestingly enough the DiagramGraphic elements. In modelio graphical entities
#   are not modeled, but the exploration is made possible.
#
# Installation:
#   This script should be installed as a workspace macro with the following options:
#      - "Applicable on" : No Selection. The macro is application on any kind of element
#      - "Show in contextual menu" : YES
#      - "Show in toolbar" : YES
#   This script is based on the content of the "lib" directory which should be copied by
#   hand to the macros directory of the workspace. That is, in the directory where this file
#   CoExplorer.py is installed.
#   Ultimately we should have
#      CoExplorer.py
#      lib/
#          introspection.py
#          misc.py
#          res/
#               assoc-1.gif
#               assoc-n.gif
#               ... all other images ...

DEVELOPEMENT_MODE = True

#---- add the "lib" directory to the path
try:
  from org.modelio.api.modelio import Modelio
  orgVersion = True
except:
  orgVersion = False
import os
import sys 
WORKSPACE_PATH=Modelio.getInstance().getContext().getWorkspacePath()
if orgVersion:
  SCRIPT_LIBRARY_PATH=os.path.join(WORKSPACE_PATH.toString(),'macros','lib')
else:
  SCRIPT_LIBRARY_PATH=os.path.join(WORKSPACE_PATH.toString(),'.config','macros','lib')
sys.path.append(SCRIPT_LIBRARY_PATH)


#----- imports (reload in development mode)
if DEVELOPEMENT_MODE:
  try: del sys.modules["misc"] ; del misc
  except: pass
from misc import *

if DEVELOPEMENT_MODE:
  try: del sys.modules["introspection"] ; del introspection
  except: pass
from introspection import *


#----- Do the job
coexplorer = explore(selectedElements)
