<?php
/**
 * This file is used for plugin uninstall.
 *
 * @author   Tech Banker
 * @package  contact-bank
 * @version  3.1.0
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
	die;
} else {
	if ( ! current_user_can( 'manage_options' ) ) {
			return;
	} else {
		global $wpdb;
		if ( is_multisite() ) {
			$blog_ids = $wpdb->get_col( "SELECT blog_id FROM $wpdb->blogs" );// WPCS: db call ok, no-cache ok.
			foreach ( $blog_ids as $blog_id ) {
				switch_to_blog( $blog_id );// @codingStandardsIgnoreLine.
				$contact_bank_version_number = get_option( 'contact-bank-version-number' );
				if ( false !== $contact_bank_version_number ) {
					global $wpdb;
					$get_other_settings      = $wpdb->get_var(
						$wpdb->prepare(
							'SELECT meta_value from ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s', 'general_settings'
						)
					);// WPCS: db call ok, no-cache ok.
					$get_other_settings_data = maybe_unserialize( $get_other_settings );
					if ( 'enable' === $get_other_settings_data['remove_tables_at_uninstall'] ) {
						$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'contact_bank' );// @codingStandardsIgnoreLine.
						$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'contact_bank_meta' );// @codingStandardsIgnoreLine.
						delete_option( 'contact-bank-version-number' );
						delete_option( 'contact-bank-wizard-set-up' );
						delete_option( 'cb_admin_notice' );
					}
				}
				restore_current_blog();
			}
		} else {
			$contact_bank_version_number = get_option( 'contact-bank-version-number' );
			if ( false !== $contact_bank_version_number ) {
				global $wpdb;
				$get_other_settings      = $wpdb->get_var(
					$wpdb->prepare(
						'SELECT meta_value from ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s', 'general_settings'
					)
				);// PWCS: db call ok, no-cache ok.
				$get_other_settings_data = maybe_unserialize( $get_other_settings );
				if ( 'enable' === $get_other_settings_data['remove_tables_at_uninstall'] ) {
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'contact_bank' );// @codingStandardsIgnoreLine.
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'contact_bank_meta' );// @codingStandardsIgnoreLine.
					delete_option( 'contact-bank-version-number' );
					delete_option( 'contact-bank-wizard-set-up' );
					delete_option( 'cb_admin_notice' );
				}
			}
		}
	}
}
