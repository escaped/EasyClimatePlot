'''Submodules should use panels to interact with the user.'''

import wx

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

