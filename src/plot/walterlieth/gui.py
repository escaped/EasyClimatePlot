# -*- coding: utf-8 -*-
from mvc.workflow.hook import Hook
from mvc.workflow.wizard import Wizard

import wx
from wxcustom.panel import Panel
import wxcustom.datalistbox as dlb
import cachemanager

from control import SearchControl, SearchResultsControl, PlotControl

COLUMNS = ["ID"]

class WalterLiethWizard (Hook, Wizard):
  def createSubPanels (self):
    self.searchcontrol = SearchControl (self.pool.addWindow ("Search", SearchView (self)))
    self.searchresultscontrol = SearchResultsControl (self.pool.addWindow ("Results", SearchResultsView (self)))
    self.plotcontrol = PlotControl (self.pool.addWindow ("Plot", PlotView (self)))

  def __init__ (self, *args, **kwargs):
    Wizard.__init__ (self, *args, **kwargs)

class SearchView (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.static = wx.StaticBox (self, -1, "Search")

class SearchResultsView (Panel):
  cache = cachemanager.CacheManager.getInstance()

  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]

    self.noaa_results = self.cache.index["noaa"]
    self.static_box = wx.StaticBox(self, -1, u"Daten wählen")
    self.sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)

    # datalistbox
    self.lctChooseData = dlb.DataListBox (self, COLUMNS)
    self.sizer.Add(self.lctChooseData, 3, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)

    # clear button
    self.clearButton = wx.Button (self, -1, u"Suchergebnisse löschen")
    self.Bind (wx.EVT_BUTTON, self["Clear"], self.clearButton)
    self.sizer.Add (self.clearButton, 0)

    self.SetSizer(self.sizer)
    self.sizer.Fit (self)
    self.Layout()

    self.searchComplete = False

class PlotView (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.static = wx.StaticBox (self, -1, "Plot")
