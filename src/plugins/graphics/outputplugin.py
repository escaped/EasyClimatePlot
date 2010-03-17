class OutputPlugin (object):
  dataObjects = {}
  def setDataObjects (self, dataObjects):
    self.dataObjects = dataObjects

  def getUserOptions (self):
    raise NotImplemented

  def process (self):
    raise NotImplemented

  def saveToPath (self, name):
    raise NotImplemented

