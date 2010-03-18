
# TODO should this be some kind of singleton?
class WindowPool:
  def __init__(self):
    self.windows = {}
    self.indices = []
    self.count   = 0
    self.lower_bound = 0
    self.upper_bound = 0

  def addWindow (self, name, window):
    self.windows[name] = window
    self.indices.append (name)
    self.count += 1
    self.upper_bound += 1

  def getWindowByName (self, name):
    # TODO exceptions needed?
    return self.windows[name]

  def getWindowByID (self, id):
    # TODO exceptions needed?
    return self.windows[self.indices[id]]

  def getWindowIndex (self, window):
    return self.indices.index (window)

  def getListOfWindows (self):
    '''arbitrarily ordered list of the values from self.windows'''
    return self.windows.values ()

  def __getitem__ (self, index):
    '''Return the window to window belonging to index. If index is an integer, it is
    handled as the normal index. If it is a string, we assume that it refers to the name
    of the window.'''
    try:
      return self.windows[self.indices[index]]
    except TypeError:
      return self.windows[index]

