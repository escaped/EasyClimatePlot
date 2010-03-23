from pluginmanager import WizardPlugin
import gui

class NOAA(WizardPlugin):
  def getName(self):
    return "NOAA"

  def getDescription(self):
    return ""

  def getAuthor(self):
    return "Magnus Mueller, Alexander Frenzel"
 
  def getType(self):
    return WizardPlugin.TYPE["input"]

  def getWizard(self, parent):
    return gui.NOAA_Wizard(parent)