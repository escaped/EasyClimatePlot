from pluginmanager import WizardPlugin
import gui

class NOAA(WizardPlugin):
  def getName(self):
    return "NOAA Station Export"

  def getVersion(self):
    return "0.1"
  
  def getDescription(self):
    return "Export available stations from NOAA in a format suitable for batchgeocode.com"

  def getAuthor(self):
    return "Magnus Mueller"
 
  def getType(self):
    return WizardPlugin.T_OUTPUT

  def getWizard(self, parent):
    return gui.NOAA_Export_Wizard(parent)
