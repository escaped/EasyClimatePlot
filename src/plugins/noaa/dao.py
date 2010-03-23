# -*- coding: utf-8 -*-
import cachemanager
import plot.contour
import config
import socket
import data
import ftplib
import gzip
import utils
import os.path
import re
import sys

import cPickle

# time: used to sleep while downloading via FTP
import time
import weatherstation

# noaa_url="ftp://ftp.ncdc.noaa.gov/pub/data/gsod/"
# ftplib doesn't seem to resolv the upper url right
noaa_url="205.167.25.101"

def fileExistsInCache (f):
  f = os.path.basename (f)
  return not os.path.exists (os.path.join (config.CACHEDIR ,"noaa", "%s" %f))

class NOAA (object):
  '''Objects of this class are used to access the NOAA FTP, search and download station
  data.'''

  name = "NOAA Plugin"
  desc = "NOAA Plugin"
  data = {}

  # check cache
  cache = cachemanager.CacheManager.getInstance()

  def __init__ (self):
    # initialise list of stations, of it exists in the cache
    # TODO FRENZEL kannst du das hier auf den cachemanager umschwenken? ich verstehe den
    # nicht ganz, bekomme komische exceptions.
    try:
      f = open (os.path.join (config.CACHEDIR, config.STATION_LIST_CACHE_FILENAME), "r")
      self.listOfStations = cPickle.load (f)
      f.close ()
    except IOError:
      self.listOfStations = None 
    # TODO die länderlisten sollten auch unbedingt gecached werden
    self.ctry_wmo_list = set ()
    self.ctry_fips_list = set ()

  # TODO end sollte vom aktuellen jahr abhängen.. ;)
  def downloadData (self, start=1929, end=2011):
    
    if self.cache.hashExists("noaa", self.station_number, start, end):
        print "Data found in cache... loading!"
        self.data = self.cache.load("noaa", self.station_number, start, end)
        return 
    else:
        print "Data not found in cache... "
    
    # createDataModel - read station data from ish-history
    self.data = data.Data (str(self.station_number), (0,0))
    # download data to tmp/noaa using ftp
    files = []
    print 'Loading data: %d - %d' %(start, end)

    for year in xrange (start, end + 1):
      # should look like this:
      # decide wether to use WBAN or USAF
      # 998234-99999-2010.op.gz
      # TODO falls für eine station sowohl wban als auch usaf vorhanden ist, können auch
      # beide fehler != 999* sein.
      if self.use_usaf:
        s = "%s/%s-99999-%s.op.gz" %(year, 
            str(self.station_number).ljust (6,'0'),
            year
          )
      else:
        s = "%s/999999-%s-%s.op.gz" %(year, 
            str(self.station_number).ljust (6,'0'),
            year
          )
      files.append (s)

    self.retrieveListOfFiles (files)
    
    # unzip and cache data to one file
    lines = []
    for file in files:
      print "  loading data from %s" %(file)
      try:
        f = gzip.open(os.path.join(config.CACHEDIR,"noaa", "%s" %os.path.basename (file)), "rb")
        lines.extend(f.readlines()[1:]) # ignore first line
        f.close()
      except:
        print "   (warn) file does not exist"
    
    # parse data
    # TODO this should be somewhere. maybe in config.py?
    CAT = ['date','temp','mintemp','maxtemp','windspeed','windgust','maxwindspeed','precipitation','visibility','dewpoint','pressure','seapressure']
    DATA_COL = {'date': 2, 'temp': 3, 'mintemp': 18, 'maxtemp': 17,'windspeed': 13, 'windgust':16, 'maxwindspeed': 15, 'precipitation': 19, 'visibility': 11,  'dewpoint': 5,   'pressure': 9, 'seapressure': 7}
    DATA_INV = {'temp': 9999.9, 'mintemp': 9999.9, 'maxtemp': 9999.9, 'windspeed': 999.9, 'windgust': 999.9, 'maxwindspeed': 999.9, 'precipitation': 99.99, 'visibility': 999.9, 'dewpoint': 9999.9, 'pressure': 9999.9, 'seapressure': 9999.9}
    
    values = utils.Dict()
    for line in lines:
      tmp = line.replace('*','').replace('\n','').split()
      date = tmp[DATA_COL['date']]
      
      for type in CAT:
        index = DATA_COL[type]
        
        if index != 2: # ignore date -> already parsed
            value = tmp[index]
            p = re.compile("\d+[,\.]\d+")
            m = p.match(value)
            
            if m != None and float(m.group()) != DATA_INV[type]: # parse and convert data
                if type in ['temp', 'mintemp', 'maxtemp', 'dewpoint']:
                    values[type][date] = (float(value) - 32) * (5.0/9.0)
                elif type in ['windspeed', 'windgust', 'maxwindspeed']:
                    values[type][date] = float(value) * 0.51
                elif type == 'visibility':
                    values[type][date] = float(value) * 1.609
                elif type == 'precipitation':
                    '''
                         all Flags treated as valid
                         A = 1 report of 6-hour precipitation 
                             amount.
                         B = Summation of 2 reports of 6-hour 
                             precipitation amount.
                         C = Summation of 3 reports of 6-hour 
                             precipitation amount.
                         D = Summation of 4 reports of 6-hour 
                             precipitation amount.
                         E = 1 report of 12-hour precipitation
                             amount.
                         F = Summation of 2 reports of 12-hour
                             precipitation amount.
                         G = 1 report of 24-hour precipitation
                             amount.
                         H = Station reported '0' as the amount
                             for the day (eg, from 6-hour reports),
                             but also reported at least one
                             occurrence of precipitation in hourly
                             observations--this could indicate a
                             trace occurred, but should be considered
                             as incomplete data for the day.
                         I = Station did not report any precip data
                             for the day and did not report any
                             occurrences of precipitation in its hourly
                             observations--it's still possible that
                             precip occurred but was not reported.
                    '''
                    values[type][date] = float(m.group()) * 25.4

                else:
                    values[type, date] = float(value)
    
    # save to dataObject                
    for type in CAT:
        if type != 'date' and len(values[type].keys()) > 0:
            print type
            print values[type]
            self.data.addCategory(type, values[type])

    # self.data.save ("cache")
    self.cache.save(self.data, "noaa", self.station_number, start, end)
  
  def getData (self):
    return self.data

  def downloadCountryList (self):
    '''This method downloads the file ish-history.txt from the NOAA FTP. That file
    contains all stations, which are listed and for which some data exist on the FTP.'''
    self.retrieveListOfFiles (["ish-history.txt"])

  def retrieveListOfFiles (self, listoffiles):
    '''This method simply retrieves the files in the list listoffiles from the FTP.'''
    # check cache
    missing_files = filter (fileExistsInCache, listoffiles)

    # get missing files
    try:
      ftp = ftplib.FTP(noaa_url)
      ftp.login("anonymous", "")
      ftp.cwd ("pub/data/gsod")
      for f in missing_files:
        filename = os.path.basename (f)
        print "Downloading %s........" %filename
        try:
          ftp.retrbinary('RETR %s' %f,
              open(os.path.join (config.CACHEDIR, "noaa", "%s" %filename), 'w+').write)
        except IOError:
          print "Missing directory %s/noaa" %config.CACHEDIR
          sys.exit (-1)
        except:
          print "%s doesn't exist." %filename
        print "waiting for 2 sec...."
        time.sleep (2)
      ftp.quit ()
    except socket.error:
      sys.stderr.write ("Network error. No connection to NOAA FTP server\n")

  def getFileContents (self, filename):
    file = open (os.path.join(config.CACHEDIR ,"noaa", filename), 'r')
    content = file.readlines ()
    file.close ()

    return content

  def getIshHistory (self):
    # get ish-history
    self.downloadCountryList ()
    # read ish-history
    content = self.getFileContents ("ish-history.txt")
    # delete unneeded lines
    del content[0:20]
    return content
    
  def listAvailableStations (self):
    '''This method parses ish-history.txt, creates a WeatherStation object for each line
    and returns a list of all available WeatherStations contained in ish-history.txt.'''
    if not self.listOfStations:
      if not self.cache.hashExists("noaa", "stations"):
        content = self.getIshHistory ()
        self.listOfStations = [weatherstation.weatherStationDictionary (line) for line in content]
        self.cache.save(self.listOfStations, "noaa", "stations")

      else:
        self.listOfStations = self.cache.load("noaa", "stations")

    return self.listOfStations

  def searchStationsByRegion (self, region, stationSet = None):
    '''Search stations by region, whereby region is a FIPS country id.'''
    if stationSet: stations = stationSet
    else: stations = self.listAvailableStations ()

    return filter (lambda x: x["ctry_fips"] == region, stations)

  def searchStationsByStationID (self, stationid, usaf = True, stationSet = None):
    '''Search stations by station id, where station id is a regular
    expression. NOTE: If wban = False, then you are searching with 
    the usaf station id, which might isn't what you want.'''
    if stationSet: stations = stationSet
    else: stations = self.listAvailableStations ()

    reg = re.compile (str(stationid))
    if usaf:
      return filter (lambda x: reg.search (str (x["usaf"])), stations)
    else:
      return filter (lambda x: reg.search (str (x["wban"])), stations)

  def searchStationsByCountryCode (self, countrycode, use_FIPS = True, stationSet = None):
    '''Search stations by country code. The country code can be either a historical WMO
    country ID (with use_FIPS = False), or a FIPS country ID.'''
    if stationSet:
      stations = stationSet
    else:
      stations = self.listAvailableStations ()

    # TODO do we need to search according to regex?
    if use_FIPS:
      return filter (lambda x: x.ctry_fips == countrycode, stations)
    else:
      return filter (lambda x: x.ctry_wmo == countrycode, stations)

  # ul: upper left
  # lr: lower right
  def searchStationsByLonLat (self, ul, lr, stationSet = None):
    '''Search stations by Latitude and Longitude. Format: (lat, lon) = (+/-nn.nnnn,
    +/-nnn.nnnn). The first argument of the method is left upper corner and the second
    argument is the right lower corner of a rectangle.'''
    if stationSet: stations = stationSet
    else: stations = self.listAvailableStations ()

    # filter stations in the west, northwest or north of the ul
    stations = filter (lambda x: x["lat"] <= ul[0] and x["lon"] >= ul[1],
                                      stations)
    # filter stations in the south, southeast or east of the lr
    stations = filter (lambda x: x["lat"] >= lr[0] and x["lon"] <= lr[1],
                                      stations)

    return stations

  def getCountryList (self, FIPS=True):
    '''Get a list of the available country IDs. Use FIPS or WMO IDs.'''
    self.retrieveListOfFiles (["country-list.txt"])
    content = self.getFileContents ("country-list.txt")
    del content[:2]
    countries = set ()
    for line in content:
      data = line.split ()
      id = data[0]
      name = ' '.join (data[1:]) 
      countries.add ((id, name))
    return countries

# test routine
def example ():
  no = NOAA ()
  no.station_number = 37735
  no.use_usaf = True
  no.getCountryList ()
  no.downloadData (1969, 2011)
  # plot
  #import walterlieth
  #data = no.getData ()
  #w = walterlieth.WalterLieth (
  #      data.getData ("temp", "m"),
  #      data.getData ("precipitation", "m")
  #    )
  #w.process ()
  #c = contour.Contour (
  #      data.getData ("temp", "m"),
  #      data.getData ("temp", "m"),
  #      data.getData ("temp", "m")
  #    )
  #c.process ()

  return no

def searchStations ():
  n = NOAA ()
  # print n.searchStationsByLonLat ((-99999,-999999),(-99999,-999999))
  for station in n.searchStationsByLonLat   ((41.000, 43.0000),(38.000, 50.0000)):
    print station.station_name, station.usaf, station.ctry_fips, station.lat, station.lon

def listCountries ():
  n = NOAA ()
  for ctry in n.getCountryList ():
    print ctry


if __name__ == "__main__":
  #example ()
  #searchStations ()
  listCountries ()
