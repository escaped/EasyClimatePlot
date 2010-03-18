# -*- coding: utf-8 -*-

'''Submodules should use panels to interact with the user.'''

import wx

from windowpool import WindowPool

class Hook (wx.Panel):
  '''Hook is an abstract base class implementing basic functions used by the
  workflow panel. NOTE: Every panel which is added to a workflow should inherit this
  class!'''

  def deactivate (self):
    '''things to do before switching this panel. Returns true if switching is forbidden
    (e.g. because of missing values).'''
    return True

  def activate (self):
    '''Things to do after switching to this panel. Returns false if something went wrong
    (for example if the last panel missed some values).'''
    return True

class Workflow (wx.Panel):
  def createSubPanels (self):
    raise NotImplementedError, "Please implement in deriving classes"

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
    self.switchSubPanelByID (self.currentNumber)

    self.SetSizerAndFit (self.mainSizer)

  def switchSubPanel (self, newPanel):
    if self.currentPanel:
      # try to deactivate the panel. if something goes wrong, do nothing.
      if self.currentPanel.deactivate ():
        self.mainSizer.Detach (self.currentPanel)
        self.currentPanel.Show (False)
      else: return

    # try to activate the panel. if something goes wrong, return to the last panel
    if newPanel.activate ():
      self.currentPanel = newPanel

    self.mainSizer.Add (self.currentPanel, pos = (0,0))
    self.currentPanel.Show (True)
    self.mainSizer.Layout ()

    self.Layout ()

  def switchSubPanelByID (self, number):
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

    self.switchSubPanel (self.pool [number])

  def switchSubPanelByName  (self, name):
    self.switchSubPanel (self.pool [name])
    self.currentNumber = self.pool.getWindowIndex ()

  def getSubPanelByName (self, name):
    return self.subPanelsByName[name]

  #########
  # event handling
  #########
  def onBack (self, e):
    self.switchSubPanelByID (self.currentNumber - 1)
  
  def onForward (self, e):
    self.switchSubPanelByID (self.currentNumber + 1)
