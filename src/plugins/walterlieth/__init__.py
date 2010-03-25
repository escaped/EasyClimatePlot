from pluginmanager import WizardPlugin
import gui

class WalterLieth(WizardPlugin):
  def getName(self):
    return "WalterLieth"

  def getVersion(self):
    return "0.2"
  
  def getDescription(self):
    return "Create Walter Lieth diagrams."

  def getAuthor(self):
    return "Magnus Mueller"
 
  def getType(self):
    return WizardPlugin.T_OUTPUT

  def getWizard(self, parent):
    return gui.WalterLiethWizard(parent)