<?php

$uid=$_POST['uid'];
$access_token=$_POST['access_token'];
#$uid='1037998582';
#$access_token='CAAFbxFk1h5QBANvdl6NYxcAZCQxCGKh6WPWQZCVz3ZC0POjW3HZBE0u8WFMVMSPbIbDpxtwPnop3A8KDArhjhukd1D9c0fo8vh32YahXaieBYDkfnw2w2h3YBnACUZAlO507TUaqz5VpjaKQVOLAllziRr9NfdFZCGE82EXKnBy61k4G4avxny';
#echo $uid.'<br/>'.$access_token.'<br/>';

$result_2="";
$result_1= shell_exec('python meifbcrawler.py '.$uid.' '.$access_token);
//print_r($result_1);

if( count($result_1) > 0 ){
    $result_21= shell_exec('python fb_info_type.py '.$uid);
    $result_22= shell_exec('python fb_post_type.py '.$uid);
}

$key=array("EXT","AGR","CON","NEO","OPE");

$v1=get_object_vars(json_decode($result_21));
$v2=get_object_vars(json_decode($result_22));

$vs1=array_sum($v1);
$vs2=array_sum($v2);

$v3=array();
foreach($key as $k ){
    $v3[$k]=$v1[$k]/$vs1+$v2[$k]/$vs2;
}
$vs3=array_sum($v3);

foreach($key as $k ){
    $v3[$k]=$v3[$k]/$vs3;
}
echo json_encode($v3);



?>
