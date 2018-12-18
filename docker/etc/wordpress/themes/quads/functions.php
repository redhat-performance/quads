<?php

$option = array(
    'blogname' => 'RDU2 Scale Lab',
    'blogdescription' => 'Dynamic Inventory',
);

foreach ( $option as $key => $value ) {
    update_option( $key, $value);
}

wp_delete_comment(1);
wp_delete_post(1, TRUE);
wp_delete_post(2, TRUE);

include_once( ABSPATH . '/wp-admin/includes/plugin.php');
activate_plugin('contact-bank/contact-bank.php');
activate_plugin('jetpack-markdown/markdown.php');

switch_theme( 'krusze' );