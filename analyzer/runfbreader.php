<?php
function divide($x,$y){
    if ($y!=0){
        return $x/$y;
    }
    else{
        return 0;
    }

}
#$uid=$_POST['uid'];
#$access_token=$_POST['access_token'];
$uid='1233266413';
$access_token='CAAUpDilvHqEBAK6UWNUAZAVFCRyZADGFhfnKGhZBxz507qyHAcUt7VFpKgxE9VFjOwaVZBqCew33NP7TLb6RP9ZAV61nGmXl5M853BBP5yRToCFVWabhIibWyC1K1JZCK4YWcyA4yxJaKRFobhzTl9VR4PEfL3ZBC05h3npDTc4ZAPfGqz8t02GaRDtDaoj4gqWgSbEecZA3ZAJwZDZD';
#echo $uid.'<br/>'.$access_token.'<br/>';

$result_2="";
$result_1= shell_exec('python meifbcrawler.py '.$uid.' '.$access_token);
print_r($result_1);

//if( count($result_1) > 0 ){
$result_21= shell_exec('python fb_info_type.py '.$uid);
$result_22= shell_exec('python fb_post_type.py '.$uid);
//}

$key=array("EXT","AGR","CON","NEO","OPE");

$v1=get_object_vars(json_decode($result_21));
$v2=get_object_vars(json_decode($result_22));

$vs1=array_sum($v1);
$vs2=array_sum($v2);

$v3=array();
foreach($key as $k ){
    $v3[$k]=divide($v1[$k],$vs1)+divide($v2[$k],$vs2);
}
$vs3=array_sum($v3);

foreach($key as $k ){
    $v3[$k]=divide($v3[$k],$vs3);
}
echo json_encode($v3);



?>
