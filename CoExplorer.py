# CoExplorer
#
# Launch a model-metamodel co-explorer on the selected elements
#
# Author jmfavre
#
# Requires misc, introspection
#

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
  try: 
    del sys.modules["misc"]
    del misc
  except:
    pass
from misc import *

if DEVELOPEMENT_MODE:
  try: 
    del sys.modules["introspection"]
    del introspection
  except:
    pass
from introspection import *


#----- Do the job
coexplorer = elementTree(selectedElements)
