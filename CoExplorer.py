#
# CoExplorer
#
# Model/Metamodel co-explorer for Modelio.
#
# Author: jmfavre
#
# Compatibility: Modelio 2.x, Modelio 3.x
#
# Target audience:
#   This script mainly dedicated to developers who need to understand modelio Metamodel,
#   for instance to develop scripts or modules. It allows the co-exploration of a model
#   and the corresponding metamodel.
#
# Description:
#   This macro allows to explore the set of selected elements by navigating at the
#   same time in the model and the metamodel. While Modelio' model explorer and property
#   sheets presents a "user oriented" view of the model, the CoExplorer will present
#   a view strictly in line with the actual metamodel. 
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
#   This script should be installed as a workspace macro using standard modelio procedure
#   to add macros. The options to use are the following options:
#      - "Applicable on" : No Selection. The macro is application on any kind of element
#      - "Show in contextual menu" : YES
#      - "Show in toolbar" : YES
#   This script is based on the content of the "lib" directory which must be copied manually
#   in the same directory as this very file. That is, in the directory where this file
#   CoExplorer.py will be installed by modelio through the standard macro installation procedure.
#   Ultimately we should have the following structure 
#          CoExplorer.py             <--- this very file
#             lib/
#                 introspection.py
#                 misc.py
#                 ...                <--- possibly other jython modules
#                 res/
#                     assoc-1.gif
#                     assoc-n.gif
#                     ...            <--- other resources.
#
# History
#   Version 1.0 - October 31, 2013
#      - first public realease

DEVELOPEMENT_MODE = True

#---- add the "lib" directory to the path
# The code below compute this path and put it in the variable SCRIPT_LIBRARY_DIRECTORY. 
# Feel free to change it if necessary. Currently the "lib" directory is search within
# the directory of this very file, but if you may want to change its location you can
# uncomment the line defining SCRIPT_LIBRARY_DIRECTORY with an absolute path
try:
  from org.modelio.api.modelio import Modelio
  orgVersion = True
except:
  orgVersion = False
import os
import sys 
WORKSPACE_DIRECTORY=Modelio.getInstance().getContext().getWorkspacePath().toString()
if orgVersion:
  MACROS_DIRECTORY=os.path.join(WORKSPACE_DIRECTORY,'macros')
else:
  MACROS_DIRECTORY=os.path.join(WORKSPACE_DIRECTORY,'.config','macros')
SCRIPT_LIBRARY_DIRECTORY=os.path.join(MACROS_DIRECTORY,'lib')
# Uncomment this line and adjust it if you want to put the "lib" directory somewhere else
# SCRIPT_LIBRARY_DIRECTORY = "C:\\MODELIO3-WORKSPACE\\macros\\lib"
print SCRIPT_LIBRARY_DIRECTORY
sys.path.append(SCRIPT_LIBRARY_DIRECTORY)
print sys.path



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
