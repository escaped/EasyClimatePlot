class Plugin (object):
  name = ""
  desc = ""
  data = {}

  def downloadData (self):
    raise NotImplemented
  
  def getData (self):
    raise NotImplemented

  def getUserInput (self):
    raise NotImplemented
