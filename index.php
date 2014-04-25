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
require_once( 'util.php');
require_once( './facebook_php/fb_login.php');
?>
<!doctype html>
<html xmlns:fb="http://www.facebook.com/2008/fbml">
  <head>
    <link rel="stylesheet" type="text/css" href="./css/style.css">
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
    <title>個性問卷</title>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"> </script>
  </head>
  <body>
    <div id="fb-root">
    </div>
    <div id="div_outer">
    <h2>個性問卷</h2>
	</form>
    <?php 
    if ($user){
        $access_token=get_access_token($_SESSION);
        echo '<div class="sub_div1">';
        echo "<img id=\"user_img\" src=\"https://graph.facebook.com/$user/picture\">";
        echo '<div class="profile_1" >';
        echo '<span class="profile_2">姓名: <b>'.$user_profile['name'].'</b></span><br/>';
        echo '<span class="profile_2">Facebook ID: <b>'.$user_profile['id'].'</b></span><br/>';
        echo '</div></div>';
        echo '<div id="main_content">
<p>
問卷很快~ 不用一分鐘就完成了!
</p>

<p>
全部只有五個問題~ 每一個問題你只要幫忙選 + or - 就好了!!!
(每一個 + or - 後面都有一組詞表, 看你覺得你的個性適合哪個詞表就可以了!)
</p>


<form>
<p><span class="q_title"> [1] Extraversion </span>
<span class="q_content">
<br/><input type="radio" name="q1"  value="1"/> + 有活力 / 健談 / 大膽 / 活潑 / 積極 / 篤定的 / 愛冒險
<br/><input type="radio" name="q1"  value="0"/> - 缺乏活力 / 安靜 / 膽怯 / 不活躍 / 怠惰 / 謙遜 / 沒冒險精神
</span>
</p>
<p><span class="q_title"> [2] Agreeableness </span>
<span class="q_content">
<br/><input type="radio" name="q2"   value="1"/> + 帶來溫暖 / 和善 / 合群 / 不自私 / 信任他人 / 慷慨
<br/><input type="radio" name="q2"   value="0"/> - 冷漠 / 不友善 / 缺乏團體意識 / 自私 / 不輕易相信他人 / 吝嗇
</span>
</p>
<p><span class="q_title"> [3] Conscientiousness </span>
<span class="q_content">
<br/><input type="radio" name="q3"  value="1"/> + 有條理 / 負責任 / 務實 / 設想周全 / 勤奮 / 節儉 / 細心 / 講究
<br/><input type="radio" name="q3"  value="0"/> - 不善組織 / 不負責 / 天馬行空的 / 容易衝動 / 怠惰 / 揮霍 / 粗心 / 隨便
</span>
</p>
<p><span class="q_title"> [4] Neuroticism </span>
<span class="q_content">
<br/><input type="radio" name="q4"  value="1"/> + 易怒 / 緊張 / 緊繃 / 易忌妒 / 情緒不穩 / 不滿 / 情緒化
<br/><input type="radio" name="q4"  value="0"/> - 平靜 / 自在 / 放鬆 / 不忌妒 / 情緒穩定 / 滿足 / 不流露情感
</span>
</p>
<p><span class="q_title"> [5] Openness </span>
<span class="q_content">
<br/><input type="radio" name="q5"  value="1"/> + 聰明 / 善於分析 / 深思熟慮 / 好奇 / 有想像力 / 有創意 / 世故(社會化較深)
<br/><input type="radio" name="q5"  value="0"/> - 缺乏才智 / 不擅分析 / 粗心大意 / 不好問 / 缺乏想像力 / 缺乏創意 / 天真(較沒被社會化)
</span>
</p>
<span class="q_submit" onclick="check_data()">提交</span>
</form>
        ';


        echo '</div>';
        // echo "<p><a href=\"$logoutUrl\" class=\"fb_login\">Logout</a></p>";
    }
     else{
        echo '<p><strong>請用您的facebook帳號登入</strong></p>';
        #echo " <p><a href=\"$loginUrl\" class=\"fb_login\">Login Facebook</a></p>";
        echo "<fb:login-button></fb:login-button>";
        }

    //echo $user_profile['id'].'<br/>';
    //echo $access_token;
     ?>

    <script>
      window.fbAsyncInit = function() {
        FB.init({
          appId: '<?php echo $facebook->getAppID() ?>',
          cookie: true,
          xfbml: true,
          oauth: true
        });
        FB.Event.subscribe('auth.login', function(response) {
          window.location.reload();
        });
        FB.Event.subscribe('auth.logout', function(response) {
          window.location.reload();
        });
      };
      (function() {
        var e = document.createElement('script'); e.async = true;
        e.src = document.location.protocol +
          '//connect.facebook.net/en_US/all.js';
        document.getElementById('fb-root').appendChild(e);
      }());
    </script>
    <script type="text/javascript">
        function check_data(){
            var score='';
            var pass=true;
            for(var i=1;i<=5;i++){
                var qscore=$('input[name="q'+i+'"]:checked').val();
                if(qscore == undefined){
                    pass=false;
                    alert("您尚未填完問卷,請填完問卷再按提交");
                    break;
                }
                //console.log(score);
                score+=qscore.toString();
            }
            if(pass){
                post_data(score);
            }
        }
        function post_data(score){
            var uid = "<?php echo $user_profile['id'] ?>";
            var access_token = "<?php echo $access_token ?>";
            var target="<?php echo $app_url;?>"+"analyzer/getfbdata.php";
            var result="";
        
            $("#main_content").html("<p>提交完畢</p><p>感謝您的幫忙~</p>")
            $.ajax({
              type: "POST",
              url: target,
              data: { uid: uid, access_token: access_token ,score:score},
              dataType: "json"
            })
            //.done(function( s ) {
            //  console.log(  s );
            // // $("#ps_div").html(echos);
            //});
        }
    </script>
<hr style="border: 1px; border-bottom: 1px solid #c0e9ff; background: #c0e9ff;" />
<h4>註：</h4>
<ol>
<li>
本軟體將擷取您的資訊來分析所屬個性。這些資訊僅供學術使用,不會外流,也不會外洩個資!所欲擷取的資訊包含:
公開的個人檔案、朋友名單、自訂朋友名單、動態消息、感情狀態、生日、文章、近況更新、打卡動態、活動、社團、興趣、相片、追蹤的和追蹤者、影片、個人簡介、說讚的內容和遊戲動態
</li>
<li>
若登入facebook後,沒有出現問卷表單,或者畫面沒有改變,請按<b>重新整理</b>
</li>
</ol>
</div>
  </body>
</html>
