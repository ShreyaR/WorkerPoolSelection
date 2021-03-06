<?php

/*
renderWorkflow0 and renderWorkflow1 must begin with the following:
  echo '<html><head></head><body>';
  echo '<form name="form" action="http://www.mturk.com/mturk/externalSubmit">' .
    '<input type="hidden" name="assignmentId" value="' . $assignmentId . '"/> ';
  echo '<input type="hidden" name="pn" value="'.$questionNumber .'"/>';
*/


function renderWorkflow0($assignmentId, $questionNumber) {
  $lines = explode("\n", file_get_contents('./questions'));
  $numberOfLines = count($lines) - 1;
  
  $line = explode("\t", $lines[$questionNumber * 4]);
  $start = $line[0];
  $end = $line[1];
  $text = $line[2];
  $choices = array($line[3], $line[4]);
  
  echo '<html><head></head><body>';
  echo '<form name="form" action="http://www.mturk.com/mturk/externalSubmit">' .
    '<input type="hidden" name="assignmentId" value="' . $assignmentId . '"/> ';
  echo '<input type="hidden" name="pn" value="'.$questionNumber .'"/>';
  
  $length = $end - $start;
  $object = '<b>' . substr($text, $start, $length) . '</b>';
  $text = substr_replace($text, $object, $start, $length);

  echo '<table border="1" bordercolor="blue"> <tr> <td>'. $text .
    '</td></tr><table><br/>';
  echo 'Which of the following Wikipedia articles defines the word "' . $object . 
    '" in <i>exactly</i> the way it is used in the above sentence? <br/><br/>';
  
  echo  ' <table>'; 
  
  $randomArray = generateRandomArray(count($choices));
  
  for ($i = 0; $i < count($choices); $i++){
    
    $option = ltrim(rtrim($choices[$randomArray[$i]]));
    
    echo '<tr><td valign="top">';
    echo '<input type="radio" name="vote" value="' . 
      $option . '"/></td><td>' . 
      '<a href="http://en.wikipedia.org/wiki/' . str_replace(' ', '_', $option) . 
      '" target="_blank">' . $option . 
      '</a>&nbsp<img src="external.png" height="10" width="10"/>' .
      '<br/>';
    echo '<i>http://en.wikipedia.org/wiki/' . str_replace(' ', '_', $option) .
      '</i><br/>';
    echo wikidefinition(str_replace(' ', '_', $option)) . 
      '...<br/><br/></td></tr>';
  }
  
  echo '</tr><table><br/><br/>';
  echo '<input type="submit"/>';
  echo '</form></body></html>';
}

function renderWorkflow1($assignmentId, $questionNumber) {
  $lines = explode("\n", file_get_contents('./questions'));
  $numberOfLines = count($lines) - 1;
  
  $line = explode("\t", $lines[$questionNumber * 4]);
  $start = $line[0];
  $end = $line[1];
  $text = $line[2];
  $wikichoices = array($line[3], $line[4]);
  $choices = array($lines[$questionNumber * 4 + 1], 
		   $lines[$questionNumber * 4 + 2]);
  
  echo '<html><head></head><body>';
  echo '<form name="form" action="http://www.mturk.com/mturk/externalSubmit">' .
    '<input type="hidden" name="assignmentId" value="' . $assignmentId . '"/> ';
  echo '<input type="hidden" name="pn" value="'.$questionNumber .'"/>';
  $length = $end - $start;
  $object = '<b>' . substr($text, $start, $length) . '</b>';
  $text = substr_replace($text, $object, $start, $length);

  echo '<table border="1" bordercolor="blue"> <tr> <td>'. $text .
    '</td></tr><table><br/>';
  echo 'Which of the following sets of tags best describes the word "' . $object . 
    '" in the way it is used in the above sentence? ' .
    '<br/><br/>';
  echo  ' <table border="1" bordercolor="black">'; 

  $randomArray = generateRandomArray(count($choices));

  for ($i = 0; $i < count($choices); $i++){
    $tags = explode(",", $choices[$randomArray[$i]]);
    echo '<tr><td valign="top">';
    echo '<input type="radio" name="vote' . 
      '" value="' . $wikichoices[$randomArray[$i]] . '"/></td>';
    echo '<td>';
    for ($j = 0; $j < min(count($tags), 7); $j++) {
      $tagsarray = explode("/", $tags[$j]);
      echo $tagsarray[count($tagsarray) -1] . '<br/>';
    }

    echo '</td></tr>';
  }
  
  echo '</tr></table><br/><br/>';
  echo '<input type="submit"/>';  
  echo '</form></body></html>';

}

function renderNoWorkflow() {
  echo '<html><head></head><body>';
  echo 'Unfortunately, you have completed all available tasks at this time.';
  echo 'Please try again later.';
  echo '</form></body></html>';
}

function renderPreview(){
  echo '<html><head></head><body>';
  echo 'You will be asked a question involving Named Entity Recognition';
  echo '</form></body></html>';  
}


//modified from http://www.barattalo.it/2010/08/29/php-bot-to-get-wikipedia-definitions/
function wikidefinition($s) {
  $url = 'http://en.wikipedia.org/w/api.php?action=opensearch&search='.
    $s .'&format=xml&limit=1';
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_HTTPGET, TRUE);
  curl_setopt($ch, CURLOPT_POST, FALSE);
  curl_setopt($ch, CURLOPT_HEADER, false);
  curl_setopt($ch, CURLOPT_NOBODY, FALSE);
  curl_setopt($ch, CURLOPT_VERBOSE, FALSE);
  curl_setopt($ch, CURLOPT_REFERER, "");
  curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
  curl_setopt($ch, CURLOPT_MAXREDIRS, 4);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
  curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.1; he; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8");
    $page = curl_exec($ch);
    $xml = simplexml_load_string($page);
    if((string)$xml->Section->Item->Description) {
      return rtrim($xml->Section->Item->Description);
      //return array((string)$xml->Section->Item->Text, (string)$xml->Section->Item->Description, (string)$xml->Section->Item->Url);
    } else {
        return "";
    }
}
function generateRandomArray($numberOfElements){
  $randomArray = array();
  $r = rand(0, $numberOfElements - 1);
  for ($i = 0; $i < $numberOfElements; $i++) {
    while (in_array($r, $randomArray)){
      $r = rand(0, $numberOfElements - 1);
    }  
    $randomArray[$i] = $r;
  }
  return $randomArray;
}


?>