
<?php
require_once( 'facebook.php');
$app_url='http://r444b.ee.ntu.edu.tw/facebook_nltk/';
$facebook = new Facebook(array(
  #'appId'  => '611086378941074',
  #'secret' => '57ae467b8039fda188c683fc62c2021b',
  'appId'  => '1452515684982433',
  'secret' => '584f3e9710e2866c4fb4d934b4817f2c',
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
	//$params = array('scope' => 'read_stream','redirect_uri' => 'http://r444b.ee.ntu.edu.tw/facebook_nltk/');
	//$params = array('req_perms' =>'read_stream,read_requests,manage_notifications','redirect_uri' => $app_url);
	$params = array('req_perms' =>'read_stream,read_requests,manage_notifications');
	$loginUrl = $facebook->getLoginUrl($params);
}

?>
