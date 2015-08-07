<?php
/*
Plugin Name: Where's Brendan Post Notifier
Plugin URI: http://wheresbrendan.com
Description: A plugin that pings wheresbrendan whenever a post is generated.
Version: 0.1
Author: Brendan Ebers
Author URI: http://brendanebers.com
*/

add_action( 'publish_post', 'published_notification', 10, 2 );

function published_notification( $ID, $post ) {
  // TODO: Point this at the actual site sometime.
  // POST is probably smarter.
  $url = 'http://wheresbrendan.com/api/wordpress/?id=' . $ID;

  try {
    file_get_contents($url);
  }
  catch (Exception $e) {
    // Look at me not caring!
  }
}
?>
