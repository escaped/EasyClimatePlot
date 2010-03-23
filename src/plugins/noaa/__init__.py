from pluginmanager import WizardPlugin
import gui

class NOAA(WizardPlugin):
  def getName(self):
    return "NOAA"

  def getVersion(self):
    return "0.6"
  
  def getDescription(self):
    return "Search and Download data from NOAA."

  def getAuthor(self):
    return "Magnus Mueller, Alexander Frenzel"
 
  def getType(self):
    return WizardPlugin.TYPE["input"]

  def getWizard(self, parent):
    return gui.NOAA_Wizard(parent)