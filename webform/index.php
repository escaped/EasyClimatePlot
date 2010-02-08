<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="de">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>NOAA Extractor</title>
		<meta name="author" content="Alexander Frenzel">
 		<link rel="stylesheet" href="css/boilerplate.css" type="text/css" media="screen" charset="utf-8">
		<link rel="stylesheet" href="css/plugins.css" type="text/css" media="screen" charset="utf-8">
		<link rel="stylesheet" href="css/notices.css" type="text/css" media="screen" charset="utf-8">
		<!--[if lte IE 6]>
			<link rel="stylesheet" href="css/ie.css" type="text/css" media="screen" charset="utf-8">
		<![endif]-->
		
		<link rel="stylesheet" href="css/main.css" type="text/css" media="screen" charset="utf-8">
	</head>

	<body>
		<h1>NOAA Extractor</h1>
		<h2>Anleitung</h2>
		<ol>
			<li>Wähle deine Station <a href="http://gis.ncdc.noaa.gov/website/ims-cdo/gsod/viewer.htm">hier</a> aus</li>
			<li>Lade die entsprechende .txt-Datei herunter und stelle sicher, dass bei &ldquo;<b>Selected Output Format</b>&rdquo; &ldquo;Comma Delimited&rdquo; ausgewählt ist.</li>
			<li>W&auml;hle im Formular die Datei aus.</li>
			<li>Gebe die Start und Endzeit an. (Format: YYYYMMDD z.B. 19461201 für 01.12.1946)</li>
			<li>W&auml;hle die Daten aus, die du in der Resultierenden Datei haben möchtest.</li>
			<li>Schicke das Formular ab. Eventuelle Fehler/Probleme, werden angezeigt.</li>
		</ol>
<?php
	// do a cleanup in downloaddir
	foreach (glob('download/*.*') as $file) {
		if (filemtime($file) < time()-(3*24*60*60)) {
			// remove after 3 days
			unlink($file);
		}		
	}
	
	$msg = array();
	if (!empty($_POST['send'])) {
		
		// check input
		// date
		if (!preg_match('/\d{8}/', $_POST['endtime'])) {
			$msg[] = 'Bitte &uuml;berpr&uuml;fe die Endzeit.';
		}
		if (!preg_match('/\d{8}/', $_POST['starttime'])) {
			$msg[] = 'Bitte &uuml;berpr&uuml;fe die Startzeit.';
		}
		if (count($_POST['data']) <= 0) {
			$msg[] = 'W&auml;hle min. einen Datentyp aus.';
		}
		if (empty($_FILES['file']['name']))
			$msg[] = 'Bitte w&auml;hle eine Datei aus.';		
			
		if (count($msg) == 0) {
			// create CLI Parameter Array for verification
			$argv[] = 'noaa.php';
			$argv[] = 'test';
			$argv[] = '-i';
			$argv[] = $_FILES['file']['tmp_name'];
			$argv[] = '-v';
			$argv[] = 'mi'; // show missing years
			$argv[] = '-v';
			$argv[] = 'cy'; // complete years
			$argv[] = '-v';
			$argv[] = 'cm'; // complete months
			$argv[] = '-v';
			$argv[] = 'y';
			$argv[] = '-v';
			$argv[] = 'm';			
			foreach ($_POST['data'] as $key => $value) {
				$argv[] = '-t';
				$argv[] = $key;
			}			
			ob_start();
			require_once('noaa.php');
			$test_output = ob_get_contents();
			ob_end_clean();
			
			$argv = array();
			// create CLI Parameter Array for extraction
			$filename = 'download/'.rand().rand().'_'.$_FILES['file']['name'];	
			$argv[] = 'noaa.php';
			$argv[] = 'extract';
			$argv[] = '-convert';
			$argv[] = '-inv';
			$argv[] = '-s';
			$argv[] = $_POST['starttime'];
			$argv[] = '-e';
			$argv[] = $_POST['endtime'];
			$argv[] = '-i';
			$argv[] = $_FILES['file']['tmp_name'];
			$argv[] = '-o';
			$argv[] = $filename; 
			foreach ($_POST['data'] as $key => $value) {
				$argv[] = '-t';
				$argv[] = $key;
			}			
			ob_start();
			$noaa = new NOAAParser($argv); // do Output
			$calc_output = ob_get_contents();
			ob_end_clean();
?>
<p>&nbsp;</p>
<h3><a name="ergebnis">Ergebnisse</a></h3>
<ul>
	<li>Unter <a href="#hinweis">Hinweise</a> werden fehlerhafte oder unvollständige Daten angezeigt, die ignoriert wurden.</li>
	<li>Unter <a href="#info">zus&auml;tzliche Informationen</a>, werden allg. Aussagen über die vollständigkeit der DAten getroffen. </li>
	<li><a href="<?=$filename?>">Textdatei herunterladen</a> (Datei wird nach ca. 3 Tagen gel&ouml;scht.)</li>
</ul>

<p>&nbsp;</p>
<h3><a name="hinweis">Hinweise</a></h3>
<p><a href="#ergebnis">zur&uuml;ck zu den Ergebnissen</a></p>
<p><?=str_replace("\n", '<br />', $calc_output)?></p>
				
<h3><a name="info">zus&auml;tzliche Informationen:</a></h3>";
<p><a href="#ergebnis">zur&uuml;ck zu den Ergebnissen</a></p>
<p><?=str_replace("\n", '<br />', $test_output)?></p>
<p><a href="#ergebnis">zur&uuml;ck zu den Ergebnissen</a></p>

<?php
		}
 	}

	if (empty($_POST['send']) || count($msg) > 0) {
		foreach ($msg as $m) {
			echo '<p class="error">'.$m.'</p>';
		}
?>
		<form class="hform" method="post" action="index.php" enctype="multipart/form-data"  style="width: 500px">
			<fieldset>
				<legend>Formular</legend>
				<p>
					<label for="file">Datei</label>
					<input type="file" name="file" id="file" />
				</p>
				<p>
					<label for="starttime">Startzeit:</label>
					<input type="text" name="starttime" id="starttime" value="<?=(!empty($_POST['starttime']))?$_POST['starttime']:'YYYYMMDD'?>" />
				</p>					
				<p>
					<label for="endtime">Endzeit:</label>
					<input type="text" name="endtime" id="endtime" value="<?=(!empty($_POST['endtime']))?$_POST['endtime']:'YYYYMMDD'?>" />
				<p>&nbsp;</p>
				<p><label>Datentyp:</label></p>
				<p class="checkbox">					
					<input type="checkbox" id="precipitation" name="data[precipitation]" <?=(!empty($_POST['data']['precipitation']))?'checked="checked"':''?> />
					<label for="precipitation">Niederschlag</label>				
				</p>					
				<p class="checkbox">
					<input type="checkbox" id="temp" name="data[temp]" <?=(!empty($_POST['data']['temp']))?'checked="checked"':''?> />
					<label for="temp">Temperatur</label>
				</p>						
				<p class="checkbox">
					<input type="checkbox" id="maxtemp" name="data[maxtemp]" <?=(!empty($_POST['data']['maxtemp']))?'checked="checked"':''?> />
					<label for="maxtemp">max. Temperatur</label>
				</p>
				<p class="checkbox">
					<input type="checkbox" id="mintemp" name="data[mintemp]" <?=(!empty($_POST['data']['mintemp']))?'checked="checked"':''?> />
					<label for="mintemp">min. Temperatur</label>
				</p>
				<p class="checkbox">
					<input type="checkbox" id="windspeed" name="data[windspeed]" <?=(!empty($_POST['data']['windspeed']))?'checked="checked"':''?> />
					<label for="windspeed">Windgeschwindigkeit</label>
				</p>
				<p class="checkbox">
					<input type="checkbox" id="windgust" name="data[windgust]" <?=(!empty($_POST['data']['windgust']))?'checked="checked"':''?> />
					<label for="windgust">B&ouml;hen</label>
				</p>
				<p class="checkbox">
					<input type="checkbox" id="maxwindspeed" name="data[maxwindspeed]" <?=(!empty($_POST['data']['maxwindspeed']))?'checked="checked"':''?> />
					<label for="maxwindspeed">max. Windgeschwindigkeit</label>
				</p>
			</fieldset>		
			<p><input type="submit" name="send" value="send" /></p>			
		</form>
<?php
	}
?>
	</body>
</html>
