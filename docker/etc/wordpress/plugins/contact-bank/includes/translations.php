<?php
/**
 * This file is used for translating strings.
 *
 * @author   Tech Banker
 * @package  contact-bank/includes
 * @version  3.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
} // Exit if accessed directly
if ( ! is_user_logged_in() ) {
	return;
} else {
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

		// Disclaimer.
		$cb_upgrade_need_help = __( 'Know about ', 'contact-bank' );
		$cb_documentation     = __( 'Full Features', 'contact-bank' );
		$cb_read_and_check    = __( ' or check our ', 'contact-bank' );
		$cb_demos_section     = __( 'Online Demos', 'contact-bank' );

		// Premium edition.
		$cb_wizard_choose_template  = __( 'Choose Template', 'contact-bank' );
		$cb_copied_failed           = __( 'Copy', 'contact-bank' );
		$cb_message_premium_edition = __( 'This feature is available only in Premium Editions! <br> Kindly Purchase to unlock it!', 'contact-bank' );
		$cb_premium_edition         = __( 'Premium Editions', 'contact-bank' );
		$cb_premium                 = __( 'Premium ', 'contact-bank' );

		// Footer.
		$cb_saved_settings               = __( 'Settings Saved!', 'contact-bank' );
		$cb_confirm_data                 = __( 'Are you Sure ?', 'contact-bank' );
		$cb_textarea                     = __( 'Textarea', 'contact-bank' );
		$cb_manage_backups_close         = __( 'Close', 'contact-bank' );
		$cb_popup_query_placeholder      = __( 'Please enter the text.', 'contact-bank' );
		$cb_invalid_card_number          = __( 'Invalid Card Number', 'contact-bank' );
		$cb_invalid_cvv_number           = __( 'Invalid CVV Number', 'contact-bank' );
		$cb_card_expiry_date             = __( 'Required Expiration Date', 'contact-bank' );
		$cb_number_enter_between_message = __( 'Please enter number between', 'contact-bank' );
		$cb_number_increment_by_message  = __( 'Please Increment By', 'contact-bank' );
		$cb_delete_message               = __( 'Data Deleted', 'contact-bank' );
		$cb_wizard_choose_template       = __( 'Choose Template', 'contact-bank' );

		// Common.
		$cb_manage_forms          = __( 'Manage Forms', 'contact-bank' );
		$cb_add_new_form          = __( 'Add New Form', 'contact-bank' );
		$cb_contact_bank          = __( 'Contact Bank', 'contact-bank' );
		$cb_user_access_message   = __( 'You do not have Sufficient Access to this Page. Kindly contact the Administrator for more Privileges', 'contact-bank' );
		$cb_enable                = __( 'Enable', 'contact-bank' );
		$cb_disable               = __( 'Disable', 'contact-bank' );
		$cb_save_changes          = __( 'Save Changes', 'contact-bank' );
		$cb_bulk_action           = __( 'Bulk Action', 'contact-bank' );
		$cb_delete                = __( 'Delete Form', 'contact-bank' );
		$cb_duplicate             = __( 'Duplicate Form', 'contact-bank' );
		$cb_bulk_delete           = __( 'Delete Forms', 'contact-bank' );
		$cb_bulk_duplicate        = __( 'Duplicate Forms', 'contact-bank' );
		$cb_edit                  = __( 'Edit Form', 'contact-bank' );
		$cb_apply                 = __( 'Apply', 'contact-bank' );
		$cb_add_form              = __( 'Add Form', 'contact-bank' );
		$cb_form_width            = __( 'Form Width (px or %)', 'contact-bank' );
		$cb_success               = __( 'Success!', 'contact-bank' );
		$cb_alignment             = __( 'Alignment', 'contact-bank' );
		$cb_alignment_tooltip     = __( 'Choose Alignment for Text', 'contact-bank' );
		$cb_add_option            = __( 'Add', 'contact-bank' );
		$cb_add_import            = __( 'Import', 'contact-bank' );
		$cb_add_delete            = __( 'Delete', 'contact-bank' );
		$cb_add_fill_option_value = __( 'Please Fill the option and Value', 'contact-bank' );
		$cb_not_available         = __( 'N/A', 'contact-bank' );

		// Forms.
		$cb_controls          = __( 'Controls', 'contact-bank' );
		$cb_advanced_settings = __( 'Advanced Settings', 'contact-bank' );
		$cb_form_id           = __( 'Form ID', 'contact-bank' );
		$cb_details           = __( 'Forms', 'contact-bank' );
		$cb_email_settings    = __( 'Email Settings', 'contact-bank' );
		$cb_form_entries      = __( 'Form Submissions', 'contact-bank' );
		$cb_date_time         = __( 'Date / Time', 'contact-bank' );
		$cb_preview           = __( 'Preview Form', 'contact-bank' );

		// add new form.
		$cb_add_data_to_import             = __( 'Please provide atleast one option and value seperated by comma to Import!', 'contact-bank' );
		$cb_choose_arithematic_operation   = __( 'Please choose atleast one arithematic operation', 'contact-bank' );
		$cb_choose_relational_operation    = __( 'Please choose atleast one relational operation', 'contact-bank' );
		$cb_choose_arrange_order_operation = __( 'Please choose atleast one arrange order operation', 'contact-bank' );
		$cb_title_alignment_tooltip        = __( 'Choose Alignment for Text', 'contact-bank' );
		$cb_form_title                     = __( 'Form Title', 'contact-bank' );
		$cb_form_description               = __( 'Form Description', 'contact-bank' );
		$cb_form_title_tooltip             = __( 'Enter Form Title', 'contact-bank' );
		$cb_add_new_title_placeholder      = __( 'Please provide form title here', 'contact-bank' );
		$cb_form_description_tooltip       = __( 'Enter Form Description', 'contact-bank' );
		$cb_forms_title_description        = __( 'Form Title & Description', 'contact-bank' );
		$cb_success_message                = __( 'Success Message', 'contact-bank' );
		$cb_success_message_tooltip        = __( 'Enter Success Message after Form Submission', 'contact-bank' );
		$cb_redirect                       = __( 'Redirect Url After Form Submission', 'contact-bank' );
		$cb_redirect_tooltip               = __( 'Choose either Page or Url where you want to redirect the page after submission', 'contact-bank' );
		$cb_url                            = __( 'URL', 'contact-bank' );
		$cb_url_redirect_placeholder       = __( 'Enter Redirect URL', 'contact-form' );
		$cb_page                           = __( 'Page', 'contact-bank' );
		$cb_page_tooltip                   = __( 'Choose the page where you want to redirect after form submission', 'contact-bank' );
		$cb_wizard_create_form             = __( 'Create Form', 'contact-bank' );
		$cb_next_step                      = __( 'Next Step', 'contact-bank' );
		$cb_previous_step                  = __( 'Previous Step', 'contact-bank' );
		$cb_blank_form                     = __( 'Blank Form', 'contact-bank' );
		$cb_blank_form_desc                = __( 'The blank form allows you to create any type of form using our drag &amp; drop builder.', 'contact-bank' );
		$cb_contact_us                     = __( 'Contact Us', 'contact-bank' );
		$cb_contact_us_desc                = __( 'Allow your users to contact you with this simple contact form. You can add and remove fields as needed.', 'contact-bank' );
		$cb_quote_request                  = __( 'Quote Request', 'contact-bank' );
		$cb_quote_request_desc             = __( 'Manage quote requests from your website easily with this template. You can add and remove fields as needed.', 'contact-bank' );
		$cb_event_registration             = __( 'Event Registration', 'contact-bank' );
		$cb_event_registration_desc        = __( 'Allow user to register for your next event this easy to complete form. You can add and remove fields as needed.', 'contact-bank' );
		$cb_select_form_message            = __( 'Please select Template to Proceed', 'contact-bank' );
		$cb_select_form_error_message      = __( 'Please select form to Proceed!', 'contact-bank' );
		$cb_untitled_form                  = __( 'Untitled Form', 'contact-bank' );
		$cb_enter_digit_star               = __( 'Please enter digits between 1 and 5', 'contact-bank' );
		$enable_tooltip                    = __( 'Enable Tooltip', 'contact-bank' );
		$enable_message_tooltips           = __( 'Do you want to show tooltips in controls of Contact Form?', 'contact-bank' );

		// Tabs.
		$cb_general_tab      = __( 'General', 'contact-bank' );
		$cb_options_tab      = __( 'Options', 'contact-bank' );
		$cb_appearance_tab   = __( 'Appearance', 'contact-bank' );
		$cb_restrictions_tab = __( 'Restrictions', 'contact-bank' );
		$cb_advanced_tab     = __( 'Advanced', 'contact-bank' );

		// General Tab.
		$cb_general_label_form                           = __( 'Enter the suitable label for Control', 'contact-bank' );
		$cb_label_general_placeholder                    = __( 'Please provide label', 'contact-bank' );
		$cb_general_tooltip_description                  = __( 'Enter the description for Control', 'contact-bank' );
		$cb_general_tootltip_placeholder                 = __( 'Please provide description for tooltip', 'contact-bank' );
		$cb_general_label_placement                      = __( 'Here, You can Select the position of your label relative to the field element itself', 'contact-bank' );
		$cb_general_logical_captcha                      = __( 'You can Select this option to make the Logical Captcha', 'contact-bank' );
		$cb_general_mathematical_operations              = __( 'Mathematical Operations', 'contact-bank' );
		$cb_general_arithmetic                           = __( 'Arithmetic', 'contact-bank' );
		$cb_general_relational                           = __( 'Relational', 'contact-bank' );
		$cb_general_arrange_order                        = __( 'Arrange Order', 'contact-bank' );
		$cb_general_arithmetic_operations                = __( 'Arithmetic Actions', 'contact-bank' );
		$cb_general_arithmetic_operations_tooltip        = __( 'Choose specific Arithmetic actions to create a Captcha Control', 'contact-bank' );
		$cb_general_arithmeric_addition                  = __( 'Addition(+)', 'contact-bank' );
		$cb_general_arithmeric_subtraction               = __( 'Subtraction(-)', 'contact-bank' );
		$cb_general_arithmeric_mutiplication             = __( 'Multiplication(*)', 'contact-bank' );
		$cb_general_arithmeric_division                  = __( 'Division(/)', 'contact-bank' );
		$cb_general_relational_operations                = __( 'Relational Actions', 'contact-bank' );
		$cb_general_relational_operations_tooltip        = __( 'Choose specific Relational actions to create a Captcha Control', 'contact-bank' );
		$cb_general_relational_largest_number            = __( 'Largest Number', 'contact-bank' );
		$cb_general_relational_smallest_number           = __( 'Smallest Number', 'contact-bank' );
		$cb_general_ascending_order                      = __( 'Ascending Order', 'contact-bank' );
		$cb_general_descending_order                     = __( 'Descending Order', 'contact-bank' );
		$cb_general_arrange_order_tootltip               = __( 'Choose the specific Arranging order for Captcha Control', 'contact-bank' );
		$cb_general_answer                               = __( 'Answer', 'contact-bank' );
		$cb_general_answer_tooltip                       = __( 'Enter your Answer', 'contact-bank' );
		$cb_general_answer_placeholder                   = __( 'Please provide answer', 'contact-bank' );
		$cb_general_field_description                    = __( 'Field Description', 'contact-bank' );
		$cb_general_field_description_tooltip            = __( 'Enter the Field Description for form', 'contact-bank' );
		$cb_general_field_description_placeholder        = __( 'Please provide field description', 'contact-bank' );
		$cb_general_html_editor_content                  = __( 'Content', 'contact-bank' );
		$cb_general_html_editor_content_tooltip          = __( 'Content to be used in HTML Editor', 'contact-bank' );
		$cb_general_date_format                          = __( 'Format', 'contact-bank' );
		$cb_general_date_format_tooltip                  = __( 'Choose Date format for Date Control', 'contact-bank' );
		$cb_general_date_start_year                      = __( 'Start Year', 'contact-bank' );
		$cb_general_date_start_year_tooltip              = __( 'Start Year for this field', 'contact-bank' );
		$cb_general_date_start_year_placeholder          = __( 'Please provide start year', 'contact-bank' );
		$cb_general_date_end_year                        = __( 'End Year', 'contact-bank' );
		$cb_general_date_end_year_tooltip                = __( 'End Year for this field', 'contact-bank' );
		$cb_general_date_end_year_placeholder            = __( 'Please provide end year', 'contact-bank' );
		$cb_general_default_current_date                 = __( 'Default Current Date', 'contact-bank' );
		$cb_general_default_current_date_tooltip         = __( 'Do you want to display the default Current Date?', 'contact-bank' );
		$cb_general_time_format                          = __( 'Time Format', 'contact-bank' );
		$cb_general_time_format_tooltip                  = __( 'Choose Format for the Time that you want to display', 'contact-bank' );
		$cb_general_time_format_twelve                   = __( '12 Hour', 'contact-bank' );
		$cb_general_time_format_twentyfour               = __( '24 Hour', 'contact-bank' );
		$cb_general_default_current_time                 = __( 'Default Current Time', 'contact-bank' );
		$cb_general_default_current_time_tooltip         = __( 'Do you want to display the default Current Time?', 'contact-bank' );
		$cb_general_product                              = __( 'Product', 'contact-bank' );
		$cb_general_product_tooltip                      = __( 'Choose Product', 'contact-bank' );
		$cb_general_select_product                       = __( 'Select a Product', 'contact-bank' );
		$cb_general_min_number                           = __( 'Min', 'contact-bank' );
		$cb_general_min_number_tooltip                   = __( 'Minimum Number', 'contact-bank' );
		$cb_general_min_number_placeholder               = __( 'Please provide min number', 'contact-bank' );
		$cb_general_max_number                           = __( 'Max', 'contact-bank' );
		$cb_general_max_number_tooltip                   = __( 'Maximum Number', 'contact-bank' );
		$cb_general_max_number_placeholder               = __( 'Please provide max number', 'contact-bank' );
		$cb_general_step                                 = __( 'Step', 'contact-bank' );
		$cb_general_step_tooltip                         = __( 'Step for this field which you want to increment after', 'contact-bank' );
		$cb_general_step_placeholder                     = __( 'Please provide step count', 'contact-bank' );
		$cb_general_file_upload_maximum_size             = __( 'Maximum Size', 'contact-bank' );
		$cb_general_file_upload_maximum_size_tooltip     = __( 'Enter Maximum size for File Upload', 'contact-bank' );
		$cb_general_file_upload_maximum_size_placeholder = __( 'Please provide maximum size', 'contact-bank' );
		$cb_general_file_upload_extension                = __( 'Extension', 'contact-bank' );
		$cb_general_file_upload_extension_tooltip        = __( 'Extensions to be used for File Upload', 'contact-bank' );
		$cb_general_file_upload_extension_placeholder    = __( 'Please provide file extension', 'contact-bank' );
		$cb_general_file_upload_multiple_upload          = __( 'Multiple Upload', 'contact-bank' );
		$cb_general_file_upload_multiple_upload_tooltip  = __( 'Do you want to allow Multiple Uploads?', 'contact-bank' );
		$cb_general_file_upload_attach_email             = __( 'Attach To Email', 'contact-bank' );
		$cb_general_file_upload_attach_email_tooltip     = __( 'Do you want to attach files to email?', 'contact-bank' );
		$cb_general_product_price                        = __( 'Price', 'contact-bank' );
		$cb_general_product_price_tooltip                = __( 'Enter Price', 'contact-bank' );
		$cb_general_product_price_placeholder            = __( 'Please provide product price', 'contact-bank' );
		$cb_general_shipping_cost                        = __( 'Cost', 'contact-bank' );
		$cb_general_shipping_cost_tooltip                = __( 'Enter Cost for Shipping', 'contact-bank' );
		$cb_general_shipping_cost_placeholder            = __( 'Please provide shipping cost', 'contact-bank' );
		$cb_general_credit_card_number                   = __( 'Credit Card Number', 'contact-bank' );
		$cb_general_credit_card_number_tooltip           = __( 'Enter Credit Card Number', 'contact-bank' );
		$cb_general_credit_card_number_placeholder       = __( 'Please provide card number', 'contact-bank' );
		$cb_general_credit_card_expiry_date              = __( 'Card Expiry Date', 'contact-bank' );
		$cb_general_credit_card_expiry_date_tooltip      = __( 'Enter Card Expiry Date', 'contact-bank' );
		$cb_general_credit_card_expiry_date_placeholder  = __( 'Please provide expiry date', 'contact-bank' );
		$cb_general_credit_cvv_number                    = __( 'CVV Number', 'contact-bank' );
		$cb_general_credit_cvv_number_tooltip            = __( 'Enter Credit CVV Number', 'contact-bank' );
		$cb_general_credit_cvv_number_placeholder        = __( 'Please provide cvv number', 'contact-bank' );
		$cb_general_number_stars                         = __( 'Number of Stars', 'contact-bank' );
		$cb_general_number_stars_tooltip                 = __( 'Choose the Number of Stars that you want to display in the form', 'contact-bank' );
		$cb_general_number_stars_placeholder             = __( 'Please provide Number of stars', 'contact-bank' );
		$cb_label_control                                = __( 'Label', 'contact-bank' );
		$cb_label_control_tooltip                        = __( 'Here, You can enter the label of the form field so that users will identify individual fields.', 'contact-bank' );
		$cb_tooltip_control                              = __( 'Tooltip', 'contact-bank' );
		$cb_untitled_control                             = __( 'Untitled', 'contact-bank' );
		$cb_label_placement_control                      = __( 'Label Placement', 'contact-bank' );
		$cb_label_placement_above                        = __( 'Above Element', 'contact-bank' );
		$cb_label_placement_below                        = __( 'Below Element', 'contact-bank' );
		$cb_label_placement_left                         = __( 'Left of Element', 'contact-bank' );
		$cb_label_placement_right                        = __( 'Right of Element', 'contact-bank' );
		$cb_label_placement_hidden                       = __( 'Hidden', 'contact-bank' );

		$cb_expand_field    = __( 'Click here to expand and edit the options for this field', 'contact-bank' );
		$cb_duplicate_field = __( 'Click here to duplicate this field', 'contact-bank' );
		$cb_delete_field    = __( 'Click here to delete this field', 'contact-bank' );

		// Options Tab.
		$cb_options_control             = __( 'Option', 'contact-bank' );
		$cb_options_control_placeholder = __( 'Please provide option', 'contact-bank' );
		$cb_options_value               = __( 'Value', 'contact-bank' );
		$cb_options_value_placeholder   = __( 'Please provide value', 'contact-bank' );
		$cb_options                     = __( 'Options', 'contact-bank' );
		$cb_options_tooltip             = __( 'This is the Options list in which you have added Options', 'contact-bank' );
		$cb_options_drop_down           = __( 'Drop Down', 'contact-bank' );
		$cb_options_drop_down_tooltip   = __( 'This is the dropdown list in which you have added Options', 'contact-bank' );

		// Apperance Tab.
		$cb_appearance_placeholder_label               = __( 'Placeholder', 'contact-bank' );
		$cb_appearance_placeholder_tooltip             = __( 'Enter text you would like displayed in the field before a user enters any data', 'contact-bank' );
		$cb_appearance_placeholder                     = __( 'Please provide placeholder for the field' );
		$cb_appearance_card_number_placeholder_label   = __( 'Card Number Placeholder', 'contact-bank' );
		$cb_appearance_card_number_placeholder_tooltip = __( 'Enter Placeholder for Credit Card Number', 'contact-bank' );
		$cb_appearance_card_number_placeholder         = __( 'Please provide Card Number placeholder' );
		$cb_appearance_expiry_date_placeholder_label   = __( 'Expiry Date Placeholder', 'contact-bank' );
		$cb_appearance_expiry_date_placeholder_tooltip = __( 'Enter Placeholder for Card Expiry Date', 'contact-bank' );
		$cb_appearance_expiry_date_placeholder         = __( 'Please provide Expiry Date placeholder' );
		$cb_cvv_number_placeholder_label               = __( 'CVV Number Placeholder', 'contact-bank' );
		$cb_cvv_number_placeholder_tooltip             = __( 'Enter Placeholder for Card CVV Number', 'contact-bank' );
		$cb_cvv_number_placeholder                     = __( 'Please provide CVV placeholder' );
		$cb_custom_validation_message                  = __( 'Custom Validation Message', 'contact-bank' );
		$cb_custom_validation_message_placeholder      = __( 'Please provide custom validation message', 'contact-bank' );
		$cb_custom_validation_message_tooltip          = __( 'Custom Validation Message When User Leaves The field Blank', 'contact-bank' );
		$cb_appearance_rows                            = __( 'Number Of Rows', 'contact-bank' );
		$cb_appearance_rows_tooltip                    = __( 'If you would like to increase the length of Paragraph text box then you would need to provide Number of Rows', 'contact-bank' );
		$cb_appearance_rows_placeholder                = __( 'Please provide number of rows', 'contact-bank' );
		$cb_appearance_container_class                 = __( 'Container Class', 'contact-bank' );
		$cb_appearance_container_class_placeholder     = __( 'Please provide container class', 'contact-bank' );
		$cb_appearance_container_class_tooltip         = __( 'Here, you can add an extra class to your field wrapper', 'contact-bank' );
		$cb_appearance_element_class                   = __( 'Element Class', 'contact-bank' );
		$cb_appearance_element_class_placeholder       = __( 'Please provde element class', 'contact-bank' );
		$cb_appearance_element_class_tooltip           = __( 'Here, you can add an extra class to your field element', 'contact-bank' );

		// Required Tab.
		$cb_restrictions_required                               = __( 'Required', 'contact-bank' );
		$cb_restrictions_required_tooltip                       = __( 'Ensure that this field is completed before allowing the form to be submitted', 'contact-bank' );
		$cb_restrictions_limit_input_number                     = __( 'Limit Input To This Number', 'contact-bank' );
		$cb_restrictions_limit_input_number_tooltip             = __( 'Enter the number of Digits of Characters or Words to be entered', 'contact-bank' );
		$cb_restrictions_limit_input_number_placeholder         = __( 'Please provide limit input number', 'contact-bank' );
		$cb_restrictions_text_appear_after_counter              = __( 'Text Appear After Counter', 'contact-bank' );
		$cb_restrictions_text_appear_after_counter_tooltip      = __( 'Enter the text displayed after Counter', 'contact-bank' );
		$cb_restrictions_text_appear_after_counter_placeholder  = __( 'Please provide text appear after counter', 'contact-bank' );
		$cb_restrictions_words                                  = __( 'Words', 'contact-bank' );
		$cb_restrictions_characters                             = __( 'Characters', 'contact-bank' );
		$cb_restrictions_required_disabled_autocomplete         = __( 'Disable Autocomplete', 'contact-bank' );
		$cb_restrictions_required_disabled_autocomplete_tooltip = __( 'Do you want to disable browser Autocomplete?', 'contact-bank' );
		$cb_restrictions_required_disabled_input                = __( 'Disable Input', 'contact-bank' );
		$cb_restrictions_required_disabled_input_tooltip        = __( 'Choose enable to disable the field', 'contact-bank' );
		$cb_restrictions_input_masking                          = __( 'Input Mask', 'contact-bank' );
		$cb_restrictions_input_masking_tooltip                  = __( 'Choose the kind of Input Masking that will be restricted to put into the field', 'contact-bank' );
		$cb_restriction_none                                    = __( 'None', 'contact-bank' );
		$cb_restriction_us_phone                                = __( 'US Phone', 'contact-bank' );
		$cb_restriction_date                                    = __( 'Date', 'contact-bank' );
		$cb_restriction_custom                                  = __( 'Custom', 'contact-bank' );
		$cb_restrictions_custom_masking                         = __( 'Custom Mask', 'contact-bank' );
		$cb_restrictions_custom_masking_tooltip                 = __( 'Custom Masking that will be restricted to put into the field', 'contact-bank' );
		$cb_restrictions_custom_masking_placeholder             = __( 'Please provide custom masking', 'contact-bank' );

		// Advanced Tab.
		$cb_advanced_field_key                 = __( 'Field Key', 'contact-bank' );
		$cb_advanced_field_key_tooltip         = __( 'Creates a unique key to identify and target your field for custom development', 'contact-bank' );
		$cb_advanced_field_key_placeholder     = __( 'Please provide field key', 'contact-bank' );
		$cb_advanced_default_value             = __( 'Default Value', 'contact-bank' );
		$cb_advanced_default_value_tooltip     = __( 'Enter Default Value for the field', 'contact-bank' );
		$cb_advanced_default_value_placeholder = __( 'Please provide default value', 'contact-bank' );
		$cb_advanced_admin_label               = __( 'Admin Label', 'contact-bank' );
		$cb_advanced_admin_label_tooltip       = __( 'The label to be used when viewing and exporting submissions', 'contact-bank' );
		$cb_advanced_admin_label_placeholder   = __( 'Please provide admin label', 'contact-bank' );


		// Shortcode Button.
		$cb_shortcode_button_insert_form = __( 'Insert Contact Bank Form', 'contact-bank' );
		$cb_shortcode_button_add         = __( 'Select a form below to add it to your post or page', 'contact-bank' );
		$cb_shortcode_button_select_form = __( 'Select a Form', 'contact-bank' );
		$cb_shortcode_button_form_name   = __( 'Form Name', 'contact-bank' );
		$cb_shortcode_button_show        = __( 'Show', 'contact-bank' );
		$cb_shortcode_button_hide        = __( 'Hide', 'contact-bank' );
		$cb_shortcode_insert_form        = __( 'Insert Form', 'contact-bank' );
		$cb_shortcode_cancel             = __( 'Cancel', 'contact-bank' );
		$cb_shotcode_button_choose_form  = __( 'Please choose a Form to insert into Shortcode', 'contact-bank' );

		$cb_display_form_title                         = __( 'Display Form Title', 'contact-bank' );
		$cb_display_form_description                   = __( 'Display Form Description', 'contact-bank' );
		$cb_required_user_to_be_logged_in_to_view_form = __( 'Required User To Be Logged In  To View Form', 'contact-bank' );
		$cb_submission_limit                           = __( 'Number Of Submission Limit', 'contact-bank' );
		$cb_submission_limit_tooltip                   = __( 'Enter Submission Limit', 'contact-bank' );
		$cb_save_submission_to_database                = __( 'Save Submission Form To Database', 'contact-bank' );
		$cb_save_submission_to_database_tooltip        = __( 'Choose Save Submission Form To Database', 'contact-bank' );
		$cb_submission_limit_message                   = __( 'Submission Limit', 'contact-bank' );
		$cb_submission_limit_message_tooltip           = __( 'Do you want to show Submission Limit Message', 'contact-bank' );
		$cb_submission_limit_placeholder               = __( 'Enter Submission Limit', 'contact-bank' );
		$cb_submission_message                         = __( 'Submission Limit Message', 'contact-bank' );
		$cb_submission_message_tooltip                 = __( 'Enter Submission Limit Message after the Submissions are over', 'contact-bank' );
		$cb_common_fields                              = 'Common Fields';
		$cb_single_line_text_control                   = 'Single Line Text';
		$cb_paragraph_text_control                     = 'Paragraph Text';
		$cb_select_control                             = 'Select';
		$cb_multi_select_control                       = 'Multi Select';
		$cb_single_checkbox_control                    = 'Checkbox';
		$cb_checkbox_list_control                      = 'Checkbox List';
		$cb_radio_list_control                         = 'Radio List';
		$cb_date_control                               = 'Date';
		$cb_time_control                               = 'Time';
		$cb_number_control                             = 'Number';
		$cb_file_upload_control                        = 'File Upload';
		$cb_file_upload_select_files                   = __( 'Select Files', 'contact-bank' );
		$cb_file_upload_files                          = __( 'Upload Files', 'contact-bank' );
		$cb_hidden_control                             = 'Hidden';
		$cb_user_information_fields                    = 'User Information Fields';
		$cb_first_name_control                         = 'First Name';
		$cb_last_name_control                          = 'Last Name';
		$cb_email_address_control                      = 'Email Address';
		$cb_website_url_control                        = 'Website URL';
		$cb_phone_number_control                       = 'Phone';
		$cb_address_control                            = 'Address';
		$cb_city_control                               = 'City';
		$cb_zip_control                                = 'Zip';
		$cb_us_states_control                          = 'US States';
		$cb_country_control                            = 'Country';
		$cb_pricing_fields                             = 'Pricing Fields';
		$cb_product                                    = 'Product';
		$cb_quantity_control                           = 'Quantity';
		$cb_shipping_control                           = 'Shipping';
		$cb_total                                      = 'Total';
		$cb_credit_card_control                        = 'Credit Card';
		$cb_layout_fields                              = 'Layout Fields';
		$cb_html_control                               = 'HTML';
		$cb_divider_control                            = 'Divider';
		$cb_security_fields                            = 'Security Fields';
		$cb_re_captcha_control                         = 'Re-Captcha';
		$cb_anti_spam_control                          = 'Anti Spam';
		$cb_logical_captcha_control                    = 'Logical Captcha';
		$cb_miscellaneous_fields                       = 'Miscellaneous Fields';
		$cb_user_id_control                            = 'User ID';
		$cb_star_rating_control                        = 'Star Rating';
		$cb_password_control                           = 'Password';
		$cb_section_break_control                      = 'Section Break';
		$cb_color_picker_control                       = 'Colorpicker';

		// submissions.
		$cb_start_date                     = __( 'Start Date', 'contact-bank' );
		$cb_submissions_start_date_tooltip = __( 'Choose Start Date for Submissions', 'contact-bank' );
		$cb_start_date_placeholder         = __( 'Please provide start date', 'contact-bank' );
		$cb_end_date                       = __( 'End Date', 'contact-bank' );
		$cb_submissions_end_date_tooltip   = __( 'Choose End Date for Submissions', 'contact-bank' );
		$cb_end_date_placeholder           = __( 'Please provide end date', 'contact-bank' );
		$cb_submit                         = __( 'Submit', 'contact-bank' );

		// Shortcode.
		$cb_shortcode_copy_to_clipboard = __( 'Copy', 'contact-bank' );
		$cb_shortcode_copy_successful   = __( 'Copied Succesful!', 'contact-bank' );

		// Email Templates.
		$cb_from_name_label                          = __( 'From Name', 'contact-bank' );
		$cb_from_name_tooltip                        = __( 'Enter the Name from which email will be send', 'contact-bank' );
		$cb_from_name_placeholder                    = __( 'Please provide From Name', 'contact-bank' );
		$cb_from_email_label                         = __( 'From Email', 'contact-bank' );
		$cb_from_email_tooltip                       = __( 'Enter the Email from which email will be send', 'contact-bank' );
		$cb_from_email_placeholder                   = __( 'Please provide From Email address', 'contact-bank' );
		$cb_actions                                  = __( 'Action', 'contact-bank' );
		$cb_message                                  = __( 'Message', 'contact-bank' );
		$cb_email                                    = __( 'Email', 'contact-bank' );
		$cb_email_templates                          = __( 'Email Templates', 'contact-bank' );
		$cb_add_new_email_template                   = __( 'Add New Email Template', 'contact-bank' );
		$cb_choose_form                              = __( 'Choose Form', 'contact-bank' );
		$cb_select_form                              = __( 'Select Form', 'contact-bank' );
		$cb_template_for                             = __( 'Template For', 'contact-bank' );
		$cb_template_for_tooltip                     = __( 'Choose available Template', 'contact-bank' );
		$cb_template_admin_notification_template     = __( 'Admin Notification', 'contact-bank' );
		$cb_template_client_notification_template    = __( 'Client Notification ', 'contact-bank' );
		$cb_send_to                                  = __( 'Send To', 'contact-bank' );
		$cb_send_to_tooltips                         = __( 'Choose Send To Option', 'contact-bank' );
		$cb_send_to_enter_email                      = __( 'Enter Email', 'contact-bank' );
		$cb_send_to_select_field                     = __( 'Select a Field', 'contact-bank' );
		$cb_email_tooltip                            = __( 'Enter your Email from which you want to recieve Email', 'contact-bank' );
		$cb_email_placeholder                        = __( 'Please Provide Your Email', 'contact-bank' );
		$cb_send_to_field                            = __( 'Send To Field', 'contact-bank' );
		$cb_send_to_field_tooltip                    = __( 'Enter the field from which you want to receive Email', 'contact-bank' );
		$cb_send_to_field_placeholder                = __( 'Please provide Email address', 'contact-bank' );
		$cb_send_to_select_field_subject             = __( 'Subject', 'contact-bank' );
		$cb_send_to_select_field_reply_to            = __( 'Reply To', 'contact-bank' );
		$cb_send_to_select_field_reply_to_tooltip    = __( "A valid Email Address that will be used in the 'Reply To' field of the email", 'contact-bank' );
		$cb_send_to_select_field_cc                  = __( 'CC', 'contact-bank' );
		$cb_send_to_select_field_cc_tooltip          = __( 'A valid Email Address account used in the "CC" field. Use "," to separate multiple email addresses', 'contact-bank' );
		$cb_send_to_select_field_cc_placeholder      = __( 'Please provide the CC Email Address', 'contact-bank' );
		$cb_send_to_select_field_bcc                 = __( 'BCC', 'contact-bank' );
		$cb_send_to_select_field_bcc_tooltip         = __( 'A valid Email Address account used in the "BCC" field. Use "," to separate multiple email addresses', 'contact-bank' );
		$cb_send_to_select_field_bcc_placeholder     = __( 'Please provide the BCC Email Address', 'contact-bank' );
		$cb_send_to_select_field_subject_tooltip     = __( 'Enter the Subject of email', 'contact-bank' );
		$cb_send_to_select_field_subject_placeholder = __( 'Please Provide subject', 'contact-bank' );

		// Roles and Capabilities.
		$cb_roles_capabilities_show_menu                        = __( 'Show Contact Bank Menu', 'contact-bank' );
		$cb_roles_capabilities_show_menu_tooltip                = __( 'Choose among the following roles who would be able to see the Contact Bank Menu? ', 'contact-bank' );
		$cb_roles_capabilities_administrator                    = __( 'Administrator', 'contact-bank' );
		$cb_roles_capabilities_author                           = __( 'Author', 'contact-bank' );
		$cb_roles_capabilities_editor                           = __( 'Editor', 'contact-bank' );
		$cb_roles_capabilities_contributor                      = __( 'Contributor', 'contact-bank' );
		$cb_roles_capabilities_subscriber                       = __( 'Subscriber', 'contact-bank' );
		$cb_roles_capabilities_others                           = __( 'Others', 'contact-bank' );
		$cb_roles_capabilities_topbar_menu                      = __( 'Show Contact Bank Top Bar Menu', 'contact-bank' );
		$cb_roles_capabilities_topbar_menu_tooltip              = __( 'Do you want to show Contact Bank menu in Top Bar?', 'contact-bank' );
		$cb_roles_capabilities_administrator_role               = __( 'An Administrator Role can do the following', 'contact-bank' );
		$cb_roles_capabilities_administrator_role_tooltip       = __( 'Choose what pages would be visible to the users having Administrator Access', 'contact-bank' );
		$cb_roles_capabilities_full_control                     = __( 'Full Control', 'contact-bank' );
		$cb_roles_capabilities_author_role                      = __( 'An Author Role can do the following', 'contact-bank' );
		$cb_roles_capabilities_author_role_tooltip              = __( 'Choose what pages would be visible to the users having Author Access', 'contact-bank' );
		$cb_roles_capabilities_editor_role                      = __( 'An Editor Role can do the following', 'contact-bank' );
		$cb_roles_capabilities_editor_role_tooltip              = __( 'Choose what pages would be visible to the users having Editor Access', 'contact-bank' );
		$cb_roles_capabilities_contributor_role                 = __( 'A Contributor Role can do the following', 'contact-bank' );
		$cb_roles_capabilities_contributor_role_tooltip         = __( 'Choose what pages would be visible to the users having Contributor Access', 'contact-bank' );
		$cb_roles_capabilities_subscriber_role                  = __( 'A Subscriber Role can do the following', 'contact-bank' );
		$cb_roles_capabilities_subscriber_role_tooltip          = __( 'Choose what pages would be visible to the users having Subscriber Access', 'contact-bank' );
		$cb_roles_capabilities_other_role                       = __( 'Other Roles can do the following', 'contact-bank' );
		$cb_roles_capabilities_other_role_tooltip               = __( 'Choose what pages would be visible to the users having Others Role Access', 'contact-bank' );
		$cb_roles_capabilities_other_roles_capabilities         = __( 'Please tick appropriate capabilities for security purposes', 'contact-bank' );
		$cb_roles_capabilities_other_roles_capabilities_tooltip = __( 'Only users with these capabilities can access Contact Bank', 'contact-bank' );

		// layout settings.
		$cb_form_design   = __( 'Form Design', 'contact-bank' );
		$cb_input_fields  = __( 'Input Fields', 'contact-bank' );
		$cb_label_fields  = __( 'Label Fields', 'contact-bank' );
		$cb_buttons       = __( 'Buttons', 'contact-bank' );
		$cb_messages      = __( 'Messages', 'contact-bank' );
		$cb_error_fields  = __( 'Error Fields', 'contact-bank' );
		$cb_layout_margin = __( 'Error Fields', 'contact-bank' );

		// Error Messages.
		$cb_error_message_background_color                = __( 'Error Message Background Color', 'contact-bank' );
		$cb_error_message_background_color_tooltip        = __( 'Choose Background Color', 'contact-bank' );
		$cb_error_message_background_color_placeholder    = __( 'Please Provide Background Color', 'contact-bank' );
		$cb_error_message_background_transparency         = __( 'Error Message Background Transparency', 'contact-bank' );
		$cb_error_message_background_transparency_tooltip = __( 'Choose Background Transparency', 'contact-bank' );
		$cb_error_message_font_style                      = __( 'Error Messages Font Style', 'contact-bank' );
		$cb_error_message_font_family                     = __( 'Error Messages Font Family', 'contact-bank' );
		$cb_error_message_font_family_tooltip             = __( 'Choose Font Family for Error Messages', 'contact-bank' );
		$cb_error_message_padding_tooltip                 = __( 'Padding to be used for Error Message', 'contact-bank' );

		// Entry Management.
		$cb_submissions = __( 'Form Submissions', 'contact-bank' );

		// Admin Bar Menu.
		$cb_forms                  = __( 'Forms', 'contact-bank' );
		$cb_layout_settings        = __( 'Layout Settings', 'contact-bank' );
		$cb_custom_css             = __( 'Custom CSS', 'contact-bank' );
		$cb_ask_for_help           = __( 'Ask for Help', 'contact-bank' );
		$cb_system_information     = __( 'System Information', 'contact-bank' );
		$cb_roles_and_capabilities = __( 'Roles and Capabilities', 'contact-bank' );

		// general settings.
		$cb_general_settings                                   = __( 'General Settings', 'contact-bank' );
		$cb_general_settings_remove_table_at_uninstall_title   = __( 'Remove Table at Uninstall', 'contact-bank' );
		$cb_general_settings_remove_table_at_uninstall_tooltip = __( 'Do you want to remove Database at Uninstall of the Plugin?', 'contact-bank' );
		$cb_default_currency                                   = __( 'Default Currency', 'contact-bank' );
		$cb_default_currency_tooltip                           = __( 'Here, Choose Default Currency', 'contact-bank' );
		$cb_australian_dollars                                 = __( 'Australian Dollars', 'contact-bank' );
		$cb_canadian_dollars                                   = __( 'Canadian Dollars', 'contact-bank' );
		$cb_crech_koruna                                       = __( 'Czech Koruna', 'contact-bank' );
		$cb_danish_krone                                       = __( 'Danish Krone', 'contact-bank' );
		$cb_euros                             = __( 'Euros', 'contact-bank' );
		$cb_hong_kong_dollars                 = __( 'Hong Kong Dollars', 'contact-bank' );
		$cb_hungarian_forints                 = __( 'Hungarian Forints', 'contact-bank' );
		$cb_israeli_new_sheqels               = __( 'Israeli New Sheqels', 'contact-bank' );
		$cb_japanese_yen                      = __( 'Japanese Yen', 'contact-bank' );
		$cb_mexican_pesos                     = __( 'Mexican Pesos', 'contact-bank' );
		$cb_norwegian_krone                   = __( 'Norwegian Krone', 'contact-bank' );
		$cb_new_zealanddollars                = __( 'New Zealand Dollars', 'contact-bank' );
		$cb_philippine_pesos                  = __( 'Philippine Pesos', 'contact-bank' );
		$cb_polish_zloty                      = __( 'Polish Zloty', 'contact-bank' );
		$cb_british_pounds_sterling           = __( 'British Pounds Sterling', 'contact-bank' );
		$cb_singapore_dollars                 = __( 'Singapore Dollars', 'contact-bank' );
		$cb_swedish_krona                     = __( 'Swedish Krona', 'contact-bank' );
		$cb_swiss_franc                       = __( 'Swiss Franc', 'contact-bank' );
		$cb_taiwan_new_dollars                = __( 'Taiwan New Dollars', 'contact-bank' );
		$cb_thai_baht                         = __( 'Thai Baht', 'contact-bank' );
		$cb_indian_rupee                      = __( 'Indian Rupee', 'contact-bank' );
		$cb_us_dollars                        = __( 'U.S. Dollars', 'contact-bank' );
		$cb_language_direction                = __( 'Language Direction', 'contact-bank' );
		$cb_gdpr_compliance                   = __( 'GDPR Compliance', 'contact-bank' );
		$cb_gdpr_compliance_text              = __( 'GDPR Compliance Text', 'contact-bank' );
		$cb_gdpr_compliance_text_placeholder  = __( 'Please provide the text for GDPR Compliance', 'contact-bank' );
		$cb_gdpr_compliance_text_tooltip      = __( 'Please provide the text for GDPR Compliance to display on forms.', 'contact-bank' );
		$cb_gdpr_compliance_tooltip           = __( 'Choose Enable to display GDPR Compliance Checkbox on forms or vice-versa.', 'contact-bank' );
		$cb_language_direction_tooltip        = __( 'Choose Language Direction', 'contact-bank' );
		$cb_right_to_left                     = __( 'Right to Left', 'contact-bank' );
		$cb_left_to_right                     = __( 'Left to Right', 'contact-bank' );
		$cb_recaptcha_public_key              = __( 'Recaptcha Public Key', 'contact-bank' );
		$cb_recaptcha_public_key_tooltip      = __( 'Enter your Recaptcha Public Key', 'contact-bank' );
		$cb_recaptcha_public_key_placeholder  = __( 'Please Enter Your Recaptcha Public Key', 'contact-bank' );
		$cb_recaptcha_private_key             = __( 'Recaptcha Private Key', 'contact-bank' );
		$cb_recaptcha_private_key_tooltip     = __( 'Enter your Recaptcha Private Key', 'contact-bank' );
		$cb_recaptcha_private_key_placeholder = __( 'Please Enter Your Recaptcha Private Key', 'contact-bank' );
		$cb_recaptcha_label                   = __( 'Recaptcha', 'contact-bank' );

		// custom css.
		$cb_custom_css_placeholder = __( 'Please provide Custom CSS', 'contact-bank' );
		$cb_custom_css_tooltip     = __( 'CSS code manually to add extra styling', 'contact-bank' );

		// form-design.
		$cb_layout_settings_form_width_tooltip     = __( 'Width to be used for this field', 'contact-bank' );
		$cb_form_position                          = __( 'Form Position', 'contact-bank' );
		$cb_form_position_tooltips                 = __( 'Choose Position to be used for Form', 'contact-bank' );
		$cb_left                                   = 'Left';
		$cb_right                                  = 'Right';
		$cb_center                                 = 'Center';
		$cb_justify                                = 'Justify';
		$cb_bottom                                 = 'Bottom';
		$cb_single_row                             = __( 'Single Row', 'contact-bank' );
		$cb_multiple_row                           = __( 'Multiple Row', 'contact-bank' );
		$cb_font_style                             = __( 'Font Style', 'contact-bank' );
		$cb_font_family                            = __( 'Font Family', 'contact-bank' );
		$cb_font_family_tooltip                    = __( 'Choose Font Family to be used', 'contact-bank' );
		$cb_border_style                           = __( 'Border Style (Width,Thickness,Color)', 'contact-bank' );
		$cb_none                                   = __( 'None', 'contact-bank' );
		$cb_solid                                  = __( 'Solid', 'contact-bank' );
		$cb_dashed                                 = __( 'Dashed', 'contact-bank' );
		$cb_dotted                                 = __( 'Dotted', 'contact-bank' );
		$cb_border_radius                          = __( 'Border Radius (px)', 'contact-bank' );
		$cb_margin_title                           = __( 'Margin (px)', 'contact-bank' );
		$cb_font_size_placeholder                  = __( 'Font Size', 'contact-bank' );
		$cb_background_color                       = __( 'Background Color', 'contact-bank' );
		$cb_background_color_tooltips              = __( 'Choose Background Color', 'contact-bank' );
		$cb_color_placeholder                      = __( 'Color', 'contact-bank' );
		$cb_background_transparency                = __( 'Background Transparency (%)', 'contact-bank' );
		$cb_background_transparency_tooltips       = __( 'Choose Transparency(%) for selected Background Color', 'contact-bank' );
		$cb_title_html_tag                         = __( 'Title HTML Tag', 'contact-bank' );
		$cb_layout_settings_title_html_tag_tooltip = __( 'Choose HTML Tag to be used for this control', 'contact-bank' );
		$cb_h1_tag                                 = 'H1 Tag';
		$cb_h2_tag                                 = 'H2 Tag';
		$cb_h3_tag                                 = 'H3 Tag';
		$cb_h4_tag                                 = 'H4 Tag';
		$cb_h5_tag                                 = 'H5 Tag';
		$cb_h6_tag                                 = 'H6 Tag';
		$cb_blockquote_tag                         = 'Blockquote Tag';
		$cb_paragraph_tag                          = 'Paragraph Tag';
		$cb_span_tag                               = 'Span Tag';
		$cb_title_alignment                        = __( 'Title Alignment', 'contact-bank' );
		$cb_title_font_style                       = __( 'Title Font Style', 'contact-bank' );
		$cb_title_font_family                      = __( 'Title Font Family', 'contact-bank' );
		$cb_title_font_family_tooltips             = __( 'Type of Font Families available to be used', 'contact-bank' );
		$cb_description_font_family                = __( 'Description Font Family', 'contact-bank' );
		$cb_description_font_style                 = __( 'Description Font Style', 'contact-bank' );
		$cb_title_font_style_tooltips              = __( 'Font Size and Color to be used for this Control', 'contact-bank' );
		$cb_description_html_tag                   = __( 'Description HTML Tag', 'contact-bank' );
		$cb_description_alignment                  = __( 'Description Alignment', 'contact-bank' );
		$cb_description_alignment_tooltips         = __( 'Choose Alignment for Description', 'contact-bank' );
		$cb_form_margin                            = __( 'Form Margin', 'contact-bank' );
		$cb_margin_tooltip                         = __( 'Margin to be used for this Control', 'contact-bank' );
		$cb_form_padding                           = __( 'Form Padding', 'contact-bank' );
		$cb_form_padding_tooltips                  = __( 'Padding to be used for Form', 'contact-bank' );
		$cb_title_margin                           = __( 'Title Margin', 'contact-bank' );
		$cb_title_padding                          = __( 'Title Padding', 'contact-bank' );
		$cb_title_padding_tooltips                 = __( 'Padding to be used for Title', 'contact-bank' );
		$cb_description_margin                     = __( 'Description Margin', 'contact-bank' );
		$cb_description_padding                    = __( 'Description Padding', 'contact-bank' );
		$cb_description_padding_tooltips           = __( 'Padding to be used for Description', 'contact-bank' );

		$cb_top     = __( 'Top', 'contact-bank' );
		$cb_padding = __( 'Padding (px)', 'contact-bank' );

		$cb_input_field_radio_button_alignment                = __( 'Radio Button Alignment', 'contact-bank' );
		$cb_input_field_radio_button_alignment_tooltip        = __( 'Choose Radio Button Alignment', 'contact-bank' );
		$cb_input_field_checkbox_alignment                    = __( 'Checkbox Alignment', 'contact-bank' );
		$cb_input_field_checkbox_alignment_tooltip            = __( 'Choose Checkbox Alignment', 'contact-bank' );
		$cb_input_field_width                                 = __( 'Input Field Width (px or %)', 'contact-bank' );
		$cb_input_field_height                                = __( 'Input Field Height (px or %)', 'contact-bank' );
		$cb_field_height_tooltip                              = __( 'Height to be used for this Field', 'contact-bank' );
		$cb_input_field_background_color_transparency         = __( 'Input Field Background Color and Transparency', 'contact-bank' );
		$cb_input_field_background_color_transparency_tooltip = __( 'Choose Background Color and Transparency for Input Field', 'contact-bank' );
		$cb_input_field_border_style_tooltip                  = __( 'Width,Thickness and Color to be used for Input Field', 'contact-bank' );
		$cb_input_field_border_radius_tooltip                 = __( 'Border Radius to be used for Input Field', 'contact-bank' );
		$cb_input_field_padding_tooltip                       = __( 'Padding to be used for Input Field', 'contact-bank' );
		$cb_label_field_background_color_transparency         = __( 'Label Field Background Color and Transparency', 'contact-bank' );
		$cb_label_field_background_color_tooltips             = __( 'Choose Background Color and Transparency for Label Field', 'contact-bank' );

		$cb_button_font_style                    = __( 'Button Font Style', 'contact-bank' );
		$cb_button_font_family_title             = __( 'Button Font Family', 'contact-bank' );
		$cb_button_bg_color                      = __( 'Button Background Color', 'contact-bank' );
		$cb_button_bg_color_placeholder          = __( 'Background Color', 'contact-bank' );
		$cb_button_bg_color_tooltip              = __( 'Choose Background Color to be used for Button', 'contact-bank' );
		$cb_button_bg_transparency               = __( 'Background Transparency', 'contact-bank' );
		$cb_button_bg_transparency_tooltip       = __( 'Background Transparency for Button', 'contact-bank' );
		$cb_button_hover_bg_color                = __( 'Button Hover Background Color', 'contact-bank' );
		$cb_button_hover_bg_color_placeholder    = __( 'Please choose Hover Background Color', 'contact-bank' );
		$cb_button_hover_bg_color_tooltip        = __( 'Choose Background Color to be used for Button on Hover', 'contact-bank' );
		$cb_button_hover_bg_transparency         = __( 'Button Hover Background Transparency', 'contact-bank' );
		$cb_button_hover_bg_transparency_tooltip = __( 'Background Transparency for Button on Hover', 'contact-bank' );
		$cb_border_style_title                   = __( 'Button Border Style', 'contact-bank' );
		$cb_border_style_tooltip                 = __( 'Width,Thickness and Color to be used for Button', 'contact-bank' );
		$cb_border_hover_style_title             = __( 'Button Border Hover Color', 'contact-bank' );
		$cb_border_hover_style_tooltip           = __( 'Border Color for Button on hover', 'contact-bank' );
		$cb_button_border_width_placeholder      = __( 'Width (px)', 'contact-bank' );
		$cb_button_border_radius_tooltip         = __( 'Border Radius to be used for Button', 'contact-bank' );
		$cb_padding_tooltip                      = __( 'Padding to be used for Button', 'contact-bank' );
		$cb_button_text                          = __( 'Button Text', 'contact-bank' );
		$cb_button_text_tooltip                  = __( 'Text to be used for Button', 'contact-bank' );
		$cb_button_width                         = __( 'Button Width (px or %)', 'contact-bank' );
		$cb_button_height                        = __( 'Button Height (px or %)', 'contact-bank' );

		$cb_label_field_width_title      = __( 'Label Field Width (px or %)', 'contact-bank' );
		$cb_label_field_height_title     = __( 'Label Field Height (px or %)', 'contact-bank' );
		$cb_padding_label_field_tooltip  = __( 'Padding to be used for Label Field', 'contact-bank' );
		$cb_choose_templates             = __( 'Choose Form', 'contact-bank' );
		$cb_blank_form_templates         = __( 'Blank Form Template', 'contact-bank' );
		$cb_contact_us_templates         = __( 'Contact Us Template', 'contact-bank' );
		$cb_quotes_request_templates     = __( 'Quote Request Template', 'contact-bank' );
		$cb_event_registration_templates = __( 'Event Registration Template', 'contact-bank' );
		$cb_choose_templates_tooltip     = __( 'Here you can choose the Form which you want to add styling', 'contact-bank' );

		// Messages.
		$cb_messages_color                                 = __( 'Messages Color', 'contact-bank' );
		$cb_messages_font_style                            = __( 'Messages Font Style', 'contact-bank' );
		$cb_messages_font_family                           = __( 'Messages Font Family', 'contact-bank' );
		$cb_messages_background_color_transparency         = __( 'Messages Background Color and Transparency', 'contact-bank' );
		$cb_messages_background_color_transparency_tooltip = __( 'Choose Background Color to be used for Messages', 'contact-bank' );
		$cb_messages_padding_tooltip                       = __( 'Padding to be used for Messages', 'contact-bank' );
		$cb_bulk_delete_data                               = __( 'Please choose an Action !', 'contact-bank' );
		$cb_bulk_delete_empty_records                      = __( 'Choose at least 1 record!', 'contact-bank' );
		$cb_form_duplicate_message                         = __( 'Duplicated Successfully', 'contact-bank' );

		$cb_frontend_credit_card_number         = __( 'Credit Card Number', 'contact-bank' );
		$cb_frontend_credit_card_number_tooltip = __( 'Enter Credit Card Number', 'contact-bank' );
		$cb_frontend_card_expiry_date           = __( 'Card Expiry Date', 'contact-bank' );
		$cb_frontend_card_expiry_date_tooltip   = __( 'Enter Card Expiry Date', 'contact-bank' );
		$cb_frontend_credit_cvv_number          = __( 'CVV Number', 'contact-bank' );
		$cb_frontend_credit_cvv_number_tooltip  = __( 'Enter CVV Number', 'contact-bank' );
		$cb_frontend_file_upload_select_files   = __( 'Select Files', 'contact-bank' );
		$cb_frontend_upload_files               = __( 'Upload Files', 'contact-bank' );
		$cb_empty_captcha                       = __( 'You have entered an empty captcha.', 'contact-bank' );
		$cb_invalid_captcha                     = __( 'You have entered an Invalid Captcha. Please try again.', 'contact-bank' );
		$cb_empty_antispam_answer               = __( 'Error: Empty answer.', 'contacr-bank' );
		$cb_invalid_antispam_answer             = __( 'You have entered incorrect answer. Please try again.', 'contact-bank' );
		$cb_files_uploaded_successfully         = __( 'Selected Files have been Uploaded Successfully', 'contact-bank' );
		$cb_maximum_file_upload_size            = __( 'Your Maximum file upload size exceeds!', 'contact-bank' );
	}
}
