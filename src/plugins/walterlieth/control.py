from mvc.control import Control
import cachemanager
import os
import config
import gnuplot
import re

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
          usaf, wban = eval (key)
        except:
          continue

        for subkey, subitem in item.items ():
          # get station data for each item
          print subkey
          from_, to = (subkey)
          stationdata = self.cache.load ("noaa", key, from_, to)
          station = stationdata.weatherstation
          data.append ({"usaf": usaf, "wban":wban,
            "range": subkey, "cacheid": subitem,
            "name": station["station_name"]})
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
    for item in self.view.getSelected():
      self.plot (item)

  def plot (self, data):
    dataobject = self.cache.load ('noaa', (data["usaf"], data["wban"]), data["range"][0], data["range"][1])
    name = dataobject.weatherstation["station_name"]
    plottitle  = "%s: %d - %d" %(name, data["range"][0],data["range"][1])
    plotoutput = "%s_%d_%d" %(name, data["range"][0],data["range"][1])
    plotoutput = os.path.join(os.getcwd() + os.sep + re.sub('[^a-zA-Z0-9_\-.() ]+', '', plotoutput+'.png'))
    
    data = [dataobject.getData("temp", "m"), 
            dataobject.getData("mintemp", "m"), 
            dataobject.getData("maxtemp", "m"), 
            dataobject.getData ("precipitation", "m")]
    
    datafile = gnuplot.GnuplotData(data, "m")
       
    template = gnuplot.GnuplotTemplate(os.path.dirname(__file__)+os.sep+"wl.gp" )
    template.setTitle(plottitle)
    template.setOutput(plotoutput)
    
    g = gnuplot.Gnuplot()    
    g.plot(template, [datafile])