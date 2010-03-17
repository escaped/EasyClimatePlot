import cPickle
import datetime
import hashlib
import os
import calendar
import utils

categories = ['temp','mintemp','maxtemp','windspeed','windgust','maxwindspeed','precipitation','visibility','dewpoint','pressure','seapressure']
def hashName (name):
  return hashlib.md5 (name).hexdigest ()

class Data:

  # NOTE: all membervariables are overridden in the constructor __init__ !
  name = ""
  coord = (0,0) 

  # data: field of data
  data = {}
  cache = {}

  minDate = datetime.date (datetime.MAXYEAR, 1, 1)
  maxDate = datetime.date (datetime.MINYEAR, 1, 1)

  # lists incomplete data
  incomplete = {}

  # ctor
  def __init__ (self, name, coords):
    self.name = name
    self.coords = coords
    self.data = {}
    self.cache = {}
    self.incomplete = {}

  def availableCategories (self):
    return self.data.keys ()

  def addCategory (self, category, data): 
    self.data[category] = data
    dates = data.keys()
    dates.sort()

    # convert dates to integer
    dates = [int (x) for x in dates]

    # convert
    mi = int (min (dates))
    ma = int (max (dates))
    # TODO das sollte wohl irgendwo anders hin?
    _minDate = datetime.date (datetime.MAXYEAR, 1, 1)
    _maxDate = datetime.date (datetime.MINYEAR, 1, 1)
    try:
      _minDate = datetime.date (mi % 10000, mi % 10000 / 100, mi % 100) 
      _maxDate = datetime.date (ma % 10000, ma % 10000 / 100, ma % 100)
    except ValueError:
      print "Date corrupt: ", mi

    if _minDate < self.minDate:
        self.minDate = _minDate
    
    if _maxDate > self.maxDate:
        self.maxDate = _maxDate

  def __getstate__(self):
      return self.data
  
  def __setstate__(self, d):
      self.data = d

  def save (self, path):
    pass
    # cPickle.dump(self, open(os.path.join (path, hashName (self.name)),'w+'))
    
  def _getData(self):
      return self.data
  
  def getData (self, category, resolution = 'm'):
    # return the category according to the given resolution
    if resolution == 'm':
        dat = self.data[category]
        dates = dat.keys()
        dates.sort()
        counter = [0,0,0,0,0,0,0,0,0,0,0,0]
        tmpdata = [0,0,0,0,0,0,0,0,0,0,0,0]        
        
        for date in dates:
            index = int(date[4:6])-1 #month
            tmpdata[index] += dat[date]
            counter[index] += 1
        
        for index in range(0,12):
            tmpdata[index] /= counter[index]
            
        if category == 'precipitation':
            for index in range(0,12):
                tmpdata[index] *= calendar.mdays[index+1]

        return tmpdata
            
        
    return None

def loadDataObject (path, name):
    pass
  # return cPickle.load(os.path.join (path, hashName (name)))
