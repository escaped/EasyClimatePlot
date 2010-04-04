from pluginmanager import WizardPlugin
import gui

class NOAA(WizardPlugin):
  def getName(self):
    return "Data Viewer"

  def getVersion(self):
    return "0.1"
  
  def getDescription(self):
    return "Load data from cache and show it as a table"

  def getAuthor(self):
    return "Magnus Mueller"
 
  def getType(self):
    return WizardPlugin.T_OUTPUT

  def getWizard(self, parent):
    raise NotImplementedError, "Not yet implemented"
    return gui.NOAA_Export_Wizard(parent)
