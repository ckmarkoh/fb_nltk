<?php
/**
 * Copyright 2011 Facebook, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

require 'util.php';
require './src/facebook.php';

// Create our Application instance (replace this with your appId and secret).
$facebook = new Facebook(array(
  'appId'  => '214325311934533',
  'secret' => '919c052b1d845e6507bf2459c2631ac6',
));

// Get User ID
$user = $facebook->getUser();

// We may or may not have this data based on whether the user is logged in.
//
// If we have a $user id here, it means we know the user is logged into
// Facebook, but we don't know if the access token is valid. An access
// token is invalid if the user logged out of Facebook.

if ($user) {
  try {
    // Proceed knowing you have a logged in user who's authenticated.
	$target='me';
	if(isset($_GET['fbid'])){
		$target=$_GET['fbid'];
	}
    $user_profile = $facebook->api('/'.$target);
    $user_post = $facebook->api('/'.$target.'/feed?fields=description&limit=20');
	
  } catch (FacebookApiException $e) {
    error_log($e);
    $user = null;
  }
}

// Login or logout url will be needed depending on current user state.
if ($user) {



  $logoutUrl = $facebook->getLogoutUrl();

} else {

	$statusUrl = $facebook->getLoginStatusUrl();
	$params = array('scope' => 'read_stream','redirect_uri' => 'http://r444b.ee.ntu.edu.tw/~markchang/facebook_php_sdk/example.php');
	$loginUrl = $facebook->getLoginUrl($params);
	//echo '<a href="' . $loginUrl . '">Login</a>';

  //$loginUrl = $facebook->getLoginUrl();
}

// This call will always work since we are fetching public data.
//$naitik = $facebook->api('/naitik');

?>
<!doctype html>
<html xmlns:fb="http://www.facebook.com/2008/fbml">
  <head>
    <title>php-sdk</title>
    <style>
      body {
        font-family: 'Lucida Grande', Verdana, Arial, sans-serif;
      }
      h1 a {
        text-decoration: none;
        color: #3b5998;
      }
      h1 a:hover {
        text-decoration: underline;
      }
    </style>
  </head>
  <body>
    <h1>php-sdk</h1>

	<!--<form name="input" action="example.php" method="get">
	facebook id: <input type="text" name="go">
	<input type="submit" value="fbid">--!>
	</form>

    <?php if ($user): ?>
      <a href="<?php echo $logoutUrl; ?>">Logout</a>
    <?php else: ?>
      <div>
        Check the login status using OAuth 2.0 handled by the PHP SDK:
        <a href="<?php echo $statusUrl; ?>">Check the login status</a>
      </div>
      <div>
        Login using OAuth 2.0 handled by the PHP SDK:
        <a href="<?php echo $loginUrl; ?>">Login with Facebook</a>
      </div>
    <?php endif ?>

    <!--<h3>PHP Session</h3>
    <pre><?php //print_r($_SESSION); ?></pre>--!>

    <?php if ($user): ?>
      <h3>You</h3>
      <img src="https://graph.facebook.com/<?php echo $user; ?>/picture">

      <h3>Your User Object (/me)</h3>
      <pre><?php 
		//print_r($user_profile);
		echo 'id:'.$user_profile['id'].'<br/>';
		echo 'name:'.$user_profile['name'].'<br/>';;
		echo 'link:'.$user_profile['link'].'<br/>';;

		?></pre>
      <h3>Your Post (/me/feed)</h3>
      <pre><?php 
		$i=0;
		$post_array=array();
		while($i++<50){		
			//$user_post= to_array($user_post);
			if(isset($user_post['data'])){
				foreach( $user_post['data'] as $ud){
					if(isset($ud['description'])){
						array_push($post_array,$ud['description']);
					}
				}
			}
			if(count($post_array)>20){
				break;
			}
			//print_r($user_post); 
			if(isset($user_post['paging'])){
				$paging=$user_post['paging'];
				//$paging= to_array($user_post['paging']);
				//echo "<h1>next:".$paging['next']."</h1>";
				$session_val='';
				foreach( $_SESSION as $s_key=>$s_val){
					$pos1 = strpos($s_key, 'fb');
					$pos2 = strpos($s_key, 'access_token');
					if (($pos1 !== false) &&  ($pos2 !== false)){
						$session_val=$s_val;
						break;
					} 
				}
				//echo 'session:'.$session_val.'<br/>';
				//$user_post=json_decode(file_get_contents($paging['next'].'&access_token='.$_SESSION['fb_214325311934533_access_token']),true);
				$user_post=json_decode(file_get_contents($paging['next'].'&access_token='.$session_val),true);
			}
			else{
				break;
			}
		}
		print_r($post_array);
		$post_str= implode($post_array,"。");
		$post_str= str_replace("\"","'",$post_str);
		//$result_1= exec('ls -a');
		//print_r($result_1);
		//$result_2= exec('python fb_post_type.py '.'"'.$post_str.'"');
	
		//$result_2= exec('python test.py');
		//print_r($result_2);
		$uniqid="subjects/".uniqid().".txt";
		file_put_contents($uniqid,$post_str); 
		$result_2= shell_exec('python fb_post_type.py '.$uniqid);
		//print_r($result_2);
		//echo exec('whoami');
		
	?></pre>

	<h3>Your Personality</h3>
		<pre> <?php
				echo $result_2;
			?>
		</pre>
    <?php else: ?>
      <strong><em>You are not Connected.</em></strong>
    <?php endif ?>

  </body>
</html>
