<?php

function to_array($obj){
	return is_object($obj) ? get_object_vars($obj) : $obj;
}
function get_access_token($session){
        $session_val='';
        foreach( $session as $s_key=>$s_val){
            $pos1 = strpos($s_key, 'fb');
            $pos2 = strpos($s_key, 'access_token');
            if (($pos1 !== false) &&  ($pos2 !== false)){
                $session_val=$s_val;
                break;
            } 
        }
        return $session_val;
}
?>
