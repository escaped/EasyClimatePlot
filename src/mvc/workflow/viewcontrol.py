# -*- coding: utf-8 -*-
'''Submodules should use panels to interact with the user.'''

import wx
from mvc.windowpool import WindowPool
import hook

class ViewControl (wx.Panel):
  def createSubPanels (self):
    raise NotImplementedError, "Please implement in deriving classes"

  #########
  # constructor
  #########
  def __init__(self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]
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
    self.SetAutoLayout (True)

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
    else:
      # TODO better use a debug facility
      print "activate () of newPanel didn't return True"

    self.mainSizer.Insert (0, self.currentPanel, -1, wx.EXPAND, 0)
    self.mainSizer.Fit (self)
    self.currentPanel.Show (True)
    self.parent.Layout ()
    
    return True

  def switchSubPanelByName  (self, name):
    bool = self.switchSubPanel (self.pool [name])
    self.currentNumber = self.pool.getWindowIndex (name)
    return bool

  def getSubPanelByName (self, name):
    return self.subPanelsByName[name]

  def switchSubPanelByID (self, number):
    return self.switchSubPanel (self.pool [number])
