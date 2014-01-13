<?php

function to_array($obj){
	return is_object($obj) ? get_object_vars($obj) : $obj;
}

?>
