<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
/////////////////////////////////////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////////////////////////////////// 
initializeModelModule("mysqli_interface");
/////////////////////////////////////////////

///////////////////////////
// Retreive Request Data
///////////////////////////
$type = $_POST["type"];
$amount = $_POST["amt"];


//////////////////////////
// Choose URL's to parse
/////////////////////////
require_once('chooseURLs.php');
$urls = chooseURLs($type, $amount);


/////////////////////////
// Set background parsing task (to replace below up to report confirmation)
////////////////////////


///////////////////////
// Parse each url
///////////////////////
require_once('parseURLs.php');
parseURLs($urls, $type);



print "done.";
die();



//////////////
// Report confirmation
//////////////
print "[[==]]SCS[[==]]";
