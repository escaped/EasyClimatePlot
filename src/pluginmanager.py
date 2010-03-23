import os

PLUGINDIR = "plugins"

class Plugin(object):
  pass

class PluginManager(object):
  def __init__(self):
    self.output = []
    self.input = []
    
  def loadPlugins(self):
    print "loading plugins"
    for dir in os.listdir(PLUGINDIR):
      path = PLUGINDIR + os.sep + dir
      if os.path.isdir(path) and os.path.isfile(path + os.sep + "__init__.py"):
        print "found %s" %(dir) 
        __import__(PLUGINDIR + "." + dir, fromlist=[PLUGINDIR]);
        print Plugin.__subclasses__()
 
''' 
  ipython:
  In [1]: import pluginmanager
  In [2]: m = pluginmanager.PluginManager ()
  In [3]: m.loadPlugins ()
    loading plugins
    found test1
    [<class 'test1.Test1'>]
    
  python pluginmanager.py:
    loading plugins
    found test1
    []
    
  ahhh... warum is die List leer -.-
'''        

        
if __name__ == '__main__':
  m = PluginManager()
  m.loadPlugins()
        