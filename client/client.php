<?php
include('workflow.php');
$NUMWORKFLOWS = 2;
  
$assignmentId = $_GET["assignmentId"];
$workerId = $_GET["workerId"];

if ($assignmentId === 'ASSIGNMENT_ID_NOT_AVAILABLE') {
  renderPreview();
  return;
} 
$workflowRendered = False;
for ($w = 0; $w < $NUMWORKFLOWS; $w++) {

  $workflowId = $w;

  //acquire locks
  while (!mkdir("../locks/aql" . $workflowId . "lock")) {
    continue;
  }
  while (!mkdir("../locks/ip" . $workflowId . "lock")) {
    continue;
  }


  //first we want to read the available questions list.
  $availableQuestions = explode(",", 
				file_get_contents("../log/aql". $workflowId));
  $nextQuestion = 0;

  $allQuestionsDone = True;
  for ($i = 0; $i < count($availableQuestions) - 1; $i++) {
    $availableQuestion = $availableQuestions[$i];
    //check  to see if the worker has already done this question
    while (!mkdir("../locks/w" . $workflowId . 
		  "q" . $availableQuestion . "lock")) {
      continue;
    }
    $workerList = explode("\n", 
			  file_get_contents("../log/w" . $workflowId . 
					    "q" . $availableQuestion));
    $workerFound = False;		
    for ($j = 0; $j < count($workerList) - 1; $j++) {
      if ($workerList[$j] === $workerId) {
	$workerFound = True;
	break;
      }
    }  
  
    if (!$workerFound) {
      $allQuestionsDone = False;
      $nextQuestion = $availableQuestion;
      file_put_contents("../log/w" . $workflowId . 
			"q".$availableQuestion, $workerId."\n", 
			FILE_APPEND);
      file_put_contents("../log/ip". $workflowId, $nextQuestion."\n",
			FILE_APPEND);
      file_put_contents("../log/aql" . $workflowId, "");
      for ($j = 0; $j < count($availableQuestions) - 1; $j++) {
	if ($availableQuestions[$j] == $nextQuestion) {
	  continue;
	}
	file_put_contents("../log/aql".$workflowId, $availableQuestions[$j].",",
			  FILE_APPEND);
      }

      rmdir("../locks/w" . $workflowId . 
		  "q" . $availableQuestion . "lock");
      break;
    }
    rmdir("../locks/w" . $workflowId . 
		  "q" . $availableQuestion . "lock");

  }
  rmdir("../locks/aql" . $workflowId . "lock");
  rmdir("../locks/ip" . $workflowId . "lock");

  //if the worker has completed all available questions, tell
  //him he can't do anything at this time
  if (!$allQuestionsDone) {
    $workflowRendered = True;
    if ($workflowId == 0) {
      renderWorkflow0($assignmentId, $nextQuestion);
    } else {
      renderWorkflow1($assignmentId, $nextQuestion);
    }
    break;
  }

}
if (!$workflowRendered) {
  renderNoWorkflow();
}
?>
