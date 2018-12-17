<?php
/**
 * This file is used for creating table.
 *
 * @author   Tech Banker
 * @package  contact-bank/lib
 * @version 3.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
} // Exit if accessed directly
if ( ! is_user_logged_in() ) {
	return;
} else {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	} else {
		if ( ! class_exists( 'Dbhelper_Install_Script_Contact_Bank' ) ) {
			/**
			 * This Class is used for Insert,Update and Delete operations.
			 */
			class Dbhelper_Install_Script_Contact_Bank {
				/**
				 * It is used for insert data in database.
				 *
				 * @param string $table_name .
				 * @param string $data .
				 */
				public function insert_command( $table_name, $data ) {
					global $wpdb;
					$wpdb->insert( $table_name, $data );// WPCS: db call ok, no-cache ok.
					return $wpdb->insert_id;
				}
				/**
				 * It is used for update data in database.
				 *
				 * @param string $table_name .
				 * @param string $data .
				 * @param string $where .
				 */
				public function update_command( $table_name, $data, $where ) {
					global $wpdb;
					$wpdb->update( $table_name, $data, $where );// WPCS: db call ok, no-cache ok.
				}
			}
		}
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		$contact_bank_version_number = get_option( 'contact-bank-version-number' );

		if ( ! function_exists( 'contact_bank_main_table' ) ) {
			/**
			 * It is used for creating a parent table.
			 */
			function contact_bank_main_table() {
				global $wpdb;
				$collate = $wpdb->get_charset_collate();
				$sql     = 'CREATE TABLE IF NOT EXISTS ' . contact_bank() . '
				(
					`id` int(10) NOT NULL AUTO_INCREMENT,
					`type` longtext NOT NULL,
					`parent_id` int(10) DEFAULT NULL,
					PRIMARY KEY (`id`)
				)' . $collate;
				dbDelta( $sql );
				$data = 'INSERT INTO ' . contact_bank() . " (`type`, `parent_id`) VALUES
				('forms',0),
				('custom_css', 0),
				('collation_type', 0),
				('general_settings', 0),
				('roles_and_capabilities', 0)";
				dbDelta( $data );
			}
		}
		if ( ! function_exists( 'contact_bank_meta_table' ) ) {
			/**
			 * It is used for creating a meta table.
			 */
			function contact_bank_meta_table() {
				global $wpdb;
				$collate                   = $wpdb->get_charset_collate();
				$obj_dbhelper_contact_bank = new Dbhelper_Install_Script_Contact_Bank();
				$sql                       = 'CREATE TABLE IF NOT EXISTS ' . contact_bank_meta() . '
				(
					`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
					`meta_id` int(10) NOT NULL,
					`meta_key` varchar(100) NOT NULL,
					`meta_value` longtext NOT NULL,
					`old_form_id` int(10) NOT NULL,
					PRIMARY KEY (`id`)
				)' . $collate;
				dbDelta( $sql );
				$parent_table_data = $wpdb->get_results( 'SELECT id,type FROM ' . $wpdb->prefix . 'contact_bank' );// WPCS: db call ok, no-cache ok.
				foreach ( $parent_table_data as $row ) {
					switch ( $row->type ) {
						case 'custom_css':
							$custom_css_data_array               = array();
							$custom_css_data_array['custom_css'] = '';

							$insert_custom_css_array                = array();
							$insert_custom_css_array['old_form_id'] = $row->id;
							$insert_custom_css_array['meta_id']     = $row->id;
							$insert_custom_css_array['meta_key']    = 'custom_css'; // WPCS: slow query ok.
							$insert_custom_css_array['meta_value']  = maybe_serialize( $custom_css_data_array );// WPCS: slow query ok.
							$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $insert_custom_css_array );
							break;
						case 'general_settings':
							$general_settings_data_array                               = array();
							$general_settings_data_array['remove_tables_at_uninstall'] = 'enable';
							$general_settings_data_array['automatic_updates']          = 'disable';
							$general_settings_data_array['default_currency']           = 'USD';
							$general_settings_data_array['language_direction']         = 'left_to_right';
							$general_settings_data_array['recaptcha_public_key']       = '';
							$general_settings_data_array['recaptcha_private_key']      = '';
							$general_settings_data_array['gdpr_compliance']            = 'enable';
							$general_settings_data_array['gdpr_compliance_text']       = 'By using this form you agree with the storage and handling of your data by this website';

							$insert_general_settings_array                = array();
							$insert_general_settings_array['old_form_id'] = $row->id;
							$insert_general_settings_array['meta_id']     = $row->id;
							$insert_general_settings_array['meta_key']    = 'general_settings';// WPCS: slow query ok.
							$insert_general_settings_array['meta_value']  = maybe_serialize( $general_settings_data_array );// WPCS: slow query ok.
							$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $insert_general_settings_array );
							break;

						case 'roles_and_capabilities':
							$roles_data                                   = array();
							$roles_data['roles_and_capabilities']         = '1,1,1,0,0,0';
							$roles_data['show_contact_bank_top_bar_menu'] = 'enable';
							$roles_data['others_full_control_capability'] = '0';
							$roles_data['administrator_privileges']       = '1,1,1,1,1,1,1,1,1,1';
							$roles_data['author_privileges']              = '0,1,1,0,0,0,1,0,0,1';
							$roles_data['editor_privileges']              = '0,0,0,1,0,1,0,0,0,0';
							$roles_data['contributor_privileges']         = '0,0,0,1,0,0,1,0,0,0';
							$roles_data['subscriber_privileges']          = '0,0,0,0,0,0,0,0,0,0';
							$roles_data['other_privileges']               = '0,0,0,0,0,0,0,0,0,0';
							$user_capabilities                            = get_others_capabilities_contact_bank();
							$other_roles_array                            = array();
							$other_roles_access_array                     = array(
								'manage_options',
								'edit_plugins',
								'edit_posts',
								'publish_posts',
								'publish_pages',
								'edit_pages',
								'read',
							);
							foreach ( $other_roles_access_array as $role ) {
								if ( in_array( $role, $user_capabilities, true ) ) {
									array_push( $other_roles_array, $role );
								}
							}
							$roles_data['capabilities'] = $other_roles_array;

							$roles_data_serialize                = array();
							$roles_data_serialize['old_form_id'] = $row->id;
							$roles_data_serialize['meta_id']     = $row->id;
							$roles_data_serialize['meta_key']    = 'roles_and_capabilities';// WPCS: slow query ok.
							$roles_data_serialize['meta_value']  = maybe_serialize( $roles_data );// WPCS: slow query ok.
							$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $roles_data_serialize );
							break;
					}
				}
			}
		}
		$obj_dbhelper_contact_bank = new Dbhelper_Install_Script_Contact_Bank();
		switch ( $contact_bank_version_number ) {
			case '':
				$contact_bank_admin_notices_array                    = array();
				$contact_bank_start_date                             = date( 'm/d/Y' );
				$contact_bank_start_date                             = strtotime( $contact_bank_start_date );
				$contact_bank_start_date                             = strtotime( '+7 day', $contact_bank_start_date );
				$contact_bank_start_date                             = date( 'm/d/Y', $contact_bank_start_date );
				$contact_bank_admin_notices_array['two_week_review'] = array( 'start' => $contact_bank_start_date, 'int' => 7, 'dismissed' => 0 ); // @codingStandardsIgnoreLine.
				update_option( 'cb_admin_notice', $contact_bank_admin_notices_array );
				contact_bank_main_table();
				contact_bank_meta_table();
				global $wpdb;
				$parent_id = $wpdb->get_var(
					$wpdb->prepare(
						'SELECT id FROM ' . $wpdb->prefix . 'contact_bank WHERE type = %s', 'forms'
					)
				);// WPCS: db call ok, no-cache ok.

				$controls_array                   = array( 'first_name', 'email', 'text', 'paragraph' );
				$controls_label_array             = array( 'Name', 'Email', 'Subject', 'Message' );
				$controls_label_tooltips_array    = array( 'In this field,you would need to provide your First Name', 'In this field, you would need to provide your Email Address', 'In this field, you would need to provide your Subject', 'In this field, you would need to provide your Message' );
				$controls_label_placement_array   = array( 'above', 'above', 'above', 'above' );
				$controls_placeholder_array       = array( 'Please provide your first name', 'Please provide your email address', 'Please provide your subject', 'Please provide your message here' );
				$controls_required_array          = array( 'enable', 'enable', 'disable', 'disable' );
				$controls_limit_input_number      = array( '', '', '50', '255' );
				$controls_text_appear_after_count = array( '', '', 'Character(s) left', 'Character(s) left' );
				$controls_input_mask              = array( '', '', 'none', 'none' );
				$controls_custom_mask             = array( '', '', '999,999,999,999', '999,999,999,999' );
				$controls_auto_complete           = array( 'enable', '', 'enable', 'enable' );
				$controls_disable_input           = array( 'disable', '', 'disable', 'disable' );
				$controls_input_validation_type   = array( '', '', 'characters', 'characters' );
				$controls_field_key               = array( 'first_name_field_key_', 'email_address_field_key_', 'single_line_text_field_key_', 'paragraph_text_field_key_' );

				$form_controls                              = '';
				$form_unserialized_data                     = array();
				$controls                                   = array();
				$form_unserialized_data['form_title']       = 'Contact Us Form';
				$form_unserialized_data['form_description'] = '';
				$form_unserialized_data['form_submission_limit_message'] = 'disable';
				$form_unserialized_data['form_submission_message']       = 'Your Forms Submission Limit is Over.';
				$form_unserialized_data['form_success_message']          = 'Your Form has been Successfully Submitted.';
				$form_unserialized_data['form_enable_tooltip']           = 'show';
				$form_unserialized_data['form_redirect']                 = 'page';
				$form_unserialized_data['form_redirect_url']             = '';
				$form_unserialized_data['form_redirect_page_url']        = '';
				$form_unserialized_data['form_save_submission_to_db']    = 'enable';
				$form_unserialized_data['form_submission_limit']         = '10';
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
					$template_label_name = '' !== $add_form_controls_data['admin_label'] ? esc_attr( $add_form_controls_data['admin_label'] ) : ( '' !== $add_form_controls_data['label_name'] ? esc_attr( $add_form_controls_data['label_name'] ) : 'Untitled' );
					$form_controls      .= '<p><strong>' . $template_label_name . '</strong>: [control_' . $add_form_controls_data['timestamp'] . ']</p>';
					array_push( $controls, $add_form_controls_data );
				}
				$control_timestamp                                  = '<p>Hello Admin,</p><p>A new user visited your website.</p><p>Here are the details :</p>' . $form_controls . '<p>Thanks,</p><p><strong>Technical Support Team</strong></p><p><strong>' . $site_title_name . '</strong></p>';
				$form_unserialized_data['layout_settings_template'] = 'layout_settings_contact_us_form_template';
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

				$form_unserialized_data['layout_settings_template'] = 'layout_settings_contact_us_form_template';
				$form_unserialized_data['controls']                 = $controls;

				$layout_settings_data_array                                      = array();
				$layout_settings_data_array['layout_settings_form_design_width'] = '100%';
				$layout_settings_data_array['layout_settings_form_design_position']                = 'left';
				$layout_settings_data_array['layout_settings_form_design_background_color']        = '#ffffff';
				$layout_settings_data_array['layout_settings_form_design_background_transparency'] = '100';
				$layout_settings_data_array['layout_settings_form_design_title_html_tag']          = 'h1';
				$layout_settings_data_array['layout_settings_form_design_title_alignment']         = 'left';
				$layout_settings_data_array['layout_settings_form_design_title_font_style']        = '24,#000000';
				$layout_settings_data_array['layout_settings_form_design_title_font_family']       = 'Roboto Slab:700';
				$layout_settings_data_array['layout_settings_form_design_description_html_tag']    = 'p';
				$layout_settings_data_array['layout_settings_form_design_description_alignment']   = 'left';
				$layout_settings_data_array['layout_settings_form_design_description_font_style']  = '12,#000000';
				$layout_settings_data_array['layout_settings_form_design_description_font_family'] = 'Roboto Slab:300';
				$layout_settings_data_array['layout_settings_form_design_form_margin']             = '0,0,0,0';
				$layout_settings_data_array['layout_settings_form_design_form_padding']            = '10,10,10,10';
				$layout_settings_data_array['layout_settings_form_design_title_margin']            = '0,0,5,0';
				$layout_settings_data_array['layout_settings_form_design_title_padding']           = '5,0,0,0';
				$layout_settings_data_array['layout_settings_form_design_description_margin']      = '0,0,5,0';
				$layout_settings_data_array['layout_settings_form_design_description_padding']     = '0,0,5,0';

				$layout_settings_data_array['layout_settings_input_field_width']                         = '90%';
				$layout_settings_data_array['layout_settings_input_field_height']                        = '100%';
				$layout_settings_data_array['layout_settings_input_field_text_alignment']                = 'left';
				$layout_settings_data_array['layout_settings_input_field_radio_button_alignment']        = 'single_row';
				$layout_settings_data_array['layout_settings_input_field_checkbox_alignment']            = 'single_row';
				$layout_settings_data_array['layout_settings_input_field_font_style']                    = '14,#000000';
				$layout_settings_data_array['layout_settings_input_field_font_family']                   = 'Roboto Condensed';
				$layout_settings_data_array['layout_settings_input_field_background_color_transparency'] = '#f7f7f7,100';
				$layout_settings_data_array['layout_settings_input_field_border_style']                  = '1,solid,#d1d1d1';
				$layout_settings_data_array['layout_settings_input_field_border_radius']                 = '2';
				$layout_settings_data_array['layout_settings_input_field_margin']                        = '5,0,5,0';
				$layout_settings_data_array['layout_settings_input_field_padding']                       = '10,10,10,10';

				$layout_settings_data_array['layout_settings_label_field_text_alignment']                = 'left';
				$layout_settings_data_array['layout_settings_label_field_width']                         = '100%';
				$layout_settings_data_array['layout_settings_label_field_height']                        = '100%';
				$layout_settings_data_array['layout_settings_label_field_font_style']                    = '16,#000000';
				$layout_settings_data_array['layout_settings_label_field_font_family']                   = 'Roboto Condensed';
				$layout_settings_data_array['layout_settings_label_field_background_color_transparency'] = '#ffffff,0';
				$layout_settings_data_array['layout_settings_label_field_margin']                        = '0,0,0,0';
				$layout_settings_data_array['layout_settings_label_field_padding']                       = '10,10,10,0';

				$layout_settings_data_array['layout_settings_button_text_alignment']                = 'center';
				$layout_settings_data_array['layout_settings_button_text']                          = 'Submit';
				$layout_settings_data_array['layout_settings_button_width']                         = '100px';
				$layout_settings_data_array['layout_settings_button_height']                        = '100%';
				$layout_settings_data_array['layout_settings_button_font_style']                    = '16,#ffffff';
				$layout_settings_data_array['layout_settings_button_font_family']                   = 'Roboto Slab';
				$layout_settings_data_array['layout_settings_button_background_color']              = '#524c52';
				$layout_settings_data_array['layout_settings_button_background_transparency']       = '100';
				$layout_settings_data_array['layout_settings_button_hover_background_color']        = '#706c70';
				$layout_settings_data_array['layout_settings_button_hover_background_transparency'] = '100';
				$layout_settings_data_array['layout_settings_button_border_style']                  = '1,solid,#524c52';
				$layout_settings_data_array['layout_settings_button_border_radius']                 = '4';
				$layout_settings_data_array['layout_settings_button_hover_border_color']            = '#706c70';
				$layout_settings_data_array['layout_settings_button_margin']                        = '10,0,0,0';
				$layout_settings_data_array['layout_settings_button_padding']                       = '10,10,10,10';

				$layout_settings_data_array['layout_settings_messages_text_alignment']                = 'left';
				$layout_settings_data_array['layout_settings_messages_background_color_transparency'] = '#e5ffd5,50';
				$layout_settings_data_array['layout_settings_messages_font_style']                    = '18,#6aa500';
				$layout_settings_data_array['layout_settings_messages_font_family']                   = 'Roboto Slab';
				$layout_settings_data_array['layout_settings_messages_margin']                        = '0,0,0,0';
				$layout_settings_data_array['layout_settings_messages_padding']                       = '0,0,0,0';

				$layout_settings_data_array['layout_settings_error_messages_background_color']        = '#ffffff';
				$layout_settings_data_array['layout_settings_error_messages_background_transparency'] = '50';
				$layout_settings_data_array['layout_settings_error_messages_font_style']              = '12,#ff2c38';
				$layout_settings_data_array['layout_settings_error_messages_font_family']             = 'Roboto Slab';
				$layout_settings_data_array['layout_settings_error_messages_margin']                  = '0,0,0,0';
				$layout_settings_data_array['layout_settings_error_messages_padding']                 = '5px,0px,0px,0px';

				$add_form_parent_data              = array();
				$add_form_parent_data['type']      = 'form';
				$add_form_parent_data['parent_id'] = $parent_id;
				$parent_last_id                    = $obj_dbhelper_contact_bank->insert_command( contact_bank(), $add_form_parent_data );

				$add_form_meta_data                = array();
				$add_form_meta_data['meta_id']     = $parent_last_id;
				$add_form_meta_data['meta_key']    = 'form_data';// WPCS: Slow Query ok.
				$add_form_meta_data['old_form_id'] = $parent_last_id;
				$add_form_meta_data['meta_value']  = maybe_serialize( $form_unserialized_data );// WPCS: Slow Query ok.
				$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $add_form_meta_data );

				$form_layout_settings                = array();
				$form_layout_settings['meta_id']     = $parent_last_id;
				$form_layout_settings['meta_key']    = 'layout_settings';// WPCS: Slow Query ok.
				$form_layout_settings['old_form_id'] = $parent_last_id;
				$form_layout_settings['meta_value']  = maybe_serialize( $layout_settings_data_array );// WPCS: Slow Query ok.
				$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $form_layout_settings );
				break;
			default:
				global $wpdb, $current_user;
				if ( $wpdb->query( "SHOW TABLES LIKE '" . $wpdb->prefix . "cb_contact_form'" ) !== 0 && $wpdb->query( "SHOW TABLES LIKE '" . $wpdb->prefix . "cb_form_settings_table'" ) !== 0 && $wpdb->query( "SHOW TABLES LIKE '" . $wpdb->prefix . "cb_create_control_form'" ) !== 0 ) {
					contact_bank_main_table();// WPCS: db call ok, no-cache ok.
					contact_bank_meta_table();

					// fetch form_ids of all forms.
					$get_contact_form = $wpdb->get_results( 'SELECT * FROM ' . $wpdb->prefix . 'cb_contact_form' );// WPCS: db call ok, no-cache ok.
					if ( count( $get_contact_form ) > 0 ) {
						foreach ( $get_contact_form as $value ) {
							$form_id   = $value->form_id;
							$form_name = $value->form_name;
							// fetch data of each form.
							$get_contact_form_data = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . $wpdb->prefix . 'cb_form_settings_table where form_id = %d', $form_id ) );// WPCS: db call ok, no-cache ok.
							// get email template data.
							$get_contact_form_email_template_data = $wpdb->get_results(
								$wpdb->prepare(
									'SELECT * FROM ' . $wpdb->prefix . 'cb_email_template_admin where form_id = %d', $form_id
								)
							);// WPCS: db call ok, no-cache ok.

							$admin_email_template_form_data  = array();
							$client_email_template_form_data = array();
							$email_template_count            = 0;
							foreach ( $get_contact_form_email_template_data as $email_template_data ) {
								if ( 0 == $email_template_count ) {// WPCS: loose comparison ok.
									$admin_email_template_form_data['template_send_to_email'] = $email_template_data->email_to;
									$admin_email_template_form_data['template_cc']            = $email_template_data->cc;
									$admin_email_template_form_data['template_send_to']       = 0 == $email_template_data->send_to ? 'send_to_email' : 'select_field';// WPCS: loose comparison ok.
									$admin_email_template_form_data['template_send_to_field'] = $email_template_data->email_to;
									$admin_email_template_form_data['template_bcc']           = $email_template_data->bcc;
									$admin_email_template_form_data['template_from_name']     = $email_template_data->from_name;
									$admin_email_template_form_data['template_from_email']    = $email_template_data->email_from;
									$admin_email_template_form_data['template_reply_to']      = $email_template_data->reply_to;
									$admin_email_template_form_data['template_subject']       = $email_template_data->subject;
									$admin_email_template_form_data['template_message']       = $email_template_data->body_content;
								} else {
									$client_email_template_form_data['template_send_to_email'] = $email_template_data->email_to;
									$client_email_template_form_data['template_cc']            = $email_template_data->cc;
									$client_email_template_form_data['template_send_to']       = 0 == $email_template_data->send_to ? 'send_to_email' : 'select_field';// WPCS: loose comparison ok.
									$client_email_template_form_data['template_send_to_field'] = $email_template_data->email_to;
									$client_email_template_form_data['template_bcc']           = $email_template_data->bcc;
									$client_email_template_form_data['template_from_name']     = $email_template_data->from_name;
									$client_email_template_form_data['template_from_email']    = $email_template_data->email_from;
									$client_email_template_form_data['template_reply_to']      = $email_template_data->reply_to;
									$client_email_template_form_data['template_subject']       = $email_template_data->subject;
									$client_email_template_form_data['template_message']       = $email_template_data->body_content;
								}
								$email_template_count++;
							}
							$form_data_array = array();
							if ( count( $get_contact_form_data ) > 0 ) {
								// create array of data of each form .
								foreach ( $get_contact_form_data as $key => $value ) {
									$form_data_array[ $value->form_message_key ] = $value->form_message_value;
								}
								$cb_form_data_array                                   = array();
								$cb_form_data_array['form_title']                     = $form_name;
								$cb_form_data_array['form_description']               = $form_data_array['form_description'];
								$cb_form_data_array['form_submission_limit']          = 10;
								$cb_form_data_array['created_date']                   = time();
								$cb_form_data_array['edited_on']                      = time();
								$cb_form_data_array['author']                         = $current_user->display_name;
								$cb_form_data_array['edited_by']                      = $current_user->display_name;
								$cb_form_data_array['form_save_submission_to_db']     = 'enable';
								$cb_form_data_array['form_submission_limit_message']  = 'disable';
								$cb_form_data_array['form_submission_message']        = '';
								$cb_form_data_array['form_success_message']           = $form_data_array['success_message'];
								$cb_form_data_array['form_enable_tooltip']            = 'show';
								$cb_form_data_array['form_redirect']                  = 0 == $form_data_array['redirect'] ? 'page' : 'url';// WPCS: loose comparison ok.
								$cb_form_data_array['form_redirect_url']              = 1 == $form_data_array['redirect'] ? $form_data_array['redirect_url'] : '';// WPCS: loose comparison ok.
								$cb_form_data_array['form_redirect_page_url']         = 0 == $form_data_array['redirect'] ? $form_data_array['redirect_url'] : '';// WPCS: loose comparison ok.
								$cb_form_data_array['form_admin_notification_email']  = '';
								$cb_form_data_array['form_client_notification_email'] = '';
								$cb_form_data_array['layout_settings_template']       = 'layout_settings_blank_form_template';
								$controls = array();
								// fetch controls ids of each form .
								$cb_create_control_form = $wpdb->get_results(
									$wpdb->prepare(
										'SELECT * FROM ' . $wpdb->prefix . 'cb_create_control_form where form_id = %d ORDER BY sorting_order ASC', $form_id
									)
								);// WPCS: db call ok, no-cache ok.
								if ( count( $cb_create_control_form ) > 0 ) {
									$count = 0;
									foreach ( $cb_create_control_form as $value ) {
										$count++;
										$control_id = $value->control_id;
										$field_id   = $value->field_id;
										// fetch data of controls of each form .
										$get_contact_form_table_data = $wpdb->get_results(
											$wpdb->prepare(
												'SELECT * FROM ' . $wpdb->prefix . 'cb_dynamic_settings where dynamicId = %d', $control_id
											)
										);// WPCS: db call ok, no-cache ok.

										$label_name_array = array();
										$cb_controls_data = array();

										foreach ( $get_contact_form_table_data as $key => $value ) {
											$cb_controls_data[ $value->dynamic_settings_key ] = $value->dynamic_settings_value;
										}
										if ( count( $cb_controls_data ) > 0 ) {
											$cb_form_controls_array                              = array();
											$cb_form_controls_array['label_name']                = '' != $cb_controls_data['cb_label_value'] ? $cb_controls_data['cb_label_value'] : 'Untitled';// WPCS: loose comparison ok.
											$cb_form_controls_array['required_type']             = 1 == $cb_controls_data['cb_control_required'] ? 'enable' : 'disable';// WPCS: loose comparison ok.
											$cb_form_controls_array['label_tooltip']             = isset( $cb_controls_data['cb_description'] ) ? esc_attr( $cb_controls_data['cb_description'] ) : esc_attr( $cb_controls_data['cb_tooltip_txt'] );
											$cb_form_controls_array['placeholder']               = isset( $cb_controls_data['cb_default_txt_val'] ) ? $cb_controls_data['cb_default_txt_val'] : '';
											$cb_form_controls_array['admin_label']               = $cb_controls_data['cb_admin_label'];
											$cb_form_controls_array['label_placement']           = 'above';
											$cb_form_controls_array['container_class']           = '';
											$cb_form_controls_array['element_class']             = '';
											$cb_form_controls_array['autocomplete_type']         = 'enable';
											$cb_form_controls_array['disable_input']             = 'disable';
											$cb_form_controls_array['custom_validation_message'] = '';
											$cb_form_controls_array['timestamp']                 = time() + $count;
											array_push( $label_name_array, $cb_form_controls_array['label_name'] );
											$timestamp = time() + $count;
											switch ( $field_id ) {
												case '1':
														$cb_form_controls_array['control_type']          = 'text';
														$cb_form_controls_array['input_limit_number']    = 50;
														$cb_form_controls_array['text_appear']           = 'Characters Left';
														$cb_form_controls_array['input_mask_type']       = 'none';
														$cb_form_controls_array['custom_mask']           = '999,999,999,999';
														$cb_form_controls_array['input_validation_type'] = 'characters';
														$cb_form_controls_array['default_value']         = '';
														$cb_form_controls_array['field_key']             = 'single_line_text_field_key_' . $timestamp;
													break;
												case '2':
													$cb_form_controls_array['control_type']          = 'paragraph';
													$cb_form_controls_array['rows_number']           = 2;
													$cb_form_controls_array['input_limit_number']    = 50;
													$cb_form_controls_array['text_appear']           = 'Characters Left';
													$cb_form_controls_array['input_mask_type']       = 'none';
													$cb_form_controls_array['custom_mask']           = '999,999,999,999';
													$cb_form_controls_array['input_validation_type'] = 'characters';
													$cb_form_controls_array['default_value']         = '';
													$cb_form_controls_array['field_key']             = 'paragraph_text_field_key_' . $timestamp;
													break;
												case '3':
													$cb_form_controls_array['control_type']  = 'email';
													$cb_form_controls_array['default_value'] = '';
													$cb_form_controls_array['field_key']     = 'email_address_field_key_' . $timestamp;
													break;
												case '4':
													$cb_form_controls_array['control_type'] = 'select';
													$cb_select_control_array                = maybe_unserialize( $cb_controls_data['cb_dropdown_option_val'] );
													$option_values                          = '[';
													foreach ( $cb_select_control_array as $value ) {
														$option_values .= '{"value":"' . $value . '","text":"' . $value . '"},';
													}
													if ( substr( $option_values, -1, 1 ) == ',' ) {// WPCS: loose comparison ok.
														$option_values = substr( $option_values, 0, -1 );
													}
													$option_values                                    .= ']';
													$cb_form_controls_array['drop_down_option_values'] = json_decode( stripslashes( $option_values ) );
													$cb_form_controls_array['default_value']           = '';
													$cb_form_controls_array['field_key']               = 'select_field_key_' . $timestamp;
													break;
												case '5':
													$cb_form_controls_array['control_type'] = 'checkbox-list';
													$cb_checkbox_list_array                 = maybe_unserialize( $cb_controls_data['cb_checkbox_option_val'] );
													$option_values                          = '[';
													foreach ( $cb_checkbox_list_array as $value ) {
														$option_values .= '{"value":"' . $value . '","text":"' . $value . '"},';
													}
													if ( substr( $option_values, -1, 1 ) == ',' ) {// WPCS: loose comparison ok.
														$option_values = substr( $option_values, 0, -1 );
													}
													$option_values                                    .= ']';
													$cb_form_controls_array['drop_down_option_values'] = json_decode( stripslashes( $option_values ) );
													$cb_form_controls_array['field_key']               = 'checkbox_list_field_key_' . $timestamp;
													break;
												case '6':
													$cb_form_controls_array['control_type'] = 'radio-list';
													$cb_radio_list_array                    = maybe_unserialize( $cb_controls_data['cb_radio_option_val'] );
													$option_values                          = '[';
													foreach ( $cb_radio_list_array as $value ) {
														$option_values .= '{"value":"' . $value . '","text":"' . $value . '"},';
													}
													if ( substr( $option_values, -1, 1 ) == ',' ) {// WPCS: loose comparison ok.
														$option_values = substr( $option_values, 0, -1 );
													}
													$option_values                                    .= ']';
													$cb_form_controls_array['drop_down_option_values'] = json_decode( stripslashes( $option_values ) );
													$cb_form_controls_array['field_key']               = 'radio_list_field_key_' . $timestamp;
													break;
												case '7':
													$cb_form_controls_array['control_type']  = 'number';
													$cb_form_controls_array['max_number']    = 20;
													$cb_form_controls_array['min_number']    = 10;
													$cb_form_controls_array['step']          = 2;
													$cb_form_controls_array['default_value'] = '';
													$cb_form_controls_array['field_key']     = 'number_field_key_' . $timestamp;
													break;
												case '8':
													$cb_form_controls_array['control_type']  = 'first_name';
													$cb_form_controls_array['default_value'] = '';
													$cb_form_controls_array['field_key']     = 'first_name_field_key_' . $timestamp;
													break;
												case '9':
													$cb_form_controls_array['control_type']    = 'file_upload';
													$cb_form_controls_array['maximum_size']    = $cb_controls_data['cb_maximum_file_allowed'] . 'mb';
													$cb_form_controls_array['extension']       = $cb_controls_data['cb_allow_file_ext_upload'];
													$cb_form_controls_array['multiple_upload'] = 1 == $cb_controls_data['cb_allow_multiple_file'] ? 'true' : 'false';// WPCS: loose comparison ok.
													$cb_form_controls_array['attach_to_email'] = 'enable';
													$cb_form_controls_array['default_value']   = '';
													$cb_form_controls_array['field_key']       = 'file_upload_field_key_' . $timestamp;
													break;
												case '10':
													$cb_form_controls_array['control_type']          = 'phone';
													$cb_form_controls_array['input_limit_number']    = 50;
													$cb_form_controls_array['text_appear']           = 'Characters Left';
													$cb_form_controls_array['input_mask_type']       = 'none';
													$cb_form_controls_array['custom_mask']           = '999,999,999,999';
													$cb_form_controls_array['input_validation_type'] = 'characters';
													$cb_form_controls_array['default_value']         = '';
													$cb_form_controls_array['field_key']             = 'phone_field_key_' . $timestamp;
													break;
												case '11':
													$cb_form_controls_array['control_type']          = 'address';
													$cb_form_controls_array['input_limit_number']    = 50;
													$cb_form_controls_array['text_appear']           = 'Characters Left';
													$cb_form_controls_array['input_mask_type']       = 'none';
													$cb_form_controls_array['custom_mask']           = '999,999,999,999';
													$cb_form_controls_array['input_validation_type'] = 'characters';
													$cb_form_controls_array['default_value']         = '';
													$cb_form_controls_array['field_key']             = 'address_field_key_' . $timestamp;
													break;
												case '12':
													$date_format = $cb_controls_data['cb_date_format'];
													switch ( $date_format ) {
														case '0':
															$cb_form_controls_array['date_format'] = 'F j ,Y';
															break;
														case '1':
															$cb_form_controls_array['date_format'] = 'Y/m/d';
															break;
														case '2':
															$cb_form_controls_array['date_format'] = 'm/d/Y';
															break;
														case '3':
															$cb_form_controls_array['date_format'] = 'd/m/Y';
															break;
													}
													$cb_form_controls_array['control_type']         = 'date';
													$cb_form_controls_array['start_year']           = $cb_controls_data['cb_start_year'];
													$cb_form_controls_array['end_year']             = $cb_controls_data['cb_end_year'];
													$cb_form_controls_array['default_current_date'] = 'disable';
													$cb_form_controls_array['default_value']        = '';
													$cb_form_controls_array['field_key']            = 'date_field_key_' . $timestamp;
													break;
												case '13':
													$cb_form_controls_array['control_type']  = 'time';
													$cb_form_controls_array['time_format']   = 12 == $cb_controls_data['cb_hour_format'] ? '12hour' : '24hour';// WPCS: loose comparison ok.
													$cb_form_controls_array['current_time']  = 'disable';
													$cb_form_controls_array['default_value'] = '';
													$cb_form_controls_array['field_key']     = 'time_field_key_' . $timestamp;
													break;
												case '15':
													$cb_form_controls_array['control_type']          = 'password';
													$cb_form_controls_array['default_current_date']  = 'disable';
													$cb_form_controls_array['input_limit_number']    = 50;
													$cb_form_controls_array['text_appear']           = 'Characters Left';
													$cb_form_controls_array['input_mask_type']       = 'none';
													$cb_form_controls_array['custom_mask']           = '999,999,999,999';
													$cb_form_controls_array['input_validation_type'] = 'characters';
													$cb_form_controls_array['default_value']         = '';
													$cb_form_controls_array['field_key']             = 'password_field_key_' . $timestamp;
													break;
												case '16':
													$cb_form_controls_array['control_type']  = 'website_url';
													$cb_form_controls_array['default_value'] = '';
													$cb_form_controls_array['field_key']     = 'website_url_field_key_' . $timestamp;
													break;
											}
											// Admin email template.
											$admin_email_template_form_data['template_send_to_email'] = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $admin_email_template_form_data['template_send_to_email'] );
											$admin_email_template_form_data['template_cc']            = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $admin_email_template_form_data['template_cc'] );
											$admin_email_template_form_data['template_send_to_field'] = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $admin_email_template_form_data['template_send_to_field'] );
											$admin_email_template_form_data['template_bcc']           = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $admin_email_template_form_data['template_bcc'] );
											$admin_email_template_form_data['template_from_name']     = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $admin_email_template_form_data['template_from_name'] );
											$admin_email_template_form_data['template_from_email']    = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $admin_email_template_form_data['template_from_email'] );
											$admin_email_template_form_data['template_reply_to']      = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $admin_email_template_form_data['template_reply_to'] );
											$admin_email_template_form_data['template_subject']       = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $admin_email_template_form_data['template_subject'] );
											$admin_email_template_form_data['template_message']       = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $admin_email_template_form_data['template_message'] );
											// Client email template.
											$client_email_template_form_data['template_send_to_email'] = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $client_email_template_form_data['template_send_to_email'] );
											$client_email_template_form_data['template_cc']            = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $client_email_template_form_data['template_cc'] );
											$client_email_template_form_data['template_send_to_field'] = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $client_email_template_form_data['template_send_to_field'] );
											$client_email_template_form_data['template_bcc']           = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $client_email_template_form_data['template_bcc'] );
											$client_email_template_form_data['template_from_name']     = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $client_email_template_form_data['template_from_name'] );
											$client_email_template_form_data['template_from_email']    = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $client_email_template_form_data['template_from_email'] );
											$client_email_template_form_data['template_reply_to']      = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $client_email_template_form_data['template_reply_to'] );
											$client_email_template_form_data['template_subject']       = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $client_email_template_form_data['template_subject'] );
											$client_email_template_form_data['template_message']       = str_replace( '[control_' . $control_id . ']', '[control_' . $cb_form_controls_array['timestamp'] . ']', $client_email_template_form_data['template_message'] );
											array_push( $controls, $cb_form_controls_array );
										}
									}
								}
								$cb_form_data_array['controls'] = $controls;
								// Email templates data.
								$admin_email_template_form_data['template_message']   = htmlspecialchars_decode( $admin_email_template_form_data['template_message'] );
								$client_email_template_form_data['template_message']  = htmlspecialchars_decode( $client_email_template_form_data['template_message'] );
								$cb_form_data_array['form_admin_notification_email']  = $admin_email_template_form_data;
								$cb_form_data_array['form_client_notification_email'] = $client_email_template_form_data;

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
								$layout_settings_array['layout_settings_button_padding']                       = '10,10,10,10';

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

								$parent_id = $wpdb->get_var(
									$wpdb->prepare(
										'SELECT id FROM ' . $wpdb->prefix . 'contact_bank WHERE type = %s', 'forms'
									)
								);// WPCS: db call ok, no-cache ok.

								$add_form_parent_data              = array();
								$add_form_parent_data['type']      = 'form';
								$add_form_parent_data['parent_id'] = $parent_id;
								$parent_last_id                    = $obj_dbhelper_contact_bank->insert_command( contact_bank(), $add_form_parent_data );

								$add_form_meta_data                = array();
								$add_form_meta_data['old_form_id'] = $form_id;
								$add_form_meta_data['meta_id']     = $parent_last_id;
								$add_form_meta_data['meta_key']    = 'form_data';// WPCS: slow query ok.
								$add_form_meta_data['meta_value']  = maybe_serialize( $cb_form_data_array );// WPCS: slow query ok.
								$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $add_form_meta_data );

								$add_form_layout_settings_meta_data                = array();
								$add_form_layout_settings_meta_data['old_form_id'] = $form_id;
								$add_form_layout_settings_meta_data['meta_id']     = $parent_last_id;
								$add_form_layout_settings_meta_data['meta_key']    = 'layout_settings';// WPCS: slow query ok.
								$add_form_layout_settings_meta_data['meta_value']  = maybe_serialize( $layout_settings_array );// WPCS: slow query ok.
								$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $add_form_layout_settings_meta_data );

								// frontend form data .
								$get_frontend_form_data = $wpdb->get_results(
									$wpdb->prepare(
										'SELECT form_submit_id FROM ' . $wpdb->prefix . 'cb_frontend_data_table WHERE form_id = %d', $form_id // get frontend form submit id .
									)
								);// WPCS: db call ok, no-cache ok.
								$form_submit_id         = array();
								if ( count( $get_frontend_form_data ) > 0 ) {
									foreach ( $get_frontend_form_data as $value ) {
										array_push( $form_submit_id, $value->form_submit_id );
									}
									$unique_form_submit_id = array();
									$unique_form_submit_id = array_unique( $form_submit_id ); // unique form submit id .
									foreach ( $unique_form_submit_id as $key ) {
										// get frontend form submit data .
										$cb_dynamic_frontend_form_data = $wpdb->get_results(
											$wpdb->prepare(
												'SELECT * FROM ' . $wpdb->prefix . 'cb_frontend_data_table where form_id = %d and form_submit_id = %d', $form_id, $key
											)
										);// WPCS: db call ok, no-cache ok.

										$cb_front_end_data_array = array();

										foreach ( $cb_dynamic_frontend_form_data as $value ) {
											if ( $value->field_Id == 5 ) { // @codingStandardsIgnoreLine.
												$cb_checkbox_list                                      = str_replace( '-', ',', $value->dynamic_frontend_value );
												$cb_front_end_data_array[ $value->dynamic_control_id ] = $cb_checkbox_list;
											} else {
												$cb_front_end_data_array[ $value->dynamic_control_id ] = $value->dynamic_frontend_value;
											}
										}
										$cb_label_value_array = array();
										foreach ( $cb_front_end_data_array as $id => $label_value ) {
											// get label control value.
											$cb_dynamic_settings_value = $wpdb->get_var(
												$wpdb->prepare(
													'SELECT dynamic_settings_value FROM ' . $wpdb->prefix . 'cb_dynamic_settings where dynamicId = %d and dynamic_settings_key = %s', $id, 'cb_label_value'
												)
											);// WPCS: db call ok, no-cache ok.

											$cb_selected_form_data = $wpdb->get_var(
												$wpdb->prepare(
													'SELECT meta_value FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_id = %d and meta_key = %s', $parent_last_id, 'form_data'
												)
											);// WPCS: db call ok, no-cache ok.

											$cb_unserialize_selected_form_data = maybe_unserialize( $cb_selected_form_data );
											if ( isset( $cb_unserialize_selected_form_data['controls'] ) && count( $cb_unserialize_selected_form_data['controls'] ) > 0 ) {
												foreach ( $cb_unserialize_selected_form_data['controls'] as $control_value ) {
													if ( $cb_dynamic_settings_value == $control_value['label_name'] ) { // WPCS: loose comparison ok.
														$cb_label_timestamp                          = $control_value['timestamp'];
														$cb_label_value_array[ $cb_label_timestamp ] = $label_value;
													}
												}
											}
										}
										$cb_label_value_array['timestamp']      = time();
										$frontend_form_meta_data                = array();
										$frontend_form_meta_data['old_form_id'] = $form_id;
										$frontend_form_meta_data['meta_id']     = $form_id;
										$frontend_form_meta_data['meta_key']    = 'submission_form_data';// WPCS: slow query ok.
										$frontend_form_meta_data['meta_value']  = maybe_serialize( $cb_label_value_array );// WPCS: slow query ok.
										$obj_dbhelper_contact_bank->insert_command( contact_bank_meta(), $frontend_form_meta_data );
									}
								}
							}
						}
					}
					// Drop Tables .
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'cb_contact_form' );// @codingStandardsIgnoreLine.
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'cb_dynamic_settings' );// @codingStandardsIgnoreLine.
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'cb_create_control_form' );// @codingStandardsIgnoreLine.
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'cb_frontend_data_table' );// @codingStandardsIgnoreLine.
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'cb_email_template_admin' );// @codingStandardsIgnoreLine.
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'cb_frontend_forms_table' );// @codingStandardsIgnoreLine.
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'cb_form_settings_table' );// @codingStandardsIgnoreLine.
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'cb_layout_settings_table' );// @codingStandardsIgnoreLine.
					$wpdb->query( 'DROP TABLE IF EXISTS ' . $wpdb->prefix . 'cb_roles_capability' );// @codingStandardsIgnoreLine.
				}
				global $wpdb;
				$general_settings_serialized_data = $wpdb->get_var(
					$wpdb->prepare(
						'SELECT meta_value FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s', 'general_settings'
					)
				);// WPCS: db call ok, no-cache ok.

				$general_settings_unserialized_data = maybe_unserialize( $general_settings_serialized_data );
				if ( ! in_array( 'gdpr_compliance', $general_settings_unserialized_data ) ) {// @codingStandardsIgnoreLine.
					$where             = array();
					$where['meta_key'] = 'general_settings';// WPCS: slow query ok.
					$general_settings_unserialized_data['gdpr_compliance']      = 'enable';
					$general_settings_unserialized_data['gdpr_compliance_text'] = 'By using this form you agree with the storage and handling of your data by this website';

					$general_settings_data_array               = array();
					$general_settings_data_array['meta_value'] = maybe_serialize( $general_settings_unserialized_data );// WPCS: slow query ok.
					$obj_dbhelper_contact_bank->update_command( contact_bank_meta(), $general_settings_data_array, $where );
				}
				$get_collate_status_data = $wpdb->query(
					$wpdb->prepare(
						'SELECT type FROM ' . $wpdb->prefix . 'contact_bank WHERE type=%s', 'collation_type'
					)
				);// db call ok; no-cache ok.
				$charset_collate         = '';
				if ( ! empty( $wpdb->charset ) ) {
					$charset_collate .= 'CONVERT TO CHARACTER SET ' . $wpdb->charset;
				}
				if ( ! empty( $wpdb->collate ) ) {
					$charset_collate .= ' COLLATE ' . $wpdb->collate;
				}
				if ( 0 === $get_collate_status_data ) {
					if ( ! empty( $charset_collate ) ) {
						$change_collate_main_table = $wpdb->query(
							'ALTER TABLE ' . $wpdb->prefix . 'contact_bank ' . $charset_collate // @codingStandardsIgnoreLine.
						);// WPCS: db call ok, no-cache ok.
						$change_collate_meta_table = $wpdb->query(
							'ALTER TABLE ' . $wpdb->prefix . 'contact_bank_meta ' . $charset_collate // @codingStandardsIgnoreLine.
						);// WPCS: db call ok, no-cache ok.

						$collation_data_array              = array();
						$collation_data_array['type']      = 'collation_type';
						$collation_data_array['parent_id'] = '0';
						$obj_dbhelper_contact_bank->insert_command( contact_bank(), $collation_data_array );
					}
				}
				break;
		}
			update_option( 'contact-bank-version-number', '3.0.1' );
	}
}
