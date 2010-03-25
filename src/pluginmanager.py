from singletonmixin import Singleton
import config
import os

class Plugin(object):
  def getName(self):
    raise NotImplementedError, "Not implemented"
  
  def getVersion(self):
    return ""
  
  def getDescription(self):
    return ""
  
  def getAuthor(self):
    return ""
    
class WizardPlugin(Plugin):
  T_INPUT = 0
  T_OUTPUT = 1
  
  def __init__(self):
    Plugin.__init__(self)
    
  def getType(self):
    return None
  
  def getWizard(self, parent):
    raise NotImplementedError, "Not implemented."
  

class PluginManager(Singleton):
  def __init__(self):
    self.output = {}
    self.input = {}
    
    print "loading plugins"
    for dir in os.listdir(config.PLUGINDIR):
      path = config.PLUGINDIR + os.sep + dir
      if os.path.isdir(path) and os.path.isfile(path + os.sep + "__init__.py"):
        __import__(config.PLUGINDIR + "." + dir, fromlist=[config.PLUGINDIR]);
    
    for plugin in WizardPlugin.__subclasses__():
      p = plugin()
      try: 
        print "Found Plugin: %s (Type: %d)" %(p.getName(), p.getType())
        if p.getType() == WizardPlugin.T_INPUT:
          self.input[p.getName()] = p
          print "added %s" %(plugin)
        elif p.getType() == WizardPlugin.T_OUTPUT:
          self.output[p.getName()] = p 
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
