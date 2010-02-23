from plugin import Plugin
import data
import main
import os
import sys

class NOAA (Plugin):
  name = "NOAA Plugin"
  desc = "NOAA Plugin"
  data = {}

  def downloadData (self):
    # check if subdir tmp/noaa exists
    # createDataModel - read station data from ish-history
    self.data = data.Data (self.station_number, (0,0))
    # download data to tmp/noaa
    # convert tmp/noaa to self.data
    # saveModelToCacheWithHashIndexFile
    self.data.save ("cache")
  
  def getData (self):
    return self.data

  def getUserInput (self):
    self.use_wban = main.dowhile ("Do you want to use WBAN? Yes/No [Default: No]", ['Y','N'])
    print 'Please insert stationnumber: ',
    self.station_number = sys.stdin.readline ()
