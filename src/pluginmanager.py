import os

PLUGINDIR = "plugins"

class Plugin(object):
  def getName(self):
    raise Exception("Not implemented")
  
  def getDescription(self):
    return ""
  
  def getAuthor(self):
    raise Exception("Not implemented")

class WizardPlugin(Plugin):
  TYPE = {"input":0, "output":1}
  
  def __init__(self):
    Plugin.__init__(self)
    
  def getType(self):
    return None
  
  def getWizard(self, parent):
    raise Exception("Not implemented.")
  

class PluginManager(object):
  def __init__(self):
    self.output = {}
    self.input = {}
    
  def loadPlugins(self):
    print "loading plugins"
    for dir in os.listdir(PLUGINDIR):
      path = PLUGINDIR + os.sep + dir
      if os.path.isdir(path) and os.path.isfile(path + os.sep + "__init__.py"):
        __import__(PLUGINDIR + "." + dir, fromlist=[PLUGINDIR]);
    
    for plugin in WizardPlugin.__subclasses__():
      p = plugin()
      try: 
        print "Found Plugin: %s (Type: %d)" %(p.getName(), p.getType())
        if p.getType() == WizardPlugin.TYPE["input"]:
          self.input[plugin] = p
          print "added %s" %(plugin)
        elif p.getType() == WizardPlugin.TYPE["output"]:
          self.output[plugin] = p 
          print "added %s" %(plugin)
        else:
          print "Unknown PluginType: %s by %s (%s)" %(p.getName, p.getAuthor, plugin)
      except:
        print "Invalid Plugin: %s" %(plugin)
  
  def getOutputPlugins(self):
    return self.output
  
  def getInputPlugins(self):
    return self.input

if __name__ == '__main__':
  print "please test with an extra file."