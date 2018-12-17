<?php
/**
 * This file is used for displaying form in page/post.
 *
 * @author  Tech Banker
 * @package contact-bank/user-views/layouts
 * @version 3.1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
if ( isset( $form_unserialized_meta_value['controls'] ) && count( $form_unserialized_meta_value['controls'] ) > 0 ) {
	if ( ! function_exists( 'get_currency_symbol_contact_bank' ) ) {
		/**
		 * This function is used t get currency symbol.
		 *
		 * @param string $country_code .
		 */
		function get_currency_symbol_contact_bank( $country_code ) {
			$country_code = strtoupper( $country_code );
			$currency     = array(
				'USD' => '&#36;', // U.S. Dollar.
				'AUD' => '&#36;', // Australian Dollar.
				'CAD' => 'C&#36;', // Canadian Dollar.
				'CZK' => 'K&#269;', // Czech Koruna.
				'DKK' => 'kr', // Danish Krone.
				'EUR' => '&euro;', // Euro.
				'HKD' => '&#36', // Hong Kong Dollar.
				'HUF' => 'Ft', // Hungarian Forint.
				'ILS' => '&#x20aa;', // Israeli New Sheqel.
				'JPY' => '&yen;', // also use &#165; Japanese Yen.
				'MXN' => '&#36', // Mexican Peso.
				'NOK' => 'kr', // Norwegian Krone.
				'NZD' => '&#36', // New Zealand Dollar.
				'PHP' => '&#x20b1;', // Philippine Peso.
				'PLN' => '&#122;&#322;', // Polish Zloty.
				'GBP' => '&pound;', // Pound Sterling.
				'SGD' => '&#36;', // Singapore Dollar.
				'SEK' => 'kr', // Swedish Krona.
				'CHF' => 'Fr', // Swiss Franc.
				'TWD' => '&#36;', // Taiwan New Dollar.
				'THB' => '&#3647;', // Thai Baht.
				'INR' => '&#8377;', // Indian Rupee.
			);
			if ( array_key_exists( $country_code, $currency ) ) {
				return $currency[ $country_code ];
			}
		}
	}
	$country_code                    = $selected_general_setting_unserialize['default_currency'];
	$contact_bank_currency_code      = get_currency_symbol_contact_bank( $country_code );
	$upload_local_system_files_nonce = wp_create_nonce( 'upload_local_system_files_nonce' );
	?>
	<div class="main_container_contact_bank_<?php echo intval( $random ); ?> form-layout-main-container-contact-bank_<?php echo intval( $random ); ?> language_direction_contact_bank_<?php echo intval( $random ); ?>">
		<form name="ux_frm_main_container_<?php echo intval( $random ); ?>" id="ux_frm_main_container_<?php echo intval( $random ); ?>">
			<div id="form_error_message_frontend_<?php echo intval( $random ); ?>" class="custom-message error-message" style="display: none; margin-bottom: 10px;">
				<span class="error_message_text">
					<strong><?php echo esc_attr( $form_unserialized_meta_value['form_submission_message'] ); ?></strong>
				</span>
			</div>
			<div id="form_success_message_frontend_<?php echo intval( $random ); ?>" class="custom-message message-layout-contact-bank_<?php echo intval( $random ); ?>" style="display: none; margin-bottom: 10px;">
				<div id="success_message_text_<?php echo intval( $random ); ?>"></div>
			</div>
			<?php
			if ( 'show' === $form_title && '' !== htmlspecialchars_decode( $form_unserialized_meta_value['form_title'] ) ) {
				?>
				<div class="form-layout-title-contact-bank_<?php echo intval( $random ); ?>">
					<<?php echo esc_attr( $layout_settings_form_design_title_html_tag ); ?>><?php echo isset( $form_unserialized_meta_value['form_title'] ) ? htmlspecialchars_decode( $form_unserialized_meta_value['form_title'] ) : 'Untitled Form'; // WPCS: XSS ok. ?></<?php echo esc_attr( $layout_settings_form_design_title_html_tag ); ?>>
				</div>
				<?php
			}
			if ( 'show' === $form_description && '' !== htmlspecialchars_decode( $form_unserialized_meta_value['form_description'] ) ) {
				?>
				<div class="form-layout-description-contact-bank_<?php echo intval( $random ); ?>">
					<<?php echo esc_attr( $layout_settings_form_design_description_html_tag ); ?>><?php echo isset( $form_unserialized_meta_value['form_description'] ) ? htmlspecialchars_decode( $form_unserialized_meta_value['form_description'] ) : ''; // WPCS: XSS ok. ?> </<?php echo esc_attr( $layout_settings_form_design_description_html_tag ); ?>>
				</div>
				<?php
			}
			$controls_ids = array();
			if ( isset( $form_unserialized_meta_value ) && isset( $form_unserialized_meta_value['controls'] ) ) {
				if ( count( $form_unserialized_meta_value['controls'] ) > 0 ) {
					foreach ( $form_unserialized_meta_value['controls'] as $values ) {
						$timestamp = isset( $values['timestamp'] ) ? doubleval( $values['timestamp'] ) : '';
						array_push( $controls_ids, $timestamp );
						$label_placement                 = isset( $values['label_placement'] ) ? esc_attr( $values['label_placement'] ) : 'above';
						$max_limit                       = isset( $values['input_limit_number'] ) ? esc_attr( $values['input_limit_number'] ) : 50;
						$text_appear                     = isset( $values['text_appear'] ) ? esc_attr( $values['text_appear'] ) : 'Characters Left';
						$input_validation_type           = isset( $values['input_validation_type'] ) && 'characters' === esc_attr( $values['input_validation_type'] ) ? "onkeyup=\"only_characters_contact_bank_$random(event,$timestamp,'$max_limit','$text_appear');\"" : ( isset( $values['input_validation_type'] ) && 'digits' === esc_attr( $values['input_validation_type'] ) ? "onkeypress=\"only_digits_contact_bank_$random(event,$timestamp,'$max_limit','$text_appear')\"" : '' );
						$container_class                 = isset( $values['container_class'] ) && '' !== $values['container_class'] ? esc_attr( $values['container_class'] ) : '';
						$element_class                   = isset( $values['element_class'] ) && '' !== $values['element_class'] ? esc_attr( $values['element_class'] ) : '';
						$input_class                     = 'left' === $label_placement ? "class='left-placement-input-contact-bank_$random untitled_control $element_class'" : ( 'right' === $label_placement ? "class='right-placement-input-contact-bank_$random untitled_control $element_class'" : "class='input-layout-field-contact-bank_$random untitled_control $element_class'" );
						$control_class                   = "class='sub_div $container_class'";
						$text_appear_after_counter_class = 'position:relative;';
						$label_class                     = 'left' === $label_placement ? "class='label_left_placement_$random control-label field_label'" : ( 'right' === $label_placement ? "class='label_left_placement_credit_card_$random control-label'" : "class='label-layout-field-contact-bank_$random control-label field_label'" );
						$right_label_placement           = 'right' === $label_placement ? "class='radio_list_label_right_placement_$random'" : '';
						$control_name                    = isset( $values['control_type'] ) ? esc_attr( $values['control_type'] ) : 'Text';
						$label_style_class               = '';
						$input_style_class               = '';
						$onfocus_event                   = '';
						$onkeyup_event                   = '';
						$radio_button_alignment          = '';
						$checkbox_list_alignment         = '';
						$min_number                      = isset( $values['min_number'] ) ? esc_attr( $values['min_number'] ) : '';
						$max_number                      = isset( $values['max_number'] ) ? esc_attr( $values['max_number'] ) : '';
						$step_number_cb                  = isset( $values['step'] ) ? esc_attr( $values['step'] ) : '';
						switch ( $control_name ) {
							case 'number':
								$onkeyup_event = "onkeyup=number_settings_contact_bank_$random($timestamp,event,$step_number_cb,$min_number,$max_number);";
								break;
							case 'checkbox':
								$label_class = 'left' === $label_placement ? "class='label_left_placement_$random control-label field_label'" : ( 'right' === $label_placement ? "class='checkbox_label_right_placement_$random control-label field_label'" : "class='label-layout-field-contact-bank_$random control-label field_label'" );
								$input_class = 'right' === $label_placement ? "class = 'checkbox_input_right_placement_$random'" : "class='input-layout-field-contact-bank_$random checkbox_class $element_class'";
								break;
							case 'checkbox-list':
								if ( 'single_row' === $layout_settings_input_field_checkbox_alignment && 'left' === $label_placement ) {
									$checkbox_list_alignment = 'float:left,width:60%;';
								} elseif ( 'multiple_row' === $layout_settings_input_field_checkbox_alignment && 'left' === $label_placement ) {
									$checkbox_list_alignment = 'float:left';
								}
								$input_class = "class='checkbox_class_$timestamp $element_class'";
								$label_class = 'left' === $label_placement ? "class='label_left_placement_$random control-label field_label'" : ( 'right' === $label_placement ? "class='radio_list_label_$random control-label field_label'" : "class='label-layout-field-contact-bank_$random control-label field_label'" );
								break;
							case 'radio-list':
								if ( 'single_row' === $layout_settings_input_field_radio_button_alignment && 'left' === $label_placement ) {
									$radio_button_alignment = 'float:left,width:60%;';
								} elseif ( 'multiple_row' === $layout_settings_input_field_radio_button_alignment && 'left' === $label_placement ) {
									$radio_button_alignment = 'float:left';
								}
								$input_class = "class='checkbox_class_$timestamp $element_class'";
								$label_class = 'left' === $label_placement ? "class='label_left_placement_$random control-label field_label'" : ( 'right' === $label_placement ? "class='radio_list_label_$random control-label field_label'" : "class='label-layout-field-contact-bank_$random control-label field_label'" );
								break;
							case 'email':
								$input_validation_type = '';
								break;
						}
							?>
							<div style="clear:both;"<?php echo isset( $control_class ) ? $control_class : ''; // WPCS: XSS ok. ?> name="ux_sub_div_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_sub_div_<?php echo $timestamp; // WPCS: XSS ok. ?>">
									<label style="<?php echo isset( $label_style_class ) ? $label_style_class : ''; // WPCS: XSS ok. ?>" <?php echo isset( $label_class ) ? $label_class : ''; // WPCS: XSS ok. ?> name="field_label_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="field_label_<?php echo $timestamp; // WPCS: XSS ok. ?>">
										<span name="ux_label_title_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_label_title_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo isset( $values['label_name'] ) ? esc_attr( $values['label_name'] ) : ''; ?>"><?php echo isset( $values['label_name'] ) && '' !== esc_attr( $values['label_name'] ) ? esc_attr( $values['label_name'] ) : 'Untitled'; ?></span> :
										<?php
										if ( isset( $form_unserialized_meta_value['form_enable_tooltip'] ) && 'show' === $form_unserialized_meta_value['form_enable_tooltip'] ) {
											?>
											<i class="icon-custom-question tooltips label_tooltip_contact_bank" name="ux_tooltip_title_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_tooltip_title_<?php echo $timestamp; // WPCS: XSS ok. ?>" data-original-title="<?php echo isset( $values['label_tooltip'] ) ? esc_attr( $values['label_tooltip'] ) : ''; ?>" data-placement="right"></i>
											<?php
										}
										?>
										<span class="required" style="<?php echo isset( $values['required_type'] ) && 'enable' === esc_attr( $values['required_type'] ) ? 'display:' : 'display:none'; ?>" aria-required="true" name="ux_required_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_required_<?php echo $timestamp; // WPCS: XSS ok. ?>">*</span>
									</label>
									<?php
									if ( 'paragraph' === $control_name ) {
										?>
										<textarea rows="<?php echo isset( $values['rows_number'] ) ? intval( $values['rows_number'] ) : ''; ?>" style="<?php echo $input_style_class; // WPCS: XSS ok. ?>" placeholder="<?php echo isset( $values['placeholder'] ) ? esc_attr( $values['placeholder'] ) : ''; ?>" name="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $input_validation_type; // WPCS: XSS ok. ?> id="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>"<?php echo $input_class; // WPCS: XSS ok. ?> type="text" autocomplete="<?php echo isset( $values['autocomplete_type'] ) && 'enable' === esc_attr( $values['autocomplete_type'] ) ? 'off' : 'on'; ?>" <?php echo isset( $values['disable_input'] ) && 'enable' === esc_attr( $values['disable_input'] ) ? 'disabled=disabled' : ''; ?>><?php echo isset( $values['default_value'] ) ? esc_attr( $values['default_value'] ) : ''; ?></textarea>
										<?php
									} elseif ( 'select' === $control_name ) {
										?>
										<select style="<?php echo $input_style_class; // WPCS: XSS ok. ?>" name="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $input_class; // WPCS: XSS ok. ?> type="text" autocomplete="<?php echo isset( $values['autocomplete_type'] ) && 'enable' === esc_attr( $values['autocomplete_type'] ) ? 'off' : 'on'; ?>" <?php echo isset( $values['disable_input'] ) && 'enable' === esc_attr( $values['disable_input'] ) ? 'disabled=disabled' : ''; ?>>
											<?php
											if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
												foreach ( $values['drop_down_option_values'] as $key => $value ) {
													$option_value = esc_attr( $values['default_value'] ) === $value->value ? 'selected=selected' : '';
													?>
													<option <?php echo $option_value; // WPCS: XSS ok. ?> value="<?php echo esc_attr( $value->value ); ?>"><?php echo esc_attr( $value->text ); ?></option>
													<?php
												}
											}
											?>
										</select>
										<?php
									} elseif ( 'email' === $control_name ) {
										?>
										<input style="<?php echo $input_style_class; // WPCS: XSS ok. ?>" <?php echo $onfocus_event; // WPCS: XSS ok. ?> placeholder="<?php echo isset( $values['placeholder'] ) ? esc_attr( $values['placeholder'] ) : ''; ?>" name="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $input_validation_type; // WPCS: XSS ok. ?> id="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $input_class; // WPCS: XSS ok. ?> type="email" value="<?php echo isset( $values['default_value'] ) ? esc_attr( $values['default_value'] ) : ''; ?>" autocomplete="<?php echo isset( $values['autocomplete_type'] ) && 'enable' === esc_attr( $values['autocomplete_type'] ) ? 'off' : 'on'; ?>" <?php echo isset( $values['disable_input'] ) && 'enable' === esc_attr( $values['disable_input'] ) ? 'disabled=disabled' : ''; ?> <?php echo $onkeyup_event; // WPCS: XSS ok. ?>>
										<?php
									} elseif ( 'checkbox' === $control_name ) {
										?>
										<input type="checkbox"  class="checkbox_class" name="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $input_validation_type; // WPCS: XSS ok. ?> id="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $input_class; // WPCS: XSS ok. ?> type="text"  autocomplete="<?php echo isset( $values['autocomplete_type'] ) && 'enable' === esc_attr( $values['autocomplete_type'] ) ? 'off' : 'on'; ?>" <?php echo isset( $values['disable_input'] ) && 'enable' === esc_attr( $values['disable_input'] ) ? 'disabled=disabled' : ''; ?>><?php echo isset( $values['default_value'] ) ? esc_attr( $values['default_value'] ) : ''; ?>
										<?php
									} elseif ( 'checkbox-list' === $control_name ) {
										?>
										<span name="ux_txt_check_box_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_check_box_<?php echo $timestamp; // WPCS: XSS ok. ?>" class="checkbox-label">
											<label id="field_labels_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="field_labels_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $right_label_placement; // WPCS: XSS ok. ?> style="<?php echo $checkbox_list_alignment; // WPCS: XSS ok. ?>">
												<?php
												if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
													foreach ( $values['drop_down_option_values'] as $key => $value ) {
														?>
														<input class="input_chk_button_contact_bank_<?php echo intval( $random ); ?>" type="checkbox" name="ux_txt_check_box_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>[]" id="ux_txt_check_box_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>"<?php echo $input_validation_type; // WPCS: XSS ok. ?> value="<?php echo esc_attr( $value->value ); ?>" <?php echo $input_class; // WPCS: XSS ok. ?>><label name="ux_chk_label_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" class="input_chk_button_label_contact_bank_<?php echo intval( $random ); ?>" id="ux_chk_label_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->value ); ?>"><?php echo esc_attr( $value->text ); ?></label>
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
											<label id="field_labels_<?php echo $timestamp; // WPCS: XSS ok. ?>" name="field_labels_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $right_label_placement; // WPCS: XSS ok. ?> style="<?php echo $radio_button_alignment; // WPCS: XSS ok. ?>">
												<?php
												if ( isset( $values['drop_down_option_values'] ) && count( $values['drop_down_option_values'] ) > 0 ) {
													foreach ( $values['drop_down_option_values'] as $key => $value ) {
														?>
														<input class="input_radio_button_contact_bank_<?php echo intval( $random ); ?>" type="radio" name="ux_txt_check_box_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_check_box_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->value ); ?>" checked=checked  <?php echo $input_class; // WPCS: XSS ok. ?>><label name="ux_chk_label_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" class="input_radio_button_label_contact_bank_<?php echo intval( $random ); ?>" id="ux_chk_label_lists_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo esc_attr( $value->value ); ?>"><?php echo esc_attr( $value->text ); ?></label>
														<?php
													}
												}
												?>
											</label>
										</span>
										<?php
									} else {
										?>
										<input style="<?php echo $input_style_class; // WPCS: XSS ok. ?>" <?php echo $onfocus_event; // WPCS: XSS ok. ?> placeholder="<?php echo isset( $values['placeholder'] ) ? esc_attr( $values['placeholder'] ) : ''; ?>" name="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $input_validation_type; // WPCS: XSS ok. ?> id="ux_txt_singal_line_text_<?php echo $timestamp; // WPCS: XSS ok. ?>" <?php echo $input_class; // WPCS: XSS ok. ?> type="text" value="<?php echo isset( $values['default_value'] ) ? esc_attr( $values['default_value'] ) : ''; ?>" autocomplete="<?php echo isset( $values['autocomplete_type'] ) && 'enable' === esc_attr( $values['autocomplete_type'] ) ? 'off' : 'on'; ?>" <?php echo isset( $values['disable_input'] ) && 'enable' === esc_attr( $values['disable_input'] ) ? 'disabled=disabled' : ''; ?> <?php echo $onkeyup_event; // WPCS: XSS ok. ?>>
										<?php
									}
									?>
									<input type="hidden" name="ux_txt_hidden_label_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_hidden_label_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo isset( $values['label_name'] ) ? esc_attr( $values['label_name'] ) : ''; ?>">
									<span class="cb-limit-input control-label field_label" style="display:none;<?php echo $text_appear_after_counter_class; // WPCS: XSS ok. ?>" name="ux_text_appear_after_counter_<?php echo $timestamp;  // WPCS: XSS ok. ?>" id="ux_text_appear_after_counter_<?php echo $timestamp;  // WPCS: XSS ok. ?>"><?php echo isset( $values['text_appear'] ) ? esc_attr( $values['text_appear'] ) : 'Characters Left'; ?></span>
							</div>
						<input type="hidden" name="ux_txt_hidden_control_type_<?php echo $timestamp; // WPCS: XSS ok. ?>" id="ux_txt_hidden_control_type_<?php echo $timestamp; // WPCS: XSS ok. ?>" value="<?php echo isset( $values['control_type'] ) ? esc_attr( $values['control_type'] ) : ''; ?>">
						<?php
					}
				}
			}
			if ( isset( $selected_general_setting_unserialize['gdpr_compliance'] ) && 'enable' === $selected_general_setting_unserialize['gdpr_compliance'] ) {
				?>
				<div class="col-md-12" style="margin-top:2%;">
					<input style="margin-left:-3%" type="checkbox" name="ux_chk_gdpr_compliance_agree_form_<?php echo intval( $random ); ?>" id="ux_chk_gdpr_compliance_agree_form_<?php echo intval( $random ); ?>" value="1">
					<span id="gdpr_agree_text_form_contact_bank" class="label-gdrp-compliance-style"><?php echo isset( $selected_general_setting_unserialize['gdpr_compliance_text'] ) ? esc_attr( $selected_general_setting_unserialize['gdpr_compliance_text'] ) : 'By using this form you agree with the storage and handling of your data by this website'; ?></span>
					<span id="ux_chk_validation_gdpr_form_contact_bank" style="display:none">*</span>
				</div>
				<?php
			}
			?>
			<div style="clear: both;">
				<input type="submit" class="button-layout-contact-bank_<?php echo intval( $random ); ?>" name="ux_btn_save_changes" id="ux_btn_save_changes" onclick="submit_form_contact_bank_<?php echo intval( $random ); ?>(<?php echo wp_json_encode( $controls_ids ); ?>, '#ux_frm_main_container_<?php echo intval( $random ); ?>', '<?php echo esc_attr( $form_unserialized_meta_value['form_save_submission_to_db'] ); ?>', '<?php echo esc_attr( $form_unserialized_meta_value['form_redirect_page_url'] ); ?>', '<?php echo esc_attr( $form_unserialized_meta_value['form_submission_limit_message'] ); ?>', '<?php echo intval( $form_unserialized_meta_value['form_submission_limit'] ); ?>', '<?php echo esc_attr( $form_unserialized_meta_value['form_redirect'] ); ?>', '<?php echo esc_attr( $form_unserialized_meta_value['form_redirect_url'] ); ?>', '<?php echo esc_attr( sanitize_text_field( $form_unserialized_meta_value['form_success_message'] ) ); ?>')" value="<?php echo esc_attr( $layout_settings_button_text ); ?>">
			</div>
		</form>
	</div>
	<?php
}
