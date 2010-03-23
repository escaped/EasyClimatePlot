# -*- coding: utf-8 -*-

# TODO should use some kind of a logging facility
class WindowPool (object):
  '''Objects of this class offer a pool, which stores objects with a given key.'''
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

    return window

  def getWindowByName (self, name):
    # TODO exceptions needed?
    try:
      return self.windows[name]
    except KeyError:
      print "View %s does not exist" %name
      raise

  def getWindowByID (self, id):
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
      try:
        return self.windows[index]
      except KeyError:
        print "View %s does not exist" %index
        raise


