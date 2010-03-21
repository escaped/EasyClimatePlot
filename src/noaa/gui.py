# -*- coding: utf-8 -*-
'''GUI workflow for NOAA download'''

import wx
import wxcustom.datalistbox as dlb
from main.workflow.wizard import Wizard
from main.workflow.hook import Hook

import dao

# global variables
COLUMNS = ["Station Name", "Country", "USAF ID", "Lon", "Lat"]
COMBOBOX_LIMIT = 15

class SearchPanel (Hook, wx.Panel):
  def __init__(self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)

    # TODO NOAA objekt sollte global sein. das kostet sonst einfach zuviel zeit.
    self.noaa = dao.NOAA ()

    self.stbSearchBox = wx.StaticBox(self, -1, "Suche")
    self.lblStationsnummer = wx.StaticText(self, -1, "Stationsnummer:")
    self.txtStationNumber = wx.TextCtrl(self, -1, "")
    self.selectIDType = wx.RadioBox(self, -1, "USAF", choices=["USAF", "WBAN"], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
    self.lblRegion = wx.StaticText(self, -1, "Region")
    self.lsbRegion = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)

    # fill combobox with countries available at NOAA
    self.lsbRegion.Append ("", None) # Empty if none chosen
    
    for item in self.noaa.getCountryList ():
      # we associate each item with the given country code
      # TODO per GetClientData bekommt man dann den richtigen ländercode
      self.lsbRegion.Append (' '.join (item)[:COMBOBOX_LIMIT], item[0])

    self.lblLatLon1 = wx.StaticText(self, -1, "Lat/Lon")
    self.txtLat1 = wx.TextCtrl(self, -1, "")
    self.txtLon1 = wx.TextCtrl(self, -1, "")
    self.lblLatLon2 = wx.StaticText(self, -1, "Lat/Lon")
    self.txtLat2 = wx.TextCtrl(self, -1, "")
    self.txtLon2 = wx.TextCtrl(self, -1, "")


    sizer_1 = wx.StaticBoxSizer(self.stbSearchBox, wx.VERTICAL)
    sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_2.Add(self.lblStationsnummer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_2.Add(self.txtStationNumber, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_2.Add(self.selectIDType, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
    sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
    sizer_3.Add(self.lblRegion, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 8)
    sizer_3.Add(self.lsbRegion, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
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

  def USAF (self):
    '''Did the user select USAF station ID?'''
    return self.selectIDType.GetStringSelection () == "USAF"
  
  def deactivate(self):
    ''' Check Input '''
    
    # check emptyness
    station = False 
    region = False
    coord = False
    
    if len(self.txtStationNumber.GetValue().strip()) == 0:
      station = True      
    if len(self.lsbRegion.GetValue().strip()) == 0:
      region = True      
    if len(self.txtLat1.GetValue().strip()) == 0 and len(self.txtLat2.GetValue().strip()) == 0 and len(self.txtLon1.GetValue().strip()) == 0 and len(self.txtLon2.GetValue().strip()) == 0:
      coord = True
      
    # at least one field should be filled
    if station and region and coord:
      mbox = wx.MessageDialog (self, "Error", "Fill at least one field.", wx.OK)
      mbox.ShowModal ()
      mbox.Destroy ()
      return False
    
    if not station:
      try:
        int(self.txtStationNumber.GetValue())
      except:
        mbox = wx.MessageDialog (self, "Error", "Check Stationumber.", wx.OK)
        mbox.ShowModal ()
        mbox.Destroy ()
        return False
    elif not region:
      mbox = wx.MessageDialog (self, "Error", "Check Region.", wx.OK)
      mbox.ShowModal ()
      mbox.Destroy ()
      return False
    elif not coord:  
      try:
        int(self.txtLat1.GetValue())
        int(self.txtLat2.GetValue())
        int(self.txtLon1.GetValue())
        int(self.txtLon2.GetValue())
      except:
        mbox = wx.MessageDialog (self, "Error", "Check coords", wx.OK)
        mbox.ShowModal ()
        mbox.Destroy ()
        return False

    return True
      
      
      
    
    

class SearchResults (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
    self.parent = args[0]
    self.noaa = dao.NOAA ()
    self.results = []

    self.sizer_searchstation = wx.StaticBox(self, -1, u"Station wählen")
    self.lctChooseStation = dlb.DataListBox (self, COLUMNS)

    # clear button
    self.clearButton = wx.Button (self, -1, u"Suchergebnisse löschen")
    self.Bind (wx.EVT_BUTTON, self.onClear, self.clearButton)

    sizer_main = wx.StaticBoxSizer(self.sizer_searchstation, wx.VERTICAL)
    sizer_main.Add(self.lctChooseStation, 3, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
    sizer_main.Add (self.clearButton, 1)

    self.SetSizer(sizer_main)
    #sizer_main.Fit(self)
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
      stationNumber = self.parent.pool["Search"].txtStationNumber.GetValue()
      # TODO search something..
      searchResults = []
      if stationNumber:
        if self.parent.pool["Search"].USAF (): 
          searchResults = self.noaa.searchStationsByStationID (str(stationNumber))
        else:
          searchResults = self.noaa.searchStationsByStationID (str(stationNumber), False)
        
      if searchResults != []: 
        self.searchComplete = True
        self.lctChooseStation.AddManyData (searchResults, ["station_name", "ctry_fips", "usaf", "lon", "lat"])

    return True

class DownloadData (Hook, wx.Panel):
  def __init__ (self, *args, **kwargs):
    wx.Panel.__init__ (self, *args, **kwargs)
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
    
