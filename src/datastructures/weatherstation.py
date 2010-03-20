# fields (i omit ST = State)
fields = {"USAF": (0,6), "WBAN":(7,12), "STATION NAME":(13,43), "CTRY WMO":(43,45),
    "CTRY FIPS":(46,48), "CALL":(52,54), "LAT":(59,64), "LON":(65,72), "ELEV":(73,79)}

class WeatherStation (object):
  # USAF = Air Force Datsav3 station number
  usaf = ""
  # WBAN = NCDC WBAN number
  wban = ""

  station_name = ""

  # Historical WMO Country ID
  ctry_wmo = ""
  # FIPS Country ID
  ctry_fips = ""
  # LAT = Latitude in thousandths of decimal degrees
  lat = ""
  # LON = Longitude in thousandths of decimal degrees
  lon = ""
  # ELEV = Elevation in tenths of meters
  elev = ""

  # ctor parses one line of ish-history.txt
  # TODO das geht sicher mit weniger code
  def __init__(self, line):
    self.usaf         = line[int (fields["USAF"][0])        :int(fields["USAF"][1])]
    self.wban         = line[int (fields["WBAN"][0])        :int(fields["WBAN"][1])]
    self.station_name = line[int (fields["STATION NAME"][0]):int(fields["STATION NAME"][1])]
    self.ctry_wmo     = line[int (fields["CTRY WMO"][0])    :int(fields["CTRY WMO"][1])]
    self.ctry_fips    = line[int (fields["CTRY FIPS"][0])   :int(fields["CTRY FIPS"][1])]
    try:
      self.lat          = float(line[int (fields["LAT"][0]) :int(fields["LAT"][1])]) / 1000
      self.lon          = float(line[int (fields["LON"][0]) :int(fields["LON"][1])]) / 1000
      self.elev         = float(line[int (fields["ELEV"][0]):int(fields["ELEV"][1])])
    except ValueError:
      # If this happens, one of the upper values was empty. We don't care about that.
      pass

def weatherStationDictionary (line):
  station = {}
  station["usaf"]         = line[int (fields["USAF"][0])        :int(fields["USAF"][1])]
  station["wban"]         = line[int (fields["WBAN"][0])        :int(fields["WBAN"][1])]
  station["station_name"] = line[int (fields["STATION NAME"][0]):int(fields["STATION NAME"][1])]
  station["ctry_wmo"]     = line[int (fields["CTRY WMO"][0])    :int(fields["CTRY WMO"][1])]
  station["ctry_fips"]    = line[int (fields["CTRY FIPS"][0])   :int(fields["CTRY FIPS"][1])]
  station["lat"]          = 0
  station["lon"]          = 0
  station["elev"]         = 0
  try:
    station["lat"]          = float(line[int (fields["LAT"][0]) :int(fields["LAT"][1])]) / 1000
    station["lon"]          = float(line[int (fields["LON"][0]) :int(fields["LON"][1])]) / 1000
    station["elev"]         = float(line[int (fields["ELEV"][0]):int(fields["ELEV"][1])])
  except ValueError:
    # If this happens, one of the upper values was empty. We don't care about that.
    pass

  return station

