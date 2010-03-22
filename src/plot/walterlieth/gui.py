# -*- coding: utf-8 -*-
from main.workflow.hook import Hook
from main.workflow.wizard import Wizard

import wx
import wxcustom.datalistbox as dlb
import cachemanager

COLUMNS = ["ID"]

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
  cache = cachemanager.CacheManager.getInstance()
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.static = wx.StaticBox (self, -1, "Results")

    self.sizer = wx.BoxSizer ()
    self.sizer.Add (self.static)

    self.lctChooseStation = dlb.DataListBox (self, COLUMNS)
    self.sizer.Add(self.lctChooseStation, 3, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)

    # currently only lists every item from the cachemanager index and module noaa
    noaa_results = self.cache.index["noaa"]

    self.SetSizer (self.sizer)
    self.Layout ()

class PlotView (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.static = wx.StaticBox (self, -1, "Plot")
