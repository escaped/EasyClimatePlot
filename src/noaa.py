from plugin import Plugin

import contour
import socket
import data
import ftplib
import gzip
import main
import multidict
import os
import re
import sys

# time: used to sleep
import time
import weatherstation


#noaa_url="ftp://ftp.ncdc.noaa.gov/pub/data/gsod/"
# XXX
# ftplib hat ein problem mit namensauflsung
noaa_url="205.167.25.101"

def example ():
  no = NOAA ()
  no.station_number = 37735
  no.use_wban = True
  no.getCountryList ()
  no.downloadData (1969, 2011)
  # plot
  import walterlieth
  data = no.getData ()
  w = walterlieth.WalterLieth (
        data.getData ("temp", "m"),
        data.getData ("precipitation", "m")
      )
  w.process ()
  c = contour.Contour (
        data.getData ("temp", "m"),
        data.getData ("temp", "m"),
        data.getData ("temp", "m")
      )
  c.process ()

  return no

def fileExistsInCache (f):
  f = os.path.basename (f)
  return not os.path.exists (os.path.join("cache","noaa", "%s" %f))

class NOAA (Plugin):
  '''Objects of this class are used to access the NOAA FTP, search and download station
  data.'''

  name = "NOAA Plugin"
  desc = "NOAA Plugin"
  data = {}

  def downloadData (self, start=1929, end=2011):
    # check if subdir tmp/noaa exists
    # createDataModel - read station data from ish-history
    self.data = data.Data (str(self.station_number), (0,0))
    # download data to tmp/noaa using ftp
    files = []
    print 'Loading data: %d - %d' %(start, end)
    # TODO use right time range
    for year in range (start, end):
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
    
    # unzip and cache data to one file
    lines = []
    for file in files:
      print "  loading data from %s" %(file)
      try:
        f = gzip.open(os.path.join("cache","noaa", "%s" %os.path.basename (file)), "rb")
        lines.extend(f.readlines()[1:]) # ignore first line
        f.close()
      except:
        print "   (warn) file does not exist"
    
    # parse data
    CAT = ['date','temp','mintemp','maxtemp','windspeed','windgust','maxwindspeed','precipitation','visibility','dewpoint','pressure','seapressure']
    DATA_COL = {'date': 2, 'temp': 3, 'mintemp': 18, 'maxtemp': 17,'windspeed': 13, 'windgust':16, 'maxwindspeed': 15, 'precipitation': 19, 'visibility': 11,  'dewpoint': 5,   'pressure': 9, 'seapressure': 7}
    DATA_INV = {'temp': 9999.9, 'mintemp': 9999.9, 'maxtemp': 9999.9, 'windspeed': 999.9, 'windgust': 999.9, 'maxwindspeed': 999.9, 'precipitation': 99.99, 'visibility': 999.9, 'dewpoint': 9999.9, 'pressure': 9999.9, 'seapressure': 9999.9}
    
    values = multidict.MultiDict()
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
        self.data.addCategory(type, values[type])
 
    # saveModelToCacheWithHashIndexFile
    # self.data.save ("cache")
  
  def getData (self):
    return self.data

  def getUserInput (self):
    self.use_wban = main.dowhile ("Do you want to use WBAN? Yes/No [Default: No]", ['Y','N'])
    print 'Please insert stationnumber: ',
    # read station number and remove \n
    self.station_number = sys.stdin.readline ().rstrip ()

  def getCountryList (self):
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
              open(os.path.join ("cache", "noaa", "%s" %filename), 'w+').write)
        except IOError:
          print "Missing directory cache/noaa"
          sys.exit (-1)
        except:
          print "%s doesn't exist." %filename
        print "waiting for 2 sec...."
        time.sleep (2)
      ftp.quit ()
    except socket.error:
      sys.stderr.write ("Network error. No connection to NOAA FTP server\n")

  def listAvailableStations (self):
    # TODO we should cache the resulting list
    '''This method parses ish-history.txt, creates a WeatherStation object for each line
    and returns a list of all available WeatherStations contained in ish-history.txt.'''
    # get ish-history
    self.getCountryList ()

    # read ish-history
    file = open (os.path.join("cache","noaa", "ish-history.txt"), 'r')
    content = file.readlines ()
    file.close ()
    # delete unneeded lines
    del content[0:20]

    stations = [weatherstation.WeatherStation (line) for line in content]
    
    return stations
  
  def searchStationsByCountryCode (self, countrycode, use_FIPS = True):
    '''Search stations by country code. The country code can be either a historical WMO
    country ID (with use_FIPS = False), or a FIPS country ID.'''

    # TODO do we need to search according to regex?
    if use_FIPS:
      return filter (lambda x: x.ctry_fips == countrycode, self.listAvailableStations ())
    else:
      return filter (lambda x: x.ctry_wmo == countrycode, self.listAvailableStations ())

  # ul: upper left
  # lr: lower right
  def searchStationsByLonLat (self, ul, lr):
    '''Search stations by Longitude and Latitude. Format: (lon,lat) = (+/-nnn.nnnn,
    +/-nn.nnnn). The first argument of the method is left upper corner and the second
    argument is the right lower corner of a rectangle.'''

    # filter stations in the west, northwest or north of the ul
    stations = filter (lambda x: x.lon >= ul[0] and x.lat >= ul[1],
                                      self.listAvailableStations ())
    # filter stations in the south, southeast or east of the lr
    stations = filter (lambda x: x.lon <= lr[0] and x.lat <= lr[1],
                                      stations)

    return stations

def searchStations ():
  n = NOAA ()
  print n.searchStationsByLonLat ((-99999,-99999),(-99999,-99999))

# test routine
if __name__ == "__main__":
  #example ()
  searchStations ()
