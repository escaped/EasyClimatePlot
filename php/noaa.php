#!/usr/bin/php
<?php
function leapYear($year){
 if ($year % 400 == 0 || ($year % 4 == 0 && $year % 100 != 0)) return TRUE;
 return FALSE;
}

function daysInMonth($month = 0, $year = ''){
 $days_in_month    = array(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
 $d = array("Jan" => 31, "Feb" => 28, "Mar" => 31, "Apr" => 30, "May" => 31, "Jun" => 30, "Jul" => 31, "Aug" => 31, "Sept" => 30, "Oct" => 31, "Nov" => 30, "Dec" => 31);
 if(!is_numeric($year) || strlen($year) != 4) $year = date('Y');
 if($month == 2 || $month == 'Feb'){
  if(leapYear($year)) return 29;
 }
 if(is_numeric($month)){
  if($month < 1 || $month > 12) return 0;
  else return $days_in_month[$month - 1];
 }
 else{
  if(in_array($month, array_keys($d))) return $d[$month];
  else return 0;
 }
}

$DATA_TYPES = array('temp','mintemp','maxtemp','windspeed','windgust','maxwindspeed',
					'precipitation','visibility','dewpoint','pressure','seapressure');
class DataProcessing {
	var $DATA_COL = array(
						'date' => 2,
						'temp' => 3,
						'mintemp' => 18,
						'maxtemp' => 17,
						'windspeed' => 13,
						'windgust' => 16,
						'maxwindspeed'  => 15,
						'precipitation' => 19,
						'visibility' => 11,
						'dewpoint' => 5,
						'pressure' => 9,
						'seapressure' => 7
					);
	var $DATA_INV = array (
						'temp' => 9999.9,
						'mintemp' => 9999.9,
						'maxtemp' => 9999.9,
						'windspeed' => 999.9,
						'windgust' => 999.9,
						'maxwindspeed'  => 999.9,
						'precipitation' => 99.99,
						'visibility' => 999.9,
						'dewpoint' => 9999.9,
						'pressure' => 9999.9,
						'seapressure' => 9999.9
					);
	var $DATA_TRANS = array (
						'temp' => 'T',
						'mintemp' => 'T',
						'maxtemp' => 'T',
						'windspeed' => 'S',
						'windgust' => 'S',
						'maxwindspeed'  => 'S',
						'precipitation' => 'N',
						'visibility' => 999.9,
						'dewpoint' => 9999.9,
						'pressure' => 9999.9,
						'seapressure' => 9999.9
					);
	
	function c_F2C($value) {
		return  ($value - 32) * (5/(float)9);
	}
	
	function c_mb2hPa($value) {
		return $value; // 1mb = 1hPa
	}
	
	function c_miles2km($value) {
		return $value * 1.609;
	}
	
	function c_knots2ms($value) {
		return $value * 0.51;
	}
	
	function c_inch2mm($value) {
		return $value * 25.4;
	}
	
	function getData($type, array $data, $convert = false) {
		global $DATA_TYPES;
		if (!in_array($type, $DATA_TYPES)) {
			echo "Warning: invalid type suplied: $type\n";
			return null;
		}
		$value = $data[$this->DATA_COL[$type]];
		$value = trim($value);
		$value = str_replace('*', '', $value);

		// validate
		if ($type == 'precipitation') {
			if (strpos($value,'I') || strpos($value,'H')) // treat as invalid
				return false;
					
			// strip Chars
			$result = null;
			preg_match('/(\\d+\\.\\d+)/', $value, $result);			
			if (count($result) < 2) {
				echo "Warning: No number found in precipitation: $value\n";
				return false;
			}
			$value = (float)$result[1];
		}	
		if (!is_numeric($value) || $value == $this->DATA_INV[$type]) {
			return false;
		}
		// transform $value
		if ($convert) {
			switch($type) {
				case 'temp':
				case 'mintemp':
				case 'maxtemp':
				case 'dewpoint':
					$value = $this->c_F2C($value);				
					break;
				case 'windspeed':
				case 'windgust':
				case 'maxwindspeed':
					$value = $this->c_knots2ms($value);
					break;
				case 'precipitation':
					$value = $this->c_inch2mm($value);
					break;
				case 'visibility':
					$value = $this->c_miles2km($value);
					break;			
				case 'pressure':
				case 'seapressure':
					$value = $this->c_mb2hPa($value);
					break;
			}
		}
		return $value;
	}
	
	function getYear(array $data) {
		$str = $data[$this->DATA_COL['date']];
		return substr($str,0,5);
	}
	
	function stripZero($m) {
		return ($m[0] == '0') ? $m[1] : $m;
	}
	
	function getMonth(array $data) {
		$str = $data[$this->DATA_COL['date']];		
		return ($str / 100) % 100;
	}
	
	function getDay(array $data) {
		$str = $data[$this->DATA_COL['date']];
		return substr($str,7,2);
	}
}

class Config {
		var $starttime = 0;
		var $endtime = 'INF';
		var $types = array();
		var $mode = 'm';
		var $filename = null;	
		var $output = null;
		var $showCompleteMonths = false;
		var $showCompleteYears = false;
		var $showIncompleteMonths = false;
		var $showIncompleteYears = false;
		var $showMissingYears = false;
		var $convert = false;
		var $digits = 2;
		var $comma = false;
		var $invalid = false;
		
		function parse($args) {
			for ($i = 2; $i < count($args); $i++) {
				switch ($args[$i]) {
					case '-v': // show incomplete
						$i++;
						if ($args[$i] == 'y') 
							$this->showIncompleteYears = true;
						else if ($args[$i] == 'm')
							$this->showIncompleteMonths = true;
						else if ($args[$i] == 'cy') 
							$this->showCompleteYears = true;
						else if ($args[$i] == 'cm')
							$this->showCompleteMonths = true;
						else if ($args[$i] == 'mi')
							$this->showMissingYears = true;
						else
							echo "Warning: invalid verbose mode: {$args[$i]}\n";
						break;
						
					case '-s': // starttime
						$i++;
						if (preg_match('/[12]\d{3}\d{2}\d{2}/', $args[$i]))
							$this->starttime = $args[$i];
						else
							echo "Warning: invalid starttime: {$args[$i]}\n";
						break;
						
					case '-e': // endtime
						$i++;
						if (preg_match('/[12]\d{3}\d{2}\d{2}/', $args[$i]))	
							$this->endtime = $args[$i];
						else
							echo "Warning: invalid endtime: {$args[$i]}\n";
						break;
						
					case '-t':
						$i++; // type
						global $DATA_TYPES;
						if (in_array($args[$i], $DATA_TYPES))
							$this->types[$args[$i]] = true;
						else if ($args[$i] == 'all') {
							foreach ($DATA_TYPES as $type) {
								$this->types[$type] = true;
							}
						} else
							echo "Warning: invalid type supplied: {$args[$i]}\n";
						break;
	
					case '-m': // mode
						$i++;
							if ($args[$i] == 'm')
							$this->mode = 'm';
						else if ($args[$i] == 'y')
							$this->mode = 'y';
						else 
							echo "Warning: invalid mode supplied: {$args[$i]}\n";
						break;
						
					case '-i':
						$i++;
						if (is_file($args[$i]))
							$this->filename = $args[$i];
						else
							echo "Warning: invalid inputfile  {$args[$i]}\n";
						break;
						
					case '-o':
						$i++;
						if (!is_file($args[$i])) 
							$this->output = $args[$i];
						else {
							$this->output = $args[$i];
							echo "Warning: outputfile exists {$args[$i]}\n";
						}
						break;
					
					case '-d':
						$i++;
						if (is_numeric($args[$i]))
							$this->digits = (int)$args[$i];
						else
							echo "Warning: invalid number for decimal digits: {$args[$i]}\n";
						break;
						
					case '-convert':
						$this->convert = true;
						break;
						
					case '-inv':
						$this->invalid = true;
						break;
					
					case '-comma':
						$this->comma = true;
						break;
						
					default:
							echo "Warning: invalid option: {$args[$i]}\n";
						break;
				}
			}						
		}		
	}
	class NOAAParser {			
		var $filecontents;
		var $task;
		var $config;
		var $result;
		
		function checkRequirements() {
			// need input file and output file
			if (!is_file($this->config->filename)) {
				echo 'Error: please specify an input file.'."\n";
				die();
			}
		}
		
		function __construct($args) {
			$this->task = $args[1]; 
			$this->config = new Config();
			$this->config->parse($args);

			switch ($this->task) {
				case 'test':
					$this->checkRequirements();
					echo "-- load file: {$this->config->filename}\n";
					$this->loadFile($this->config->filename);
					echo "-- validate file\n";
					$this->validateFile();
					echo "-- ready\n";
					echo "----\n";
					break;
				case 'process':
					$this->checkRequirements();
					echo "-- load file: {$this->config->filename}\n";
					$this->loadFile($this->config->filename);
					echo "-- validate file\n";
					$this->validateFile();
					echo "-- process data\n";
					$this->processData();
					echo "-- save data\n";
					$this->saveData();
					echo "-- ready\n";
					echo "----\n";
					break;
				case 'extract':
					$this->checkRequirements();
					echo "-- load file: {$this->config->filename}\n";
					$this->loadFile($this->config->filename);
					echo "-- validate file\n";
					$this->validateFile();
					echo "-- process data (extract)\n";
					$this->extractData();
					echo "-- save data\n";
					$this->saveData();
					echo "-- ready\n";
					echo "----\n";
					break;
				case 'help': 
					global $DATA_TYPES;
					echo 'Usage:'."\n";
					echo 'help                                                     - Display help'."\n";
					echo 'test [-v|-i]                                             - Test input Data'."\n";					
					echo 'process [-v|-s|-e|-t|-m|-i|-o|-comma|-d|-convert|-inv]   - Calc arithmetic average of specified data'."\n";
					echo 'extract [-v|-s|-e|-t|-m|-i|-o|-comma|-d|-convert|-inv]   - Extract specified Data'."\n";
					echo "\n";
					echo 'Options: '."\n";
					echo '  Use as many options as you want. On Duplikate the last one will be used.'."\n";
					echo "\n";
					echo '      -v <type>               - y -> Show incomplete years'."\n";
					echo '                                m -> Show incomplete months'."\n";
					echo '                                cy -> Show complete years'."\n";
					echo '                                cm -> Show complete months'."\n";
					echo '                                mi -> missing Years'."\n";
					echo '      -s <starttime>          - start date in YYYYMMDD'."\n";
					echo '      -e <endtime>            - end date in YYYYMMDD'."\n";
					echo '      -t <type>               - If not set no data will processed.'."\n";
					echo '                                Possible types: '."\n";
					echo '                                    ';
					foreach ($DATA_TYPES as $type) echo $type.', ';
					echo "\n";
					echo '                                    all -> process all data. overrides different -t options'."\n";
					echo '      -convert                - convert units to °C, m/s, km, mm'."\n";
					echo '      -comma                  - use , instead of . for decimal numbers'."\n";
					echo '      -m <mode>               - m -> monthly'."\n";
					echo '                                y -> yearly'."\n";
					echo '      -d <number>             - max. decimal digits. default: 2'."\n";
					echo '      -inv                    - mark empty DataSets with "Inv" instead of 0'."\n";
					echo '      -i <inputfile>          - Inputfile'."\n";
					echo '      -o <outputfile>         - Outputfile'."\n";
					break;
				default:
					echo 'ERROR: Invalid Arguments! see help for more info.'."\n";
			}
		}
		
		function loadFile($filename) {
			if (!is_file($filename))
				throw new Exception('Error: File does not exist: '.$filename."\n");
				
			$this->content = file($filename);
		}

		function validateFile() {
			if (empty($this->content))
				throw new Exception('Error: File is empty'."\n");
				
			$years = array();			
			$first = true;
			foreach ($this->content as $line) {
				if ($first) {
					$first = false;
					continue;
				}
			
				// parse each line
				$data = explode(',',$line);

				// split date
				$tmp = trim($data[2]);
				$year = substr($tmp,0,4);
				$month = substr($tmp,4,2);
				$day = substr($tmp,6,2);
				
				// create Tree
				$years[$year][$month][$day] = 1;				
			}
			// sort by key
			ksort($years);

			if ($this->config->showMissingYears) {			
				$last = nil;
				$start = nil;
				$serien = array();
				foreach ($years as $year => $v) {
					if ($last == nil) {
						$last = $year;
						$start = $year;
						continue;
					}
					$last++;
					if ($last != $year) {
						$serien[] = "$start - $last; ".($last-$start)." years";
						for ($i = $last; $i < $year; $i++) {
							echo "Warning: $i: no data found.\n";
						}
						$last = $year;
						$start = $year;
					}
				}
				$serien[] = "$start - $last; ".($last-$start)." years";
				echo "Serien:\n";
				foreach($serien as $serie) {
					echo "\t$serie\n";
				}
			}
			
			// test Tree
			$invYears = array();
			$invMonths = array();
			$valYears = array();
			$valMonths = array();
			foreach($years as $year => $months) {
				$error = false;
				if (count($months) < 12) {					
					$invYears[$year] = count($months); 
				} else
					$valYears[] = $year;
					
				foreach($months as $month => $days) {
					if (daysInMonth($month,$year) != count($days)) {											
						$invMonths[$year][$month][0] = daysInMonth($month,$year);
						$invMonths[$year][$month][1] = count($days);
					} else
						$valMonths[$year][] = $month;
				}
			}
			if ($this->config->showIncompleteYears) {
				foreach ($invYears as $year => $months) 
					echo "$year\t is incomplete. only $months months.\n";
			}
			if ($this->config->showIncompleteMonths) {
				foreach ($invMonths as $year => $v1) {
					foreach ($invMonths[$year] as $month => $days) {
						echo "$year/$month\t is incomplete. only {$days[1]} of {$days[0]} days.\n";	
					}
				}
			}
			
			if ($this->config->showCompleteYears) {
				foreach ($valYears as $year) 
					echo "$year\t is complete.\n";
			}
			if ($this->config->showCompleteMonths) {
				foreach ($valMonths as $year => $v1) {
					foreach ($valMonths[$year] as $month) {
						echo "$year/$month\t is complete.\n";	
					}
				}
			}
		}
		
		function processData() {
			global $DATA_TYPES;
			$sum = array();
			$counter = array();
			$process = new DataProcessing();
			$first = true;
			echo "-- parse data\n";
			foreach ($this->content as $line) {
				if ($first) {
					$first = false;
					continue;
				}
				$data = explode(',', $line); 
				if ($data[2] < $this->config->starttime || $data[2] > $this->config->endtime)
					continue; // ignore line
				
				foreach ($this->config->types as $type => $processType) { // iterate types
					if ($processType) {
						$value = $process->getData($type, $data, $this->config->convert); // get data
						if ($value !== false) { // valid data?
							switch ($this->config->mode) { // set index
								case 'm':	
									$index = $process->stripZero($process->getMonth($data));
									break;
								case 'y':	
									$index = $process->getYear($data);
									break;
								default:
									$index = 'invalid';
									break;
							}
							//echo $type.": $index: $value\n";
							$sum[$index][$type] += $value;
							$counter[$index][$type]++;
						} else {
							echo "Warning: invalid or missing '$type' data in ".$process->getYear($data)."".$process->getMonth($data)."".$process->getDay($data)."\n";
							if (!isset($sum[$index][$type]))
								$sum[$index][$type] = 0;
						}
					}
				}			
			}
			echo "-- calculations\n";
			foreach($sum as $index => $v1) {
				foreach($sum[$index] as $type => $v2) {
					if ($counter[$index][$type] != 0) {
						$this->result[(string)$index][$type] = $sum[$index][$type]/$counter[$index][$type];
						//echo "$index/$type: ".$sum[$index][$type]." /= ".$counter[$index][$type]." = ".$this->result[$index][$type]."\n";
					} else {
						if ($this->config->invalid)
							$this->result[(string)$index][$type] = 'Inv';
						echo "Warning: no data for type '$type' in";
						if ($this->config->mode == 'm') 
						 	echo " month: ";
						else 
							echo " year: ";
						echo "$index.\n";
					}
				}
			}
			echo "-- sort Array\n";
			ksort($this->result);
		}
		
		function extractData() {
			global $DATA_TYPES;
			$process = new DataProcessing();
			$first = true;
			echo "-- parse data\n";
			foreach ($this->content as $line) {
				if ($first) {
					$first = false;
					continue;
				}
				$data = explode(',', $line); 
				if ($data[2] < $this->config->starttime || $data[2] > $this->config->endtime)
					continue; // ignore line
				
				foreach ($this->config->types as $type => $processType) { // iterate types
					if ($processType) {
						$value = $process->getData($type, $data, $this->config->convert); // get data
						if ($value !== false) { // valid data?
							$month = $process->getMonth($data);
							$year = $process->getYear($data);
							$day = $process->getDay($data);
							
							$this->result[$year.$month.$day][$type] = $value;	
						} else {
							if ($this->config->invalid)
								$this->result[$year.$month.$day][$type] = 'Inv';
							echo "Warning: No data for '$type' in ".$process->getYear($data)."".$process->getMonth($data)."".$process->getDay($data)."\n";
						}
					}
				}			
			}
			if ($this->result)
				ksort($this->result);
		}
		
		function saveData() {
			$filename = $this->config->output;
			if (is_file($filename)) {
				echo 'Error: output file already exist. Skip saving...'."\n";
				return;
			} 
			if (empty($filename)) {
				echo 'Warning: no output (-o <filename>) specified. Using stdout:'."\n\n";
				$fh = STDOUT;
			} else {
				$fh = fopen($filename, 'w') or die("Error: Could not create File.\n");
			}
			if ($this->result) {
				$header = '#Date';

				foreach ($this->config->types as $type => $v) {
					$header .= "\t".$type;
				}
				fwrite($fh, $header."\n");
			
				// write data
				foreach ($this->result as $index => $v1) {
					fwrite($fh, $index);

					$count = 0;
					foreach ($this->result[$index] as $value) {
						$tmp = (is_numeric($value))?round($value, $this->config->digits):$value;
						$tmp = ($this->config->comma)?str_replace('.',',',$tmp):$tmp;
						fwrite($fh, "\t".$tmp);
						$count++;
					}
					if ($count != count($this->config->types)) {
						for ($i = $count; $i < count($this->config->types); $i++)
							fwrite($fh, "\t0.00");
					}
				
					fwrite($fh,"\n");
				} 
			} else {
					fwrite($fh,"No Data\n");
			}
			fclose($fh);
		}
	}



	echo "\n";
	echo 'NAOO txt parser by Alexander Frenzel'."\n";
	echo '------------------------------------'."\n";
	echo "\n";

	$noaa = new NOAAParser($argv);
?>
