'''Submodules should use panels to interact with the user.'''

import time

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
    self.grid.Detach (self.current_panel)
    self.current_panel.Show (False)
    self.grid.Add (panel, pos = (0,1))
    self.current_panel = panel
    self.current_panel.Show (True)
    self.grid.Layout ()

  def onClick (self, e):
    self.switch (self.pan2)
    self.parent.Layout ()


class Panel1 (wx.Panel):
  def __init__ (self, parent):
    wx.Panel.__init__ (self, parent)
    self.lbltext = wx.StaticText(self, label="Panel 1")
class Panel2 (wx.Panel):
  def __init__ (self, parent):
    wx.Panel.__init__ (self, parent)
    self.lbltext = wx.StaticText(self, label="Panel 2")

class StartDownloadPanel (wx.Panel):
  '''Let the user choose wether to download from noaa or from nasa.'''
  def __init__ (self, parent):
    wx.Panel.__init__ (self, parent)

    # sizer
    grid = wx.GridBagSizer (hgap = 1, vgap = 2)

    # buttons
    noaaButton = wx.Button (self, wx.ID_ANY, label = "NOAA")
    nasaButton = wx.Button (self, wx.ID_ANY, label = "NASA")

    grid.Add (noaaButton, pos = (0,0))
    grid.Add (nasaButton, pos = (1,0))

    self.SetSizerAndFit (grid)

