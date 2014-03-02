
<?php
require_once( 'facebook.php');

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
	//$params = array('scope' => 'read_stream','redirect_uri' => 'http://r444b.ee.ntu.edu.tw/facebook_nltk/');
	$params = array('scope' => 'read_stream');
	$loginUrl = $facebook->getLoginUrl($params);
}

?>
