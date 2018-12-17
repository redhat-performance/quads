<?php
/**
 * Template for add new form.
 *
 * @author  Tech Banker
 * @package     contact-bank/views/forms
 * @version 3.1.0
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
	} elseif ( FORMS_CONTACT_BANK === '1' ) {
		$add_quote_request_nonce               = wp_create_nonce( 'add_quote_request_nonce' );
		$add_new_form_module                   = wp_create_nonce( 'add_new_form_module' );
		$event_registration_nonce              = wp_create_nonce( 'contact_bank_event_registration_nonce' );
		$template_type                         = isset( $form_unserialized_meta_value['layout_settings_template'] ) ? esc_attr( $form_unserialized_meta_value['layout_settings_template'] ) : '';
		$cb_add_form_contact_us_template_nonce = wp_create_nonce( 'cb_add_form_contact_us_template_nonce' );
		$id                                    = 0;
		?>
		<div class="page-bar">
			<ul class="page-breadcrumb">
				<li>
					<i class="icon-custom-home"></i>
					<a href="admin.php?page=contact_dashboard">
						<?php echo esc_attr( $cb_contact_bank ); ?>
					</a>
					<span>></span>
				</li>
				<li>
					<a href="admin.php?page=contact_dashboard">
						<?php echo esc_attr( $cb_forms ); ?>
					</a>
					<span>></span>
				</li>
				<li>
					<span>
						<?php echo esc_attr( $cb_add_new_form ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-plus"></i>
							<?php echo esc_attr( $cb_add_new_form ); ?>
						</div>
						<p class="premium-editions">
							<?php echo esc_attr( $cb_upgrade_need_help ); ?><a href="https://contact-bank.tech-banker.com/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_documentation ); ?></a><?php echo esc_attr( $cb_read_and_check ); ?><a href="https://contact-bank.tech-banker.com/frontend-demos/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_demos_section ); ?></a>
						</p>
					</div>
					<div class="portlet-body form">
						<form id="ux_frm_add_new_forms">
							<div class="form-body">
								<div class="form-wizard" id="ux_div_frm_wizard">
									<ul class="nav nav-pills nav-justified steps">
										<li class="active">
											<a aria-expanded="true" href="javascript:void(0);" class="step">
												<span class="number"> 1 </span>
												<span class="desc"> <?php echo esc_attr( $cb_wizard_choose_template ); ?> </span>
											</a>
										</li>
										<li>
											<a href="javascript:void(0);" class="step">
												<span class="number"> 2 </span>
												<span class="desc"><?php echo esc_attr( $cb_wizard_create_form ); ?> </span>
											</a>
										</li>
									</ul>
								</div>
								<div id="ux_div_step_progres_bar" class="progress progress-striped" role="progressbar">
									<div id="ux_div_step_progres_bar_width" style="width: 50%;" class="progress-bar progress-bar-success"></div>
								</div>
								<div class="line-separator"></div>
								<div id="ux_div_first_step">
									<div class="template-list-contact-bank">
										<div class="template-contact-bank blank <?php echo 'layout_settings_blank_form_template' === $template_type ? 'cb-active' : ''; ?>" onclick="add_class_active_contact_bank('blank');" value="layout_settings_blank_form_template">
											<p class="contact-bank-heading"><?php echo esc_attr( $cb_blank_form ); ?></p>
											<div><?php echo esc_attr( $cb_blank_form_desc ); ?></div>
										</div>
										<div class="template-contact-bank contact_us <?php echo 'layout_settings_contact_us_form_template' === $template_type ? 'cb-active' : ''; ?>" onclick="add_class_active_contact_bank('contact_us');" value="layout_settings_contact_us_form_template">
											<p class="contact-bank-heading"><?php echo esc_attr( $cb_contact_us ); ?></p>
											<div><?php echo esc_attr( $cb_contact_us_desc ); ?></div>
										</div>
										<div class="template-contact-bank quote_request <?php echo 'layout_settings_quote_request_form_template' === $template_type ? 'cb-active' : ''; ?>" onclick="add_class_active_contact_bank('quote_request');" value="layout_settings_quote_request_form_template">
											<p class="contact-bank-heading"><?php echo esc_attr( $cb_quote_request ); ?></p>
											<div><?php echo esc_attr( $cb_quote_request_desc ); ?></div>
										</div>
										<div class="template-contact-bank event_registration <?php echo 'layout_settings_event_form_registration_template' === $template_type ? 'cb-active' : ''; ?>" onclick="add_class_active_contact_bank('event_registration');" value="layout_settings_event_form_registration_template">
											<p class="contact-bank-heading"><?php echo esc_attr( $cb_event_registration ); ?></p>
											<div><?php echo esc_attr( $cb_event_registration_desc ); ?></div>
										</div>
									</div>
									<div class="line-separator"></div>
									<div class="form-actions">
										<div class="pull-right">
											<button class="btn vivid-green" name="ux_btn_next_step_second" id="ux_btn_next_step_second" onclick="contact_bank_move_to_second_step();" > <?php echo esc_attr( $cb_next_step ); ?> >> </button>
										</div>
									</div>
								</div>
								<div id="ux_div_second_step" style="display:none">
									<div class="tabbable-custom">
										<ul class="nav nav-tabs ">
											<li class="active">
												<a aria-expanded="true" href="#controls" data-toggle="tab">
													<?php echo esc_attr( $cb_controls ); ?>
												</a>
											</li>
											<li>
												<a aria-expanded="false" href="#advanced_settings" data-toggle="tab">
													<?php echo esc_attr( $cb_advanced_settings ); ?>
												</a>
											</li>
										</ul>
										<div class="tab-content">
											<div class="tab-pane active" id="controls">
												<div class="form-group">
													<label class="control-label">
														<?php echo esc_attr( $cb_form_title ); ?> :
														<span class="required" aria-required="true">*</span>
													</label>
													<input type="text" class="form-control" name="ux_txt_form_title" id="ux_txt_form_title" placeholder="<?php echo esc_attr( $cb_add_new_title_placeholder ); ?>" value="<?php echo isset( $form_unserialized_meta_value['form_title'] ) && '' !== esc_attr( $form_unserialized_meta_value['form_title'] ) ? esc_attr( $form_unserialized_meta_value['form_title'] ) : 'Untitled Form'; ?>">
													<i class="controls-description"><?php echo esc_attr( $cb_form_title_tooltip ); ?></i>
												</div>
												<div class="form-group">
													<label class="control-label">
														<?php echo esc_attr( $cb_form_description ); ?> :
														<span class="required" aria-required="true"></span>
													</label>
													<?php
													$form_description_value = isset( $form_unserialized_meta_value['form_description'] ) ? htmlspecialchars_decode( $form_unserialized_meta_value['form_description'] ) : '';
													wp_editor(
														$form_description_value, 'ux_heading_content', array(
															'teeny'         => true,
															'textarea_name' => 'description',
															'media_buttons' => true,
															'textarea_rows' => 10,
														)
													);
													?>
													<textarea name="ux_txtarea_add_form_heading_content" id="ux_txtarea_add_form_heading_content" style="display:none;"></textarea>
													<i class="controls-description"><?php echo esc_attr( $cb_form_description_tooltip ); ?></i>
												</div>
												<div class="line-separator"></div>
												<div class="row" id="custon_title_style">
													<div class="col-md-8">
														<div id="sortable" class="add_fields droppable" style="min-height: 1500px;border:1px solid #e5e5e5;padding:8px;">
															<?php
															if ( isset( $form_unserialized_meta_value ) && isset( $form_unserialized_meta_value['controls'] ) && count( $form_unserialized_meta_value['controls'] ) > 0 ) {
																foreach ( $form_unserialized_meta_value['controls'] as $values ) {
																	$timestamp             = esc_attr( $values['timestamp'] );
																	$input_validation_type = isset( $values['input_validation_type'] ) && esc_attr( $values['input_validation_type'] ) === 'characters' ? "onkeyup='only_characters_contact_bank(event,$timestamp)'" : ( isset( $values['input_validation_type'] ) && 'digits' === esc_attr( $values['input_validation_type'] ) ? "onkeypress='only_digits_contact_bank(event,$timestamp)'" : '' );
																	$container_class       = isset( $values['container_class'] ) && '' !== $values['container_class'] ? esc_attr( $values['container_class'] ) : '';
																	$element_class         = isset( $values['element_class'] ) && '' !== $values['element_class'] ? esc_attr( $values['element_class'] ) : '';
																	$label_placement_type  = isset( $values['label_placement'] ) && '' !== $values['label_placement'] ? esc_attr( $values['label_placement'] ) : 'above';
																	$input_class           = "class='untitled_control $element_class'";
																	$control_class         = "class='control-label field_label sub_div $container_class'";
																	$label_class           = '';
																	$controls_form_style   = 'padding-bottom:20px;';
																	$control_name          = isset( $values['control_type'] ) && '' !== $values['control_type'] ? esc_attr( $values['control_type'] ) : 'text';
																	$input_style_class     = '';
																	switch ( $label_placement_type ) {
																		case 'above':
																			$label_class   = "class='control-label field_label'";
																			$control_class = "class='sub_div $container_class'";
																			break;
																		case 'below':
																			$label_class = "class='control-label field_label'";
																			break;
																	}
																	$control_type                         = '';
																	$input_mask_control                   = 'display:none;';
																	$input_validation_control             = 'display:none;';
																	$autocomplete_settings_control        = '';
																	$appearance_setting_control           = '';
																	$restriction_setting_control          = '';
																	$number_settings_control              = 'display:none;';
																	$placeholder_control                  = '';
																	$custom_validation_control            = '';
																	$no_of_rows_control                   = 'display:none;';
																	$default_value_control                = '';
																	$label_placement_onchange_event       = "onchange=change_label_placement_contact_bank('ux_ddl_label_placement_$timestamp',$timestamp)";
																	$options_settings_class               = 'display:none;';
																	$onfocus_event                        = '';
																	$onblur_event                         = '';
																	$required_field_control               = '';
																	$class_settings                       = '';
																	$enable_autocomplete_control          = '';
																	$disable_input_control_class          = 'col-md-6';
																	$enable_autocomplete_control_class    = 'col-md-6';
																	$onkeyup_event                        = '';
																	$label_placement_control              = '';
																	$tooltip_control                      = '';
																	$admin_label_control                  = '';
																	$section_label_style                  = '';
																	$field_description_control            = 'display:none;';
																	$general_setting_controls             = '';
																	$label_title_style                    = '';
																	$apperance_active_class               = '';
																	$onclick_add_event                    = '';
																	$onclick_delete_event                 = '';
																	$onclick_import_event                 = '';
																	$admin_label_control_class            = 'col-md-6';
																	$control_label_name                   = 'Label';
																	$control_label_placement              = 'Label Placement';
																	$label_settings                       = 'display:block;';
																	$append_element_class                 = 'untitled_control';
																	$datepicker_element_class             = '';
																	$autocomplete_onchange_event          = "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_$timestamp','ux_ddl_autocomplete_$timestamp')";
																	$disable_input_onchange_event         = "disable_fields_contact_bank('ux_txt_singal_line_text_$timestamp','ux_ddl_disable_input_$timestamp')";
																	$require_input_onchange_event         = "enable_disable_required_contact_bank('ux_ddl_required_$timestamp','ux_required_$timestamp')";
																	$append_container_class_onkeyup_event = "append_class_contact_bank('ux_sub_div_$timestamp',this.value, 'sub_div', 'field_label', 'control-label', '', '')";
																	$append_element_class_onkeyup_event   = "append_class_contact_bank('ux_txt_singal_line_text_$timestamp',this.value, '$append_element_class','', '', '', '')";
																	$default_value_control_class          = 'col-md-6';
																	$onclick_event                        = '';
																	$onclick_event_arrange                = '';
																	$onclick_event_relational             = '';
																	$enable_disable_input                 = '';
																	$change_option_value                  = '';
																	switch ( $control_name ) {
																		case 'text':
																			$control_type             = $cb_single_line_text_control;
																			$input_mask_control       = 'display:block;';
																			$input_validation_control = 'display:block;';
																			break;
																		case 'paragraph':
																			$control_type             = $cb_paragraph_text_control;
																			$input_validation_control = 'display:block;';
																			$no_of_rows_control       = 'display:block;';
																			break;
																		case 'first_name':
																			$control_type = $cb_first_name_control;
																			break;
																		case 'last_name':
																			$control_type = $cb_last_name_control;
																			break;
																		case 'email':
																			$control_type                  = $cb_email_address_control;
																			$autocomplete_settings_control = 'display:none;';
																			break;
																		case 'phone':
																			$control_type             = $cb_phone_number_control;
																			$input_mask_control       = 'display:block;';
																			$input_validation_control = 'display:block;';
																			break;
																		case 'website_url':
																			$control_type = $cb_website_url_control;
																			break;
																		case 'number':
																			$control_type                  = $cb_number_control;
																			$autocomplete_settings_control = 'display:none;';
																			$number_settings_control       = 'display:block;';
																			$onkeyup_event                 = "onkeyup=number_settings_contact_bank($timestamp,event);";
																			break;
																		case 'select':
																			$control_type              = $cb_select_control;
																			$custom_validation_control = 'display:none;';
																			$placeholder_control       = 'display:none;';
																			$required_field_control    = 'display:none;';
																			$options_settings_class    = '';
																			$onclick_add_event         = "onclick=\"add_select_options_contact_bank($timestamp, 'select')\";";
																			$onclick_import_event      = "onclick=\"import_select_options_contact_bank($timestamp, 'select')\";";
																			$change_option_value       = "select_option_value_change_contact_bank($timestamp);";
																			break;
																		case 'checkbox':
																			$control_type                  = $cb_single_checkbox_control;
																			$placeholder_control           = 'display:none;';
																			$default_value_control         = 'display:none;';
																			$admin_label_control_class     = 'col-md-12';
																			$autocomplete_settings_control = 'display:none;';
																			$append_element_class          = 'checkbox_class';
																			$input_class                   = "class='checkbox_class $element_class'";
																			break;
																		case 'checkbox-list':
																			$control_type                       = $cb_checkbox_list_control;
																			$placeholder_control                = 'display:none;';
																			$default_value_control              = 'display:none;';
																			$options_settings_class             = '';
																			$onclick_add_event                  = "onclick=\"add_control_options_contact_bank($timestamp,'checkbox')\";";
																			$onclick_import_event               = "onclick=\"import_controls_values_contact_bank($timestamp,'checkbox')\";";
																			$admin_label_control_class          = 'col-md-12';
																			$autocomplete_settings_control      = 'display:none;';
																			$input_class                        = "class='checkbox_class_$timestamp $element_class'";
																			$append_element_class_onkeyup_event = "append_class_contact_bank('ux_txt_check_box_lists_$timestamp',this.value, 'checkbox_class_$timestamp', '', '', '$timestamp', 'checkbox-list')";
																			$change_option_value                = "radio_option_value_change_contact_bank($timestamp, 'checkbox');";
																			break;
																		case 'radio-list':
																			$control_type                       = $cb_radio_list_control;
																			$restriction_setting_control        = 'display:none;';
																			$custom_validation_control          = 'display:none;';
																			$placeholder_control                = 'display:none;';
																			$default_value_control              = 'display:none;';
																			$options_settings_class             = '';
																			$onclick_add_event                  = "onclick=\"add_control_options_contact_bank($timestamp,'radio')\";";
																			$onclick_import_event               = "onclick=\"import_controls_values_contact_bank($timestamp,'radio')\";";
																			$admin_label_control_class          = 'col-md-12';
																			$autocomplete_settings_control      = 'display:none;';
																			$input_class                        = "class='checkbox_class_$timestamp $element_class'";
																			$append_element_class_onkeyup_event = "append_class_contact_bank('ux_txt_check_box_lists_$timestamp',this.value, 'checkbox_class_$timestamp', '', '', '$timestamp', 'radio-list')";
																			$change_option_value                = "radio_option_value_change_contact_bank($timestamp, 'radio');";
																			break;
																	}
																	?>
																	<div id="ux_div_single_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="ux_div_single_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>"style="cursor:pointer;padding:5px;border:1px solid #fff;" class="result_hover" data-timestamp="<?php echo $timestamp; // WPCS: XSS ok. ?>">
																		<div class="main_div" id="ux_div_widget_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																			<div class="header_title" name="ux_header_title_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_header_title_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="visibility: hidden;">
																				<div class="header_title_left" name="ux_header_title_left_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_header_title_left_<?php echo $timestamp; // WPCS: XSS ok. ?>"><b><?php echo $control_type;// WPCS: XSS ok. ?></b></div>
																				<div class="header_title_rigth" name="ux_header_title_right_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_header_title_right_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="float: right;margin-right: 10px;">
																					<a title="<?php echo esc_attr( $cb_expand_field ); ?>" id="ux_expand_edit_fields_<?php echo $timestamp; // WPCS: XSS ok. ?>" onclick="show_hide_text_field_options(<?php echo $timestamp; // WPCS: XSS ok. ?>)"><i class="icon-custom-note"></i></a>
																					<a title="<?php echo esc_attr( $cb_duplicate_field ); ?>" id="ux_duplicate_fields_<?php echo $timestamp; // WPCS: XSS ok. ?>" onclick="duplicate_fields_contact_bank('<?php echo $control_name;// WPCS: XSS ok. ?>',<?php echo $timestamp; // WPCS: XSS ok. ?>);"><i class="icon-custom-docs"></i></a>
																					<a title="<?php echo esc_attr( $cb_delete_field ); ?>" id="ux_delete_fields_<?php echo $timestamp; // WPCS: XSS ok. ?>" onclick="delete_controls_contact_bank('ux_div_single_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>',<?php echo $timestamp; // WPCS: XSS ok. ?>);"><i class="icon-custom-trash"></i></a>
																				</div>
																				<input type="hidden" name="ux_control_type_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_control_type_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo isset( $values['control_type'] ) ? esc_attr( $values['control_type'] ) : 'text'; ?>">
																			</div>
																			<div <?php echo isset( $control_class ) ? $control_class : '';// WPCS: XSS ok. ?> name="ux_sub_div_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_sub_div_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="<?php echo esc_attr( $controls_form_style ); ?>">
																				<label style="<?php echo esc_attr( $section_label_style ); ?>" <?php echo isset( $label_class ) ? $label_class : '';// WPCS: XSS ok. ?> name="field_label_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="field_label_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																					<span  name="ux_label_title_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_label_title_<?php echo $timestamp; // WPCS: XSS ok. ?>"><?php echo isset( $values['label_name'] ) && '' !== esc_attr( $values['label_name'] ) ? esc_attr( $values['label_name'] ) : 'Untitled'; ?></span> :
																					<i class="icon-custom-question tooltips" name="ux_tooltip_title_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_tooltip_title_<?php echo $timestamp; // WPCS: XSS ok. ?>" data-original-title="<?php echo isset( $values['label_tooltip'] ) ? esc_attr( $values['label_tooltip'] ) : ''; ?>" data-placement="right"></i>
																					<span class="required" style="<?php echo isset( $values['required_type'] ) && 'enable' === esc_attr( $values['required_type'] ) ? 'display:' : 'display:none'; ?>" aria-required="true" name="ux_required_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_required_<?php echo $timestamp; // WPCS: XSS ok. ?>">*</span>
																				</label>
																					<?php
																					if ( 'paragraph' === $control_name ) {
																						?>
																						<textarea rows="<?php echo isset( $values['rows_number'] ) ? intval( $values['rows_number'] ) : ''; ?>" style="<?php echo esc_attr( $input_style_class ); ?> vertical-align:middle;" placeholder="<?php echo isset( $values['placeholder'] ) ? esc_attr( $values['placeholder'] ) : ''; ?>" name="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo esc_attr( $input_validation_type ); ?> id="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>')" onclick="show_hide_text_field_options(<?php echo $timestamp; // WPCS: XSS ok. ?>);" <?php echo $input_class;// WPCS: XSS ok. ?> autocomplete="<?php echo isset( $values['autocomplete_type'] ) && 'enable' === esc_attr( $values['autocomplete_type'] ) ? 'off' : 'on'; ?>" <?php echo isset( $values['disable_input'] ) && 'enable' === esc_attr( $values['disable_input'] ) ? 'disabled=disabled' : ''; ?>><?php echo isset( $values['default_value'] ) ? esc_attr( $values['default_value'] ) : ''; ?>
																						</textarea>
																					<?php
																					} elseif ( 'select' === $control_name ) {
																						?>
																						<select style="<?php echo esc_attr( $input_style_class ); ?>" name="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>"  onclick="show_hide_text_field_options(<?php echo $timestamp; // WPCS: XSS ok. ?>);" <?php echo $input_class;// WPCS: XSS ok. ?> type="text" autocomplete="<?php echo isset( $values['autocomplete_type'] ) && 'enable' === esc_attr( $values['autocomplete_type'] ) ? 'off' : 'on'; ?>" <?php echo isset( $values['disable_input'] ) && esc_attr( $values['disable_input'] ) === 'enable' ? 'disabled=disabled' : ''; ?>>
																							<?php
																							if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
																								foreach ( $values['drop_down_option_values'] as $key => $value ) {
																									$option_value = $values['default_value'] === $value->value ? 'selected=selected' : '';
																									?>
																									<option <?php echo esc_attr( $option_value ); ?> value="<?php echo esc_attr( $value->value ); ?>"><?php echo esc_attr( $value->text ); ?></option>
																									<?php
																								}
																							}
																								?>
																						</select>
																						<?php
																					} elseif ( 'checkbox' === $control_name ) {
																						?>
																						<input type="checkbox"  class="checkbox_class" name="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo esc_attr( $input_validation_type ); ?> id="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>')" onclick="show_hide_text_field_options(<?php echo $timestamp; // WPCS: XSS ok. ?>);" <?php echo $input_class;// WPCS: XSS ok. ?> type="text"  autocomplete="<?php echo isset( $values['autocomplete_type'] ) && 'enable' === esc_attr( $values['autocomplete_type'] ) ? 'off' : 'on'; ?>" <?php echo isset( $values['disable_input'] ) && 'enable' === esc_attr( $values['disable_input'] ) ? 'disabled=disabled' : ''; ?>><?php echo isset( $values['default_value'] ) ? esc_attr( $values['default_value'] ) : ''; ?>
																						<?php
																					} elseif ( 'checkbox-list' === $control_name ) {
																						?>
																						<span name="ux_txt_check_box_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_check_box_<?php echo $timestamp; // WPCS: XSS ok. ?>" class= "checkbox-label">
																							<label id="field_labels_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="field_labels_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																								<?php
																								if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
																									foreach ( $values['drop_down_option_values'] as $key => $value ) {
																									?>
																										<input style="margin-left:9px;" type="checkbox" name="ux_txt_check_box_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_check_box_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>"<?php echo esc_attr( $input_validation_type ); ?> value="<?php echo esc_attr( $value->value ); ?>" onclick="show_hide_text_field_options('<?php echo $timestamp; // WPCS: XSS ok. ?>');" <?php echo $input_class;// WPCS: XSS ok. ?>><label name="ux_chk_label_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_chk_label_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->value ); ?>"><?php echo esc_attr( $value->text ); ?></label>
																									<?php
																									}
																								}
																								?>
																							</label>
																						</span>
																						<?php
																					} elseif ( 'radio-list' === $control_name ) {
																						?>
																						<span name="ux_txt_check_box_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_check_box_<?php echo $timestamp; // WPCS: XSS ok. ?>" class= "checkbox-label">
																						<label id="field_labels_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="field_labels_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																					<?php
																					if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
																						foreach ( $values['drop_down_option_values'] as $key => $value ) {
																							?>
																							<input style="margin-left:9px;" type="radio" name="ux_txt_check_box_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_check_box_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->value ); ?>" checked=checked onclick="show_hide_text_field_options('<?php echo $timestamp; // WPCS: XSS ok. ?>');" <?php echo $input_class;// WPCS: XSS ok. ?>><label name="ux_chk_label_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_chk_label_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->value ); ?>"><?php echo esc_attr( $value->text ); ?></label>
																								<?php
																						}
																					}
																						?>
																						</label>
																						</span>
																						<?php
																					} else {
																						?>
																						<input style="<?php echo $input_style_class;// WPCS: XSS ok. ?>" <?php echo esc_attr( $onfocus_event ); ?> placeholder="<?php echo isset( $values['placeholder'] ) ? esc_attr( $values['placeholder'] ) : ''; ?>" name="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo esc_attr( $input_validation_type ); ?> id="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>')" onclick="show_hide_text_field_options(<?php echo $timestamp; // WPCS: XSS ok. ?>);" <?php echo $input_class;// WPCS: XSS ok. ?> type="text" value="<?php echo isset( $values['default_value'] ) ? esc_attr( $values['default_value'] ) : ''; ?>" autocomplete="<?php echo isset( $values['autocomplete_type'] ) && esc_attr( $values['autocomplete_type'] ) === 'enable' ? 'off' : 'on'; ?>" <?php echo isset( $values['disable_input'] ) && 'enable' === esc_attr( $values['disable_input'] ) ? 'disabled=disabled' : ''; ?> <?php echo esc_attr( $onkeyup_event ); ?>>
																						<?php
																					}

																				?>
																				<span class="control-label field_label" style="display:none;" name="ux_text_appear_after_counter_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_text_appear_after_counter_<?php echo $timestamp; // WPCS: XSS ok. ?>"><?php echo isset( $values['text_appear'] ) ? esc_attr( $values['text_appear'] ) : 'Characters Left'; ?></span>
																			</div>
																		</div>
																		<div class="ux_div_widget_content" name="ux_div_widget_content_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_div_widget_content_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																			<div class="tabbable-form-custom">
																				<ul class="nav nav-tabs ">
																					<li class="active general_settings" style="<?php echo esc_attr( $general_setting_controls ); ?>">
																						<a aria-expanded="true" data-toggle="tab" href="#general_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																							<?php echo esc_attr( $cb_general_tab ); ?>
																						</a>
																					</li>
																					<li  class="options_settings" style="<?php echo esc_attr( $options_settings_class ); ?>">
																						<a aria-expanded="false" data-toggle="tab" href="#option_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																							<?php echo esc_attr( $cb_options_tab ); ?>
																						</a>
																					</li>
																					<li class="<?php echo esc_attr( $apperance_active_class ); ?> appearance_settings" style="<?php echo esc_attr( $appearance_setting_control ); ?>">
																						<a aria-expanded="false" data-toggle="tab" href="#apperance_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																							<?php echo esc_attr( $cb_appearance_tab ); ?>
																						</a>
																					</li>
																					<li class="restrictions_settings" style="<?php echo esc_attr( $restriction_setting_control ); ?>">
																						<a aria-expanded="false" data-toggle="tab" href="#restriction_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																							<?php echo esc_attr( $cb_restrictions_tab ); ?>
																						</a>
																					</li>
																					<li class="advanced_settings">
																						<a aria-expanded="false" data-toggle="tab" href="#advanced_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																							<?php echo esc_attr( $cb_advanced_tab ); ?>
																						</a>
																					</li>
																				</ul>
																				<div class="tab-content" name="ux_div_tab_contents_" id="ux_div_tab_contents_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																					<div class="tab-pane general_settings active" id="general_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="general_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="<?php echo esc_attr( $general_setting_controls ); ?>">
																						<div class="form-group label_settings" style="<?php echo esc_attr( $label_settings ); ?>">
																							<label class="control-label" name="ux_control_label_placeholder_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_control_label_placeholder_<?php echo $timestamp; // WPCS: XSS ok. ?>" >
																								<?php echo esc_attr( $control_label_name ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_label_form ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<input type="text" class="form-control" name="ux_txt_label_field_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_label_field_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_label_field_<?php echo $timestamp; // WPCS: XSS ok. ?>')" onkeyup="change_label_name_contact_bank('ux_label_title_<?php echo $timestamp; // WPCS: XSS ok. ?>',this.value);" placeholder="<?php echo esc_attr( $cb_label_general_placeholder ); ?>" value="<?php echo isset( $values['label_name'] ) ? esc_attr( $values['label_name'] ) : ''; ?>">
																						</div>
																						<div class="form-group tooltip_settings" style="<?php echo esc_attr( $tooltip_control ); ?>">
																							<label class="control-label" name="ux_control_label_description_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_control_label_description_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																								<?php echo esc_attr( $cb_tooltip_control ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_tooltip_description ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<input type="text" class="form-control" name="ux_txt_description_field_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_description_field_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo isset( $values['label_tooltip'] ) ? esc_attr( $values['label_tooltip'] ) : ''; ?>" onkeyup="change_tootltip_content_contact_bank('ux_tooltip_title_<?php echo $timestamp; // WPCS: XSS ok. ?>',this.value);" onkeydown="select_all_content_contact_bank(event,'ux_txt_description_field_<?php echo $timestamp; // WPCS: XSS ok. ?>');" placeholder="<?php echo esc_attr( $cb_general_tootltip_placeholder ); ?>">
																						</div>
																						<div class="form-group label_placement_settings" style="<?php echo esc_attr( $label_placement_control ); ?>">
																							<label class="control-label">
																								<?php echo esc_attr( $control_label_placement ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_label_placement ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<select class="form-control" name="ux_ddl_label_placement_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_ddl_label_placement_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $label_placement_onchange_event; // WPCS: XSS ok. ?>>
																								<option value="above"><?php echo esc_attr( $cb_label_placement_above ); ?></option>
																								<option value="below"><?php echo esc_attr( $cb_label_placement_below ); ?></option>
																								<option value="left"><?php echo esc_attr( $cb_label_placement_left ); ?></option>
																								<option value="right"><?php echo esc_attr( $cb_label_placement_right ); ?></option>
																								<option value="hidden"><?php echo esc_attr( $cb_label_placement_hidden ); ?></option>
																							</select>
																						</div>
																						<div class="form-group field_description_settings" style="<?php echo esc_attr( $field_description_control ); ?>">
																							<label class="control-label" name="ux_control_label_placeholder_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_control_label_placeholder_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																								<?php echo esc_attr( $cb_general_field_description ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_field_description_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<textarea type="text" class="form-control" name="ux_txt_field_description_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_field_description_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_field_description_<?php echo $timestamp; // WPCS: XSS ok. ?>')" onkeyup="change_label_name_contact_bank('ux_field_description_<?php echo $timestamp; // WPCS: XSS ok. ?>',this.value);"><?php echo isset( $values['field_description'] ) ? esc_attr( $values['field_description'] ) : ''; ?></textarea>
																						</div>
																						<div class="number_settings" style="<?php echo esc_attr( $number_settings_control ); ?>">
																							<div class="row">
																								<div class="col-md-6">
																									<div class="form-group">
																										<label class="control-label">
																											<?php echo esc_attr( $cb_general_min_number ); ?> :
																											<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_min_number_tooltip ); ?>" data-placement="right"></i>
																											<span class="required" aria-required="true">*</span>
																										</label>
																										<input type="text" class="form-control" onkeypress="enter_only_digits_for_price(event);" name="ux_txt_min_number_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_min_number_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_min_number_<?php echo $timestamp; // WPCS: XSS ok. ?>')" value="<?php echo isset( $values['min_number'] ) ? esc_attr( $values['min_number'] ) : ''; ?>">
																									</div>
																								</div>
																								<div class="col-md-6">
																									<div class="form-group">
																										<label class="control-label">
																											<?php echo esc_attr( $cb_general_max_number ); ?> :
																											<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_max_number_tooltip ); ?>" data-placement="right"></i>
																											<span class="required" aria-required="true">*</span>
																										</label>
																										<input type="text" class="form-control" onkeypress="enter_only_digits_for_price(event);" name="ux_txt_max_number_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_max_number_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_max_number_<?php echo $timestamp; // WPCS: XSS ok. ?>')" value="<?php echo isset( $values['max_number'] ) ? esc_attr( $values['max_number'] ) : ''; ?>">
																									</div>
																								</div>
																							</div>
																							<div class="form-group">
																								<label class="control-label">
																									<?php echo esc_attr( $cb_general_step ); ?> :
																									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_step_tooltip ); ?>" data-placement="right"></i>
																									<span class="required" aria-required="true">*</span>
																								</label>
																								<input type="text" class="form-control" name="ux_txt_step_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_step_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeypress="enter_only_digits_for_price(event);" onkeydown="select_all_content_contact_bank(event,'ux_txt_step_<?php echo $timestamp; // WPCS: XSS ok. ?>')" value="<?php echo isset( $values['step'] ) ? esc_attr( $values['step'] ) : ''; ?>">
																							</div>
																						</div>
																					</div>
																					<div class="tab-pane options_settings" style="<?php echo esc_attr( $options_settings_class ); ?>" id="option_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																						<div class="row">
																							<div class="col-md-6">
																								<?php echo esc_attr( $cb_options_control ); ?>
																								<input type="text" class="form-control" name="ux_txt_add_form_option_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_options_control_placeholder ); ?>" id="ux_txt_add_form_option_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="" onkeydown="select_all_content_contact_bank(event,'ux_txt_add_form_option_<?php echo $timestamp; // WPCS: XSS ok. ?>');">
																							</div>
																							<div class="col-md-6">
																								<?php echo esc_attr( $cb_options_value ); ?>
																								<input type="text" class="form-control" name="ux_txt_add_form_values_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_options_value_placeholder ); ?>" id="ux_txt_add_form_values_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_add_form_values_<?php echo $timestamp; // WPCS: XSS ok. ?>');">
																							</div>
																							<div class="pull-right" style="margin-right:10px;margin-top:5px;">
																								<input type="button" class="btn vivid-green"  id="ux_btn_add_options_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="ux_btn_add_options_<?php echo $timestamp; // WPCS: XSS ok. ?>"  value="<?php echo esc_attr( $cb_add_option ); ?>" <?php echo $onclick_add_event;// WPCS: XSS ok. ?>>
																								<input type="button" class="btn vivid-green" name="ux_btn_add_option" id="ux_btn_add_import" value="<?php echo esc_attr( $cb_add_import ); ?>" data-popup-open="ux_open_popup_translator_<?php echo $timestamp; // WPCS: XSS ok. ?>" onclick="contact_bank_open_popup(<?php echo $timestamp; // WPCS: XSS ok. ?>);">
																								<input type="hidden" class="form-control select-hidden" name="ux_hidden_options_values_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_hidden_options_values_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																							</div>
																						</div>
																						<?php
																						if ( 'select' === $control_name ) {
																							?>
																								<div class="form-group" id="ux_drop_down_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="<?php echo isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ? 'display:block;' : 'display:none;'; ?>">
																									<label class="control-label">
																										<?php echo esc_attr( $cb_options_drop_down ); ?> :
																										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_options_drop_down_tooltip ); ?>" data-placement="right"></i>
																										<span class="required" aria-required="true">*</span>
																									</label>
																									<select class="form-control custom-drop-down input-inline" name="ux_ddl_options_required_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_ddl_options_required_<?php echo $timestamp; // WPCS: XSS ok. ?>"  style="display: none;">
																											<?php
																											if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
																												foreach ( $values['drop_down_option_values'] as $key => $value ) {
																												?>
																												<option value="<?php echo esc_attr( $value->value ); ?>"><?php echo esc_attr( $value->text ); ?></option>
																												<?php
																												}
																											}
																										?>
																									</select>
																									<div id="ux_div_append_input_radio_<?php echo $timestamp; // WPCS: XSS ok. ?>" class="append_input_radio_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="margin-top: 10px;">
																									<?php
																									if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
																										foreach ( $values['drop_down_option_values'] as $key => $value ) {
																											$id++;
																											$timestamp_id = $timestamp . '_' . $id;
																											?>
																											<div id="ux_div_full_control_radio_<?php echo esc_attr( $timestamp_id ); ?>" class="full_control_radio_<?php echo $timestamp; // WPCS: XSS ok. ?> radio-drag" style="margin-bottom: 5px;">
																												<input type="radio" id="ux_txt_radio_add_button_<?php echo esc_attr( $timestamp_id ); ?>" name="ux_txt_radio_add_button_<?php echo $timestamp; // WPCS: XSS ok. ?>" class="radio_add_button_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																												<input type="text" id="ux_txt_option_value_<?php echo esc_attr( $timestamp_id ); ?>" class="txt_option_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->text ); ?>" onchange="<?php echo esc_attr( $change_option_value ); ?>">
																												<input type="text" id="ux_txt_ddl_value_<?php echo esc_attr( $timestamp_id ); ?>" class="txt_ddl_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->value ); ?>" onchange="<?php echo esc_attr( $change_option_value ); ?>">
																												<i class="icon-custom-minus cb-radio-minus" id="ux_btn_delete_option_<?php echo esc_attr( $timestamp_id ); ?>" onclick="delete_select_options_contact_bank('<?php echo esc_attr( $timestamp_id ); ?>', '<?php echo $timestamp; // WPCS: XSS ok. ?>')" style="margin-left:5px;"></i>
																											</div>
																											<?php
																										}
																									}
																									?>
																									</div>
																								</div>
																							<?php
																						} elseif ( 'checkbox-list' === $control_name || 'radio-list' === $control_name ) {
																							?>
																								<div class="form-group" id="ux_drop_down_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="<?php echo isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ? 'display:block;' : 'display:none;'; ?>">
																									<label class="control-label">
																										<?php echo esc_attr( $cb_options ); ?> :
																										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_options_tooltip ); ?>" data-placement="right"></i>
																										<span class="required" aria-required="true">*</span>
																									</label>
																									<select class="form-control custom-drop-down input-inline" name="ux_ddl_options_required_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_ddl_options_required_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="display: none;">
																											<?php
																											if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
																												foreach ( $values['drop_down_option_values'] as $key => $value ) {
																												?>
																												<option value="<?php echo esc_attr( $value->value ); ?>"><?php echo esc_attr( $value->text ); ?></option>
																												<?php
																												}
																											}
																										?>
																									</select>
																									<div id="ux_div_append_input_radio_<?php echo $timestamp; // WPCS: XSS ok. ?>" class="append_input_radio_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="margin-top: 10px;">
																									<?php
																									if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
																										foreach ( $values['drop_down_option_values'] as $key => $value ) {
																											$id++;
																											$timestamp_id = $timestamp . '_' . $id;
																											?>
																											<div id="ux_div_full_control_radio_<?php echo esc_attr( $timestamp_id ); ?>" class="full_control_radio_<?php echo $timestamp; // WPCS: XSS ok. ?> radio-drag" style="margin-bottom: 5px;">
																												<input type="radio" id="ux_txt_radio_add_button_<?php echo esc_attr( $timestamp_id ); ?>" name="ux_txt_radio_add_button_<?php echo $timestamp; // WPCS: XSS ok. ?>" class="radio_add_button_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																												<input type="text" id="ux_txt_option_value_<?php echo esc_attr( $timestamp_id ); ?>" class="txt_option_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->text ); ?>" onchange="<?php echo esc_attr( $change_option_value ); ?>">
																												<input type="text" id="ux_txt_ddl_value_<?php echo esc_attr( $timestamp_id ); ?>" class="txt_ddl_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->value ); ?>" onchange="<?php echo esc_attr( $change_option_value ); ?>">
																												<i class="icon-custom-minus cb-radio-minus" id="ux_btn_delete_option_<?php echo esc_attr( $timestamp_id ); ?>" onclick="delete_radio_options_contact_bank('<?php echo esc_attr( $timestamp_id ); ?>', '<?php echo $timestamp; // WPCS: XSS ok. ?>')" style="margin-left:5px;"></i>
																											</div>
																											<?php
																										}
																									}
																									?>
																									</div>
																								</div>
																							<?php
																						}
																						?>
																						<div class="popup" data-popup="ux_open_popup_translator_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="open_popup" >
																							<div class="popup-inner">
																								<div class="portlet box vivid-green" style="margin-bottom:0px;">
																									<div class="portlet-title">
																										<div class="caption" id="ux_div_action">
																											<?php echo esc_attr( $cb_textarea ); ?>
																										</div>
																									</div>
																									<div class="portlet-body form">
																										<div id="ux_div_popup_header">
																											<div class="form-body">
																												<div class="form-group">
																													<label class="control-label">
																														<?php echo esc_attr( $cb_textarea ); ?> :
																														<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_textarea ); ?>" data-placement="right"></i>
																														<span class="required" aria-required="true">*</span>
																													</label>
																													<textarea class="form-control" rows="7" placeholder="<?php echo esc_attr( $cb_popup_query_placeholder ); ?>" name="ux_txt_textarea_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_textarea_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_textarea_<?php echo $timestamp; // WPCS: XSS ok. ?>');"></textarea>
																												</div>
																											</div>
																											<div class="modal-footer">
																												<div class="form-actions">
																													<div class="pull-right">
																														<input type="button"  class="btn vivid-green" name="ux_send_query" id="ux_txt_popup_import_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="ux_txt_popup_import_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $cb_add_import ); ?>" data-popup-close-translator="ux_open_popup_translator_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $onclick_import_event; // WPCS: XSS ok. ?>>
																														<input type="button" data-popup-close-translator="ux_open_popup_translator_<?php echo $timestamp; // WPCS: XSS ok. ?>" class="btn vivid-green" id="ux_btn_close" value="<?php echo esc_attr( $cb_manage_backups_close ); ?>" onclick="contact_bank_close_popup_box(<?php echo $timestamp; // WPCS: XSS ok. ?>)">
																													</div>
																												</div>
																											</div>
																										</div>
																									</div>
																								</div>
																							</div>
																						</div>
																					</div>
																					<div class="tab-pane appearance_settings <?php echo esc_attr( $apperance_active_class ); ?>" style="<?php echo esc_attr( $appearance_setting_control ); ?>" id="apperance_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="apperance_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																						<div class="form-group placeholder_settings" style="<?php echo esc_attr( $placeholder_control ); ?>">
																							<label class="control-label">
																								<?php echo esc_attr( $cb_appearance_placeholder_label ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_placeholder_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<input type="text" class="form-control" name="ux_txt_placeholder_field_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_appearance_placeholder ); ?>" id="ux_txt_placeholder_field_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_placeholder_field_<?php echo $timestamp; // WPCS: XSS ok. ?>')" onkeyup="change_placeholder_content_contact_bank('ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>',this.value);" value="<?php echo isset( $values['placeholder'] ) ? esc_attr( $values['placeholder'] ) : ''; ?>">
																						</div>
																						<div class="form-group custom_validation_settings" style="<?php echo esc_attr( $custom_validation_control ); ?>">
																							<label class="control-label">
																								<?php echo esc_attr( $cb_custom_validation_message ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_custom_validation_message_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<input type="text" class="form-control" name="ux_txt_custom_validation_field_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_custom_validation_message_placeholder ); ?>" id="ux_txt_custom_validation_field_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_custom_validation_field_<?php echo $timestamp; // WPCS: XSS ok. ?>')" value="<?php echo isset( $values['custom_validation_message'] ) ? esc_attr( $values['custom_validation_message'] ) : ''; ?>">
																						</div>
																						<div class="form-group rows_number" style="<?php echo esc_attr( $no_of_rows_control ); ?>">
																							<label class="control-label">
																								<?php echo esc_attr( $cb_appearance_rows ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_rows_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<input type="text" class="form-control" onkeypress="enter_only_digits_contact_bank(event);" id="ux_txt_no_of_rows_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_appearance_rows_placeholder ); ?>" name="ux_txt_no_of_rows_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo isset( $values['rows_number'] ) ? esc_attr( $values['rows_number'] ) : ''; ?>" onkeyup="change_textarea_rows_contact_bank(<?php echo $timestamp; // WPCS: XSS ok. ?>);" maxlength="3">
																						</div>
																						<div class="row class_settings" style="<?php echo esc_attr( $class_settings ); ?>">
																							<div class="col-md-6">
																								<div class="form-group">
																									<label class="control-label">
																										<?php echo esc_attr( $cb_appearance_container_class ); ?> :
																										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_container_class_tooltip ); ?>" data-placement="right"></i>
																										<span class="required" aria-required="true">*</span>
																									</label>
																									<input type="text" class="form-control" name="ux_txt_container_class_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_container_class_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_appearance_container_class_placeholder ); ?>" onkeyup="<?php echo $append_container_class_onkeyup_event; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_container_class_<?php echo $timestamp; // WPCS: XSS ok. ?>');" value="<?php echo isset( $values['container_class'] ) ? esc_attr( $values['container_class'] ) : ''; ?>">
																								</div>
																							</div>
																							<div class="col-md-6">
																								<div class="form-group">
																									<label class="control-label">
																										<?php echo esc_attr( $cb_appearance_element_class ); ?> :
																										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_element_class_tooltip ); ?>" data-placement="right"></i>
																										<span class="required" aria-required="true">*</span>
																									</label>
																									<input type="text" class="form-control" name="ux_txt_element_class_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_element_class_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_appearance_element_class_placeholder ); ?>" onkeyup="<?php echo $append_element_class_onkeyup_event; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_element_class_<?php echo $timestamp; // WPCS: XSS ok. ?>');" value="<?php echo isset( $values['element_class'] ) ? esc_attr( $values['element_class'] ) : ''; ?>">
																								</div>
																							</div>
																						</div>
																					</div>
																					<div class="tab-pane restrictions_settings" style="<?php echo esc_attr( $restriction_setting_control ); ?>" id="restriction_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="restriction_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																						<div class="form-group required_settings" style="<?php echo esc_attr( $required_field_control ); ?>">
																							<label class="control-label">
																								<?php echo esc_attr( $cb_restrictions_required ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_required_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<select class="form-control" name="ux_ddl_required_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_ddl_required_<?php echo $timestamp; // WPCS: XSS ok. ?>" onchange="<?php echo $require_input_onchange_event; // WPCS: XSS ok. ?>">
																								<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
																								<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
																							</select>
																						</div>
																						<div class="form-group limit_input_number_settings" style="<?php echo esc_attr( $input_validation_control ); ?>">
																							<label class="control-label">
																								<?php echo esc_attr( $cb_restrictions_limit_input_number ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_limit_input_number_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<div class="row">
																								<div class="col-md-6">
																									<input type="text" class="form-control" value="<?php echo isset( $values['input_limit_number'] ) ? esc_attr( $values['input_limit_number'] ) : 50; ?>" placeholder="<?php echo esc_attr( $cb_restrictions_limit_input_number_placeholder ); ?>" name="ux_txt_limit_input_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_limit_input_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeypress="enter_only_digits_for_price(event);" onkeydown="select_all_content_contact_bank(event,'ux_txt_limit_input_<?php echo $timestamp; // WPCS: XSS ok. ?>');">
																								</div>
																								<div class="col-md-6">
																									<select class="form-control" name="ux_ddl_limit_input_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_ddl_limit_input_<?php echo $timestamp; // WPCS: XSS ok. ?>" onchange="limit_input_event_contact_bank(<?php echo $timestamp; // WPCS: XSS ok. ?>)">
																										<option value="characters" <?php echo isset( $values['input_validation_type'] ) && esc_attr( $values['input_validation_type'] ) === 'characters' ? 'selected=selected' : ''; ?>><?php echo esc_attr( $cb_restrictions_characters ); ?></option>
																										<option value="digits" <?php echo isset( $values['input_validation_type'] ) && esc_attr( $values['input_validation_type'] ) === 'digits' ? 'selected=selected' : ''; ?>><?php echo esc_attr( $cb_restrictions_words ); ?></option>
																									</select>
																								</div>
																							</div>
																						</div>
																						<div class="form-group text_appear_settings" style="<?php echo esc_attr( $input_validation_control ); ?>">
																							<label class="control-label">
																								<?php echo esc_attr( $cb_restrictions_text_appear_after_counter ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_text_appear_after_counter_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<input type="text" class="form-control" name="ux_txt_text_appear_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_text_appear_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_restrictions_text_appear_after_counter_placeholder ); ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_text_appear_<?php echo $timestamp; // WPCS: XSS ok. ?>');" onkeyup="change_error_message_content_contact_bank('ux_text_appear_after_counter_<?php echo $timestamp; // WPCS: XSS ok. ?>',this.value)" value="<?php echo isset( $values['text_appear'] ) ? esc_attr( $values['text_appear'] ) : 'Characters Left'; ?>">
																						</div>
																						<div class="row autocomplete_settings" style="<?php echo esc_attr( $autocomplete_settings_control ); ?>">
																							<div class="<?php echo esc_attr( $enable_autocomplete_control_class ); ?> enable_autocomplete" style="<?php echo esc_attr( $enable_autocomplete_control ); ?>">
																								<div class="form-group">
																									<label class="control-label">
																										<?php echo esc_attr( $cb_restrictions_required_disabled_autocomplete ); ?> :
																										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_required_disabled_autocomplete_tooltip ); ?>" data-placement="right"></i>
																										<span class="required" aria-required="true">*</span>
																									</label>
																									<select class="form-control" name="ux_ddl_autocomplete_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_ddl_autocomplete_<?php echo $timestamp; // WPCS: XSS ok. ?>" onchange="<?php echo $autocomplete_onchange_event; // WPCS: XSS ok. ?>">
																										<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
																										<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
																									</select>
																								</div>
																							</div>
																							<div class="<?php echo esc_attr( $disable_input_control_class ); ?> enable_disable_input" style="<?php echo esc_attr( $enable_disable_input ); ?>">
																								<div class="form-group disable_input_settings">
																									<label class="control-label">
																										<?php echo esc_attr( $cb_restrictions_required_disabled_input ); ?> :
																										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_required_disabled_input_tooltip ); ?>" data-placement="right"></i>
																										<span class="required" aria-required="true">*</span>
																									</label>
																									<select class="form-control" name="ux_ddl_disable_input_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_ddl_disable_input_<?php echo $timestamp; // WPCS: XSS ok. ?>" onchange="<?php echo $disable_input_onchange_event; // WPCS: XSS ok. ?>">
																										<option value="disable"><?php echo 'Disable'; ?></option>
																										<option value="enable"><?php echo 'Enable'; ?></option>
																									</select>
																								</div>
																							</div>
																						</div>
																						<div class="form-group input_mask_settings" style="<?php echo esc_attr( $input_mask_control ); ?>">
																							<label class="control-label">
																								<?php echo esc_attr( $cb_restrictions_input_masking ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_input_masking_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<select class="form-control" name="ux_ddl_input_mask_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_ddl_input_mask_<?php echo $timestamp; // WPCS: XSS ok. ?>" onchange="apply_input_masking_contact_bank('ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>','ux_ddl_input_mask_<?php echo $timestamp; // WPCS: XSS ok. ?>','ux_div_custom_mask_settings_<?php echo $timestamp; // WPCS: XSS ok. ?>',<?php echo $timestamp; // WPCS: XSS ok. ?>);">
																								<option value="none"><?php echo esc_attr( $cb_restriction_none ); ?></option>
																								<option value="us_phone"><?php echo esc_attr( $cb_restriction_us_phone ); ?></option>
																								<option value="date"><?php echo esc_attr( $cb_restriction_date ); ?></option>
																								<option value="custom"><?php echo esc_attr( $cb_restriction_custom ); ?></option>
																							</select>
																						</div>
																						<div class="form-group custom_mask_settings" name="ux_div_custom_mask_settings_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_div_custom_mask_settings_<?php echo $timestamp; // WPCS: XSS ok. ?>" style="<?php echo isset( $values['input_mask_type'] ) && esc_attr( $values['input_mask_type'] ) === 'custom' ? 'display:block' : 'display:none'; ?>">
																							<label class="control-label">
																								<?php echo esc_attr( $cb_restrictions_custom_masking ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_custom_masking_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<input type="text" class="form-control" name="ux_txt_custom_mask_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_restrictions_custom_masking_placeholder ); ?>" id="ux_txt_custom_mask_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo isset( $values['custom_mask'] ) ? esc_attr( $values['custom_mask'] ) : '999,999,999,999'; ?>" onblur="apply_input_masking_contact_bank('ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>','ux_ddl_input_mask_<?php echo $timestamp; // WPCS: XSS ok. ?>','ux_div_custom_mask_settings_<?php echo $timestamp; // WPCS: XSS ok. ?>',<?php echo $timestamp; // WPCS: XSS ok. ?>);" onkeydown="select_all_content_contact_bank(event,'ux_txt_custom_mask_<?php echo $timestamp; // WPCS: XSS ok. ?>')">
																						</div>
																					</div>
																					<div class="tab-pane advanced_settings" id="advanced_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="advanced_<?php echo $timestamp; // WPCS: XSS ok. ?>">
																						<div class="form-group">
																							<label class="control-label">
																								<?php echo esc_attr( $cb_advanced_field_key ); ?> :
																								<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_advanced_field_key_tooltip ); ?>" data-placement="right"></i>
																								<span class="required" aria-required="true">*</span>
																							</label>
																							<input type="text" class="form-control" name="single_line_text_field_key_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_advanced_field_key_placeholder ); ?>" id="single_line_text_field_key_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'single_line_text_field_key_<?php echo $timestamp; // WPCS: XSS ok. ?>');" value="<?php echo isset( $values['field_key'] ) ? esc_attr( $values['field_key'] ) : ''; ?>">
																						</div>
																						<div class="row">
																							<div class="col-md-6 default_value_settings" style="<?php echo esc_attr( $default_value_control ); ?>">
																								<div class="form-group">
																									<label class="control-label">
																										<?php echo esc_attr( $cb_advanced_default_value ); ?> :
																										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_advanced_default_value_tooltip ); ?>" data-placement="right"></i>
																										<span class="required" aria-required="true">*</span>
																									</label>
																									<?php
																									if ( 'select' === $control_name || 'multi-select' === $control_name ) {
																										?>
																										<select class="form-control" name="ux_txt_default_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" onchange="set_default_value_contact_bank(<?php echo $timestamp; // WPCS: XSS ok. ?>)" id="ux_txt_default_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo isset( $values['default_value'] ) ? esc_attr( $values['default_value'] ) : ''; ?>">
																											<?php
																											if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
																												foreach ( $values['drop_down_option_values'] as $key => $value ) {
																												?>
																													<option <?php echo isset( $values['default_value'] ) && esc_attr( $values['default_value'] ) === $value->value ? 'selected=selected' : ''; ?> value="<?php echo esc_attr( $value->value ); ?>"><?php echo esc_attr( $value->text ); ?></option>
																												<?php
																												}
																											}
																											?>
																										</select>
																										<?php
																									} else {
																										?>
																									<input type="text" class="form-control" name="ux_txt_default_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_advanced_default_value_placeholder ); ?>" id="ux_txt_default_value_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeyup="control_default_value_contact_bank('ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>',this.value);" onkeydown="select_all_content_contact_bank(event,'ux_txt_default_value_<?php echo $timestamp; // WPCS: XSS ok. ?>');" value="<?php echo isset( $values['default_value'] ) ? esc_attr( $values['default_value'] ) : ''; ?>">
																										<?php
																									}
																									?>
																								</div>
																							</div>
																							<div class="<?php echo esc_attr( $admin_label_control_class ); ?> admin_label_settings" style="<?php echo esc_attr( $admin_label_control ); ?>">
																								<div class="form-group">
																									<label class="control-label">
																										<?php echo esc_attr( $cb_advanced_admin_label ); ?> :
																										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_advanced_admin_label_tooltip ); ?>" data-placement="right"></i>
																										<span class="required" aria-required="true">*</span>
																									</label>
																									<input type="text" class="form-control" name="ux_txt_admin_label_<?php echo $timestamp; // WPCS: XSS ok. ?>" placeholder="<?php echo esc_attr( $cb_advanced_admin_label_placeholder ); ?>" id="ux_txt_admin_label_<?php echo $timestamp; // WPCS: XSS ok. ?>" onkeydown="select_all_content_contact_bank(event,'ux_txt_admin_label_<?php echo $timestamp; // WPCS: XSS ok. ?>');" value="<?php echo isset( $values['admin_label'] ) ? esc_attr( $values['admin_label'] ) : ''; ?>">
																								</div>
																							</div>
																						</div>
																					</div>
																				</div>
																			</div>
																		</div>
																	</div>
																	<?php
																}
															}
															?>
														</div>
													</div>
													<div class="row">
														<div class="col-md-4 button-controls-contact-bank">
															<div class="portlet box cb-accordian">
																<div class="portlet-title" onclick="toggling_fields_contact_bank('common_fields_cb');">
																	<div class="caption">
																		<i class="icon-custom-plus cb-accordian-dashicons"></i>
																		<div class="add-buttons-title" id="contact_bank_common_fields">
																			<?php echo esc_attr( $cb_common_fields ); ?>
																		</div>
																	</div>
																	<span class="cb-accordian-dashicons dashicons dashicons-arrow-down"></span>
																</div>
																<div class="portlet-body form">
																	<div class="form-actions">
																		<div class="common_fields_cb" style="border:0px solid black;">
																			<ul class="field_type_list">

																				<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('text')" id="text">
																					<i class="icon-custom-notebook"></i>
																					<a><?php echo esc_attr( $cb_single_line_text_control ); ?></a>
																				</li>
																				<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('paragraph')" id="paragraph">
																					<i class="icon-custom-pencil"></i>
																					<a><?php echo esc_attr( $cb_paragraph_text_control ); ?></a>
																				</li>
																				<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('select')" id="select">
																					<i class="icon-custom-arrow-up"></i>
																					<a><?php echo esc_attr( $cb_select_control ); ?></a>
																				</li>
																				<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('checkbox')" id="checkbox">
																					<i class="icon-custom-check"></i>
																					<a><?php echo esc_attr( $cb_single_checkbox_control ); ?></a>
																				</li>
																				<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('checkbox-list')" id="checkbox-list">
																					<i class="icon-custom-check"></i>
																					<a><?php echo esc_attr( $cb_checkbox_list_control ); ?></a>
																				</li>
																				<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('radio-list')" id="radio-list">
																					<i class="icon-custom-support"></i>
																					<a><?php echo esc_attr( $cb_radio_list_control ); ?></a>
																				</li>
																				<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('number')" id="number" style="width: 95% !important;">
																					<i class="icon-custom-calculator"></i>
																					<a><?php echo esc_attr( $cb_number_control ); ?></a>
																				</li>
																			</ul>
																		</div>
																	</div>
																</div>
															</div>
														</div>
														<div class="col-md-4 button-controls-contact-bank">
															<div class="portlet box cb-accordian">
																<div class="portlet-title" onclick="toggling_fields_contact_bank('common_fields_cb_pro');">
																		<div class="caption">
																			<i class="icon-custom-plus cb-accordian-dashicons"></i>
																			<div class="add-buttons-title" id="contact_bank_common_fields">
																					<?php echo esc_attr( $cb_common_fields ); ?>
																					<span style="color:red;"><?php echo '(Pro)'; ?></span>
																				</div>
																		</div>
																		<span class="cb-accordian-dashicons dashicons dashicons-arrow-down"></span>
																	</div>
																	<div class="portlet-body form">
																		<div class="form-actions">
																			<div class="common_fields_cb_pro" style="border:0px solid black;">
																					<ul class="field_type_list">
																						<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="multi-select">
																								<i class="icon-custom-loop"></i>
																								<a><?php echo esc_attr( $cb_multi_select_control ); ?></a>
																							</li>
																							<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="date">
																								<i class="icon-custom-calendar"></i>
																								<a><?php echo esc_attr( $cb_date_control ); ?></a>
																							</li>
																							<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="time">
																								<i class="icon-custom-clock"></i>
																								<a><?php echo esc_attr( $cb_time_control ); ?></a>
																							</li>
																							<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="file_upload">
																								<i class="icon-custom-cloud-upload"></i>
																								<a><?php echo esc_attr( $cb_file_upload_control ); ?></a>
																							</li>
																							<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="hidden" style="width: 95% !important;">
																								<i class="icon-custom-eye"></i>
																								<a><?php echo esc_attr( $cb_hidden_control ); ?></a>
																							</li>
																						</ul>
																					</div>
																				</div>
																			</div>
																		</div>
																	</div>
																	<div class="col-md-4 button-controls-contact-bank">
																		<div class="portlet box cb-accordian">
																			<div class="portlet-title" onclick="toggling_fields_contact_bank('user_info_fields');">
																				<div class="caption">
																					<i class="icon-custom-plus cb-accordian-dashicons"></i>
																					<div class="add-buttons-title" id="contact_bank_user_information_fields">
																						<?php echo esc_attr( $cb_user_information_fields ); ?>
																					</div>
																				</div>
																				<span class="dashicons dashicons-arrow-down cb-accordian-dashicons"></span>
																			</div>
																			<div class="portlet-body form">
																				<form>
																					<div class="form-actions">
																						<div class="user_info_fields" style="border:0px solid black;">
																							<ul>
																								<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('first_name')" id="first_name">
																									<i class="icon-custom-user"></i>
																									<a><?php echo esc_attr( $cb_first_name_control ); ?></a>
																								</li>
																								<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('last_name')" id="last_name">
																									<i class="icon-custom-user"></i>
																									<a><?php echo esc_attr( $cb_last_name_control ); ?></a>
																								</li>
																								<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('email')" id="email">
																									<i class="icon-custom-envelope"></i>
																									<a><?php echo esc_attr( $cb_email_address_control ); ?></a>
																								</li>
																								<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('website_url')" id="website_url">
																									<i class="icon-custom-globe"></i>
																									<a><?php echo esc_attr( $cb_website_url_control ); ?></a>
																								</li>
																								<li class="button-contact-bank contact_bank_draggable"  onclick="contact_bank_field_fill('phone')" id="phone" style="Width:95 !important;">
																									<i class="icon-custom-phone"></i>
																									<a><?php echo esc_attr( $cb_phone_number_control ); ?></a>
																								</li>
																							</ul>
																						</div>
																					</div>
																				</form>
																			</div>
																	</div>
																</div>
																<div class="col-md-4 button-controls-contact-bank">
																	<div class="portlet box cb-accordian">
																			<div class="portlet-title" onclick="toggling_fields_contact_bank('user_info_fields_pro');">
																				<div class="caption">
																						<i class="icon-custom-plus cb-accordian-dashicons"></i>
																						<div class="add-buttons-title" id="contact_bank_user_information_fields">
																							<?php echo esc_attr( $cb_user_information_fields ); ?>
																								<span style="color:red;"><?php echo '(Pro)'; ?></span>
																						</div>
																					</div>
																					<span class="dashicons dashicons-arrow-down cb-accordian-dashicons"></span>
																			</div>
																			<div class="portlet-body form">
																				<form>
																						<div class="form-actions">
																							<div class="user_info_fields_pro" style="border:0px solid black;">
																									<ul>
																										<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank()" id="address">
																												<i class="icon-custom-location-pin"></i>
																												<a><?php echo esc_attr( $cb_address_control ); ?></a>
																											</li>
																											<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank()" id="city">
																												<i class="icon-custom-location-pin"></i>
																												<a><?php echo esc_attr( $cb_city_control ); ?></a>
																											</li>
																											<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank()" id="zip">
																												<i class="icon-custom-location-pin"></i>
																												<a><?php echo esc_attr( $cb_zip_control ); ?></a>
																											</li>
																											<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank()" id="state">
																												<i class="icon-custom-star"></i>
																												<a><?php echo esc_attr( $cb_us_states_control ); ?></a>
																											</li>
																											<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank()" id="country" style="width:95%">
																												<i class="icon-custom-event"></i>
																												<a><?php echo esc_attr( $cb_country_control ); ?></a>
																											</li>
																										</ul>
																									</div>
																								</div>
																							</form>
																						</div>
																					</div>
																				</div>
																			<div class="col-md-4 button-controls-contact-bank">
																				<div class="portlet box cb-accordian">
																					<div class="portlet-title" onclick="toggling_fields_contact_bank('pricing_fields');">
																						<div class="caption">
																							<i class="icon-custom-plus cb-accordian-dashicons"></i>
																							<div class="add-buttons-title" id="contact_bank_pricing_fields">
																								<?php echo esc_attr( $cb_pricing_fields ); ?>
																								<span style="color:red;"><?php echo '(Pro)'; ?></span>
																							</div>
																						</div>
																						<span class="dashicons dashicons-arrow-down cb-accordian-dashicons"></span>
																					</div>
																					<div class="portlet-body form">
																						<form>
																							<div class="form-actions">
																								<div class="pricing_fields" style="border:0px solid black;">
																									<ul>
																										<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="product">
																											<i class="icon-custom-tag"></i>
																											<a><?php echo esc_attr( $cb_product ); ?></a>
																										</li>
																										<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="quantity">
																											<i class="icon-custom-tag"></i>
																											<a><?php echo esc_attr( $cb_quantity_control ); ?></a>
																										</li>
																										<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="shipping">
																											<i class="icon-custom-basket-loaded"></i>
																											<a><?php echo esc_attr( $cb_shipping_control ); ?></a>
																										</li>
																										<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="total_control">
																											<i class="icon-custom-diamond"></i>
																											<a><?php echo esc_attr( $cb_total ); ?></a>
																										</li>
																										<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="credit_card" style="width: 95% !important;">
																											<i class="icon-custom-credit-card"></i>
																											<a><?php echo esc_attr( $cb_credit_card_control ); ?></a>
																										</li>
																									</ul>
																								</div>
																							</div>
																						</form>
																					</div>
																				</div>
																			</div>
																			<div class="col-md-4 button-controls-contact-bank">
																				<div class="portlet box cb-accordian">
																					<div class="portlet-title" onclick="toggling_fields_contact_bank('layout_fields');">
																						<div class="caption">
																							<i class="icon-custom-plus cb-accordian-dashicons"></i>
																							<div class="add-buttons-title" id="contact_bank_layout_fields">
																								<?php echo esc_attr( $cb_layout_fields ); ?>
																								<span style="color:red;"><?php echo '(Pro)'; ?></span>
																							</div>
																						</div>
																						<span class="dashicons dashicons-arrow-down cb-accordian-dashicons"></span>
																					</div>
																					<div class="portlet-body form">
																						<form>
																							<div class="form-actions">
																								<div class="layout_fields" style="border:0px solid black;">
																									<ul>
																										<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="html">
																											<i class="icon-custom-note"></i>
																											<a><?php echo esc_attr( $cb_html_control ); ?></a>
																										</li>
																										<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="divider">
																											<i class="icon-custom-arrow-right-circle"></i>
																											<a><?php echo esc_attr( $cb_divider_control ); ?></a>
																										</li>
																									</ul>
																								</div>
																							</div>
																						</form>
																					</div>
																				</div>
																			</div>
																		<div class="col-md-4 button-controls-contact-bank">
																			<div class="portlet box cb-accordian">
																				<div class="portlet-title" onclick="toggling_fields_contact_bank('security_fields');">
																					<div class="caption">
																						<i class="icon-custom-plus cb-accordian-dashicons"></i>
																						<div class="add-buttons-title" id="contact_bank_security_fields">
																							<?php echo esc_attr( $cb_security_fields ); ?>
																							<span style="color:red;"><?php echo '(Pro)'; ?></span>
																						</div>
																					</div>
																					<span class="dashicons dashicons-arrow-down cb-accordian-dashicons"></span>
																				</div>
																				<div class="portlet-body form">
																					<form>
																						<div class="form-actions">
																							<div class="security_fields" style="border:0px solid black;">
																								<ul>
																									<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="recaptcha">
																										<i class="icon-custom-lock-open"></i>
																										<a><?php echo esc_attr( $cb_re_captcha_control ); ?></a>
																									</li>
																									<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="anti_spam">
																										<i class="icon-custom-shield"></i>
																										<a><?php echo esc_attr( $cb_anti_spam_control ); ?></a>
																									</li>
																									<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="logical-captcha" style="width: 95% !important;">
																										<i class="icon-custom-lock-open"></i>
																										<a><?php echo esc_attr( $cb_logical_captcha_control ); ?></a>
																									</li>
																								</ul>
																							</div>
																						</div>
																					</form>
																				</div>
																			</div>
																		</div>
																		<div class="col-md-4 button-controls-contact-bank">
																			<div class="portlet box cb-accordian">
																				<div class="portlet-title" onclick="toggling_fields_contact_bank('miscellaneous_fields');">
																					<div class="caption">
																						<i class="icon-custom-plus cb-accordian-dashicons"></i>
																						<div class="add-buttons-title" id="contact_bank_miscellaneous_fields">
																							<?php echo esc_attr( $cb_miscellaneous_fields ); ?>
																							<span style="color:red;"><?php echo '(Pro)'; ?></span>
																						</div>
																					</div>
																					<span class="dashicons dashicons-arrow-down cb-accordian-dashicons"></span>
																				</div>
																				<div class="portlet-body form">
																					<form>
																						<div class="form-actions">
																							<div class="miscellaneous_fields" style="border:0px solid black;;">
																								<ul>
																									<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="user_id">
																										<i class="icon-custom-user"></i>
																										<a><?php echo esc_attr( $cb_user_id_control ); ?></a>
																									</li>
																									<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="star_rating">
																										<i class="icon-custom-star"></i>
																										<a><?php echo esc_attr( $cb_star_rating_control ); ?></a>
																									</li>
																									<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="password">
																										<i class="icon-custom-lock"></i>
																										<a><?php echo esc_attr( $cb_password_control ); ?></a>
																									</li>
																									<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="section_break">
																										<i class="icon-custom-arrow-left-circle"></i>
																										<a><?php echo esc_attr( $cb_section_break_control ); ?></a>
																									</li>
																									<li class="button-contact-bank contact_bank_draggable"  onclick="premium_edition_notification_contact_bank();" id="color_picker" style="width: 95% !important;">
																										<i class="icon-custom-magic-wand"></i>
																										<a><?php echo esc_attr( $cb_color_picker_control ); ?></a>
																									</li>
																								</ul>
																							</div>
																						</div>
																					</form>
																				</div>
																			</div>
																		</div>
																	</div>
																</div>
															</div>
															<div class="tab-pane" id="advanced_settings">
																<div class="row">
																	<div class="col-md-6">
																		<div class="form-group">
																			<label class="control-label">
																				<?php echo esc_attr( $cb_submission_limit_message ); ?> :
																				<span class="required" aria-required="true">*</span>
																			</label>
																			<select id="ux_ddl_submission_limit_message" name="ux_ddl_submission_limit_message" class="form-control" onchange="show_hide_submission_message_contact_bank();">
																				<option value="enable" > <?php echo esc_attr( $cb_enable ); ?> </option>
																				<option value="disable" > <?php echo esc_attr( $cb_disable ); ?> </option>
																			</select>
																			<i class="controls-description"><?php echo esc_attr( $cb_submission_limit_message_tooltip ); ?></i>
																		</div>
																	</div>
																	<div class="col-md-6">
																		<div class="form-group">
																			<label class="control-label">
																				<?php echo esc_attr( $cb_save_submission_to_database ); ?> :
																				<span class="required" aria-required="true">*</span>
																			</label>
																			<select id="ux_ddl_save_submission_to_db" name="ux_ddl_save_submission_to_db" class="form-control" onchange="show_hide_redirect_controls_contact_bank('type');">
																				<option value="enable" > <?php echo esc_attr( $cb_enable ); ?> </option>
																				<option  value="disable" > <?php echo esc_attr( $cb_disable ); ?> </option>
																			</select>
																			<i class="controls-description"><?php echo esc_attr( $cb_save_submission_to_database_tooltip ); ?></i>
																		</div>
																	</div>
																</div>
																<div class="form-group" id="submission_limit_number">
																	<label class="control-label">
																		<?php echo esc_attr( $cb_submission_limit ); ?> :
																		<span class="required" aria-required="true">*</span>
																	</label>
																	<input  type="text" name="ux_txt_submission_limit" id="ux_txt_submission_limit" class="form-control" placeholder="<?php echo esc_attr( $cb_submission_limit_placeholder ); ?>" onkeypress="enter_only_digits_contact_bank(event);" value="<?php echo isset( $form_unserialized_meta_value['form_submission_limit'] ) ? esc_attr( $form_unserialized_meta_value['form_submission_limit'] ) : ''; ?>" onchange="show_hide_submission_message_contact_bank('value');">
																	<i class="controls-description"><?php echo esc_attr( $cb_submission_limit_tooltip ); ?></i>
																</div>
																<div class="form-group" style="display:block;" id="ux_div_submission_message">
																	<label class="control-label">
																		<?php echo esc_attr( $cb_submission_message ); ?> :
																		<span class="required" aria-required="true">*</span>
																	</label>
																	<textarea name="ux_txt_submission_limit_message" id="ux_txt_submission_limit_message" class="form-control" placeholder="<?php echo esc_attr( $cb_submission_message ); ?>"><?php echo isset( $form_unserialized_meta_value['form_submission_message'] ) ? esc_attr( $form_unserialized_meta_value['form_submission_message'] ) : ''; ?></textarea>
																	<i class="controls-description"><?php echo esc_attr( $cb_submission_message_tooltip ); ?></i>
																</div>
																<div class="form-group">
																	<label class="control-label">
																		<?php echo esc_attr( $cb_success_message ); ?> :
																		<span class="required" aria-required="true">*</span>
																	</label>
																	<textarea name="ux_txt_success_message" id="ux_txt_success_message" class="form-control" placeholder="<?php echo esc_attr( $cb_success_message ); ?>"><?php echo isset( $form_unserialized_meta_value['form_success_message'] ) ? esc_attr( $form_unserialized_meta_value['form_success_message'] ) : 'Your Form has been Successfully Submitted.'; ?></textarea>
																	<i class="controls-description"><?php echo esc_attr( $cb_success_message_tooltip ); ?></i>
																</div>
																<div class="form-group">
																	<label class="control-label">
																		<?php echo esc_attr( $enable_tooltip ); ?> :
																		<span class="required" aria-required="true">*</span>
																	</label>
																	<select id="ux_ddl_enable_tooltip" name="ux_ddl_enable_tooltip" class="form-control">
																		<option value="show"> <?php echo esc_attr( $cb_shortcode_button_show ); ?> </option>
																		<option  value="hide"> <?php echo esc_attr( $cb_shortcode_button_hide ); ?> </option>
																	</select>
																	<i class="controls-description"><?php echo esc_attr( $enable_message_tooltips ); ?></i>
																</div>
																<div class="row">
																	<div class="col-md-6">
																		<div class="form-group">
																			<label class="control-label">
																				<?php echo esc_attr( $cb_redirect ); ?> :
																				<span class="required" aria-required="true">*</span>
																			</label>
																			<select id="ux_ddl_redirect_type" name="ux_ddl_redirect_type" class="form-control" onchange="show_hide_redirect_controls_contact_bank('type');">
																				<option value="page"> <?php echo esc_attr( $cb_page ); ?> </option>
																				<option  value="url"> <?php echo esc_attr( $cb_url ); ?> </option>
																			</select>
																			<i class="controls-description"><?php echo esc_attr( $cb_redirect_tooltip ); ?></i>
																		</div>
																	</div>
																	<div class="col-md-6">
																		<div class="form-group" id="ux_div_redirect_url">
																			<label class="control-label">
																				<?php echo esc_attr( $cb_url ); ?> :
																				<span class="required" aria-required="true">*</span>
																			</label>
																			<input type="text" id="ux_txt_url_redirect" class="form-control" name="ux_txt_url_redirect" placeholder="<?php echo esc_attr( $cb_url_redirect_placeholder ); ?>" value="<?php echo isset( $form_unserialized_meta_value['form_redirect_url'] ) ? esc_attr( $form_unserialized_meta_value['form_redirect_url'] ) : ''; ?>">
																			<i class="controls-description"><?php echo esc_attr( $cb_redirect_tooltip ); ?></i>
																		</div>
																		<div class="form-group" id="ux_div_redirect_page" style="display: none;">
																			<label class="control-label">
																				<?php echo esc_attr( $cb_page ); ?> :
																				<span class="required" aria-required="true">*</span>
																			</label>
																			<select id="ux_ddl_redirect_page" name="ux_ddl_redirect_page" class="form-control">
																				<?php
																				for ( $flag = 0; $flag < count( $publish_pages ); $flag++ ) { // @codingStandardsIgnoreLine.
																					$permalink = get_permalink( $publish_pages[ $flag ]->ID );
																					?>
																					<option value="<?php echo esc_attr( $permalink ); ?>"><?php echo esc_attr( $publish_pages[ $flag ]->post_name ); ?></option>
																					<?php
																				}
																				?>
																			</select>
																			<i class="controls-description"><?php echo esc_attr( $cb_page_tooltip ); ?></i>
																		</div>
																	</div>
																</div>
															</div>
														</div>
														<div class = "line-separator"></div>
														<div class="form-actions">
															<div class="pull-left">
																<input type="button" class="btn vivid-green" name="ux_btn_previsious_step_first" id="ux_btn_previsious_step_first" onclick="contact_bank_move_to_first_step()" value="<< <?php echo esc_attr( $cb_previous_step ); ?>">
															</div>
															<div class="pull-right">
																<button class="btn vivid-green" name="ux_btn_next_step_third" id="ux_btn_next_step_third" onclick="contact_bank_move_to_third_step();"> <?php echo esc_attr( $cb_save_changes ); ?> </button>
															</div>
														</div>
													</div>
												</div>
											</div>
										</form>
									</div>
								</div>
							</div>
						</div>
						<?php
	} else {
		?>
		<div class="page-bar">
			<ul class="page-breadcrumb">
				<li>
					<i class="icon-custom-home"></i>
					<a href="admin.php?page=contact_dashboard">
						<?php echo esc_attr( $cb_contact_bank ); ?>
					</a>
					<span>></span>
				</li>
				<li>
					<a href="admin.php?page=cb_forms">
						<?php echo esc_attr( $cb_forms ); ?>
					</a>
					<span>></span>

				</li>
				<li>
					<span>
						<?php echo esc_attr( $cb_add_new_form ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-plus"></i>
							<?php echo esc_attr( $cb_add_new_form ); ?>
						</div>
					</div>
					<div class="portlet-body form">
						<div class="form-body">
							<strong><?php echo esc_attr( $cb_user_access_message ); ?></strong>
						</div>
					</div>
				</div>
			</div>
		</div>
		<?php
	}
}
