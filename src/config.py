###################
# global variables
###################
CACHEDIR = "cache"
PLUGINDIR = "plugins"
CACHE_INDEX_FILENAME = "index.dat"
STATION_LIST_CACHE_FILENAME = "stationlist"

# date functions
import datetime
import time
CURRENTYEAR = datetime.date.fromtimestamp (time.time ()).year

###################
#
# global output
# 
###################
import sys
out = sys.stdout
err = sys.stderr

def createOutputStreams ():
  global out
  global err
  # create to different frames. for each stream one
  import wxcustom.outputframe
  import wx

  outFrame = wxcustom.outputframe.OutputFrame (None, title="Hinweismeldungen")
  errFrame = wxcustom.outputframe.OutputFrame (None, title="Fehlermeldungen")
