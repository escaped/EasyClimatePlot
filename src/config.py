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
  import wxcustom.outputpanel
  import wx

  outFrame = wx.Frame (None, title="Hinweismeldungen")
  errFrame = wx.Frame (None, title="Fehlermeldungen")
  out = wxcustom.outputpanel.OutputPanel (outFrame)
  err = wxcustom.outputpanel.OutputPanel (errFrame)
