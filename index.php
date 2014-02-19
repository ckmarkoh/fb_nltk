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
  'appId'  => '611086378941074',
  'secret' => '57ae467b8039fda188c683fc62c2021b',
));
// Get User ID
$user = $facebook->getUser();
if ($user) {
  try {
    // Proceed knowing you have a logged in user who's authenticated.
	$target='me';
    $user_profile = $facebook->api('/'.$target);
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
	$params = array('scope' => 'read_stream','redirect_uri' => 'http://r444b.ee.ntu.edu.tw/facebook_nltk/');
	$loginUrl = $facebook->getLoginUrl($params);
}
?>
<!doctype html>
<html xmlns:fb="http://www.facebook.com/2008/fbml">
  <head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>What's Your Personality?</title>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"> </script>
  </head>
  <body>
    <div id="div_outer">
    <h2>What's Your Personality? </h2>
	</form>
    <?php 
    if ($user){
        $access_token=get_access_token($_SESSION);
        echo"<h3>You</h3> ";
        echo '<div class="sub_div1">';
        echo "<img id=\"user_img\" src=\"https://graph.facebook.com/$user/picture\">";
        echo '<div class="profile_1" >';
            echo '<span class="profile_2">Name: <b>'.$user_profile['name'].'</b></span><br/>';
            echo '<span class="profile_2">Id: <b>'.$user_profile['id'].'</b></span><br/>';
        echo '</div></div>';
	    echo '<h3>Your Personality</h3>';
        echo '<div class="sub_div2">';
        echo '<div id="ps_div">
                <div style="margin:0px auto;float">Loading...
                <div id="facebookG">
                <div id="blockG_1" class="facebook_blockG">
                </div>
                <div id="blockG_2" class="facebook_blockG">
                </div>
                <div id="blockG_3" class="facebook_blockG">
                </div>
                </div>
                </div> 
        </div>';
        echo '</div>';
         echo "<p><a href=\"$logoutUrl\" class=\"fb_login\">Logout</a></p>";
    }
     else{
        echo '<p><strong><em>You are not Connected.</em></strong></p>';
        echo " <p><a href=\"$loginUrl\" class=\"fb_login\">Login with Facebook</a></p>";
        }
     ?>
    <script type="text/javascript">
        var uid = "<?php echo $user_profile['id'] ?>";
        var access_token = "<?php echo $access_token ?>";
        var target="http://r444b.ee.ntu.edu.tw/facebook_nltk/runfbreader.php";
        var result="";
        var key1=["EXT","AGR","CON","NEO","OPE"];
        var key2=["Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism" ,"Openness"];
        
        $.ajax({
          type: "POST",
          url: target,
          data: { uid: uid, access_token: access_token },
          dataType: "json"
        })
          .done(function( s ) {
            result=s;
            console.log(  s );
            var echos='';
            for (var i=0; i<5 ; i++ ){
              var this_width=Math.floor(result[key1[i]]*500).toString();
              var this_percent=Math.floor(result[key1[i]]*100).toString();
              echos +='<div class="p_title"><span class="p_title_inner" style="width:'+this_width+'px;">'+key2[i]+'<br/>'+this_percent+'%</span></div>';

            }
            $("#ps_div").html(echos);
      });
    </script>
    </div>
  </body>
</html>
