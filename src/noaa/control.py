'''control.py is responsible to create the gui views and it is used to access the dao.'''

import eventhandling.eventpool

class Control (object):
  '''Abstract class, whose deriving classes should be used as controllers in MVC'''

  def __init__ (self, view):
    '''Constructor. view must be of type eventpool!'''
    if not isinstance (view, eventhandling.eventpool.EventPool):
      raise TypeError, "view must be of type EventPool!"

    self.view = view

    # subsribe to the events of the view
    # NOTE: we have to subscribe to EVERY GIVEN EVENT!
    self.__subscribe__ ()

  def __subscribe__ (self):
    for key, event in self.view.events.items ():
      try:
        event += getattr (self, "on" + key)
      except AttributeError:
        # TODO debugging facility
        print "please implement on%s for event %s" %(key, key)


from noaa import dao
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
    station = region = coord = False
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

      stationNumber = searchView.txtStationNumber.GetValue()
      region        = searchView.lsbRegion.GetClientData (searchView.lsbRegion.GetSelection ())
      ul, lr = ((searchView.txtLat1, searchView.txtLon1),
                        (searchView.txtLat2, searchView.txtLon2))

      # compose the possible functions
      searchFunctions = [lambda x: x] 

      searchResults = []
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
    for station in self.view.parent.pool["SearchResults"].getSelectedStations ():
      self.noaa.station_number = station["usaf"]
      self.noaa.use_usaf = True
      self.noaa.downloadData (1990, 2000)

  def onActivate (self, *args, **kwargs):
    pass

  def onDeactivate (self, *args, **kwargs):
    pass

