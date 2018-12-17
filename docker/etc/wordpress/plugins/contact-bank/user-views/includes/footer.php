<?php
/**
 * This file contains javascript.
 *
 * @author Tech Banker
 * @package contact-bank/user-views/includes
 * @version 3.1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
} // Exit if accessed directly
?>
<script type="text/javascript">
	var ajaxurl = "<?php echo esc_attr( admin_url( 'admin-ajax.php' ) ); ?>";
	jQuery(".tooltips").tooltip_tip({placement: "right"});
	if (typeof (base64_encode_contact_bank) != "function")
	{
		function base64_encode_contact_bank(data) {
			var b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
			var o1, o2, o3, h1, h2, h3, h4, bits, i = 0,
					ac = 0,
					enc = "",
					tmp_arr = [];
			if (!data) {
				return data;
			}
			do {
				o1 = data.charCodeAt(i++);
				o2 = data.charCodeAt(i++);
				o3 = data.charCodeAt(i++);
				bits = o1 << 16 | o2 << 8 | o3;
				h1 = bits >> 18 & 0x3f;
				h2 = bits >> 12 & 0x3f;
				h3 = bits >> 6 & 0x3f;
				h4 = bits & 0x3f;
				tmp_arr[ac++] = b64.charAt(h1) + b64.charAt(h2) + b64.charAt(h3) + b64.charAt(h4);
			} while (i < data.length);
			enc = tmp_arr.join("");
			var r = data.length % 3;
			return(r ? enc.slice(0, r - 3) : enc) + "===".slice(r || 3);
		}
	}
	if (typeof (overlay_loading_contact_bank_<?php echo intval( $random ); ?>) !== "function")
	{
		function overlay_loading_contact_bank_<?php echo intval( $random ); ?>(message) {
			var overlay_opacity = jQuery("<div class=\"opacity_overlay\"></div>");
			jQuery("body").append(overlay_opacity);
			var overlay = jQuery("<div class=\"loader_opacity\"><div class=\"processing_overlay\"></div></div>");
			jQuery("body").append(overlay);
		}
	}
	if (typeof (remove_overlay_contact_bank_<?php echo intval( $random ); ?>) !== "function")
	{
		function remove_overlay_contact_bank_<?php echo intval( $random ); ?>() {
			jQuery(".loader_opacity").remove();
			jQuery(".opacity_overlay").remove();
		}
	}
	if (typeof (only_characters_contact_bank_<?php echo intval( $random ); ?>) !== "function")
	{
		function only_characters_contact_bank_<?php echo intval( $random ); ?>(event, timestamp, max_limit, value) {
			var content = jQuery("#ux_txt_singal_line_text_" + timestamp).val();
			var characters_length = content.length;
			max_limit !== "" ? jQuery("#ux_txt_singal_line_text_" + timestamp).attr("maxlength", max_limit) : "";
			if (max_limit === "")
			{
				jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "none");
			} else if (characters_length > max_limit) {
				var lastIndex = content.lastIndexOf(" ");
				jQuery("#ux_txt_singal_line_text_" + timestamp).val(content.substring(0, lastIndex));
				jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "block").addClass("field_label");
				jQuery("#ux_text_appear_after_counter_" + timestamp).text(max_limit - characters_length + " " + value);
			} else {
				jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "block").addClass("field_label");
				jQuery("#ux_text_appear_after_counter_" + timestamp).text(max_limit - characters_length + " " + value);
			}
		}
	}
	if (typeof (only_digits_contact_bank_<?php echo intval( $random ); ?>) !== "function")
	{
		function only_digits_contact_bank_<?php echo intval( $random ); ?>(event, timestamp, max_limit, text_appear)
		{
			var content = jQuery("#ux_txt_singal_line_text_" + timestamp).val();
			var words = content.split(/\s+/);
			var words_length = words.length;
			jQuery("#ux_txt_singal_line_text_" + timestamp).removeAttr("maxlength", "");
			var value = text_appear;
			if (words_length > max_limit) {
				event.preventDefault();
				var lastIndex = content.lastIndexOf(" ");
				jQuery("#ux_txt_singal_line_text_" + timestamp).val(content.substring(0, lastIndex));
				jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "block").addClass("field_label");
				if (max_limit > words_length)
				{
					jQuery("#ux_text_appear_after_counter_" + timestamp).text(max_limit - words_length + " " + value);
				}
			}
			else
			{
				jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "block").addClass("field_label");
				jQuery("#ux_text_appear_after_counter_" + timestamp).text(max_limit - words_length + " " + value);
			}
		}
	}
	if (typeof (apply_input_masking_contact_bank_<?php echo intval( $random ); ?>) !== "function")
	{
		function apply_input_masking_contact_bank_<?php echo intval( $random ); ?>(input_id, timestamp, input_mask_type, custom_mask_value) {
			switch (input_mask_type) {
				case "none":
					jQuery("#ux_txt_singal_line_text_" + timestamp).unmask();
				break;
				case "us_phone":
					jQuery("#ux_txt_singal_line_text_" + timestamp).unmask();
					jQuery("#ux_txt_singal_line_text_" + timestamp).mask("(999)999-9999");
				break;
				case "date":
					jQuery("#ux_txt_singal_line_text_" + timestamp).unmask();
					jQuery("#ux_txt_singal_line_text_" + timestamp).mask("99/99/9999");
				break;
				case "custom":
					jQuery("#ux_txt_singal_line_text_" + timestamp).unmask();
					jQuery("#ux_txt_singal_line_text_" + timestamp).mask(custom_mask_value);
				break;
			}
		}
	}
	if (typeof (change_label_placement_contact_bank_<?php echo intval( $random ); ?>) !== "function")
	{
		function change_label_placement_contact_bank_<?php echo intval( $random ); ?>(input_id, timestamp, label_placement_type, control_name)
		{
			switch (label_placement_type)
			{
				case "above":
					jQuery("#field_label_" + timestamp).css("display", "block");
					if (control_name == "radio-list" || control_name == "checkbox-list")
					{
						jQuery("#ux_txt_check_box_" + timestamp).insertAfter("#field_label_" + timestamp);
					}
					else
					{
						jQuery("#ux_txt_singal_line_text_" + timestamp).insertAfter("#field_label_" + timestamp);
					}
					jQuery("#ux_text_appear_after_counter_" + timestamp).css({"position": "", "margin-top": "", "margin-left": ""});
					jQuery("#ux_txt_singal_line_text_" + timestamp).css({"display": "block", "margin-left": "9px", "margin-right": "0"});
					jQuery("#ux_sub_div_" + timestamp).removeClass("field_label").removeClass("control-label");
				break;
				case "below":
					jQuery("#field_label_" + timestamp).css("display", "block");
					if (control_name == "radio-list" || control_name == "checkbox-list")
					{
						jQuery("#ux_txt_check_box_" + timestamp).insertBefore(jQuery("#field_label_" + timestamp).addClass("field_label").addClass("control-label"));
					}
					else
					{
						jQuery("#ux_txt_singal_line_text_" + timestamp).insertBefore(jQuery("#field_label_" + timestamp).addClass("field_label").addClass("control-label")).css({"margin-right": "0", "margin-bottom": "-8% !important"});
					}
					jQuery("#ux_text_appear_after_counter_" + timestamp).css({"position": ""});
					jQuery("#ux_sub_div_" + timestamp).addClass("field_label").addClass("control-label").css("padding-bottom", "10px");
				break;
				case "left":
					jQuery("#field_label_" + timestamp).css("display", "");
					if(control_name == "radio-list" || control_name == "checkbox-list")
					{
						jQuery("#ux_txt_check_box_" + timestamp);
					}
					jQuery("#ux_text_appear_after_counter_" + timestamp).css({"position": "relative", "margin-top": "", "margin-left": "30%"});
					jQuery("#ux_txt_singal_line_text_" + timestamp).css({"display": "inline-block", "margin-left": "0px", "margin-right": "0"});
					jQuery("#ux_sub_div_" + timestamp).addClass("field_label").addClass("control-label");
				break;
				case "right":
					jQuery("#field_label_" + timestamp).css("display", "");
					if(control_name == "radio-list" || control_name == "checkbox-list")
					{
						jQuery("#ux_txt_check_box_" + timestamp).prependTo("#field_label_" + timestamp);
					}
					jQuery("#ux_text_appear_after_counter_" + timestamp).css({"position": "", "margin-top": "", "margin-left": ""});
					jQuery("#ux_txt_singal_line_text_" + timestamp).css({"display": "inline-block", "margin-left": "0px", "margin-right": "5%"});
					jQuery("#ux_sub_div_" + timestamp).addClass("field_label").addClass("control-label");
				break;
				case "hidden":
					jQuery("#field_label_" + timestamp).addClass("field_label").addClass("control-label");
					jQuery("#ux_text_appear_after_counter_" + timestamp).css({"position": "", "margin-top": "", "margin-left": ""});
					jQuery("#ux_txt_singal_line_text_" + timestamp).css({"display": "block", "margin-left": "9px"});
					if(control_name == "radio-list" || control_name == "checkbox-list")
					{
						jQuery("#ux_txt_check_box_" + timestamp).insertAfter("#field_label_" + timestamp);
					}
					else
					{
						jQuery("#ux_txt_singal_line_text_" + timestamp).insertAfter("#field_label_" + timestamp).css({"margin-right": "0"});
					}
					jQuery("#field_label_" + timestamp).css("display", "none");
				break;
			}
		}
	}
	if (typeof (number_settings_contact_bank_<?php echo intval( $random ); ?>) !== "function")
	{
		function number_settings_contact_bank_<?php echo intval( $random ); ?>(timestamp, event, step_number_cb, min_number, max_number)
		{
			var count = 0;
			var step_count = 0;
			step_number_cb = parseInt(step_number_cb);
			min_number = parseInt(min_number);
			max_number = parseInt(max_number);
			var input_number = parseInt(jQuery("#ux_txt_singal_line_text_" + timestamp).val());
			jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "none");
			if (min_number !== "" && max_number !== "")
			{
				jQuery("#ux_btn_save_changes").removeAttr("disabled","disabled");
				if (input_number > max_number)
				{
					count = 1;
				}
				else if (jQuery.trim(input_number) < min_number)
				{
					count = 1;
				}
			}
			if (input_number % step_number_cb !== 0 && step_number_cb !== "") {
				step_count = 1;
			}
			if (count === 1 && step_count === 1) {
				jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "block").html("Please enter number between " + min_number + " and " + max_number + " Please Increment By " + step_number_cb).addClass("field_label");
				jQuery("#ux_btn_save_changes").attr("disabled","disabled");
			}
			else if (step_count === 1)
			{
				jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "block").html("Please Increment By " + step_number_cb).addClass("field_label");
				jQuery("#ux_btn_save_changes").attr("disabled","disabled");
			}
			else if (count === 1)
			{
				jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "block").html("Please enter number between " + min_number + " and " + max_number + "").addClass("field_label");
				jQuery("#ux_btn_save_changes").attr("disabled","disabled");
			}
			if (input_number === "")
			{
				jQuery("#ux_text_appear_after_counter_" + timestamp).css("display", "none");
				jQuery("#ux_btn_save_changes").attr("disabled","disabled");
			}
		}
	}
	if (typeof (submit_form_contact_bank_<?php echo intval( $random ); ?>) !== "function")
	{
		function submit_form_contact_bank_<?php echo intval( $random ); ?>(controls_ids, form_name, save_submssion, page_url, submission_enable_disable, submission_limit, redirect_type, redirect_url,form_success_message)
		{
			<?php
			if ( isset( $_REQUEST['cb_preview_form'] ) ) {// WPCS: Input var ok, CSRF ok.
				?>
					var form_id = "<?php echo isset( $_REQUEST['cb_preview_form'] ) ? intval( $_REQUEST['cb_preview_form'] ) : ''; // WPCS: Input var ok, CSRF ok. ?>";
				<?php
			} else {
				?>
					var form_id = "<?php echo isset( $form_id ) ? intval( $form_id ) : ''; ?>";
				<?php
			}
			?>
			var id_count = "<?php echo isset( $id_count ) ? intval( $id_count ) : ''; ?>";
			var url_redirect_after_submit = redirect_type == "page" ? page_url : redirect_url;
			jQuery("#ux_frm_main_container_<?php echo intval( $random ); ?>").validate({
				errorClass: "custom-error",
				rules:
				{
					<?php
					if ( isset( $form_unserialized_meta_value['controls'] ) && count( $form_unserialized_meta_value['controls'] ) > 0 ) {
						foreach ( $form_unserialized_meta_value['controls'] as $controls ) {
							switch ( $controls['required_type'] ) {
								case 'enable':
									switch ( $controls['control_type'] ) {
										case 'website_url':
											?>
												ux_txt_singal_line_text_<?php echo $controls['timestamp']; // WPCS: XSS ok. ?> :
												{
													required: true,
													url: true
												},
											<?php
											break;
										case 'checkbox-list':
											?>
												"ux_txt_check_box_lists_<?php echo $controls['timestamp']; // WPCS: XSS ok. ?>[]" :
												{
													required: true
												},
											<?php
											break;
										default:
											?>
												ux_txt_singal_line_text_<?php echo $controls['timestamp']; // WPCS: XSS ok. ?> :
												{
													required: true
												},
											<?php
									}
									break;
							}
						}
					}
					?>
					ux_chk_gdpr_compliance_agree_form_<?php echo intval( $random ); ?>:
					{
					required: true
					},
				},
				messages:
				{
					<?php
					if ( isset( $form_unserialized_meta_value['controls'] ) && count( $form_unserialized_meta_value['controls'] ) > 0 ) {
						foreach ( $form_unserialized_meta_value['controls'] as $controls ) {
							switch ( $controls['required_type'] ) {
								case 'enable':
									switch ( $controls['control_type'] ) {
										case 'website_url':
											?>
												ux_txt_singal_line_text_<?php echo $controls['timestamp']; // WPCS: XSS ok. ?>: "<?php echo isset( $controls['custom_validation_message'] ) && '' !== $controls['custom_validation_message'] ? esc_attr( $controls['custom_validation_message'] ) : 'This field is Required!'; ?>",
											<?php
											break;
										case 'checkbox-list':
											?>
												"ux_txt_check_box_lists_<?php echo $controls['timestamp']; // WPCS: XSS ok. ?>[]" : "<?php echo isset( $controls['custom_validation_message'] ) && '' !== $controls['custom_validation_message'] ? esc_attr( $controls['custom_validation_message'] ) : 'This field is Required!'; ?>",
											<?php
											break;
										default:
											?>
												ux_txt_singal_line_text_<?php echo $controls['timestamp']; // WPCS: XSS ok. ?>: "<?php echo isset( $controls['custom_validation_message'] ) && '' !== $controls['custom_validation_message'] ? esc_attr( $controls['custom_validation_message'] ) : 'This field is Required!'; ?>",
											<?php
									}
									break;
							}
						}
					}
					?>
					ux_chk_gdpr_compliance_agree_form_<?php echo intval( $random ); ?>: "This field is Required!",
				},
				errorPlacement: function(error, element)
				{
					<?php
					if ( isset( $form_unserialized_meta_value['controls'] ) && count( $form_unserialized_meta_value['controls'] ) > 0 ) {
						foreach ( $form_unserialized_meta_value['controls'] as $controls ) {
							if ( 'radio-list' === $controls['control_type'] || 'checkbox-list' === $controls['control_type'] ) {
								?>
									error.insertAfter(element.parent().children("label:last-child"));
								<?php
							} else {
								?>
									error.insertAfter(element.parent());
								<?php
							}
						}
					}
					?>
				},
				submitHandler: function ()
				{
					jQuery("html, body").animate({ scrollTop: 0 }, "slow");
					if ((submission_enable_disable == "disable") || (submission_enable_disable == "enable" && id_count < submission_limit))
					{
						jQuery("#form_error_message_frontend_<?php echo intval( $random ); ?>").css("display", "none");
						jQuery("#form_success_message_frontend_<?php echo intval( $random ); ?>").css("display", "block");
						jQuery("#success_message_text_<?php echo intval( $random ); ?>").text("Kindly wait until the form is submitted.");
					}
					jQuery.post(ajaxurl, {
						form_id : form_id,
						save_submssion : save_submssion,
						submission_limit : submission_limit,
						submission_enable_disable : submission_enable_disable,
						data : base64_encode_contact_bank(jQuery(form_name).serialize()),
						controls_ids : JSON.stringify(controls_ids),
						param : "frontend_form_module",
						action : "contact_bank_frontend_ajax_call"
					},
					function(data)
					{
						if ((submission_enable_disable == "disable") || (submission_enable_disable == "enable" && id_count < submission_limit))
						{
							jQuery("#form_success_message_frontend_<?php echo intval( $random ); ?>").css("display", "block");
							overlay_loading_contact_bank_<?php echo intval( $random ); ?>();
							jQuery("#success_message_text_<?php echo intval( $random ); ?>").text(form_success_message);
							setTimeout(function ()
							{
								remove_overlay_contact_bank_<?php echo intval( $random ); ?>();
								window.location.href = url_redirect_after_submit;
							}, 3000);
						}
						else
						{
							jQuery("#form_error_message_frontend_<?php echo intval( $random ); ?>").css("display", "block");
						}
					});
				}
			});
		}
	}
	var price_arr = [];
	jQuery(document).ready(function () {
	<?php
	if ( isset( $form_unserialized_meta_value['controls'] ) && count( $form_unserialized_meta_value['controls'] ) > 0 ) {
		foreach ( $form_unserialized_meta_value['controls'] as $controls ) {
			?>
			var timestamp = <?php echo esc_attr( $controls['timestamp'] ); ?>;
			var control_name = '<?php echo isset( $controls['control_type'] ) ? esc_attr( $controls['control_type'] ) : esc_attr( site_url() ); ?>';
			var label_placement_type = "<?php echo isset( $controls['label_placement'] ) ? esc_attr( $controls['label_placement'] ) : 'above'; ?>";
			var input_mask_type = "<?php echo isset( $controls['input_mask_type'] ) ? esc_attr( $controls['input_mask_type'] ) : 'none'; ?>";
			var custom_mask = "<?php echo isset( $controls['custom_mask'] ) ? esc_attr( $controls['custom_mask'] ) : ''; ?>";
			change_label_placement_contact_bank_<?php echo intval( $random ); ?>("ux_ddl_label_placement_" + timestamp, timestamp, label_placement_type, control_name);
			apply_input_masking_contact_bank_<?php echo intval( $random ); ?>("ux_txt_singal_line_text_" + timestamp, timestamp, input_mask_type, custom_mask);
			if(control_name == "select")
			{
				jQuery("#ux_txt_singal_line_text_" + timestamp).val("<?php echo isset( $controls['default_value'] ) && '' !== $controls['default_value'] ? esc_attr( $controls['default_value'] ) : ''; ?>");
			}
		<?php
		}
	}
	?>
	});
</script>
