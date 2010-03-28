'''control.py is responsible to create the gui views and it is used to access the dao.'''
from mvc.control import Control

import dao
import functional
import functools as ft

from wxcustom.error import ErrorMessage
class SearchControl (Control):
  def __init__ (self, view):
    Control.__init__ (self, view)

  def onDeactivate(self):
    ''' Check Input '''
    return self.Validate()

  def Validate(self):
    name = station = region = coord = False
    if len(self.view.txtStationName.GetValue().strip()) == 0:
      name = True
    if len(self.view.txtStationNumber.GetValue().strip()) == 0:
      station = True      
    if len(self.view.lsbRegion.GetValue().strip()) == 0:
      region = True      
    if (len(self.view.txtLat1.GetValue().strip()) == 0 or
       len(self.view.txtLat2.GetValue().strip()) == 0 or
       len(self.view.txtLon1.GetValue().strip()) == 0 or
       len(self.view.txtLon2.GetValue().strip()) == 0):
      coord = True
      
    # at least one field should be filled
    if station and region and coord:
      ErrorMessage ("Fill at least one FieldGroup")
      return False
    
    return self.view.Validate()

class SearchResultsControl (Control):
  def __init__ (self, view):
    Control.__init__ (self, view)

    self.searchComplete = False
    self.noaa = dao.NOAA ()

  def onActivate (self):
    lct = self.view.lctChooseStation
    lct.Show (True)

    # get the values of the last panel
    if not self.searchComplete:
      stations = self.noaa.listAvailableStations ()

      # get data from previous view
      searchView = self.view.parent.pool["Search"]

      stationName   = searchView.txtStationName.GetValue ()
      stationNumber = searchView.txtStationNumber.GetValue()
      region        = searchView.lsbRegion.GetClientData (searchView.lsbRegion.GetSelection ())
      ul, lr = ((searchView.txtLat1, searchView.txtLon1),
                        (searchView.txtLat2, searchView.txtLon2))

      # compose the possible functions
      searchFunctions = [lambda x: x] 

      searchResults = []
      if stationName:
        searchFunctions.append (ft.partial (self.noaa.searchStationsByName, stationName))
      if stationNumber:
        if self.view.parent.pool["Search"].USAF (): 
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
        self.view.lctChooseStation.AddManyData (searchResults, ["station_name", "ctry_fips", "usaf", "lon", "lat"])
    return True

  def onClear (self, *args):
    self.results = []
    self.searchComplete = False
    self.view.lctChooseStation.clear ()
    self.view.parent.switchSubPanelByName ("Search")

class DownloadControl (Control):
  def __init__ (self, view):
    Control.__init__ (self, view)
    self.noaa = dao.NOAA ()

  def onDownload (self, *args, **kwargs):
    fromYear = self.view.txtFrom.GetValue ()
    toYear   = self.view.txtTo.GetValue ()

    if len (fromYear) == 0: fromYear = None
    else: fromYear = int (fromYear)
    if len (toYear)   == 0: toYear   = None
    else: toYear = int (toYear)

    for station in self.view.parent.pool["SearchResults"].getSelectedStations ():
      # TODO we should use both usaf and wban!
      self.noaa.station_number = station["usaf"]
      self.noaa.use_usaf = True
      self.noaa.downloadData (fromYear, toYear)

  def onActivate (self, *args, **kwargs):
    return True

  def onDeactivate (self, *args, **kwargs):
    return True

