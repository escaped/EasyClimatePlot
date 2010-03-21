# -*- coding: utf-8 -*-
'''Submodules should use panels to interact with the user.'''

import wx
from main.windowpool import WindowPool
import hook

class ViewControl (wx.Panel):
  def createSubPanels (self):
    raise NotImplementedError, "Please implement in deriving classes"

  #########
  # constructor
  #########
  def __init__(self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.currentPanel  = None
    self.currentNumber = 0
    self.pool = WindowPool ()

    # sizers
    self.mainSizer = wx.BoxSizer (wx.VERTICAL)

    # create the subpanels
    self.createSubPanels ()

    for i in self.pool.getListOfWindows ():
      i.Show (False)

    self.SetSizer (self.mainSizer)

  def initSubPanel (self):
    '''Switch to first subpanel. Call this method as soon as everything is initialized!'''
    # switch to first subpanel
    self.switchSubPanelByID (self.currentNumber)

  def switchSubPanel (self, newPanel):
    if self.currentPanel:
      # try to deactivate the panel. if something goes wrong, do nothing.
      if self.currentPanel.deactivate ():
        self.mainSizer.Detach (self.currentPanel)
        self.currentPanel.Show (False)
      else: 
        return False

    # try to activate the panel. if something goes wrong, return to the last panel
    if newPanel.activate ():
      self.currentPanel = newPanel

    self.mainSizer.Insert (0, self.currentPanel, wx.EXPAND)
    self.mainSizer.Layout ()
    # TODO resize funktioniert nicht richtig
    self.mainSizer.Fit (self)
    self.currentPanel.Show (True)
    
    return True

  def switchSubPanelByName  (self, name):
    bool = self.switchSubPanel (self.pool [name])
    self.currentNumber = self.pool.getWindowIndex (name)
    return bool

  def getSubPanelByName (self, name):
    return self.subPanelsByName[name]

  def switchSubPanelByID (self, number):
    return self.switchSubPanel (self.pool [number])
