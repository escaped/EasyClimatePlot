import cPickle
import hashlib
import os

categories = ['temp','mintemp','maxtemp','windspeed','windgust','maxwindspeed','precipitation','visibility','dewpoint','pressure','seapressure']
def hashName (name):
  return hashlib.md5 (name).hexdigest ()

class Data:
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

  def availableCategories (self):
    return self.data.keys ()

  def addCategory (self, category, data):
    self.data[category] = data

  def save (self, path):
    cPickle.dump (self, open(os.path.join (path, hashName (self.name)),'w+'))

  def getData (self, category, resolution = 'm'):
    # return the category according to the given resolution
    if resolution == 'm':
        dat = self.data[category]
        counter = [0,0,0,0,0,0,0,0,0,0,0,0]
        tmpdata = [0,0,0,0,0,0,0,0,0,0,0,0]
        
        for key, value in dat:
            print key
            print value
        
    return None

def loadDataObject (path, name):
  return cPickle.load (os.path.join (path, hashName (name)))
