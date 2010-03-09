import cPickle
import hashlib
import os

categories = ['TEMP','MAXTEMP','MINTEMP','WIND','MAXWIND','GUST']
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

  def getData (self, category, resolution):
    # return the category according to the given resolution
    return self.data

def loadDataObject (path, name):
  return cPickle.load (os.path.join (path, hashName (name)))
