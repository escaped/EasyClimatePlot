# -*- coding: utf-8 -*-
'''GUI workflow for NOAA download'''

import wx
import wxcustom.datalistbox as dlb
from main.workflow.wizard import Wizard
from main.workflow.hook import Hook

from noaa.validators import IntegerValidator, NumberValidator

import functional
import functools as ft

import dao

from wxcustom.panel import Panel

# global variables
COLUMNS = ["Station Name", "Country", "USAF ID", "Lon", "Lat"]
COMBOBOX_LIMIT = 15

class SearchPanel (Panel):
  def __init__(self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)

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
  
  def Validate(self):
    station = region = coord = False
    if len(self.txtStationNumber.GetValue().strip()) == 0:
      station = True      
    if len(self.lsbRegion.GetValue().strip()) == 0:
      region = True      
    if len(self.txtLat1.GetValue().strip()) == 0 or len(self.txtLat2.GetValue().strip()) == 0 or len(self.txtLon1.GetValue().strip()) == 0 or len(self.txtLon2.GetValue().strip()) == 0:
      coord = True
      
    # at least one field should be filled
    if station and region and coord:
      mbox = wx.MessageDialog (self, "Error", "Fill at least one FieldGroup.", wx.OK)
      mbox.ShowModal ()
      mbox.Destroy ()
      return False
    
    return Panel.Validate(self)
  
  def deactivate(self):
    ''' Check Input '''
    return self.Validate()

class SearchResults (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]
    self.noaa = dao.NOAA ()
    self.results = []

    self.sizer_searchstation = wx.StaticBox(self, -1, u"Station wählen")
    self.lctChooseStation = dlb.DataListBox (self, COLUMNS)

    # clear button
    self.clearButton = wx.Button (self, -1, u"Suchergebnisse löschen")
    self.Bind (wx.EVT_BUTTON, self["clearButton"], self.clearButton)

    self["clearButton"].handle (self.onClear)

    sizer_main = wx.StaticBoxSizer(self.sizer_searchstation, wx.VERTICAL)
    sizer_main.Add(self.lctChooseStation, 3, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
    sizer_main.Add (self.clearButton, 0)

    self.SetSizer(sizer_main)
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
      stations = self.noaa.listAvailableStations ()

      # get data from previous view
      searchView = self.parent.pool["Search"]

      stationNumber = searchView.txtStationNumber.GetValue()
      region        = searchView.lsbRegion.GetClientData (searchView.lsbRegion.GetSelection ())
      ul, lr = ((searchView.txtLat1, searchView.txtLon1),
                        (searchView.txtLat2, searchView.txtLon2))

      # compose the possible functions
      searchFunctions = [lambda x: x] 

      searchResults = []
      if stationNumber:
        if self.parent.pool["Search"].USAF (): 
          searchFunctions.append (ft.partial (self.noaa.searchStationsByStationID, 
                                              str (stationNumber), True))
        else:
          searchFunctions.append (ft.partial (self.noaa.searchStationsByStationID, 
                                              str (stationNumber),
                                              False))
      if region != "":
        searchFunctions.append (ft.partial (self.noaa.searchStationsByRegion, region))

      if ul and lr:
        searchFunctions.append (ft.partial (self.noaa.searchStationsByLonLat, ul, lr))

      # see: http://docs.python.org/howto/functional.html#the-functional-module
      multi_compose = ft.partial(reduce, functional.compose)
      # search 
      searchResults = multi_compose (searchFunctions)(stations)
      if searchResults != []: 
        self.searchComplete = True
        self.lctChooseStation.AddManyData (searchResults, ["station_name", "ctry_fips", "usaf", "lon", "lat"])

    return True

class DownloadData (Panel):
  def __init__ (self, *args, **kwargs):
    Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]

    self.sizer = wx.BoxSizer ()

    # TODO auswahl für jahr muss noch rein

    self.noaa = dao.NOAA ()

    self.downloadButton = wx.Button (self, -1, "Daten herunterladen..")
    self.sizer.Add (self.downloadButton)

    self.SetSizer (self.sizer)
    self.sizer.Fit (self)
    self.Bind (wx.EVT_BUTTON, self.onDownload, self.downloadButton)
    self.Layout()

  def onDownload (self, e):
    # TODO vll sollte man noaa doch anders aufbauen
    print "downloading.."
    for station in self.parent.pool["SearchResults"].getSelectedStations ():
      self.noaa.station_number = station["usaf"]
      self.noaa.use_usaf = True
      self.noaa.downloadData (1990, 2000)

class NOAA_Wizard (Wizard):
  def createSubPanels (self):
    self.pool.addWindow ("Search", SearchPanel (self))
    self.pool.addWindow ("SearchResults", SearchResults (self))
    self.pool.addWindow ("Download", DownloadData (self))
    
