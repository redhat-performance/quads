<?php
/**
 * This file is used for fetching data from database.
 *
 * @author Tech Banker
 * @package contact-bank/user-views/includes
 * @version 3.1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
$form_data                    = $wpdb->get_var(
	$wpdb->prepare( 'SELECT meta_value FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s and old_form_id = %d', 'form_data', $form_id )
);// WPCS: db call ok, no-cache ok.
$form_unserialized_meta_value = maybe_unserialize( $form_data );

$layout_setting_form_unserialize_data = $wpdb->get_var(
	$wpdb->prepare( 'SELECT meta_value FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s and old_form_id = %d', 'layout_settings', $form_id )
);// WPCS: db call ok, no-cache ok.
$layout_setting_form_data             = maybe_unserialize( $layout_setting_form_unserialize_data );
$custom_css                           = User_Helper_Contact_Bank::get_meta_value_contact_bank( 'custom_css' );


$id_count                             = $wpdb->get_var(
	$wpdb->prepare( 'SELECT count(meta_id) FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s and old_form_id = %d', 'submission_form_data', $form_id )
);// WPCS: db call ok, no-cache ok.
$selected_general_setting_value       = $wpdb->get_var(
	$wpdb->prepare(
		'SELECT meta_value FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s', 'general_settings'
	)
);// WPCS: db call ok, no-cache ok.
$selected_general_setting_unserialize = maybe_unserialize( $selected_general_setting_value );
