from plugin import Plugin
import data
import main
import os
import sys
import ftplib
import gzip
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
  return no

def fileExistsInCache (f):
  f = os.path.basename (f)
  return not os.path.exists (os.path.join("cache","noaa", "%s" %f))

class NOAA (Plugin):
  name = "NOAA Plugin"
  desc = "NOAA Plugin"
  data = {}

  def downloadData (self, start, end):
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
    
    values = MultiDict()
    for line in lines:
      tmp = line.replace('*','').replace('\n','').split()
      date = tmp[DATA_COL['date']]
      for type in CAT:
        index = DATA_COL[type]
        if index != 2: # ignore date -> already parsed
            value = tmp[index]
            if value != DATA_INV[type]: # parse and convert data
                if type in ['temp', 'mintemp', 'maxtemp', 'dewpoint']:
                    values[type][date] = (float(value) - 32) * (5.0/9.0)
                elif type in ['windspeed', 'windgust', 'maxwindspeed']:
                    values[type][date] = float(value) * 0.51
                elif type == 'visibility':
                    values[type][date] = float(value) * 1.609
                elif type == 'precipitation':
                    pass
                    #values[type][date] = float(value) * 25.4
                else:
                    values[type, date] = float(value)
    
    # save to dataObject                
    for type in CAT:
        self.data.addCategory(type, values[type])
    
    print "everything is fine"
    
    # convert tmp/noaa to self.data
    # TODO insert conversion logic here
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
            open(os.path.join ("cache", "noaa", "%s" %filename), 'w+').write)
      except IOError:
        print "Missing directory cache/noaa"
        sys.exit (-1)
      except:
        print "%s doesn't exist." %filename
      print "waiting for 2 sec...."
      time.sleep (2)
    ftp.quit ()

  def listAvailableStations (self):
    # get ish-history
    self.getCountryList ()

    # read ish-history
    file = open (os.path.join("cache","noaa", "ish-history.txt"), 'r')
    content = file.readlines ()
    file.close ()
    # delete unneeded lines
    del content[0:20]

    stations = [weatherstation.WeatherStation (line) for line in content]
    
    # TODO weg damit
    print stations[0].station_name

    return stations

class MultiDict(dict):
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except:
            return self.setdefault(key, MultiDict()) 