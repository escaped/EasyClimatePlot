from pluginmanager import WizardPlugin

class NOAA(WizardPlugin):
  def getName(self):
    return "NOAA"
  
  def getDescription(self):
    return ""
  
  def getAuthor(self):
    return "Magnus Mueller, Alexander Frenzel"
    
  def getType(self):
    return WizardPlugin.TYPE["input"]
  
  def getWizard(self):
    raise Exception("Not implemented.")