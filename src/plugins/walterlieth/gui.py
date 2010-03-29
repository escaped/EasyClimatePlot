# -*- coding: utf-8 -*-
from mvc.workflow.hook import Hook
from mvc.workflow.wizard import Wizard

import wx
from wxcustom.panel import Panel
import wxcustom.datalistbox as dlb

from control import SearchResultsControl, PlotControl

COLUMNS = ["usaf", "range", "name"]

# TODO enable other search panels (e.g. sth for NASA)
from plugins.noaa.gui import SearchPanel

class WalterLiethWizard (Hook, Wizard):
  def createSubPanels (self):
    self.searchresultscontrol = SearchResultsControl (self.pool.addWindow ("Results", SearchResultsView (self)))
    self.plotcontrol = PlotControl (self.pool.addWindow ("Plot", PlotView (self)))

  def __init__ (self, *args, **kwargs):
    Wizard.__init__ (self, *args, **kwargs)

class SearchResultsView (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.static = wx.StaticBox (self, -1, "Plot")
    self.sizer = wx.StaticBoxSizer (self.static)
    self.parent = args[0]

    self.lctChooseData = dlb.DataListBox (self, COLUMNS)

    # clear button
    self.clearButton = wx.Button (self, -1, u"Suchergebnisse löschen")
    self.Bind (wx.EVT_BUTTON, self["Clear"], self.clearButton)

    sizer_main = wx.StaticBoxSizer(self.static, wx.VERTICAL)
    sizer_main.Add(self.lctChooseData, 3, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
    sizer_main.Add (self.clearButton, 0)

    self.SetSizer(sizer_main)
    self.Layout()

    self.searchComplete = False
  
  def addData (self, items):
    self.lctChooseData.AddManyData (items, COLUMNS)

class PlotView (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]

    self.static = wx.StaticBox (self, -1, "Plot")
    self.sizer = wx.StaticBoxSizer (self.static)

    # button - plot
    self.plotButton = wx.Button (self, -1, label="Plot")

    self.sizer.Add (self.plotButton, -1)

    self.SetSizer (self.sizer)
    self.parent.Layout ()

    # events
    self.Bind (wx.EVT_BUTTON, self["Plot"], self.plotButton)

  def getSelected (self):
    return self.parent.pool["Results"].lctChooseData.getSelected ()

