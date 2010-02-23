from plugin import Plugin
import data
import main
import os
import sys
import ftplib
# time: used to sleep
import time

#noaa_url="ftp://ftp.ncdc.noaa.gov/pub/data/gsod/"

# XXX
# ftplib hat ein problem mit namensauflsung
noaa_url="205.167.25.101"

def example ():
  no = NOAA ()
  no.station_number = 37735
  no.use_wban = True
  no.getCountryList ()
  no.downloadData ()
  return no

def fileExistsInCache (f):
  f = os.path.basename (f)
  return not os.path.exists ("cache/noaa/%s" %f)

class NOAA (Plugin):
  name = "NOAA Plugin"
  desc = "NOAA Plugin"
  data = {}

  def downloadData (self):
    # check if subdir tmp/noaa exists
    # createDataModel - read station data from ish-history
    self.data = data.Data (str(self.station_number), (0,0))
    # download data to tmp/noaa using ftp
    files = []
    # TODO use right time range
    for year in range (1969, 2011):
      # should look like this:
      # decide wether to use WBAN or USAF
      # 998234-99999-2010.op.gz
      # TODO use WBAN / USAF
      s = "%s/%s-99999-%s.op.gz" %(year, 
          str(self.station_number).ljust (6,'0'),
          year
          )
      files.append (s)

    self.retrieveListOfFiles (files)

    # convert tmp/noaa to self.data

    # saveModelToCacheWithHashIndexFile
    self.data.save ("cache")
  
  def getData (self):
    return self.data

  def getUserInput (self):
    self.use_wban = main.dowhile ("Do you want to use WBAN? Yes/No [Default: No]", ['Y','N'])
    print 'Please insert stationnumber: ',
    # read station number and remove \n
    self.station_number = sys.stdin.readline ().rstrip ()

  def getCountryList (self):
    self.retrieveListOfFiles (["ish-history.txt"])

  def retrieveListOfFiles (self, listoffiles):
    # check cache
    missing_files = filter (fileExistsInCache, listoffiles)

    # get missing files
    ftp = ftplib.FTP(noaa_url)
    ftp.login("anonymous", "")
    ftp.cwd ("pub/data/gsod")
    for f in missing_files:
      filename = os.path.basename (f)
      print "Downloading %s........" %filename
      try:
        ftp.retrbinary('RETR %s' %f,
            open('cache/noaa/%s' %filename, 'w+').write)
      except:
        print "%s doesn't exist." %filename
      print "waiting for 2 sec...."
      time.sleep (2)
    ftp.quit ()
