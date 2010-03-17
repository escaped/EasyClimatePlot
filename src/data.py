import cPickle
import hashlib
import os
import calendar
import multidict

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

  minDate = "YYYYMMDD"
  maxDate = "YYYYMMDD"

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
    # TODO min und max date einfuegen
    '''
    _minDate = dates.min()
    _maxDate = dates.max()
    
    if _minDate < self.minDate:
        self.minDate = _minDate
    
    if _maxDate > self.maxDate:
        self.maxDate = _maxDate
    '''
    
  def __getstate__(self):
      return self.data
  
  def __setstatte__(self, d):
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
