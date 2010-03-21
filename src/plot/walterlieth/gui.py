# -*- coding: utf-8 -*-
from main.panel import Hook, Wizard
import wx

class WalterLiethWizard (Hook, Wizard):
  def createSubPanels (self):
    self.pool.addWindow ("Search", SearchView (self))
    self.pool.addWindow ("Results", SearchResultsView (self))
    self.pool.addWindow ("Plot", PlotView (self))

  def __init__ (self, *args, **kwargs):
    Wizard.__init__ (self, *args, **kwargs)

class SearchView (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.static = wx.StaticBox (self, -1, "Search")

class SearchResultsView (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.static = wx.StaticBox (self, -1, "Results")

class PlotView (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.static = wx.StaticBox (self, -1, "Plot")
