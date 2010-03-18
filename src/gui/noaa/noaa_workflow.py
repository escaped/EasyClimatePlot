'''GUI workflow for NOAA download'''

import wx
from gui.panel import Workflow

class Panel1 (wx.Panel):
  def __init__(self, parent, text):
    wx.Panel.__init__ (self, parent)
    self.lbltext = wx.StaticText(self, label=str (text))

class NOAA_Workflow (Workflow):
  def createSubPanels (self):
    self.pool.addWindow ("1", Panel1 (self, 1))
    self.pool.addWindow ("2", Panel1 (self, 2))
    self.pool.addWindow ("3", Panel1 (self, 3))
    
