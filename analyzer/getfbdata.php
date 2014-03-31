<?php

//if(1==1){
if( isset($_POST['uid']) && isset($_POST['uid']) && isset($_POST['uid'])) {

    $uid=$_POST['uid'];
    $access_token=$_POST['access_token'];
    $score=$_POST['score'];

//    $uid = '1233266413';
//    $access_token = 'CAAUpDilvHqEBAN2GpbZBPmBmLgSRrAB3GSNu8IxVmP5JMhWhi6H6gZBlbD5cZAy6IkCmpA3BcglFedCDZBeXtzsT3ANWDa1oj5zpRlYiJdULxlB7bGrMhCnWeZCh6p0WOaeqK24avhriZB1vfd1I9jm5jMnXSahBOI9rN27el05eSZB1GGfARBEZBrQBhzd65ZCDNyaRZAGPUKCgZDZD';
//    $score= '00011';


    $exec_str='python meifbcrawler.py '.$uid.' '.$access_token.' '.$score;

    $result_1= shell_exec($exec_str);

    echo json_encode(array("status"=>"success"));
}
else{
    echo'
    <html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>

    <p>Directory access is forbidden.</p>

    </body>
    </html>';
}

?>
