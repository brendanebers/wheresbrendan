<?php
/*
Plugin Name: Where's Brendan Post Notifier
Plugin URI: http://wheresbrendan.com
Description: A plugin that pings wheresbrendan whenever a post is generated.
Version: 1.0
Author: Brendan Ebers
Author URI: http://brendanebers.com
*/

add_action( 'save_post', 'post_saved_notification' );

function post_saved_notification( $ID ) {
  // TODO: POST is probably smarter.
  $url = 'http://wheresbrendan.com/api/wordpress/?id=' . $ID;

  try {
    file_get_contents($url);
  }
  catch (Exception $e) {
    // Look at me not caring!
  }
}
?>
