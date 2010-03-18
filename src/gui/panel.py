# -*- coding: utf-8 -*-

'''Submodules should use panels to interact with the user.'''

import wx

class Panel1 (wx.Panel):
  def __init__(self, parent, text):
    wx.Panel.__init__ (self, parent)
    self.lbltext = wx.StaticText(self, label=str (text))

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

class Workflow (wx.Panel):
  def createSubPanels (self):
    self.pool.addWindow ("1", Panel1 (self, 1))
    self.pool.addWindow ("2", Panel1 (self, 2))
    self.pool.addWindow ("3", Panel1 (self, 3))
    #raise NotImplementedError, "Please implement in deriving classes"

  #########
  # constructor
  #########
  def __init__ (self, parent):
    wx.Panel.__init__ (self, parent)
    self.currentPanel  = None
    self.currentNumber = 0
    self.pool = WindowPool ()

  def Create (self):
    # sizers
    self.mainSizer = wx.GridBagSizer (hgap = 1, vgap = 2)
    self.buttonSizer = wx.GridBagSizer (hgap = 2, vgap = 1)

    self.mainSizer.Add (self.buttonSizer, pos = (1,0))

    # back and forward buttons
    self.back = wx.Button (self, label = "Zurück")
    self.forward = wx.Button (self, label = "Weiter")

    self.Bind (wx.EVT_BUTTON, self.onBack, self.back)
    self.Bind (wx.EVT_BUTTON, self.onForward, self.forward)

    # add buttons to buttonSizer
    self.buttonSizer.Add (self.back, pos = (0,0))
    self.buttonSizer.Add (self.forward, pos = (0,1))

    # create the subpanels
    self.createSubPanels ()

    # make sure, that none of the subpanels is shown
    for i in self.pool.getListOfWindows ():
      i.Show (False)

    # switch to first subpanel
    self.switchSubPanel (self.currentNumber)

    self.SetSizerAndFit (self.mainSizer)

  def switchSubPanel (self, number):
    if number < self.pool.lower_bound or number > self.pool.upper_bound:
      # TODO hier sollte eine sinnvolle Fehlermeldung erscheinen
      raise IndexError ("Hier sollte eine sinnvolle Fehlermeldung stehen")
    self.currentNumber = number

    if number - 1 < self.pool.lower_bound:
      self.back.Disable ()
    else:
      self.back.Enable ()

    if number + 2 > self.pool.upper_bound:
      self.forward.Disable ()
    else:
      self.forward.Enable ()

    if self.currentPanel:
      self.mainSizer.Detach (self.currentPanel)
      self.currentPanel.Show (False)

    self.currentPanel = self.pool [number]

    self.mainSizer.Add (self.currentPanel, pos = (0,0))
    self.currentPanel.Show (True)
    self.mainSizer.Layout ()

    self.Layout ()

  def getSubPanelByName (self, name):
    return self.subPanelsByName[name]

  #########
  # event handling
  #########
  def onBack (self, e):
    self.switchSubPanel (self.currentNumber - 1)
  
  def onForward (self, e):
    self.switchSubPanel (self.currentNumber + 1)

