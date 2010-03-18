# -*- coding: utf-8 -*-

'''Submodules should use panels to interact with the user.'''

import wx

class NOAA_Panel (wx.Panel):
  '''The NOAA panel can dynamically switch it's subpanels.'''
  def __init__ (self, parent):
    self.parent = parent
    wx.Panel.__init__ (self, parent)

    # initialize panels
    self.pan1 = Panel1 (self)
    self.pan1.Show (True)
    self.pan2 = Panel2 (self)
    self.pan2.Show (False)

    self.current_panel = self.pan1
    
    # grid
    self.grid = wx.GridBagSizer (hgap = 2, vgap = 1)
    self.button = wx.Button (self, label = "please click me...", pos=(20,20))
    self.main = Panel1 (self)
    self.grid.Add (self.button, pos = (0,0))
    self.grid.Add (self.current_panel, pos = (0,1))
    self.Bind (wx.EVT_BUTTON, self.onClick, self.button)

    self.SetSizerAndFit (self.grid)


  def switch (self, panel):
    # switch current_panel to panel
    self.grid.Remove (self.current_panel)
    self.current_panel.Show (False)
    self.grid.Add (panel, pos = (0,1))
    self.current_panel = panel
    self.current_panel.Show (True)

  def onClick (self, e):
    self.switch (self.pan2)
    self.grid.Remove (self.button)
    self.button.Destroy ()
    self.grid.Layout ()


class Panel1 (wx.Panel):
  def __init__ (self, parent):
    wx.Panel.__init__ (self, parent)
    self.lbltext = wx.StaticText(self, label="Panel 1")
class Panel2 (wx.Panel):
  def __init__ (self, parent):
    wx.Panel.__init__ (self, parent)
    self.lbltext = wx.StaticText(self, label="Panel 2")


class Workflow (wx.Panel):
  def createSubPanels (self):
    #self.subPanels.append (Panel1 (self))
    #self.subPanels.append (Panel1 (self))
    #self.subPanels.append (Panel1 (self))
    #self.subPanels.append (Panel1 (self))
    raise NotImplementedError, "Please implement in deriving classes"

  def __init__ (self, parent):
    wx.Panel.__init__ (self, parent)
    self.currentPanel  = None
    self.currentNumber = 0
    self.subPanels = []

  def switchSubPanel (self, number):
    if number < 0 or number > len (self.subPanels):
      # throw a bad exception
      # TODO hier sollte eine sinnvolle Fehlermeldung erscheinen
      raise IndexError ("Hier sollte eine sinnvolle Fehlermeldung stehen")
    self.currentNumber = number

    if number - 1 < 0:
      self.back.Disable ()
    else:
      self.back.Enable ()

    if number + 1 > len (self.subPanels):
      self.forward.Disable ()
    else:
      self.forward.Enable ()

    if self.currentPanel:
      self.mainSizer.Detach (self.currentPanel)
      self.currentPanel.Show (False)
    self.currentPanel = self.subPanels[number]
    self.mainSizer.Add (self.currentPanel, pos = (0,0))
    self.mainSizer.Layout ()


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

    # switch to first subpanel
    self.switchSubPanel (self.currentNumber)

    self.SetSizerAndFit (self.mainSizer)

  def onBack (self, e):
    self.switchSubPanel (self.currentNumber - 1)
  
  def onForward (self, e):
    self.switchSubPanel (self.currentNumber + 1)

