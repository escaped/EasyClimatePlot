# -*- coding: utf-8 -*-
'''GUI workflow for NOAA download'''

import wx
import wxcustom.datalistbox as dlb

from mvc.workflow.wizard import Wizard
from mvc.workflow.hook import Hook

from main.validators import IntegerValidator, NumberValidator

import functional
import functools as ft

import dao
import control

from wxcustom.panel import Panel

from config import CURRENTYEAR

# global variables
COLUMNS = ["Station Name", "Country", "USAF ID", "Lon", "Lat"]
COMBOBOX_LIMIT = 15

class SearchPanel (Panel):
  def __init__(self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)

    # TODO NOAA objekt sollte global sein. das kostet sonst einfach zuviel zeit.
    self.noaa = dao.NOAA ()

    # StationNumber
    self.stbSearchBox = wx.StaticBox(self, -1, "Suche")
    self.lblStationsnummer = wx.StaticText(self, -1, "Stationsnummer:")    
    self.txtStationNumber = wx.TextCtrl(self, -1, "", validator = IntegerValidator())
    
    self.selectIDType = wx.RadioBox(self, -1, "USAF", choices=["USAF", "WBAN"], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
    self.lblRegion = wx.StaticText(self, -1, "Region")
    # TODO die sortierung stimmt noch nicht.
    self.lsbRegion = wx.ComboBox(self, -1, choices=[""], 
        style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)

    # fill combobox with countries available at NOAA
    for item in self.noaa.getCountryList ():
      # we associate each item with the given country code
      self.lsbRegion.Append (' '.join (item)[:COMBOBOX_LIMIT], item[0])

    self.lblLatLon1 = wx.StaticText(self, -1, "Lat/Lon")
    self.txtLat1 = wx.TextCtrl(self, -1, "", validator = NumberValidator((-90,90)))
    self.txtLon1 = wx.TextCtrl(self, -1, "", validator = NumberValidator((-180,180)))
    self.lblLatLon2 = wx.StaticText(self, -1, "Lat/Lon")
    self.txtLat2 = wx.TextCtrl(self, -1, "", validator = NumberValidator((-90,90)))
    self.txtLon2 = wx.TextCtrl(self, -1, "", validator = NumberValidator((-180,180)))

    # sizer for StationNumber
    stationNrSizer = wx.BoxSizer(wx.HORIZONTAL)
    stationNrSizer.Add(self.lblStationsnummer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    stationNrSizer.Add(self.txtStationNumber, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    stationNrSizer.Add(self.selectIDType, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    
    # sizer for Region
    regionSizer = wx.BoxSizer(wx.HORIZONTAL)
    regionSizer.Add(self.lblRegion, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 8)
    regionSizer.Add(self.lsbRegion, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
    
    # sizer for coord
    coordSizer = wx.BoxSizer(wx.HORIZONTAL)
    coordSizer.Add(self.lblLatLon1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    coordSizer.Add(self.txtLat1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    coordSizer.Add(self.txtLon1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    coordSizer.Add(self.lblLatLon2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    coordSizer.Add(self.txtLat2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    coordSizer.Add(self.txtLon2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)

    # combine all
    mainSizer = wx.StaticBoxSizer(self.stbSearchBox, wx.VERTICAL)
    mainSizer.Add(stationNrSizer, 0, wx.EXPAND, 0)
    mainSizer.Add(regionSizer, 0, wx.EXPAND, 0)
    mainSizer.Add(coordSizer, 0, wx.EXPAND, 0)
    
    self.SetSizer(mainSizer)
    self.Layout()
    
  def USAF (self):
    '''Did the user select USAF station ID?'''
    return self.selectIDType.GetStringSelection () == "USAF"
  
class SearchResults (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]
    self.noaa = dao.NOAA ()
    self.results = []

    self.title = wx.StaticBox(self, -1, u"Station wählen")
    self.lctChooseStation = dlb.DataListBox (self, COLUMNS)

    # clear button
    self.clearButton = wx.Button (self, -1, u"Suchergebnisse löschen")
    self.Bind (wx.EVT_BUTTON, self["Clear"], self.clearButton)

    sizer_main = wx.StaticBoxSizer(self.title, wx.VERTICAL)
    sizer_main.Add(self.lctChooseStation, 3, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
    sizer_main.Add (self.clearButton, 0)

    self.SetSizer(sizer_main)
    self.Layout()

    self.searchComplete = False

  def getSelectedStations (self):
    return self.lctChooseStation.getSelected ()

class DownloadData (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]

    self.sizer = wx.BoxSizer (wx.VERTICAL)

    self.label = wx.StaticBox (self, -1, "Zeitraum:")
    self.daterange_sizer = wx.StaticBoxSizer (self.label)

    # TODO year validator
    self.txtFrom = wx.TextCtrl (self, -1, "1929")
    self.txtTo = wx.TextCtrl (self, -1, str (CURRENTYEAR))

    self.daterange_sizer.Add (self.txtFrom)
    self.daterange_sizer.Add (self.txtTo)
    self.sizer.Add (self.daterange_sizer)

    self.noaa = dao.NOAA ()

    self.downloadButton = wx.Button (self, -1, "Daten herunterladen..")
    self.sizer.Add (self.downloadButton)

    self.SetSizer (self.sizer)
    self.sizer.Fit (self)
    self.Bind (wx.EVT_BUTTON, self["Download"], self.downloadButton)
    self.Layout()

class NOAA_Wizard (Hook, Wizard):
  def createSubPanels (self):
    self.pool.addWindow ("Search", SearchPanel (self))
    self.pool.addWindow ("SearchResults", SearchResults (self))
    self.pool.addWindow ("Download", DownloadData (self))
    
    # TODO das gehört nicht hierher
    self.sc  = control.SearchControl (self.pool["Search"])
    self.src = control.SearchResultsControl (self.pool["SearchResults"])
    self.dc  = control.DownloadControl (self.pool["Download"])
    
