# -*- coding: utf-8 -*-
'''control.py is responsible to create the gui views and it is used to access the dao.'''
from plugins.noaa.control import SearchControl, SearchResultsControl

from mvc.control import Control

import config
import plugins.noaa.dao as dao

class ExportControl (Control):
  def __init__ (self, view):
    Control.__init__ (self, view)

    self.dao = dao.NOAA.getInstance ()

  def onExport (self, event):
    '''Show stations via config.out stream.'''
    stations = self.view.parent.pool["SearchResults"].getSelectedStations ()
    print >>config.out, self.dao.exportStationsForBatchgeocode (stations)

