# -*- coding: utf-8 -*-
'''GUI workflow for NOAA download'''

import wx
import wxcustom.datachecklistbox as dcl
from main.panel import Workflow,Hook

import dao

class SearchPanel (Hook, wx.Panel):
  def __init__(self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)

    self.sizer_1_staticbox = wx.StaticBox(self, -1, "Suche")
    self.lblStationsnummer = wx.StaticText(self, -1, "Stationsnummer:")
    self.txtStationNumber = wx.TextCtrl(self, -1, "")
    self.radio_box_1 = wx.RadioBox(self, -1, "USAF", choices=["USAF", "WBAN"], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
    self.lblRegion = wx.StaticText(self, -1, "Region")
    self.cboRegion = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)
    self.lblLatLon1 = wx.StaticText(self, -1, "Lat/Lon")
    self.txtLat1 = wx.TextCtrl(self, -1, "")
    self.txtLon1 = wx.TextCtrl(self, -1, "")
    self.lblLatLon2 = wx.StaticText(self, -1, "Lat/Lon")
    self.txtLat2 = wx.TextCtrl(self, -1, "")
    self.txtLon2 = wx.TextCtrl(self, -1, "")


    sizer_1 = wx.StaticBoxSizer(self.sizer_1_staticbox, wx.VERTICAL)
    sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_2.Add(self.lblStationsnummer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_2.Add(self.txtStationNumber, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_2.Add(self.radio_box_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
    sizer_3.Add(self.lblRegion, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 8)
    sizer_3.Add(self.cboRegion, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
    sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
    sizer_4.Add(self.lblLatLon1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_4.Add(self.txtLat1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_4.Add(self.txtLon1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_4.Add(self.lblLatLon2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_4.Add(self.txtLat2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_4.Add(self.txtLon2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
    self.SetSizer(sizer_1)
    sizer_1.Fit(self)
    self.Layout()

class SearchResults (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    # TODO this needs a button to clear the search
    wx.Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]
    self.noaa = dao.NOAA ()
    self.results = []

    self.sizer_5_staticbox = wx.StaticBox(self, -1, u"Station wählen")
    #self.lctChooseStation = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
    # TODO CheckListBox ist nicht so hübsch. hier sollte ein wxGrid verwendet werden,oder?
    self.lctChooseStation = dcl.DataCheckListbox (self)

    # clear button
    self.clearButton = wx.Button (self, -1, u"Suchergebnisse löschen")
    self.Bind (wx.EVT_BUTTON, self.onClear, self.clearButton)

    sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.HORIZONTAL)
    sizer_5.Add(self.lctChooseStation, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
    self.SetSizer(sizer_5)
    sizer_5.Add (self.clearButton, 1)
    sizer_5.Fit(self)
    self.Layout()

    self.searchComplete = False

  def onClear (self, e):
    self.results = []
    self.searchComplete = False
    self.lctChooseStation.clear ()
    self.parent.switchSubPanelByName ("Search")

  def getSelectedStations (self):
    return self.lctChooseStation.getSelected ()

  def activate (self):
    self.lctChooseStation.Show (True)
    # get the values of the last panel
    # TODO use other options as well
    # TODO performance issues?
    if not self.searchComplete:
      stationNumber = self.parent.pool["Search"].txtStationNumber.GetValue ()
      if stationNumber:
        searchResults = self.noaa.searchStationsByStationID (str(stationNumber))
        self.lctChooseStation.AddManyData (searchResults,
          ["station_name", "ctry_fips", "usaf"])
      self.searchComplete = True
    return True

class DownloadData (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]

    # TODO auswahl für jahr muss noch rein

    self.noaa = dao.NOAA ()

    self.downloadButton = wx.Button (self, -1, "Daten herunterladen..")
    self.Bind (wx.EVT_BUTTON, self.onDownload, self.downloadButton)
    self.Layout ()

  def onDownload (self, e):
    # TODO vll sollte man noaa doch anders aufbauen
    print "downloading.."
    for station in self.parent.pool["SearchResults"].getSelectedStations ():
      self.noaa.station_number = station["usaf"]
      self.noaa.use_usaf = True
      self.noaa.downloadData (1990, 2000)

class NOAA_Workflow (Workflow):
  def createSubPanels (self):
    self.pool.addWindow ("Search", SearchPanel (self))
    self.pool.addWindow ("SearchResults", SearchResults (self))
    self.pool.addWindow ("Download", DownloadData (self))
    
