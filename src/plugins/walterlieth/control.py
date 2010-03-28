from mvc.control import Control
import cachemanager

import plot

class SearchControl (Control):
  def __init__ (self, view):
    Control.__init__ (self, view)

class SearchResultsControl (Control):
  cache = cachemanager.CacheManager.getInstance()

  def __init__ (self, view):
    Control.__init__ (self, view)
    self.noaa_results = self.cache.index["noaa"]

    self.searchDone = False

  def onActivate (self):

    if not self.searchDone:
      # flatten
      data = []
      print self.noaa_results.items ()
      for key, item in self.noaa_results.items ():
        # we just test, if the item converts to int.
        # if not, then it isn't a station
        try:
          int (key)
        except:
          continue

        for subkey, subitem in item.items ():
          data.append ({"usaf": key, "range": subkey, "cacheid": subitem})

      for item in self.noaa_results.keys ():
        self.view.addData (data)

      self.searchDone = True
      # TODO reset!

    return True


class PlotControl (Control):
  cache = cachemanager.CacheManager.getInstance()

  def __init__ (self, view):
    Control.__init__ (self, view)

  def onPlot (self, event):
    # plot
    for item in self.view.getSelected ():
      self.plot (item)

  def plot (self, data):
    dataobject = self.cache.load ('noaa', data["usaf"], data["range"][0], data["range"][1])
    plottitle  = "%s: %d - %d" %(dataobject.name, data["range"][0],data["range"][1])
    plotoutput = "%s_%d_%d" %(dataobject.name, data["range"][0],data["range"][1])
    self.plot = plot.WalterLieth (
         dataobject.getData("temp", "m"), 
         dataobject.getData ("precipitation", "m"),
         plottitle,
         plotoutput
        )

    self.plot.process ()
    # TODO output status to a outputwindow
