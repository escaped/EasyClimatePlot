# fields (i omit ST = State)
fields = {"USAF": (0,5), "WBAN":(7,11), "STATION NAME":(13,43), "CTRY WMO":(43,44),
    "CTRY FIPS":(46,47), "CALL":(52,53), "LAT":(59,63), "LON":(65,71), "ELEV":(73,78)}

class WeatherStation (object):
  usaf = ""
  wban = ""
  station_name = ""
  ctry_wmo = ""
  ctry_fips = ""
  lat = ""
  lon = ""
  elev = ""

  # ctor gets one line of ish-history.txt
  def __init__(self, line):
    self.usaf         = line[int (fields["USAF"][0]):int(fields["USAF"][1])]
    self.wban         = line[int (fields["WBAN"][0]):int(fields["WBAN"][1])]
    self.station_name = line[int (fields["STATION NAME"][0]):int(fields["STATION NAME"][1])]
    self.ctry_wmo     = line[int (fields["CTRY WMO"][0]):int(fields["CTRY WMO"][1])]
    self.ctry_fips    = line[int (fields["CTRY FIPS"][0]):int(fields["CTRY FIPS"][1])]
    self.lat          = line[int (fields["LAT"][0]):int(fields["LAT"][1])]
    self.lon          = line[int (fields["LON"][0]):int(fields["LON"][1])]
    self.elev         = line[int (fields["ELEV"][0]):int(fields["ELEV"][1])]
