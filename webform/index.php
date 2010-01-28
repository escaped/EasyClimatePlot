<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="de">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>NOAA Parser</title>
		<meta name="author" content="Nathan Borror">
 		<link rel="stylesheet" href="css/boilerplate.css" type="text/css" media="screen" charset="utf-8">
		<link rel="stylesheet" href="css/plugins.css" type="text/css" media="screen" charset="utf-8">
		<!--[if lte IE 6]>
			<link rel="stylesheet" href="css/ie.css" type="text/css" media="screen" charset="utf-8">
		<![endif]-->
	</head>

	<body>
		<form class="hform" method="post" action="index.php" style="width: 500px">
			<fieldset>
				<legend>Formular</legend>
				<p>
					<label for="file">Datei</label>
					<input type="file" name="file" id="file" />
				</p>
				<p>
					<label for="starttime">Startzeit:</label>
					<input type="text" name="starttime" id="starttime" value="YYYYMMDD" />
				</p>					
				<p>
					<label for="endtime">Endzeit:</label>
					<input type="text" name="endtime" id="endtime" value="YYYYMMDD" />
				<p>Daten</p>
				<p class="checkbox">					
					<input type="checkbox" id="precipitation" name="data[precipitation]" />
					<label for="precipitation">Niederschlag</label>				
				</p>					
				<p class="checkbox">
					<input type="checkbox" id="temp" name="data[temp]" />
					<label for="temp">Temperatur</label>
				</p>						
				<p class="checkbox">
					<input type="checkbox" id="maxtemp" name="data[maxtemp]" />
					<label for="maxtemp">max. Temperatur</label>
				</p>
				<p class="checkbox">
					<input type="checkbox" id="mintemp" name="data[mintemp]" />
					<label for="mintemp">min. Temperatur</label>
				</p>
				<p class="checkbox">
					<input type="checkbox" id="windspeed" name="data[windspeed]" />
					<label for="windspeed">Windgeschwindigkeit</label>
				</p>
				<p class="checkbox">
					<input type="checkbox" id="windgust" name="data[windgust]" />
					<label for="windgust">B&ouml;hen</label>
				</p>
				<p class="checkbox">
					<input type="checkbox" id="maxwindspeed" name="data[maxwindspeed]" />
					<label for="maxwindspeed">max. Windgeschwindigkeit</label>
				</p>
			</fieldset>		
			<p><input type="submit" name="start" value="send" /></p>			
		</form>

	</body>
</html>
