import datetime
import calendar

categories = ['temp','mintemp','maxtemp','windspeed','windgust','maxwindspeed','precipitation','visibility','dewpoint','pressure','seapressure']

class Data:
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
