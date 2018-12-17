<?php
/**
 * This file represents the Data Access Layer for Contact Bank.
 *
 * @author     Tech Banker
 * @package contact-bank/lib
 * @version  3.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
} // Exit if accessed directly
else {
	$access_granted = false;
	foreach ( $user_role_permission as $permission ) {
		if ( current_user_can( $permission ) ) {
			$access_granted = true;
			break;
		}
	}
	if ( ! $access_granted ) {
		return;
	} else {
		/**
		 * This function is used to get date.
		 *
		 * @param string $meta_key passes parameter as meta key.
		 * @param string $date1 passes paramater as date1.
		 * @param string $date2 passes parameter as date2.
		 * @param string $form_id passes parameter as form_id.
		 */
		function get_contact_bank_details_date( $meta_key, $date1, $date2, $form_id ) {
			global $wpdb;
			$contact_bank_manage  = $wpdb->get_results(
				$wpdb->prepare(
					'SELECT * FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s and old_form_id = %d ORDER BY id DESC', $meta_key, $form_id
				)
			);// WPCS: db call ok, cache ok.
			$contact_bank_details = array();
			if ( count( $contact_bank_manage ) > 0 ) {
				foreach ( $contact_bank_manage as $raw_row ) {
					$row                = maybe_unserialize( $raw_row->meta_value );
					$row['old_form_id'] = $raw_row->old_form_id;
					$row['meta_id']     = $raw_row->meta_id;
					$row['id']          = $raw_row->id;
					if ( $row['timestamp'] >= $date1 && $row['timestamp'] <= $date2 ) {
						array_push( $contact_bank_details, $row );
					}
				}
			}
			return $contact_bank_details;
		}
		/**
		 * This function is used to get date.
		 *
		 * @param int $id passes parameter as id.
		 */
		function get_unserialized_data_contact_bank( $id ) {
			global $wpdb;
			$selected_form_value   = $wpdb->get_var(
				$wpdb->prepare(
					'SELECT meta_value FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE old_form_id = %d and meta_key = %s', $id, 'form_data'
				)
			);// WPCS: db call ok, cache ok.
			$details_form_controls = maybe_unserialize( $selected_form_value );
			return $details_form_controls;
		}
		if ( isset( $_REQUEST['param'] ) ) {// WPCS: input var ok.
			$obj_dbhelper_contact_bank = new Dbhelper_Contact_Bank();
			switch ( sanitize_text_field( wp_unslash( $_REQUEST['param'] ) ) ) {// WPCS: input var ok, CSRF ok.
				case 'wizard_contact_bank':
					if ( wp_verify_nonce( isset( $_REQUEST['_wp_nonce'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['_wp_nonce'] ) ) : '', 'contact_bank_check_status' ) ) {// WPCS: input var ok.
						$type             = isset( $_REQUEST['type'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['type'] ) ) : '';// WPCS: input var ok.
						$user_admin_email = isset( $_REQUEST['id'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['id'] ) ) : '';// WPCS: input var ok.

						update_option( 'contact-bank-wizard-set-up', $type );
						if ( '' === $user_admin_email ) {
							$user_admin_email = get_option( 'admin_email' );
						}
						update_option( 'contact-bank-admin-email', $user_admin_email );

						if ( 'opt_in' === $type ) {
							$plugin_info_contact_bank = new plugin_info_contact_bank();

							global $wp_version;
							$url = TECH_BANKER_STATS_URL . '/wp-admin/admin-ajax.php';

							$theme_details = array();
							if ( $wp_version >= 3.4 ) {
								$active_theme                   = wp_get_theme();
								$theme_details['theme_name']    = strip_tags( $active_theme->name );
								$theme_details['theme_version'] = strip_tags( $active_theme->version );
								$theme_details['author_url']    = strip_tags( $active_theme->{'Author URI'} );
							}
							$plugin_stat_data                     = array();
							$plugin_stat_data['plugin_slug']      = 'contact-bank';
							$plugin_stat_data['type']             = 'standard_edition';
							$plugin_stat_data['version_number']   = CONTACT_BANK_WIZARD_VERSION_NUMBER;
							$plugin_stat_data['status']           = $type;
							$plugin_stat_data['event']            = 'activate';
							$plugin_stat_data['domain_url']       = site_url();
							$plugin_stat_data['wp_language']      = defined( 'WPLANG' ) && WPLANG ? WPLANG : get_locale();
							$plugin_stat_data['email']            = $user_admin_email;
							$plugin_stat_data['wp_version']       = $wp_version;
							$plugin_stat_data['php_version']      = esc_html( phpversion() );
							$plugin_stat_data['mysql_version']    = $wpdb->db_version();
							$plugin_stat_data['max_input_vars']   = ini_get( 'max_input_vars' );
							$plugin_stat_data['operating_system'] = PHP_OS . '  (' . PHP_INT_SIZE * 8 . ') BIT';
							$plugin_stat_data['php_memory_limit'] = ini_get( 'memory_limit' ) ? ini_get( 'memory_limit' ) : 'N/A';
							$plugin_stat_data['extensions']       = get_loaded_extensions();
							$plugin_stat_data['plugins']          = $plugin_info_contact_bank->get_plugin_info_contact_bank();
							$plugin_stat_data['themes']           = $theme_details;
							$response                             = wp_safe_remote_post(
								$url, array(
									'method'      => 'POST',
									'timeout'     => 45,
									'redirection' => 5,
									'httpversion' => '1.0',
									'blocking'    => true,
									'headers'     => array(),
									'body'        => array(
										'data'    => maybe_serialize( $plugin_stat_data ),
										'site_id' => false !== get_option( 'cb_tech_banker_site_id' ) ? get_option( 'cb_tech_banker_site_id' ) : '',
										'action'  => 'plugin_analysis_data',
									),
								)
							);

							if ( ! is_wp_error( $response ) ) {
								false !== $response['body'] ? update_option( 'cb_tech_banker_site_id', $response['body'] ) : '';
							}
						}
					}
					break;
				case 'cb_get_form_id_contact_bank':
					if ( wp_verify_nonce( isset( $_REQUEST['_wp_nonce'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['_wp_nonce'] ) ) : '', 'cb_get_form_id_nonce' ) ) {// WPCS: input var ok.
						global $wpdb;
						$parent_id = $wpdb->get_var(
							$wpdb->prepare(
								'SELECT id FROM ' . $wpdb->prefix . 'contact_bank WHERE type = %s', 'forms'
							)
						);// WPCS: db call ok, cache ok.

						$add_form_parent_data              = array();
						$add_form_parent_data['type']      = 'form';
						$add_form_parent_data['parent_id'] = $parent_id;
						$parent_last_id                    = $obj_dbhelper_contact_bank->insert_command( contact_bank(), $add_form_parent_data );

						$add_form_record                                   = array();
						$add_form_record['form_title']                     = '';
						$add_form_record['form_description']               = '';
						$add_form_record['form_submission_limit']          = '10';
						$add_form_record['form_save_submission_to_db']     = 'enable';
						$add_form_record['form_submission_limit_message']  = 'disable';
						$add_form_record['form_submission_message']        = '';
						$add_form_record['form_success_message']           = '';
						$add_form_record['form_enable_tooltip']            = 'show';
						$add_form_record['form_redirect']                  = 'page';
						$add_form_record['form_redirect_url']              = '';
						$add_form_record['form_redirect_page_url']         = '';
						$add_form_record['form_admin_notification_email']  = '';
						$add_form_record['form_client_notification_email'] = '';
						$add_form_record['layout_settings_template']       = 'layout_settings_blank_form_template';
						$add_form_record['controls']                       = array();
						$site_title_name                                   = get_option( 'blogname' );
						$control_timestamp                                 = '<p>Hello Admin,</p><p>A new user visited your website.</p><p>Thanks,</p><p><strong>Technical Support Team</strong></p><p><strong>' . $site_title_name . '</strong></p>';

						$add_admin_email_notifications                           = array();
						$add_admin_email_notifications['template_send_to_email'] = get_option( 'admin_email' );
						$add_admin_email_notifications['template_cc']            = '';
						$add_admin_email_notifications['template_send_to']       = 'send_to_email';
						$add_admin_email_notifications['template_send_to_field'] = '';
						$add_admin_email_notifications['template_bcc']           = '';
						$add_admin_email_notifications['template_from_name']     = 'Site Administration';
						$add_admin_email_notifications['template_from_email']    = get_option( 'admin_email' );
						$add_admin_email_notifications['template_reply_to']      = '';
						$add_admin_email_notifications['template_subject']       = 'New Contact received from Website';
						$add_admin_email_notifications['template_message']       = $control_timestamp;

						$add_client_email_notifications                           = array();
						$add_client_email_notifications['template_send_to_email'] = get_option( 'admin_email' );
						$add_client_email_notifications['template_send_to']       = 'send_to_email';
						$add_client_email_notifications['template_send_to_field'] = '';
						$add_client_email_notifications['template_cc']            = '';
						$add_client_email_notifications['template_bcc']           = '';
						$add_client_email_notifications['template_from_name']     = 'Site Administration';
						$add_client_email_notifications['template_from_email']    = get_option( 'admin_email' );
						$add_admin_email_notifications['template_reply_to']       = '';
						$add_client_email_notifications['template_subject']       = 'Thanks for visiting our Website';
						$add_client_email_notifications['template_message']       = '<p>Hi,</p><p>Thanks for visiting our website. We will Contact you within next 24 hours.</p><p>Thanks,</p><p><strong>Technical Support Team</strong></p><p><strong>' . $site_title_name . '</strong></p>';
						$add_form_record['form_admin_notification_email']         = $add_admin_email_notifications;
						$add_form_record['form_client_notification_email']        = $add_client_email_notifications;

						$add_form_meta_data                = array();
						$add_form_meta_data['old_form_id'] = $parent_last_id;
						$add_form_meta_data['meta_id']     = $parent_last_id;
						$add_form_meta_data['meta_key']    = 'form_data';// WPCS: sql slow query.
						$add_form_meta_data['meta_value']  = maybe_serialize( $add_form_record );// WPCS: sql slow query.
						$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $add_form_meta_data );

						$layout_settings_array['layout_settings_form_design_width']                   = '100%';
						$layout_settings_array['layout_settings_form_design_position']                = 'left';
						$layout_settings_array['layout_settings_form_design_background_color']        = '#ffffff';
						$layout_settings_array['layout_settings_form_design_background_transparency'] = '100';
						$layout_settings_array['layout_settings_form_design_title_html_tag']          = 'h1';
						$layout_settings_array['layout_settings_form_design_title_alignment']         = 'left';
						$layout_settings_array['layout_settings_form_design_title_font_style']        = '24,#000000';
						$layout_settings_array['layout_settings_form_design_title_font_family']       = 'Roboto Slab:700';
						$layout_settings_array['layout_settings_form_design_description_html_tag']    = 'p';
						$layout_settings_array['layout_settings_form_design_description_alignment']   = 'left';
						$layout_settings_array['layout_settings_form_design_description_font_style']  = '12,#000000';
						$layout_settings_array['layout_settings_form_design_description_font_family'] = 'Roboto Slab:300';
						$layout_settings_array['layout_settings_form_design_form_margin']             = '0,0,0,0';
						$layout_settings_array['layout_settings_form_design_form_padding']            = '10,10,10,10';
						$layout_settings_array['layout_settings_form_design_title_margin']            = '0,0,5,0';
						$layout_settings_array['layout_settings_form_design_title_padding']           = '5,0,0,0';
						$layout_settings_array['layout_settings_form_design_description_margin']      = '0,0,5,0';
						$layout_settings_array['layout_settings_form_design_description_padding']     = '0,0,5,0';

						$layout_settings_array['layout_settings_input_field_width']                         = '90%';
						$layout_settings_array['layout_settings_input_field_height']                        = '100%';
						$layout_settings_array['layout_settings_input_field_text_alignment']                = 'left';
						$layout_settings_array['layout_settings_input_field_radio_button_alignment']        = 'single_row';
						$layout_settings_array['layout_settings_input_field_checkbox_alignment']            = 'single_row';
						$layout_settings_array['layout_settings_input_field_font_style']                    = '14,#000000';
						$layout_settings_array['layout_settings_input_field_font_family']                   = 'Roboto Condensed';
						$layout_settings_array['layout_settings_input_field_background_color_transparency'] = '#f7f7f7,100';
						$layout_settings_array['layout_settings_input_field_border_style']                  = '1,solid,#d1d1d1';
						$layout_settings_array['layout_settings_input_field_border_radius']                 = '2';
						$layout_settings_array['layout_settings_input_field_margin']                        = '5,0,5,0';
						$layout_settings_array['layout_settings_input_field_padding']                       = '10,10,10,10';

						$layout_settings_array['layout_settings_label_field_text_alignment']                = 'left';
						$layout_settings_array['layout_settings_label_field_width']                         = '100%';
						$layout_settings_array['layout_settings_label_field_height']                        = '100%';
						$layout_settings_array['layout_settings_label_field_font_style']                    = '16,#000000';
						$layout_settings_array['layout_settings_label_field_font_family']                   = 'Roboto Condensed';
						$layout_settings_array['layout_settings_label_field_background_color_transparency'] = '#ffffff,0';
						$layout_settings_array['layout_settings_label_field_margin']                        = '0,0,0,0';
						$layout_settings_array['layout_settings_label_field_padding']                       = '10,10,10,0';

						$layout_settings_array['layout_settings_button_text_alignment']                = 'center';
						$layout_settings_array['layout_settings_button_text']                          = 'Submit';
						$layout_settings_array['layout_settings_button_width']                         = '100px';
						$layout_settings_array['layout_settings_button_height']                        = '100%';
						$layout_settings_array['layout_settings_button_font_style']                    = '16,#ffffff';
						$layout_settings_array['layout_settings_button_font_family']                   = 'Roboto Slab';
						$layout_settings_array['layout_settings_button_background_color']              = '#524c52';
						$layout_settings_array['layout_settings_button_background_transparency']       = '100';
						$layout_settings_array['layout_settings_button_hover_background_color']        = '#706c70';
						$layout_settings_array['layout_settings_button_hover_background_transparency'] = '100';
						$layout_settings_array['layout_settings_button_border_style']                  = '1,solid,#524c52';
						$layout_settings_array['layout_settings_button_border_radius']                 = '4';
						$layout_settings_array['layout_settings_button_hover_border_color']            = '#706c70';
						$layout_settings_array['layout_settings_button_margin']                        = '10,0,0,0';
						$layout_settings_array['layout_settings_button_padding']                       = '15,20,15,20';

						$layout_settings_array['layout_settings_messages_text_alignment']                = 'left';
						$layout_settings_array['layout_settings_messages_background_color_transparency'] = '#e5ffd5,50';
						$layout_settings_array['layout_settings_messages_font_style']                    = '18,#6aa500';
						$layout_settings_array['layout_settings_messages_font_family']                   = 'Roboto Slab';
						$layout_settings_array['layout_settings_messages_margin']                        = '0,0,0,0';
						$layout_settings_array['layout_settings_messages_padding']                       = '0,0,0,0';

						$layout_settings_array['layout_settings_error_messages_background_color']        = '#ffffff';
						$layout_settings_array['layout_settings_error_messages_background_transparency'] = '50';
						$layout_settings_array['layout_settings_error_messages_font_style']              = '12,#ff2c38';
						$layout_settings_array['layout_settings_error_messages_font_family']             = 'Roboto Slab';
						$layout_settings_array['layout_settings_error_messages_margin']                  = '0,0,0,0';
						$layout_settings_array['layout_settings_error_messages_padding']                 = '5px,0px,0px,0px';

						$add_form_meta_data                = array();
						$add_form_meta_data['meta_id']     = $parent_last_id;
						$add_form_meta_data['meta_key']    = 'layout_settings';// WPCS: db sql slow query.
						$add_form_meta_data['old_form_id'] = $parent_last_id;
						$add_form_meta_data['meta_value']  = maybe_serialize( $layout_settings_array );// WPCS: db sql slow query.
						$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $add_form_meta_data );

						echo $parent_last_id;// WPCS: XSS ok.
					}
					break;
				case 'add_form_module':
					if ( wp_verify_nonce( isset( $_REQUEST['_wp_nonce'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['_wp_nonce'] ) ) : '', 'add_new_form_module' ) ) {
						parse_str( isset( $_REQUEST['data'] ) ? base64_decode( wp_unslash( filter_input( INPUT_POST, 'data' ) ) ) : '', $add_form_data );// WPCS: input var ok.
						$id          = isset( $_REQUEST['form_meta_id'] ) ? intval( $_REQUEST['form_meta_id'] ) : 0;// WPCS: input var ok.
						$control_ids = isset( $_REQUEST['control_ids'] ) ? array_map( 'esc_attr', is_array( json_decode( wp_unslash( $_REQUEST['control_ids'] ) ) ) ? json_decode( wp_unslash( $_REQUEST['control_ids'] ) ) : array() ) : array();// WPCS: input var ok, sanitization ok.

						$contact_meta_value                               = $wpdb->get_var(
							$wpdb->prepare(
								'SELECT meta_value from ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_id = %d and meta_key = %s', $id, 'form_data'
							)
						);// WPCS: db call ok, cache ok.
						$contact_meta_id_unserialize                      = maybe_unserialize( $contact_meta_value );
						$add_form_record                                  = array();
						$add_form_record['form_title']                    = isset( $add_form_data['ux_txt_form_title'] ) ? sanitize_text_field( $add_form_data['ux_txt_form_title'] ) : '';
						$add_form_record['form_description']              = isset( $add_form_data['ux_txtarea_add_form_heading_content'] ) ? esc_html( $add_form_data['ux_txtarea_add_form_heading_content'] ) : '';
						$add_form_record['form_submission_limit']         = isset( $add_form_data['ux_txt_submission_limit'] ) ? intval( $add_form_data['ux_txt_submission_limit'] ) : '';
						$add_form_record['form_save_submission_to_db']    = isset( $add_form_data['ux_ddl_save_submission_to_db'] ) ? sanitize_text_field( $add_form_data['ux_ddl_save_submission_to_db'] ) : '';
						$add_form_record['form_submission_limit_message'] = isset( $add_form_data['ux_ddl_submission_limit_message'] ) ? sanitize_text_field( $add_form_data['ux_ddl_submission_limit_message'] ) : '';
						$add_form_record['form_submission_message']       = isset( $add_form_data['ux_txt_submission_limit_message'] ) ? esc_html( $add_form_data['ux_txt_submission_limit_message'] ) : '';
						$add_form_record['form_success_message']          = isset( $add_form_data['ux_txt_success_message'] ) ? esc_html( $add_form_data['ux_txt_success_message'] ) : '';
						$add_form_record['form_enable_tooltip']           = isset( $add_form_data['ux_ddl_enable_tooltip'] ) ? sanitize_text_field( $add_form_data['ux_ddl_enable_tooltip'] ) : '';
						$add_form_record['form_redirect']                 = isset( $add_form_data['ux_ddl_redirect_type'] ) ? sanitize_text_field( $add_form_data['ux_ddl_redirect_type'] ) : '';
						$add_form_record['form_redirect_url']             = isset( $add_form_data['ux_txt_url_redirect'] ) ? sanitize_text_field( $add_form_data['ux_txt_url_redirect'] ) : '';
						$add_form_record['form_redirect_page_url']        = isset( $add_form_data['ux_ddl_redirect_page'] ) ? sanitize_text_field( $add_form_data['ux_ddl_redirect_page'] ) : '';
						$controls        = array();
						$form_controls   = '';
						$site_title_name = get_option( 'blogname' );
						foreach ( $control_ids as $control_id ) {
							$add_form_controls_data                                   = array();
							$add_form_controls_data['control_type']                   = isset( $add_form_data[ 'ux_control_type_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_control_type_' . $control_id ] ) : '';
							$add_form_controls_data['label_name']                     = isset( $add_form_data[ 'ux_txt_label_field_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_label_field_' . $control_id ] ) : '';
							$add_form_controls_data['field_description']              = isset( $add_form_data[ 'ux_txt_field_description_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_field_description_' . $control_id ] ) : '';
							$add_form_controls_data['label_tooltip']                  = isset( $add_form_data[ 'ux_txt_description_field_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_description_field_' . $control_id ] ) : '';
							$add_form_controls_data['label_placement']                = isset( $add_form_data[ 'ux_ddl_label_placement_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_label_placement_' . $control_id ] ) : '';
							$add_form_controls_data['number_of_stars']                = isset( $add_form_data[ 'ux_txt_number_of_stars_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_number_of_stars_' . $control_id ] ) : '';
							$add_form_controls_data['placeholder']                    = isset( $add_form_data[ 'ux_txt_placeholder_field_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_placeholder_field_' . $control_id ] ) : '';
							$add_form_controls_data['custom_validation_message']      = isset( $add_form_data[ 'ux_txt_custom_validation_field_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_custom_validation_field_' . $control_id ] ) : '';
							$add_form_controls_data['rows_number']                    = isset( $add_form_data[ 'ux_txt_no_of_rows_' . $control_id ] ) ? intval( $add_form_data[ 'ux_txt_no_of_rows_' . $control_id ] ) : '2';
							$add_form_controls_data['container_class']                = isset( $add_form_data[ 'ux_txt_container_class_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_container_class_' . $control_id ] ) : '';
							$add_form_controls_data['element_class']                  = isset( $add_form_data[ 'ux_txt_element_class_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_element_class_' . $control_id ] ) : '';
							$add_form_controls_data['required_type']                  = isset( $add_form_data[ 'ux_ddl_required_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_required_' . $control_id ] ) : '';
							$add_form_controls_data['input_limit_number']             = isset( $add_form_data[ 'ux_txt_limit_input_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_limit_input_' . $control_id ] ) : '';
							$add_form_controls_data['text_appear']                    = isset( $add_form_data[ 'ux_txt_text_appear_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_text_appear_' . $control_id ] ) : '';
							$add_form_controls_data['input_mask_type']                = isset( $add_form_data[ 'ux_ddl_input_mask_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_input_mask_' . $control_id ] ) : '';
							$add_form_controls_data['custom_mask']                    = isset( $add_form_data[ 'ux_txt_custom_mask_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_custom_mask_' . $control_id ] ) : '';
							$add_form_controls_data['input_validation_type']          = isset( $add_form_data[ 'ux_ddl_limit_input_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_limit_input_' . $control_id ] ) : '';
							$add_form_controls_data['autocomplete_type']              = isset( $add_form_data[ 'ux_ddl_autocomplete_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_autocomplete_' . $control_id ] ) : '';
							$add_form_controls_data['disable_input']                  = isset( $add_form_data[ 'ux_ddl_disable_input_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_disable_input_' . $control_id ] ) : '';
							$add_form_controls_data['date_format']                    = isset( $add_form_data[ 'ux_ddl_date_format_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_date_format_' . $control_id ] ) : '';
							$add_form_controls_data['start_year']                     = isset( $add_form_data[ 'ux_txt_start_year_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_start_year_' . $control_id ] ) : '';
							$add_form_controls_data['end_year']                       = isset( $add_form_data[ 'ux_txt_end_year_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_end_year_' . $control_id ] ) : '';
							$add_form_controls_data['default_current_date']           = isset( $add_form_data[ 'ux_ddl_default_current_date_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_default_current_date_' . $control_id ] ) : '';
							$add_form_controls_data['max_number']                     = isset( $add_form_data[ 'ux_txt_max_number_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_max_number_' . $control_id ] ) : '';
							$add_form_controls_data['min_number']                     = isset( $add_form_data[ 'ux_txt_min_number_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_min_number_' . $control_id ] ) : '';
							$add_form_controls_data['step']                           = isset( $add_form_data[ 'ux_txt_step_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_step_' . $control_id ] ) : '';
							$add_form_controls_data['drop_down_option_values']        = isset( $add_form_data[ 'ux_hidden_options_values_' . $control_id ] ) ? json_decode( stripslashes( $add_form_data[ 'ux_hidden_options_values_' . $control_id ] ) ) : array();
							$add_form_controls_data['field_key']                      = isset( $add_form_data[ 'single_line_text_field_key_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'single_line_text_field_key_' . $control_id ] ) : '';
							$add_form_controls_data['default_value']                  = isset( $add_form_data[ 'ux_txt_default_value_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_default_value_' . $control_id ] ) : '';
							$add_form_controls_data['admin_label']                    = isset( $add_form_data[ 'ux_txt_admin_label_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_admin_label_' . $control_id ] ) : '';
							$add_form_controls_data['price']                          = isset( $add_form_data[ 'ux_txt_price_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_price_' . $control_id ] ) : '';
							$add_form_controls_data['time_format']                    = isset( $add_form_data[ 'ux_ddl_time_format_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_time_format_' . $control_id ] ) : '';
							$add_form_controls_data['current_time']                   = isset( $add_form_data[ 'ux_ddl_default_current_time_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_default_current_time_' . $control_id ] ) : '';
							$add_form_controls_data['product_name']                   = isset( $add_form_data[ 'ux_ddl_product_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_product_' . $control_id ] ) : '';
							$add_form_controls_data['credit_card_number']             = isset( $add_form_data[ 'ux_txt_credit_card_number_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_credit_card_number_' . $control_id ] ) : '';
							$add_form_controls_data['credit_card_expiry_date']        = isset( $add_form_data[ 'ux_txt_expiry_date_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_expiry_date_' . $control_id ] ) : '';
							$add_form_controls_data['credit_card_cvv']                = isset( $add_form_data[ 'ux_txt_cvv_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_cvv_' . $control_id ] ) : '';
							$add_form_controls_data['credit_card_placeholder']        = isset( $add_form_data[ 'card_number_placeholder_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'card_number_placeholder_' . $control_id ] ) : '';
							$add_form_controls_data['credit_card_expiry_placeholder'] = isset( $add_form_data[ 'expiry_date_placeholder_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'expiry_date_placeholder_' . $control_id ] ) : '';
							$add_form_controls_data['credit_card_cvv_placeholder']    = isset( $add_form_data[ 'card_cvv_number_placeholder_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'card_cvv_number_placeholder_' . $control_id ] ) : '';
							$add_form_controls_data['html_editor_content']            = isset( $add_form_data[ 'ux_content_heading_content_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_content_heading_content_' . $control_id ] ) : '';
							$add_form_controls_data['html_editor_type']               = isset( $add_form_data[ 'ux_txt_html_type_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_html_type_' . $control_id ] ) : '';
							$add_form_controls_data['html_editor_content_duplicate']  = isset( $add_form_data[ 'ux_content_heading_content_duplicate_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_content_heading_content_duplicate_' . $control_id ] ) : '';

							$add_form_controls_data['shipping_cost']                          = isset( $add_form_data[ 'ux_txt_cost_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_cost_' . $control_id ] ) : '';
							$add_form_controls_data['antispam_answer']                        = isset( $add_form_data[ 'ux_txt_answer_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_answer_' . $control_id ] ) : '';
							$add_form_controls_data['maximum_size']                           = isset( $add_form_data[ 'ux_txt_max_size_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_max_size_' . $control_id ] ) : '';
							$add_form_controls_data['extension']                              = isset( $add_form_data[ 'ux_txt_extension_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_txt_extension_' . $control_id ] ) : '';
							$add_form_controls_data['multiple_upload']                        = isset( $add_form_data[ 'ux_ddl_multiple_upload_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_multiple_upload_' . $control_id ] ) : '';
							$add_form_controls_data['attach_to_email']                        = isset( $add_form_data[ 'ux_ddl_attach_email_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_attach_email_' . $control_id ] ) : '';
							$add_form_controls_data['timestamp']                              = intval( $control_id );
							$add_form_controls_data['logical_captcha_mathmatical_operations'] = isset( $add_form_data[ 'ux_ddl_mathmatical_operations_' . $control_id ] ) ? sanitize_text_field( $add_form_data[ 'ux_ddl_mathmatical_operations_' . $control_id ] ) : '';
							$add_form_controls_data['logical_captcha_artimatic']              = isset( $add_form_data[ 'ux_chk_artimatic_hidden_values_' . $control_id ] ) ? implode( ',', array_map( 'intval', is_array( json_decode( stripslashes( $add_form_data[ 'ux_chk_artimatic_hidden_values_' . $control_id ] ) ) ) ? json_decode( stripslashes( $add_form_data[ 'ux_chk_artimatic_hidden_values_' . $control_id ] ) ) : array() ) ) : '';
							$add_form_controls_data['logical_captcha_relational']             = isset( $add_form_data[ 'ux_chk_hidden_relational_values_' . $control_id ] ) ? implode( ',', array_map( 'intval', is_array( json_decode( stripslashes( $add_form_data[ 'ux_chk_hidden_relational_values_' . $control_id ] ) ) ) ? json_decode( stripslashes( $add_form_data[ 'ux_chk_hidden_relational_values_' . $control_id ] ) ) : array() ) ) : '';
							$add_form_controls_data['logical_captcha_arrange_order']          = isset( $add_form_data[ 'ux_chk_hidden_arrange_value_' . $control_id ] ) ? implode( ',', array_map( 'intval', is_array( json_decode( stripslashes( $add_form_data[ 'ux_chk_hidden_arrange_value_' . $control_id ] ) ) ) ? json_decode( stripslashes( $add_form_data[ 'ux_chk_hidden_arrange_value_' . $control_id ] ) ) : array() ) ) : '';
							$template_label_name = '' !== $add_form_controls_data['admin_label'] ? sanitize_text_field( $add_form_controls_data['admin_label'] ) : ( '' !== $add_form_controls_data['label_name'] ? sanitize_text_field( $add_form_controls_data['label_name'] ) : 'Untitled' );
							$form_controls      .= '<p><strong>' . $template_label_name . '</strong>: [control_' . $add_form_controls_data['timestamp'] . ']</p>';
							array_push( $controls, $add_form_controls_data );
						}
						$control_timestamp                           = '<p>Hello Admin,</p><p>A new user visited your website.</p><p>Here are the details :</p>' . $form_controls . '<p>Thanks,</p><p><strong>Technical Support Team</strong></p><p><strong>' . $site_title_name . '</strong></p>';
						$add_form_record['layout_settings_template'] = isset( $_REQUEST['template'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['template'] ) ) : 'layout_settings_blank_form_template';// WPCS: input var ok.
						$add_form_record['controls']                 = $controls;

						$add_admin_email_notifications                           = array();
						$admin_email_template                                    = $contact_meta_id_unserialize['form_admin_notification_email'];
						$add_admin_email_notifications['template_send_to_email'] = isset( $admin_email_template['template_send_to_email'] ) ? sanitize_text_field( $admin_email_template['template_send_to_email'] ) : get_option( 'admin_email' );
						$add_admin_email_notifications['template_send_to']       = isset( $admin_email_template['template_send_to'] ) ? sanitize_text_field( $admin_email_template['template_send_to'] ) : 'send_to_email';
						$add_admin_email_notifications['template_send_to_field'] = isset( $admin_email_template['template_send_to_field'] ) ? sanitize_text_field( $admin_email_template['template_send_to_field'] ) : '';
						$add_admin_email_notifications['template_cc']            = isset( $admin_email_template['template_cc'] ) ? sanitize_text_field( $admin_email_template['template_cc'] ) : '';
						$add_admin_email_notifications['template_bcc']           = isset( $admin_email_template['template_bcc'] ) ? sanitize_text_field( $admin_email_template['template_bcc'] ) : '';
						$add_admin_email_notifications['template_from_name']     = isset( $admin_email_template['template_from_name'] ) ? sanitize_text_field( $admin_email_template['template_from_name'] ) : 'Site Administration';
						$add_admin_email_notifications['template_from_email']    = isset( $admin_email_template['template_from_email'] ) ? sanitize_text_field( $admin_email_template['template_from_email'] ) : get_option( 'admin_email' );
						$add_admin_email_notifications['template_reply_to']      = isset( $admin_email_template['template_reply_to'] ) ? sanitize_text_field( $admin_email_template['template_reply_to'] ) : '';
						$add_admin_email_notifications['template_subject']       = isset( $admin_email_template['template_subject'] ) ? sanitize_text_field( $admin_email_template['template_subject'] ) : 'New Contact received from Website';
						$add_admin_email_notifications['template_message']       = $control_timestamp;

						$add_client_email_notifications                           = array();
						$client_email_template                                    = $contact_meta_id_unserialize['form_client_notification_email'];
						$add_client_email_notifications['template_send_to_email'] = isset( $client_email_template['template_send_to_email'] ) ? sanitize_text_field( $client_email_template['template_send_to_email'] ) : get_option( 'admin_email' );
						$add_client_email_notifications['template_send_to']       = isset( $client_email_template['template_send_to'] ) ? sanitize_text_field( $client_email_template['template_send_to'] ) : 'send_to_email';
						$add_client_email_notifications['template_send_to_field'] = isset( $client_email_template['template_send_to_field'] ) ? sanitize_text_field( $client_email_template['template_send_to_field'] ) : '';
						$add_client_email_notifications['template_cc']            = isset( $client_email_template['template_cc'] ) ? sanitize_text_field( $client_email_template['template_cc'] ) : '';
						$add_client_email_notifications['template_bcc']           = isset( $client_email_template['template_bcc'] ) ? sanitize_text_field( $client_email_template['template_bcc'] ) : '';
						$add_client_email_notifications['template_from_name']     = isset( $client_email_template['template_from_name'] ) ? sanitize_text_field( $client_email_template['template_from_name'] ) : 'Site Administration';
						$add_client_email_notifications['template_from_email']    = isset( $client_email_template['template_from_email'] ) ? sanitize_text_field( $client_email_template['template_from_email'] ) : get_option( 'admin_email' );
						$add_client_email_notifications['template_reply_to']      = isset( $client_email_template['template_reply_to'] ) ? sanitize_text_field( $client_email_template['template_reply_to'] ) : '';
						$add_client_email_notifications['template_subject']       = isset( $client_email_template['template_subject'] ) ? sanitize_text_field( $client_email_template['template_subject'] ) : 'Thanks for visiting our Website';
						$add_client_email_notifications['template_message']       = isset( $client_email_template['template_message'] ) ? urldecode( stripslashes( $client_email_template['template_message'] ) ) : '<p>Hi,</p><p>Thanks for visiting our website. We will Contact you within next 24 hours.</p><p>Thanks,</p><p><strong>Technical Support Team</strong></p><p><strong>' . $site_title_name . '</strong></p>';
						$add_form_record['form_admin_notification_email']         = $add_admin_email_notifications;
						$add_form_record['form_client_notification_email']        = $add_client_email_notifications;

						global $wpdb;
						$parent_id = $wpdb->get_var(
							$wpdb->prepare(
								'SELECT id FROM ' . $wpdb->prefix . 'contact_bank WHERE type = %s', 'forms'
							)
						);// WPCS: db call ok, cache ok.
						if ( 0 == $id ) {// WPCS: loose comparison ok.
							$add_form_parent_data              = array();
							$add_form_parent_data['type']      = 'form';
							$add_form_parent_data['parent_id'] = $parent_id;
							$parent_last_id                    = $obj_dbhelper_contact_bank->insert_command( contact_bank(), $add_form_parent_data );

							$add_form_meta_data                = array();
							$add_text_control                  = array();
							$add_form_meta_data['old_form_id'] = $parent_last_id;
							$add_form_meta_data['meta_id']     = $parent_last_id;
							$add_form_meta_data['meta_key']    = 'form_data';// WPCS: sql slow query.
							$add_form_meta_data['meta_value']  = maybe_serialize( $add_form_record );// WPCS: sql slow query.
							$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $add_form_meta_data );
						} else {
							$add_form_meta_data               = array();
							$where                            = array();
							$where['old_form_id']             = $id;
							$where['meta_key']                = 'form_data';// WPCS: sql slow query.
							$add_form_meta_data['meta_value'] = maybe_serialize( $add_form_record );// WPCS: sql slow query.
							$obj_dbhelper_contact_bank->update_command( contact_bank_meta(), $add_form_meta_data, $where );
						}
					}
					break;

				case 'cb_add_form_contact_us_template':
					if ( wp_verify_nonce( isset( $_REQUEST['_wp_nonce'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['_wp_nonce'] ) ) : '', 'cb_add_form_contact_us_template_nonce' ) ) {// WPCS: input var ok.
						$form_id                                    = isset( $_REQUEST['form_meta_id'] ) ? intval( $_REQUEST['form_meta_id'] ) : '';// WPCS: input var ok.
						$controls_array                             = array( 'first_name', 'email', 'text', 'paragraph' );
						$controls_label_array                       = array( 'Name', 'Email', 'Subject', 'Message' );
						$controls_label_tooltips_array              = array( 'In this field,you would need to provide your First Name', 'In this field, you would need to provide your Email Address', 'In this field, you would need to provide your Subject', 'In this field, you would need to provide your Message' );
						$controls_label_placement_array             = array( 'above', 'above', 'above', 'above' );
						$controls_placeholder_array                 = array( 'Please provide your first name', 'Please provide your email address', 'Please provide your subject', 'Please provide your message here' );
						$controls_required_array                    = array( 'enable', 'enable', 'disable', 'disable' );
						$controls_limit_input_number                = array( '', '', '50', '255' );
						$controls_text_appear_after_count           = array( '', '', 'Character(s) left', 'Character(s) left' );
						$controls_input_mask                        = array( '', '', 'none', 'none' );
						$controls_custom_mask                       = array( '', '', '999,999,999,999', '999,999,999,999' );
						$controls_auto_complete                     = array( 'enable', '', 'enable', 'enable' );
						$controls_disable_input                     = array( 'disable', '', 'disable', 'disable' );
						$controls_input_validation_type             = array( '', '', 'characters', 'characters' );
						$controls_field_key                         = array( 'first_name_field_key_', 'email_address_field_key_', 'single_line_text_field_key_', 'paragraph_text_field_key_' );
						$contact_meta_value                         = $wpdb->get_var(
							$wpdb->prepare(
								'SELECT meta_value from ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_id = %d and meta_key = %s', $form_id, 'form_data'
							)
						);// WPCS: db call ok, cache ok.
						$form_unserialized_data                     = maybe_unserialize( $contact_meta_value );
						$form_controls                              = '';
						$controls                                   = array();
						$form_unserialized_data['form_title']       = 'Contact Us Form';
						$form_unserialized_data['form_description'] = isset( $form_unserialized_data['form_description'] ) ? esc_html( $form_unserialized_data['form_description'] ) : '';
						$form_unserialized_data['form_submission_limit_message'] = 'disable';
						$form_unserialized_data['form_submission_message']       = 'Your Forms Submission Limit is Over.';
						$form_unserialized_data['form_success_message']          = 'Your Form has been Successfully Submitted.';
						$form_unserialized_data['form_enable_tooltip']           = 'show';
						$form_unserialized_data['form_redirect']                 = 'page';
						$form_unserialized_data['form_redirect_url']             = '';
						$form_unserialized_data['form_redirect_page_url']        = '';
						$site_title_name = get_option( 'blogname' );
						for ( $i = 0; $i < 4; $i++ ) {
							$timestamp                                   = time() + $i;
							$add_form_controls_data                      = array();
							$add_form_controls_data['control_type']      = $controls_array[ $i ];
							$add_form_controls_data['label_name']        = $controls_label_array[ $i ];
							$add_form_controls_data['field_description'] = '';
							$add_form_controls_data['label_tooltip']     = $controls_label_tooltips_array[ $i ];
							$add_form_controls_data['label_placement']   = $controls_label_placement_array[ $i ];
							$add_form_controls_data['number_of_stars']   = '';
							$add_form_controls_data['placeholder']       = $controls_placeholder_array[ $i ];
							$add_form_controls_data['custom_validation_message']      = 'This field is Required!';
							$add_form_controls_data['rows_number']                    = '10';
							$add_form_controls_data['container_class']                = '';
							$add_form_controls_data['element_class']                  = '';
							$add_form_controls_data['required_type']                  = $controls_required_array[ $i ];
							$add_form_controls_data['input_limit_number']             = $controls_limit_input_number[ $i ];
							$add_form_controls_data['text_appear']                    = $controls_text_appear_after_count[ $i ];
							$add_form_controls_data['input_mask_type']                = $controls_input_mask[ $i ];
							$add_form_controls_data['custom_mask']                    = $controls_custom_mask[ $i ];
							$add_form_controls_data['input_validation_type']          = $controls_input_validation_type[ $i ];
							$add_form_controls_data['autocomplete_type']              = $controls_auto_complete[ $i ];
							$add_form_controls_data['disable_input']                  = $controls_disable_input[ $i ];
							$add_form_controls_data['date_format']                    = '';
							$add_form_controls_data['start_year']                     = '';
							$add_form_controls_data['end_year']                       = '';
							$add_form_controls_data['default_current_date']           = '';
							$add_form_controls_data['max_number']                     = '';
							$add_form_controls_data['min_number']                     = '';
							$add_form_controls_data['step']                           = '';
							$add_form_controls_data['drop_down_option_values']        = array();
							$add_form_controls_data['field_key']                      = $controls_field_key[ $i ] . $timestamp;
							$add_form_controls_data['default_value']                  = '';
							$add_form_controls_data['admin_label']                    = '';
							$add_form_controls_data['price']                          = '';
							$add_form_controls_data['time_format']                    = '';
							$add_form_controls_data['current_time']                   = '';
							$add_form_controls_data['product_name']                   = '';
							$add_form_controls_data['credit_card_number']             = '';
							$add_form_controls_data['credit_card_expiry_date']        = '';
							$add_form_controls_data['credit_card_cvv']                = '';
							$add_form_controls_data['credit_card_placeholder']        = '';
							$add_form_controls_data['credit_card_expiry_placeholder'] = '';
							$add_form_controls_data['credit_card_cvv_placeholder']    = '';
							$add_form_controls_data['html_editor_content']            = '';
							$add_form_controls_data['html_editor_type']               = '';
							$add_form_controls_data['html_editor_content_duplicate']  = '';

							$add_form_controls_data['shipping_cost']                          = '';
							$add_form_controls_data['antispam_answer']                        = '';
							$add_form_controls_data['maximum_size']                           = '';
							$add_form_controls_data['extension']                              = '';
							$add_form_controls_data['multiple_upload']                        = '';
							$add_form_controls_data['attach_to_email']                        = '';
							$add_form_controls_data['timestamp']                              = time() + $i;
							$add_form_controls_data['logical_captcha_mathmatical_operations'] = '';
							$add_form_controls_data['logical_captcha_artimatic']              = '';
							$add_form_controls_data['logical_captcha_relational']             = '';
							$add_form_controls_data['logical_captcha_arrange_order']          = '';
							$template_label_name = '' !== $add_form_controls_data['admin_label'] ? sanitize_text_field( $add_form_controls_data['admin_label'] ) : ( '' !== $add_form_controls_data['label_name'] ? sanitize_text_field( $add_form_controls_data['label_name'] ) : 'Untitled' );
							$form_controls      .= '<p><strong>' . $template_label_name . '</strong>: [control_' . $add_form_controls_data['timestamp'] . ']</p>';
							array_push( $controls, $add_form_controls_data );
						}
						$control_timestamp                                  = '<p>Hello Admin,</p><p>A new user visited your website.</p><p>Here are the details :</p>' . $form_controls . '<p>Thanks,</p><p><strong>Technical Support Team</strong></p><p><strong>' . $site_title_name . '</strong></p>';
						$form_unserialized_data['layout_settings_template'] = isset( $_REQUEST['template'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['template'] ) ) : 'layout_settings_blank_form_template';// WPCS: input var ok.
						$form_unserialized_data['controls']                 = $controls;

						$add_admin_email_notifications                           = array();
						$add_admin_email_notifications['template_send_to_email'] = get_option( 'admin_email' );
						$add_admin_email_notifications['template_send_to']       = 'send_to_email';
						$add_admin_email_notifications['template_send_to_field'] = '';
						$add_admin_email_notifications['template_cc']            = '';
						$add_admin_email_notifications['template_bcc']           = '';
						$add_admin_email_notifications['template_from_name']     = 'Site Administration';
						$add_admin_email_notifications['template_from_email']    = get_option( 'admin_email' );
						$add_admin_email_notifications['template_reply_to']      = '';
						$add_admin_email_notifications['template_subject']       = 'New Contact received from Website';
						$add_admin_email_notifications['template_message']       = $control_timestamp;

						$add_client_email_notifications                           = array();
						$add_client_email_notifications['template_send_to_email'] = get_option( 'admin_email' );
						$add_client_email_notifications['template_send_to']       = 'send_to_email';
						$add_client_email_notifications['template_send_to_field'] = '';
						$add_client_email_notifications['template_cc']            = '';
						$add_client_email_notifications['template_bcc']           = '';
						$add_client_email_notifications['template_from_name']     = 'Site Administration';
						$add_client_email_notifications['template_from_email']    = get_option( 'admin_email' );
						$add_client_email_notifications['template_reply_to']      = '';
						$add_client_email_notifications['template_subject']       = 'Thanks for visiting our Website';
						$add_client_email_notifications['template_message']       = '<p>Hi,</p><p>Thanks for visiting our website. We will Contact you within next 24 hours.</p><p>Thanks,</p><p><strong>Technical Support Team</strong></p><p><strong>' . $site_title_name . '</strong></p>';

						$form_unserialized_data['form_admin_notification_email']  = $add_admin_email_notifications;
						$form_unserialized_data['form_client_notification_email'] = $add_client_email_notifications;

						$form_unserialized_data['layout_settings_template'] = isset( $_REQUEST['template'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['template'] ) ) : 'layout_settings_blank_form_template';// WPCS: input var ok.
						$form_unserialized_data['controls']                 = $controls;
						$add_form_meta_data                                 = array();
						$where                            = array();
						$where['meta_id']                 = $form_id;
						$where['meta_key']                = 'form_data';// WPCS: slow query ok.
						$add_form_meta_data['meta_value'] = maybe_serialize( $form_unserialized_data );// WPCS: slow query ok.
						$obj_dbhelper_contact_bank->update_command( contact_bank_meta(), $add_form_meta_data, $where );
					}
					break;

				case 'delete_submission_module':
					if ( wp_verify_nonce( isset( $_REQUEST['_wp_nonce'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['_wp_nonce'] ) ) : '', 'cb_submission_single_delete' ) ) {// WPCS: input var ok.
						$id                           = isset( $_REQUEST['meta_id'] ) ? intval( stripcslashes( wp_unslash( $_REQUEST['meta_id'] ) ) ) : '';// WPCS: input var ok, sanitization ok.
						$delete_submission_data       = array();
						$delete_submission_data['id'] = $id;
						$obj_dbhelper_contact_bank->delete_command( contact_bank_meta(), $delete_submission_data );
					}
					break;
				case 'delete_contact_forms':
					if ( wp_verify_nonce( isset( $_REQUEST['_wp_nonce'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['_wp_nonce'] ) ) : '', 'contact_forms_delete_nonce' ) ) {// WPCS: input var ok.
						$meta_id                       = isset( $_REQUEST['meta_id'] ) ? intval( stripcslashes( wp_unslash( $_REQUEST['meta_id'] ) ) ) : '';// WPCS: input var ok, sanitization ok.
						$delete_form_data              = array();
						$delete_form_data_parent       = array();
						$delete_form_data['meta_id']   = $meta_id;
						$delete_form_data_parent['id'] = $meta_id;
						$obj_dbhelper_contact_bank->delete_command( contact_bank(), $delete_form_data_parent );
						$obj_dbhelper_contact_bank->delete_command( contact_bank_meta(), $delete_form_data );
					}
					break;

				case 'custom_css_module':
					if ( wp_verify_nonce( isset( $_REQUEST['_wp_nonce'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['_wp_nonce'] ) ) : '', 'custom_css_nonce' ) ) {// WPCS: input var ok.
						parse_str( isset( $_REQUEST['data'] ) ? base64_decode( wp_unslash( filter_input( INPUT_POST, 'data' ) ) ) : '', $custom_css_form_data );// WPCS: input var ok.
						$custom_css_data                       = array();
						$custom_css_data['custom_css']         = esc_html( $custom_css_form_data['ux_txt_custom_css'] );
						$update_custom_css_array               = array();
						$where                                 = array();
						$where['meta_key']                     = 'custom_css';// WPCS: slow query ok.
						$update_custom_css_array['meta_value'] = maybe_serialize( $custom_css_data );// WPCS: slow query ok.
						$obj_dbhelper_contact_bank->update_command( contact_bank_meta(), $update_custom_css_array, $where );
					}
					break;

				case 'email_templates_module':
					if ( wp_verify_nonce( isset( $_REQUEST['_wp_nonce'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['_wp_nonce'] ) ) : '', 'email_templates_nonce' ) ) {// WPCS: input var ok.
						parse_str( isset( $_REQUEST['data'] ) ? base64_decode( wp_unslash( filter_input( INPUT_POST, 'data' ) ) ) : '', $email_templates_data );// WPCS: input var ok.
						$form_id       = sanitize_text_field( $email_templates_data['ux_ddl_forms'] );
						$template_type = sanitize_text_field( $email_templates_data['ux_ddl_email_templates'] );

						$email_templates_array                           = array();
						$email_templates_array['template_send_to']       = sanitize_text_field( $email_templates_data['ux_ddl_send_to'] );
						$email_templates_array['template_send_to_email'] = sanitize_text_field( $email_templates_data['ux_txt_send_to_email'] );
						$email_templates_array['template_from_name']     = sanitize_text_field( $email_templates_data['ux_txt_from_name'] );
						$email_templates_array['template_from_email']    = sanitize_text_field( $email_templates_data['ux_txt_from_email'] );
						$email_templates_array['template_send_to_field'] = sanitize_text_field( $email_templates_data['ux_txt_send_to_field'] );
						$email_templates_array['template_reply_to']      = sanitize_text_field( $email_templates_data['ux_txt_your_reply_to'] );
						$email_templates_array['template_cc']            = sanitize_text_field( $email_templates_data['ux_txt_your_cc_field'] );
						$email_templates_array['template_bcc']           = sanitize_text_field( $email_templates_data['ux_txt_bcc_field'] );
						$email_templates_array['template_subject']       = sanitize_text_field( $email_templates_data['ux_txt_subject'] );
						$email_templates_array['template_message']       = urldecode( stripslashes( $email_templates_data['ux_txtarea_email_template_heading_content'] ) );

						$form_data = $wpdb->get_var(
							$wpdb->prepare(
								'SELECT meta_value FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s and meta_id = %d', 'form_data', $form_id
							)
						);// WPCS: db call ok, cache ok.

						$unserialized_data_forms                   = maybe_unserialize( $form_data );
						$unserialized_data_forms[ $template_type ] = $email_templates_array;

						$email_template_update_data               = array();
						$email_template_update_data['meta_value'] = maybe_serialize( $unserialized_data_forms );// WPCS: slow query ok.
						$where                                    = array();
						$where['meta_key']                        = 'form_data';// WPCS: slow query ok.
						$where['meta_id']                         = $form_id;
						$obj_dbhelper_contact_bank->update_command( contact_bank_meta(), $email_template_update_data, $where );
					}
					break;

				case 'general_settings_module':
					if ( wp_verify_nonce( isset( $_REQUEST['_wp_nonce'] ) ? sanitize_text_field( wp_unslash( $_REQUEST['_wp_nonce'] ) ) : '', 'general_settings_nonce' ) ) {// WPCS: input var ok.
						parse_str( ( isset( $_REQUEST['data'] ) ? base64_decode( wp_unslash( filter_input( INPUT_POST, 'data' ) ) ) : '' ), $general_settings_data );// WPCS: input var ok.
						$update_general_settings                               = array();
						$update_general_settings['automatic_updates']          = 'disable';
						$update_general_settings['remove_tables_at_uninstall'] = sanitize_text_field( $general_settings_data['ux_ddl_remove_table'] );
						$update_general_settings['default_currency']           = sanitize_text_field( $general_settings_data['ux_ddl_default_currency'] );
						$update_general_settings['language_direction']         = sanitize_text_field( $general_settings_data['ux_ddl_language_direction'] );
						$update_general_settings['recaptcha_private_key']      = '';
						$update_general_settings['recaptcha_public_key']       = '';
						$update_general_settings['gdpr_compliance']            = sanitize_text_field( $general_settings_data['ux_ddl_gdpr_compliance'] );
						$update_general_settings['gdpr_compliance_text']       = esc_attr( $general_settings_data['ux_txt_gdpr_compliance_text'] );

						$where                                      = array();
						$update_general_settings_data               = array();
						$where['meta_key']                          = 'general_settings';// WPCS: slow query ok.
						$update_general_settings_data['meta_value'] = maybe_serialize( $update_general_settings );// WPCS: slow query ok.
						$obj_dbhelper_contact_bank->update_command( contact_bank_meta(), $update_general_settings_data, $where );
					}
					break;
			}
			die();
		}
	}
}
