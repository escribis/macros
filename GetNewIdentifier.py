#
# GetNewIdentifier
#  This script generates a new unique identifier for module development.
#
# Author:  tma, jmfavre
#
# Applicable on: All elements
#
# Version history:
# 1.1   27 October 2013 - update for Modelio 3.0
# 1.0   16th April 2012 - creation

# check if this is modelio 3 because the API has changed
try:
  from org.modelio.api.modelio import Modelio
  orgVersion = True
except:
  from com.modeliosoft.modelio.api.modelio import Modelio
  orgVersion = False
  
newElement = modelingSession.getModel().createClass()
if orgVersion:
  print newElement.getUuid() 
else:
  print newElement.getIdentifier()
  
newElement.delete()