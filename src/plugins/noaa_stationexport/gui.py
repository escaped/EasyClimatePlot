# -*- coding: utf-8 -*-
'''GUI workflow for NOAA download'''

import wx
import wxcustom.datalistbox as dlb

from mvc.workflow.wizard import Wizard
from mvc.workflow.hook import Hook

from main.validators import IntegerValidator, NumberValidator

import plugins.noaa.dao as dao
import control

from wxcustom.panel import Panel

from config import CURRENTYEAR

# global variables
COLUMNS = ["Station Name", "Country", "USAF ID", "Lon", "Lat"]
COMBOBOX_LIMIT = 15

from plugins.noaa.gui import SearchPanel, SearchResults
  
class ExportStations (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]

    self.sizer = wx.BoxSizer (wx.VERTICAL)

    self.noaa = dao.NOAA ()

    self.exportButton = wx.Button (self, -1, "Stationen exportieren..")
    self.sizer.Add (self.exportButton)

    self.SetSizer (self.sizer)
    self.sizer.Fit (self)
    self.Bind (wx.EVT_BUTTON, self["Export"], self.exportButton)
    self.Layout()

class NOAA_Export_Wizard (Hook, Wizard):
  def createSubPanels (self):
    self.pool.addWindow ("Search", SearchPanel (self))
    self.pool.addWindow ("SearchResults", SearchResults (self))
    self.pool.addWindow ("Download", ExportStations (self))
    
    # TODO das gehört nicht hierher
    self.sc  = control.SearchControl (self.pool["Search"])
    self.src = control.SearchResultsControl (self.pool["SearchResults"])
    self.dc  = control.ExportControl (self.pool["Download"])
    
