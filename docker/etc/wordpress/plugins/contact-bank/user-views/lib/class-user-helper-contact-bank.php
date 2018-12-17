<?php
/**
 * This file is used for creating user helper class.
 *
 * @author  Tech Banker
 * @package contact-bank/user-views/lib
 * @version 3.1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
} // Exit if accessed directly

if ( ! class_exists( 'User_Helper_Contact_Bank' ) ) {
	/**
	 * This Class is used for return data in unserialize form and convert HEX-color into RGB values.
	 */
	class User_Helper_Contact_Bank {
		/**
		 * This Function is used for Insert data in database.
		 *
		 * @param string $table_name .
		 * @param array  $data .
		 */
		public function insert_command( $table_name, $data ) {
			global $wpdb;
			$wpdb->insert( $table_name, $data );// WPCS: db call ok.
			return $wpdb->insert_id;
		}

		/**
		 * This function is used for convert a normal HEX-color into RGB values.
		 *
		 * @param string $hex .
		 */
		public static function hex2rgb_contact_bank( $hex ) {
			$hex = str_replace( '#', '', $hex );
			if ( strlen( $hex ) === 3 ) {
				$r = hexdec( substr( $hex, 0, 1 ) . substr( $hex, 0, 1 ) );
				$g = hexdec( substr( $hex, 1, 1 ) . substr( $hex, 1, 1 ) );
				$b = hexdec( substr( $hex, 2, 1 ) . substr( $hex, 2, 1 ) );
			} else {
				$r = hexdec( substr( $hex, 0, 2 ) );
				$g = hexdec( substr( $hex, 2, 2 ) );
				$b = hexdec( substr( $hex, 4, 2 ) );
			}
			$rgb = array( $r, $g, $b );
			return $rgb;
		}
		/**
		 * This function is used for return data in unserialize form.
		 *
		 * @param string $meta_key .
		 */
		public static function get_meta_value_contact_bank( $meta_key ) {
			global $wpdb;
			$meta_value = $wpdb->get_var(
				$wpdb->prepare(
					'SELECT meta_value FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s', $meta_key
				)
			);// WPCS: db call ok, no-cache ok.
			return maybe_unserialize( $meta_value );
		}
		/**
		 * This function is used for font-family.
		 *
		 * @param array $font_families .
		 */
		public static function font_families_contact_bank( $font_families ) {
			foreach ( $font_families as $font_family ) {
				if ( 'inherit' !== $font_family ) {
					if ( false !== strpos( $font_family, ':' ) ) {
						$position           = strpos( $font_family, ':' );
						$font_style         = 'italic' === ( substr( $font_family, $position + 4, 6 ) ) ? "\r\n\tfont-style: italic !important;" : '';
						$font_family_name[] = "'" . substr( $font_family, 0, $position ) . "' !important;\r\n\tfont-weight: " . substr( $font_family, $position + 1, 3 ) . ' !important;' . $font_style;
					} else {
						$font_family_name[] = ( false !== strpos( $font_family, '&' ) ) ? "'" . strstr( $font_family, '&', 1 ) . "' !important;" : "'" . $font_family . "' !important;";
					}
				} else {
					$font_family_name[] = 'inherit';
				}
			}
			return $font_family_name;
		}
		/**
		 * This function is used for font-family.
		 *
		 * @param array $unique_font_families .
		 */
		public static function unique_font_families_contact_bank( $unique_font_families ) {
			$import_font_family = '';
			foreach ( $unique_font_families as $font_family ) {
				if ( 'inherit' !== $font_family ) {
					$font_family = urlencode( $font_family );// @codingStandardsIgnoreLine.
					if ( is_ssl() ) {
						$import_font_family .= "@import url('https://fonts.googleapis.com/css?family=" . $font_family . "');\r\n";
					} else {
						$import_font_family .= "@import url('http://fonts.googleapis.com/css?family=" . $font_family . "');\r\n";
					}
				}
			}
			return $import_font_family;
		}
	}
}
