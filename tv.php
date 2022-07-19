<?php

  $token = file_get_contents("token.txt");
  $channel = "http://iptv12k.com:35461" . $token . $_GET["channel"] . ".m3u8";
  $channel_headers = get_headers($channel);