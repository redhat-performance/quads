<?php
/**
 * This file contains javascript.
 *
 * @author  Tech Banker
 * @package contact-bank/includes
 * @version 3.0
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
		$get_form_id_nonce = wp_create_nonce( 'cb_get_form_id_nonce' );
		?>
		</div>
		</div>
		</div>
		<script type="text/javascript">
			function load_sidebar_content_contact_bank() {
				var menus_height = jQuery(".page-sidebar-menu-tech-banker").height();
				var content_height = jQuery(".page-content").height() + 30;
				if (parseInt(menus_height) > parseInt(content_height)) {
					jQuery(".page-content").attr("style", "min-height:" + menus_height + "px");
				} else {
					jQuery(".page-sidebar-menu-tech-banker").attr("style", "min-height:" + content_height + "px");
				}
			}
			var sidebar_load_interval = setInterval(load_sidebar_content_contact_bank, 1000);
			setTimeout(function () {
				clearInterval(sidebar_load_interval);
			}, 5000);
			jQuery("li > a").parents("li").each(function () {
				if (jQuery(this).parent("ul.page-sidebar-menu-tech-banker").size() === 1) {
					jQuery(this).find("> a").append("<span class=\"selected\"></span>");
				}
			});
			jQuery(".tooltips").tooltip_tip({placement: "right"});
			jQuery(".page-sidebar-tech-banker").on("click", "li > a", function (e) {
				var hasSubMenu = jQuery(this).next().hasClass("sub-menu");
				var parent = jQuery(this).parent().parent();
				var sidebar_menu = jQuery(".page-sidebar-menu-tech-banker");
				var sub = jQuery(this).next();
				var slideSpeed = parseInt(sidebar_menu.data("slide-speed"));
				parent.children("li.open").children(".sub-menu:not(.always-open)").slideUp(slideSpeed);
				parent.children("li.open").removeClass("open");
				var sidebar_close = parent.children("li.open").removeClass("open");
				if (sidebar_close) {
					setInterval(load_sidebar_content_contact_bank, 100);
				}
				if (sub.is(":visible")) {
					jQuery(this).parent().removeClass("open");
					sub.slideUp(slideSpeed);
				} else if (hasSubMenu) {
					jQuery(this).parent().addClass("open");
					sub.slideDown(slideSpeed);
				}
			});
			function default_value_contact_bank(id, value) {
				jQuery(id).val() === "" ? jQuery(id).val(value) : jQuery(id).val();
				jQuery(id).val() < 1 ? jQuery(id).val(value) : jQuery(id).val();
			}
			function paste_prevent_contact_bank(control_id) {
				jQuery("#" + control_id).on("paste", function (e) {
					e.preventDefault();
				});
			}
			function premium_edition_notification_contact_bank()
			{
				var premium_edition = <?php echo wp_json_encode( $cb_message_premium_edition ); ?>;
				var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
				toastr[shortCutFunction](premium_edition);
			}
			function color_picker_contact_bank(id, color_value) {
				jQuery(id).colpick({
					layout: "hex",
					colorScheme: "dark",
					color: color_value,
					onChange: function (hsb, hex, rgb, el, bySetColor) {
						if (!bySetColor)
							jQuery(el).val("#" + hex);
					}
				}).keyup(function () {
					jQuery(this).colpickSetColor("#" + this.value);
				}).focus(function () {
					jQuery(id).colpickSetColor(color_value);
				});
			}
			function check_opacity_contact_bank(input) {
				if (input.value < 0)
					input.value = 0;
				if (input.value > 100)
					input.value = 100;
			}
			function enter_only_digits_contact_bank(event) {
				if (event.which !== 8 && event.which !== 0 && (event.which < 48 || event.which > 57)) {
					event.preventDefault();
				}
			}
			function gdpr_compliance_contact_bank() {
				var gdpr_compliance_type = jQuery("#ux_ddl_gdpr_compliance").val();
				switch(gdpr_compliance_type)
				{
					case 'disable':
						jQuery("#ux_div_gdpr_compliance_text").hide();
						break;

					default:
						jQuery("#ux_div_gdpr_compliance_text").show();
						break;
				}
			}
			function enter_only_digits_for_price(event) {
				if (event.which != 46 && (event.which < 48 || event.which > 57)) {
				event.preventDefault();
				}
			}
			function contact_bank_manage_datatable(id) {
				var oTable = jQuery(id).dataTable({
					"pagingType": "full_numbers",
					"language": {
						"emptyTable": "No data available in table",
						"info": "Showing _START_ to _END_ of _TOTAL_ entries",
						"infoEmpty": "No entries found",
						"infoFiltered": "(filtered1 from _MAX_ total entries)",
						"lengthMenu": "Show _MENU_ entries",
						"search": "Search:",
						"zeroRecords": "No matching records found"
					},
					"bSort": true,
					"pageLength": 10,
					"aoColumnDefs": [{"bSortable": false, "aTargets": [0]}]
				});
				return oTable;
			}
			function overlay_loading_contact_bank(message) {
				var overlay_opacity = jQuery("<div class=\"opacity_overlay\"></div>");
				jQuery("body").append(overlay_opacity);
				var overlay = jQuery("<div class=\"loader_opacity\"><div class=\"processing_overlay\"></div></div>");
				jQuery("body").append(overlay);
				var success = <?php echo wp_json_encode( $cb_success ); ?>;
				if (message !== undefined) {
					var issuccessmessage = jQuery("#toast-container").exists();
					if (issuccessmessage !== true) {
						var shortCutFunction = jQuery("#manage_messages input:checked").val();
						toastr[shortCutFunction](message, success);
					}
				}
			}
			function remove_overlay_contact_bank() {
				jQuery(".loader_opacity").remove();
				jQuery(".opacity_overlay").remove();
			}
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
			function submit_handler_common_contact_bank(form_id, form_name, meta_id, param, nonce, overlay_loading, window_location, template, control_ids) {
				overlay_loading === "" ? overlay_loading_contact_bank() : overlay_loading_contact_bank(overlay_loading);
				jQuery.post(ajaxurl, {
					form_meta_id: form_id,
					data: base64_encode_contact_bank(jQuery(form_name).serialize()),
					id: meta_id,
					param: param,
					template: template,
					control_ids: JSON.stringify(control_ids),
					action: "contact_bank_action_module",
					_wp_nonce: nonce
				},
						function (data) {
							setTimeout(function () {
								remove_overlay_contact_bank();
								window.location.href = "admin.php?page=" + window_location;
							}, 3000);
						});
			}
			function add_new_form_contact_bank() {
				jQuery.post(ajaxurl,
				{
					param: "cb_get_form_id_contact_bank",
					action: "contact_bank_action_module",
					_wp_nonce: "<?php echo esc_attr( $get_form_id_nonce ); ?>"
				},
				function (data)
				{
					window.location.href = "admin.php?page=cb_add_new_form&form_id=" + data;
				});
			}
			function confirm_delete_contact_bank(meta_id, overlay_message, page_url, param) {
				var checkstr = confirm(<?php echo wp_json_encode( $cb_confirm_data ); ?>);
				if (checkstr === true) {
					jQuery.post(ajaxurl, {
						meta_id: meta_id,
						param: param,
						action: "contact_bank_action_module",
						_wp_nonce: "<?php echo isset( $cb_contact_bank_delete_nonce ) ? esc_attr( $cb_contact_bank_delete_nonce ) : ''; ?>"
					},
					function (data) {
						overlay_loading_contact_bank(overlay_message);
						setTimeout(function () {
							remove_overlay_contact_bank();
							window.location.href = "admin.php?page="+page_url;
						}, 3000);
					});
				}
			}
			function only_digits_contact_bank(event, random_id) {
				var content = jQuery("#ux_txt_singal_line_text_" + random_id).val();
				var words = content.split(/\s+/);
				var words_length = words.length;
				var max_limit = jQuery("#ux_txt_limit_input_" + random_id).val();
				jQuery("#ux_txt_singal_line_text_" + random_id).removeAttr("maxlength", "");
				var value = jQuery("#ux_txt_text_appear_" + random_id).val();
				if(max_limit === "")
				{
					jQuery("#ux_text_appear_after_counter_" + random_id).css("display","none");
				}
				else if (words_length > max_limit) {
					event.preventDefault();
					var lastIndex = content.lastIndexOf(" ");
					jQuery("#ux_txt_singal_line_text_" + random_id).val(content.substring(0, lastIndex));
					jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "block").addClass("field_label");
					if (max_limit > words_length)
					{
						jQuery("#ux_text_appear_after_counter_" + random_id).text(max_limit - words_length + " " + value);
					}
				} else
				{
					jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "block").addClass("field_label");
					jQuery("#ux_text_appear_after_counter_" + random_id).text(max_limit - words_length + " " + value);
				}
			}
			function only_characters_contact_bank(event, random_id) {
				var content = jQuery("#ux_txt_singal_line_text_" + random_id).val();
				var characters_length = content.length;
				var max_limit = jQuery("#ux_txt_limit_input_" + random_id).val();
				var value = jQuery("#ux_txt_text_appear_" + random_id).val();
				jQuery("#ux_txt_singal_line_text_" + random_id).attr("maxlength", max_limit);
				if(max_limit === "")
				{
					jQuery("#ux_text_appear_after_counter_" + random_id).css("display","none");
				}
				else if (characters_length > max_limit) {
					var lastIndex = content.lastIndexOf(" ");
					jQuery("#ux_txt_singal_line_text_" + random_id).val(content.substring(0, lastIndex));
					jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "block").addClass("field_label");
					jQuery("#ux_text_appear_after_counter_" + random_id).text(max_limit - characters_length + " " + value);
				}
				else {
					jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "block").addClass("field_label");
					jQuery("#ux_text_appear_after_counter_" + random_id).text(max_limit - characters_length + " " + value);
				}
			}
			function toggling_fields_contact_bank(class_name) {
				jQuery("." + class_name).animate({
					height: 'toggle'
				});
			}
			function check_all_contact_bank(id) {
				if (jQuery("input:checked", oTable.fnGetFilteredNodes()).length === jQuery("input[type=checkbox]", oTable.fnGetFilteredNodes()).not("[disabled]").length) {
					jQuery(id).attr("checked", "checked");
				} else {
					jQuery(id).removeAttr("checked");
				}
			}
			function change_textarea_rows_contact_bank(random_id)
			{
				jQuery("#ux_txt_singal_line_text_"+random_id).attr("rows",jQuery("#ux_txt_no_of_rows_"+random_id).val());
			}
			function drag_drop_radio_button_contact_bank(type)
			{
				jQuery(".radio-drag").draggable({
					cancel: "input",
					revert: false,
					helper: "clone",
					revertDuration: 0,
					cursor: "move",
					refreshPositions: true
				});
				jQuery(".radio-drag").droppable({
					drop: function(event, ui) {
						var $dragElem = jQuery(ui.draggable).clone().replaceAll(this);
						jQuery(this).replaceAll(ui.draggable);
						if(type === "checkbox")
						{
						drag_drop_radio_button_contact_bank("checkbox");
						}
						else if(type === "radio")
						{
						drag_drop_radio_button_contact_bank("radio");
						}
						else if(type === "select")
						{
						drag_drop_radio_button_contact_bank("select");
						}
						if (jQuery(ui.draggable)[0].id != "") {
						x = ui.helper.clone();
						ui.helper.remove();
						x.draggable({
							helper: 'original',
							cursor: 'move',
							drop: function(event, ui) {
							jQuery(ui.draggable).remove();
							}
						});
						}
						var arr = [];
						var line = "";
						var id = this.id;
						var ids = id.split("_");
						var element_class = jQuery("#ux_txt_element_class_"+ids[5]).val();
						if(type === "checkbox" || type === "radio")
						{
						jQuery(".sub_div").find("#ux_txt_check_box_"+ids[5]).find("#field_labels_"+ids[5]).each(function(){
							jQuery(this).children("#ux_txt_check_box_lists_"+ids[5]).remove();
							jQuery(this).children("#ux_chk_label_lists_"+ids[5]).remove();
						});
						}
						else if(type === "select")
						{
						jQuery(".sub_div").each(function(){
							jQuery(this).children("#ux_txt_singal_line_text_"+ids[5]).children("option").remove();
						});
						jQuery(".ux_div_widget_content").each(function(){
							jQuery(this).find("#ux_txt_default_value_"+ids[5]).children("option").remove();
						});
						}
						jQuery("#ux_div_append_input_radio_" + ids[5]).find("div").each(function() {
							var options = jQuery(this).children("input:eq(1)").val();
							var values = jQuery(this).children("input:eq(2)").val();
							line += options+","+values+";";
							arr[arr.length] = { text: options , value: values };
						});
						var lines = line.split(";");
						for (var i=0; i < lines.length; i++) {
						if (/\S/.test(lines[i])) {
							var value = lines[i].split(",");
							if(type === "checkbox")
							{
								jQuery("#ux_txt_check_box_"+ ids[5]).find("#field_labels_"+ids[5]).append("<input style='margin-left:9px;' type=checkbox name=ux_txt_check_box_lists_"+ids[5]+" id=ux_txt_check_box_lists_"+ids[5]+" class='"+element_class+" checkbox_class_"+ids[5]+"' value="+value[1]+" checked=checked ><label id=ux_chk_label_lists_"+ids[5]+" name=ux_chk_label_lists_"+ids[5]+" value="+value[1]+">"+value[0]+"</label></input>");
							}
							else if(type === "radio")
							{
								jQuery("#ux_txt_check_box_"+ ids[5]).find("#field_labels_"+ids[5]).append("<input type=radio style='margin-left:9px;' name=ux_txt_check_box_lists_"+ids[5]+" id=ux_txt_check_box_lists_"+ids[5]+" class='"+element_class+" checkbox_class_"+ids[5]+"' value="+value[1]+" checked=checked ><label id=ux_chk_label_lists_"+ids[5]+" name=ux_chk_label_lists_"+ids[5]+" value="+value[1]+">"+value[0]+"</label></input>");
							}
							else if(type === "select")
							{
								jQuery("#ux_txt_singal_line_text_" + ids[5]).append("<option value=\"" + value[1] + "\">" + value[0] + "</option>");
								jQuery("#ux_txt_default_value_" + ids[5]).append("<option value=\"" + value[1] + "\">" + value[0] + "</option>");
							}
						}
						}
						jQuery("#ux_hidden_options_values_" + ids[5]).val(JSON.stringify(arr));
					}
				});
			}
			function delete_radio_options_contact_bank(dynamic_id, dynamicId){
				var value = jQuery("#ux_txt_ddl_value_" + dynamic_id).val();
				var confirm_delete = confirm(<?php echo wp_json_encode( $cb_confirm_data ); ?>);
				if(confirm_delete === true)
				{
					jQuery("#ux_div_full_control_radio_"+dynamic_id).remove();
					jQuery("#ux_txt_check_box_lists_"+dynamicId+"[value='"+value+"']").remove();
					jQuery("#ux_chk_label_lists_"+dynamicId+"[value='"+value+"']").remove();
					jQuery("#ux_ddl_options_required_"+dynamicId + " option[value=\"" + value + "\"]").remove();
					var arr = [], $select = jQuery("#ux_ddl_options_required_" + dynamicId);
							$select.find("option").each(function() {
								arr[arr.length] = { text: this.text, value: this.value  };
					});
					jQuery("#ux_hidden_options_values_" + dynamicId).val(JSON.stringify(arr));
					if (jQuery("#ux_ddl_options_required_"+dynamicId).val() === null) {
						jQuery("#ux_drop_down_value_" + dynamicId).css("display", "none");
					}
				}
			}
			var id = new Date().getTime();
			function add_control_options_contact_bank(dynamicId,type) {
				var ddl_options = jQuery("#ux_txt_add_form_option_" + dynamicId).val();
				var ddl_values = jQuery("#ux_txt_add_form_values_"+dynamicId).val();
				if (ddl_options === "" && ddl_values === "") {
					var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
					toastr[shortCutFunction](<?php echo wp_json_encode( $cb_add_fill_option_value ); ?>);
				} else if(ddl_options !== "" && ddl_values === "") {
					var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
					toastr[shortCutFunction](<?php echo wp_json_encode( $cb_add_fill_option_value ); ?>);
				} else if(ddl_options === "" && ddl_values !== "") {
					var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
					toastr[shortCutFunction](<?php echo wp_json_encode( $cb_add_fill_option_value ); ?>);
				} else {
					id++;
					var dynamic_id = dynamicId+"_"+id;
					jQuery("#ux_drop_down_value_" + dynamicId).append("<div id=ux_div_append_input_radio_"+dynamicId+" class=append_input_radio_"+dynamicId+">");
					jQuery("#ux_div_append_input_radio_" + dynamicId).css("margin-top", "10px");
					jQuery("#ux_div_append_input_radio_" + dynamicId).append("<div id=ux_div_full_control_radio_"+dynamic_id+" class=full_control_radio_"+dynamicId+"><input type=radio id=ux_txt_radio_add_button_"+dynamic_id+" name=ux_txt_radio_add_button_"+dynamicId+" style='margin-right:8px;' class=radio_add_button_"+dynamicId+"><input type=text style='margin-left:2px;' id=ux_txt_option_value_"+dynamic_id+" class=txt_option_value_"+dynamicId+" value=\"" + ddl_options + "\"><input type=text style='margin-left:3px;' id=ux_txt_ddl_value_"+dynamic_id+" class=txt_ddl_value_"+dynamicId+" value=\"" + ddl_values + "\"><i class=icon-custom-minus id=ux_btn_delete_option_"+dynamic_id+"></i></div>");
					jQuery("#ux_btn_delete_option_" +dynamic_id).addClass("cb-radio-minus");
					jQuery("#ux_div_full_control_radio_"+dynamic_id).addClass("radio-drag").css("margin-bottom","5px");
					jQuery("#ux_btn_delete_option_"+dynamic_id).attr("onclick", "delete_radio_options_contact_bank('"+ dynamic_id + "','" + dynamicId + "')").css("margin-left", "9px");
					jQuery("#ux_btn_delete_option_"+dynamic_id).addClass("cb-radio-minus");
					if(type === "radio")
					{
					jQuery(".txt_option_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'radio')");
					jQuery(".txt_ddl_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'radio')");
					}
					else if (type === "checkbox")
					{
					jQuery(".txt_option_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'checkbox')");
					jQuery(".txt_ddl_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'checkbox')");
					}
					jQuery("#ux_ddl_options_required_" + dynamicId).append("<option value=\"" + ddl_values + "\">" + ddl_options + "</option>");
					jQuery("#ux_txt_singal_line_text_" + dynamicId).append("<option value=\"" + ddl_values + "\">" + ddl_options + "</option>");
					jQuery("#ux_drop_down_value_" + dynamicId).css("display", "");
					jQuery("#ux_txt_add_form_option_"+dynamicId).val("");
					jQuery("#ux_txt_add_form_values_"+dynamicId).val("");
					jQuery("#ux_ddl_options_required_" + dynamicId).hide();
					var arr = [], $select = jQuery("#ux_ddl_options_required_" + dynamicId);
					$select.find("option").each(function() {
						arr[arr.length] = { text: this.text, value: this.value };
					});
					jQuery("#ux_hidden_options_values_" + dynamicId).val(JSON.stringify(arr));
					jQuery("#ux_txt_singal_line_text_"+dynamicId).remove();
					var element_class = jQuery("#ux_txt_element_class_"+dynamicId).val();
					if(type === "checkbox")
					{
						drag_drop_radio_button_contact_bank("checkbox");
						jQuery("#ux_txt_check_box_"+ dynamicId).find("#field_labels_"+dynamicId).append("<input style='margin-left:9px;' type=checkbox onclick=show_hide_text_field_options("+dynamicId+") name=ux_txt_check_box_lists_"+dynamicId+" id=ux_txt_check_box_lists_"+dynamicId+" class='"+element_class+" checkbox_class_"+dynamicId+"' value="+ddl_values+"><label id=ux_chk_label_lists_"+dynamicId+" name=ux_chk_label_lists_"+dynamicId+" value="+ddl_values+">"+ddl_options+"</label>");
					}else if(type === "radio")
					{
						drag_drop_radio_button_contact_bank("radio");
						jQuery("#ux_txt_check_box_"+ dynamicId).find("#field_labels_"+dynamicId).append("<input type=radio onclick=show_hide_text_field_options("+dynamicId+") style='margin-left:9px;' name=ux_txt_check_box_lists_"+dynamicId+" id=ux_txt_check_box_lists_"+dynamicId+" class='"+element_class+" checkbox_class_"+dynamicId+"' value="+ddl_values+"><label id=ux_chk_label_lists_"+dynamicId+" name=ux_chk_label_lists_"+dynamicId+" value="+ddl_values+">"+ddl_options+"</label></input>");
					}
				}
			}
			function radio_option_value_change_contact_bank(dynamicId, type)
			{
				var arr = [];
				var line = "";
				var element_class = jQuery("#ux_txt_element_class_"+dynamicId).val();
				jQuery("#ux_ddl_options_required_"+dynamicId).empty();
				jQuery(".sub_div").find("#ux_txt_check_box_"+dynamicId).find("#field_labels_"+dynamicId).each(function(){
					jQuery(this).children("#ux_txt_check_box_lists_"+dynamicId).remove();
					jQuery(this).children("#ux_chk_label_lists_"+dynamicId).remove();
				});
				jQuery("#ux_div_append_input_radio_" + dynamicId).find("div").each(function() {
					var options = jQuery(this).children("input:eq(1)").val();
					var values = jQuery(this).children("input:eq(2)").val();
					line += options+"^"+values+";";
					arr[arr.length] = { text: options , value: values };
					jQuery("#ux_txt_check_box_lists_"+dynamicId).attr("value", values);
					jQuery("#ux_chk_label_lists_"+dynamicId).attr("value", values).text(options);
					jQuery("#ux_ddl_options_required_" + dynamicId).append("<option value=\"" + values + "\">" + options + "</option>");
				});
				var lines = line.split(";");
				for (var i=0; i < lines.length; i++) {
					if (/\S/.test(lines[i])) {
					var value = lines[i].split("^");
					if(type === "checkbox")
					{
						jQuery("#ux_txt_check_box_"+ dynamicId).find("#field_labels_"+dynamicId).append("<input style='margin-left:9px;' type=checkbox name=ux_txt_check_box_lists_"+dynamicId+" id=ux_txt_check_box_lists_"+dynamicId+" class='"+element_class+" checkbox_class_"+dynamicId+"' value="+value[1]+" checked=checked ><label id=ux_chk_label_lists_"+dynamicId+" name=ux_chk_label_lists_"+dynamicId+" value="+value[1]+">"+value[0]+"</label>");
					}
					else if(type === "radio")
					{
						jQuery("#ux_txt_check_box_"+ dynamicId).find("#field_labels_"+dynamicId).append("<input type=radio style='margin-left:9px;' name=ux_txt_check_box_lists_"+dynamicId+" id=ux_txt_check_box_lists_"+dynamicId+" class='"+element_class+" checkbox_class_"+dynamicId+"' value="+value[1]+" checked=checked ><label id=ux_chk_label_lists_"+dynamicId+" name=ux_chk_label_lists_"+dynamicId+" value="+value[1]+">"+value[0]+"</label></input>");
					}
					}
				}
				jQuery("#ux_hidden_options_values_" + dynamicId).val(JSON.stringify(arr));
			}
			function import_controls_values_contact_bank(dynamicId,type) {
			var lines = jQuery("#ux_txt_textarea_"+dynamicId).val().split(/\n/);
			var element_class = jQuery("#ux_txt_element_class_"+dynamicId).val();
			if(lines != "") {
				for (var i=0; i < lines.length; i++) {
					if (/\S/.test(lines[i])) {
					var value = lines[i].split(",");
					id++;
					var dynamic_id = dynamicId+"_"+id;
					if(value[1] !== undefined){
						jQuery("#ux_ddl_options_required_" + dynamicId).append("<option value=\"" + value[1] + "\">" + value[0] + "</option>");
						jQuery("#ux_txt_singal_line_text_"+dynamicId).remove();
						jQuery("#ux_ddl_options_required_" + dynamicId).hide();
						jQuery("#ux_drop_down_value_" + dynamicId).append("<div id=ux_div_append_input_radio_"+dynamicId+" class=append_input_radio_"+dynamicId+">");
						jQuery("#ux_div_append_input_radio_" + dynamicId).css("margin-top", "10px");
						jQuery("#ux_div_append_input_radio_" + dynamicId).append("<div id=ux_div_full_control_radio_"+dynamic_id+" class=full_control_radio_"+dynamicId+"><input type=radio id=ux_txt_radio_add_button_"+dynamic_id+" style='margin-left:1px' name=ux_txt_radio_add_button_"+dynamicId+" style='margin-right:8px;'  class=radio_add_button_"+dynamicId+"><input type=text style='margin-left:2px;' id=ux_txt_option_value_"+dynamic_id+" style='margin-left:4px' class=txt_option_value_"+dynamicId+" value=\"" + value[0] + "\"><input type=text style='margin-left:3px;' id=ux_txt_ddl_value_"+dynamic_id+" class=txt_ddl_value_"+dynamicId+" style='margin-left:4px' value=\"" + value[1] + "\"><i class=icon-custom-minus id=ux_btn_delete_option_"+dynamic_id+"></i></div>");
						jQuery("#ux_btn_delete_option_" +dynamic_id).addClass("cb-radio-minus");
						jQuery("#ux_div_full_control_radio_"+dynamic_id).addClass("radio-drag").css("margin-bottom","5px");
						jQuery("#ux_btn_delete_option_"+dynamic_id).attr("onclick", "delete_radio_options_contact_bank('"+ dynamic_id + "','" + dynamicId + "')").css("margin-left", "9px");
						jQuery("#ux_btn_delete_option_"+dynamic_id).addClass("cb-radio-minus");
						if(type === "checkbox")
						{
							jQuery(".txt_option_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'checkbox')");
							jQuery(".txt_ddl_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'checkbox')");
							jQuery("#ux_txt_check_box_"+ dynamicId).find("#field_labels_"+dynamicId).append("<input type=checkbox style='margin-left:9px;' name=ux_txt_check_box_lists_"+dynamicId+" id=ux_txt_check_box_lists_"+dynamicId+" class='"+element_class+" checkbox_class_"+dynamicId+"' value="+value[1]+" checked=checked ><label id=ux_chk_label_lists_"+dynamicId+" name=ux_chk_label_lists_"+dynamicId+" value="+value[1]+">"+value[0]+"</label>");
						}else if(type === "radio")
						{
							jQuery(".txt_option_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'radio')");
							jQuery(".txt_ddl_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'radio')");
							jQuery("#ux_txt_check_box_"+ dynamicId).find("#field_labels_"+dynamicId).append("<input style='margin-left:9px;' type=radio name=ux_txt_check_box_lists_"+dynamicId+" id=ux_txt_check_box_lists_"+dynamicId+" class='"+element_class+" checkbox_class_"+dynamicId+"' value="+value[1]+" checked=checked ><label id=ux_chk_label_lists_"+dynamicId+" name=ux_chk_label_lists_"+dynamicId+" value="+value[1]+">"+value[0]+"</label>");
						}
					} else {
						jQuery("#ux_ddl_options_required_" + dynamicId).append("<option value=\"" + value[0] + "\">" + value[0] + "</option>");
						jQuery("#ux_txt_singal_line_text_"+dynamicId).remove();
						jQuery("#ux_ddl_options_required_" + dynamicId).hide();
						jQuery("#ux_drop_down_value_" + dynamicId).append("<div id=ux_div_append_input_radio_"+dynamicId+" class=append_input_radio_"+dynamicId+">");
						jQuery("#ux_div_append_input_radio_" + dynamicId).css("margin-top", "10px");
						jQuery("#ux_div_append_input_radio_" + dynamicId).append("<div id=ux_div_full_control_radio_"+dynamic_id+" class=full_control_radio_"+dynamicId+"><input type=radio id=ux_txt_radio_add_button_"+dynamic_id+" name=ux_txt_radio_add_button_"+dynamicId+" style='margin-right:8px;'  class=radio_add_button_"+dynamicId+"><input type=text style='margin-left:2px;' id=ux_txt_option_value_"+dynamic_id+" class=txt_option_value_"+dynamicId+" value=\"" + value[0] + "\"><input type=text style='margin-left:3px;' id=ux_txt_ddl_value_"+dynamic_id+" class=txt_ddl_value_"+dynamicId+" value=\"" + value[0] + "\"><i class=icon-custom-minus id=ux_btn_delete_option_"+dynamic_id+"></i></div>");
						jQuery("#ux_div_full_control_radio_"+dynamic_id).addClass("radio-drag").css("margin-bottom","5px");
						jQuery("#ux_btn_delete_option_"+dynamic_id).attr("onclick", "delete_radio_options_contact_bank('"+ dynamic_id + "','" + dynamicId + "')").css("margin-left", "9px");
						jQuery("#ux_btn_delete_option_"+dynamic_id).addClass("cb-radio-minus");
						if(type === "checkbox")
						{
							jQuery(".txt_option_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'checkbox')");
							jQuery(".txt_ddl_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'checkbox')");
							jQuery("#ux_txt_check_box_"+ dynamicId).find("#field_labels_"+dynamicId).append("<input type=checkbox style='margin-left:9px;' name=ux_txt_check_box_lists_"+dynamicId+" id=ux_txt_check_box_lists_"+dynamicId+" class='"+element_class+" checkbox_class_"+dynamicId+"' value="+value[0]+" checked=checked ><label id=ux_chk_label_lists_"+dynamicId+" name=ux_chk_label_lists_"+dynamicId+" value="+value[0]+">"+value[0]+"</label>");
						}else if(type === "radio")
						{
							jQuery(".txt_option_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'radio')");
							jQuery(".txt_ddl_value_"+dynamicId).attr("onchange", "radio_option_value_change_contact_bank('"+ dynamicId + "', 'radio')");
							jQuery("#ux_txt_check_box_"+ dynamicId).find("#field_labels_"+dynamicId).append("<input style='margin-left:9px;' type=radio name=ux_txt_check_box_lists_"+dynamicId+" id=ux_txt_check_box_lists_"+dynamicId+" class='"+element_class+" checkbox_class_"+dynamicId+"' value="+value[0]+" checked=checked ><label id=ux_chk_label_lists_"+dynamicId+" name=ux_chk_label_lists_"+dynamicId+" value="+value[0]+">"+value[0]+"</label>");
						}
					}
					}
				}
				jQuery("#ux_txt_textarea_"+dynamicId).val("");
				var arr = [], $select = jQuery("#ux_ddl_options_required_" + dynamicId);
					$select.find("option").each(function() {
						arr[arr.length] = { text: this.text, value: this.value };
				});
				jQuery("#ux_hidden_options_values_" + dynamicId).val(JSON.stringify(arr));
				jQuery("#ux_drop_down_value_" + dynamicId).css("display", "block");
				var targeted_popup_class = "ux_open_popup_translator_"+dynamicId;
				jQuery('[data-popup="' + targeted_popup_class + '"]').fadeOut(350);
			}
			else
			{
				var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
				toastr[shortCutFunction](<?php echo wp_json_encode( $cb_add_data_to_import ); ?>);
			}
			type === "checkbox" ? drag_drop_radio_button_contact_bank("checkbox") : drag_drop_radio_button_contact_bank("radio");
		}
		<?php
		$check_contact_bank_wizard = get_option( 'contact-bank-wizard-set-up' );
		if ( isset( $_GET['page'] ) ) {
			$page = sanitize_text_field( wp_unslash( $_GET['page'] ) );// WPCS: CSRF ok,WPCS: input var ok.
		}
		$page_url = false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : $page;
		if ( isset( $_GET['page'] ) ) {// WPCS: CSRF ok, input var ok.
			switch ( $page_url ) {
				case 'cb_wizard_contact_bank':
				?>
				function show_hide_details_contact_bank()
				{
					if (jQuery("#ux_div_wizard_set_up").hasClass("wizard-set-up"))
					{
						jQuery("#ux_div_wizard_set_up").css("display", "none");
						jQuery("#ux_div_wizard_set_up").removeClass("wizard-set-up");
					} else
					{
						jQuery("#ux_div_wizard_set_up").css("display", "block");
						jQuery("#ux_div_wizard_set_up").addClass("wizard-set-up");
					}
				}
				function plugin_stats_contact_bank(type)
				{
					if( jQuery("#ux_txt_email_address_notifications").val() ===  "" && type !== "skip")
					{
						if( jQuery("#ux_txt_email_address_notifications").val() ===  "" )
						{
							jQuery("#ux_txt_validation_gdpr_contact_bank").css({"display":'','color':'red'});
							jQuery("#ux_txt_email_address_notifications").css("border-color","red");
						}
						else {
							jQuery("#ux_txt_validation_gdpr_contact_bank").css( 'display','none' );
							jQuery("#ux_txt_email_address_notifications").css("border-color","#ddd");
						}
					}
					else
					{
						jQuery("#ux_txt_validation_gdpr_contact_bank").css( 'display','none' );
						jQuery("#ux_txt_email_address_notifications").css("border-color","#ddd");
						overlay_loading_contact_bank();
						jQuery.post(ajaxurl,
						{
							id: jQuery("#ux_txt_email_address_notifications").val(),
							type: type,
							param: "wizard_contact_bank",
							action: "contact_bank_action_module",
							_wp_nonce: "<?php echo esc_attr( $contact_bank_check_status ); ?>"
						},
						function ()
						{
							remove_overlay_contact_bank();
							window.location.href = "admin.php?page=contact_dashboard";
						});
					}
				}
				<?php
					break;
				case 'contact_dashboard':
					?>
						jQuery("#ux_li_forms").addClass("active");
						jQuery("#ux_li_manage_forms").addClass("active");
					<?php
					if ( FORMS_CONTACT_BANK === '1' ) {
						?>
							var clipboard = new Clipboard(".icon-custom-docs");
							clipboard.on("success", function (e)
							{
								var shortCutFunction = jQuery("#manage_messages input:checked").val();
								var $toast = toastr[shortCutFunction](<?php echo wp_json_encode( $cb_shortcode_copy_successful ); ?>);
							});
							clipboard.on("error", function (e)
							{
								var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
								var $toast = toastr[shortCutFunction](<?php echo wp_json_encode( $cb_copied_failed ); ?>);
							});
							var oTable = contact_bank_manage_datatable("#ux_table_manage_forms");
							jQuery("#ux_chk_all_forms").click(function () {
								jQuery("input[type=checkbox]", oTable.fnGetFilteredNodes()).attr("checked", this.checked);
							});
						<?php
					}
					break;
				case 'cb_add_new_form':
					?>
						jQuery("#ux_li_forms").addClass("active");
						jQuery("#ux_li_add_new_forms").addClass("active");
						var contact_bank_control_ids = [];
						var product_ids = [];
					<?php
					if ( FORMS_CONTACT_BANK === '1' ) {
						?>
							function show_hide_redirect_controls_contact_bank() {
								var type = jQuery("#ux_ddl_redirect_type").val();
								switch(type)
								{
									case "page":
										jQuery("#ux_div_redirect_page").css("display", "block");
										jQuery("#ux_div_redirect_url").css("display", "none");
										break;
									default:
										jQuery("#ux_div_redirect_url").css("display", "block");
										jQuery("#ux_div_redirect_page").css("display", "none");
										break;
								}
							}
							function show_hide_submission_message_contact_bank(){
								var value_submission_message = jQuery("#ux_ddl_submission_limit_message").val();
								switch(value_submission_message)
								{
									case "enable":
										jQuery("#ux_div_submission_message,#submission_limit_number").css("display", "block");
										break;
									default:
										jQuery("#ux_div_submission_message,#submission_limit_number").css("display", "none");
										break;
								}
							}
							function change_label_placement_contact_bank(input_id, random_id) {
								var label_placement_type = jQuery("#" + input_id).val();
								switch (label_placement_type) {
									case "above":
										jQuery("#field_label_" + random_id).css("display","block").addClass("field_label").addClass("control-label");
										if(jQuery("#ux_control_type_"+random_id).val() === "radio-list" || jQuery("#ux_control_type_"+random_id).val() === "checkbox-list") {
											jQuery("#ux_txt_check_box_"+random_id).insertAfter("#field_label_" + random_id);
										}
										else
										{
											jQuery("#ux_txt_singal_line_text_"+random_id).insertAfter("#field_label_" + random_id);
											jQuery("#ux_txt_logical_captcha_"+random_id).insertAfter("#field_label_" + random_id);
										}
										jQuery("#ux_text_appear_after_counter_" + random_id).css({"position": "", "margin-top": "", "margin-left": ""});
										if(jQuery("#ux_control_type_"+random_id).val() != "star_rating") {
										jQuery("#ux_txt_singal_line_text_" + random_id).css({"display":"block","margin-left":"9px"});                                        }
										jQuery("#ux_sub_div_" + random_id).removeClass("field_label").removeClass("control-label");
										break;
									case "below":
										jQuery("#field_label_" + random_id).css("display", "block");
										if(jQuery("#ux_control_type_"+random_id).val() === "radio-list" || jQuery("#ux_control_type_"+random_id).val() === "checkbox-list") {
											jQuery("#ux_txt_check_box_"+random_id).insertBefore(jQuery("#field_label_" + random_id).addClass("field_label").addClass("control-label"));
										}
										else
										{
											jQuery("#ux_txt_singal_line_text_"+random_id).insertBefore(jQuery("#field_label_" + random_id).addClass("field_label").addClass("control-label"));
											jQuery("#ux_txt_singal_line_text_"+random_id).css("margin-left","9px")
											jQuery("#ux_txt_logical_captcha_"+random_id).insertBefore(jQuery("#field_label_" + random_id).addClass("field_label").addClass("control-label"));
										}
										jQuery("#ux_text_appear_after_counter_" + random_id).css({"position": "absolute", "margin-top":"3%","margin-left":"-8px"});
										jQuery("#ux_sub_div_" + random_id).addClass("field_label").addClass("control-label").css("padding-bottom","50px");
										break;
									case "left":
										jQuery("#field_label_" + random_id).css("display", "");
										if(jQuery("#ux_control_type_"+random_id).val() === "radio-list" || jQuery("#ux_control_type_"+random_id).val() === "checkbox-list") {
											jQuery("#ux_txt_check_box_"+random_id).appendTo("#field_label_" + random_id);
											jQuery("#ux_label_title_" + random_id).css({"vertical-align":"middle"});
										}
										else
										{
											jQuery("#ux_txt_singal_line_text_"+random_id).appendTo("#field_label_" + random_id);
											jQuery("#ux_txt_logical_captcha_"+random_id).appendTo("#field_label_" + random_id);
										}
										jQuery("#ux_text_appear_after_counter_" + random_id).css({"position": "relative", "margin-top": "", "margin-left": "12%"});
										jQuery("#ux_txt_singal_line_text_" + random_id).css({"display":"inline-block","margin-left":"0px"});
										jQuery("#ux_sub_div_" + random_id).addClass("field_label").addClass("control-label");
										break;
									case "right":
										jQuery("#field_label_" + random_id).css("display", "");
										if(jQuery("#ux_control_type_"+random_id).val() === "radio-list" || jQuery("#ux_control_type_"+random_id).val() === "checkbox-list") {
											jQuery("#ux_txt_check_box_"+random_id).prependTo("#field_label_" + random_id);
											jQuery("#ux_label_title_" + random_id+",#ux_tooltip_title_" + random_id).css({"vertical-align":"middle"});
										}
										else
										{
											jQuery("#ux_txt_singal_line_text_"+random_id).prependTo("#field_label_" + random_id);
											jQuery("#ux_txt_logical_captcha_"+random_id).prependTo("#field_label_" + random_id);
										}
										jQuery("#ux_text_appear_after_counter_" + random_id).css({"position": "", "margin-top": "", "margin-left": ""});
										jQuery("#ux_txt_singal_line_text_" + random_id).css({"display":"inline-block","margin-left":"0px"});
										jQuery("#ux_sub_div_" + random_id).addClass("field_label").addClass("control-label");
										break;
									case "hidden":
										jQuery("#ux_text_appear_after_counter_" + random_id).css({"position": "", "margin-top": "", "margin-left": ""});
										if(jQuery("#ux_control_type_"+random_id).val() != "star_rating") {
											jQuery("#ux_txt_singal_line_text_" + random_id).css({"display":"block","margin-left":"9px"});
										}
										if(jQuery("#ux_control_type_"+random_id).val() === "radio-list" || jQuery("#ux_control_type_"+random_id).val() === "checkbox-list") {
											jQuery("#ux_txt_check_box_"+random_id).insertAfter("#field_label_" + random_id);
										}
										else
										{
											jQuery("#ux_txt_singal_line_text_"+random_id).insertAfter("#field_label_" + random_id);
											jQuery("#ux_txt_logical_captcha_"+random_id).insertAfter("#field_label_" + random_id);
										}
										jQuery("#field_label_" + random_id).css("display", "none");
										jQuery("#ux_sub_div_" + random_id).addClass("field_label").addClass("control-label");
										break;
								}
							}
							function contact_bank_sort_timestamp()
							{
								contact_bank_control_ids = [];
								setTimeout(function () {
									jQuery("#sortable").find(".result_hover").each(function(){
											var timestamp = jQuery(this).attr("data-timestamp");
											contact_bank_control_ids.push(parseInt(timestamp));
										});
									}, 100);
							}
							jQuery(document).ready(function () {
								var form_redirect_page_url = "<?php echo isset( $form_unserialized_meta_value['form_redirect_page_url'] ) ? esc_attr( $form_unserialized_meta_value['form_redirect_page_url'] ) : esc_url( site_url() ); ?>";
								jQuery("#ux_ddl_save_submission_to_db").val("<?php echo( isset( $form_unserialized_meta_value['form_save_submission_to_db'] ) ) ? esc_attr( $form_unserialized_meta_value['form_save_submission_to_db'] ) : 'enable'; ?>");
								jQuery("#ux_ddl_submission_limit_message").val("<?php echo( isset( $form_unserialized_meta_value['form_submission_limit_message'] ) ) ? esc_attr( $form_unserialized_meta_value['form_submission_limit_message'] ) : 'enable'; ?>");
								jQuery("#ux_ddl_redirect_type").val("<?php echo( isset( $form_unserialized_meta_value['form_redirect'] ) ) ? esc_attr( $form_unserialized_meta_value['form_redirect'] ) : 'page'; ?>");
								jQuery("#ux_ddl_enable_tooltip").val("<?php echo( isset( $form_unserialized_meta_value['form_enable_tooltip'] ) ) ? esc_attr( $form_unserialized_meta_value['form_enable_tooltip'] ) : 'show'; ?>");
								if(form_redirect_page_url != "")
								{
									jQuery("#ux_ddl_redirect_page").val("<?php echo isset( $form_unserialized_meta_value['form_redirect_page_url'] ) ? esc_attr( $form_unserialized_meta_value['form_redirect_page_url'] ) : ''; ?>");
								}
								show_hide_submission_message_contact_bank();
								<?php
								if ( isset( $_REQUEST['mode'] ) && sanitize_text_field( wp_unslash( $_REQUEST['mode'] ) ) === 'edit' ) {// WPCS: input var ok, CSRF ok.
									?>
										if(jQuery(".template-contact-bank").hasClass("cb-active")) {
											jQuery("#ux_div_first_step").removeClass("first-step-helper");
											jQuery("#ux_div_first_step").css("display", "none");
											jQuery("#contact_bank_confirm").css("display", "none");
											jQuery("#ux_div_second_step").css("display", "block");
											jQuery("#ux_div_step_progres_bar_width").css("width", "100%");
											jQuery("#ux_div_frm_wizard li:eq(1)").addClass("active");
											jQuery("#ux_div_frm_wizard li:eq(2)").removeClass("active");
											jQuery("#ux_btn_previsious_step_first").css("display", "none");
										}
									<?php
								}
								?>
								show_hide_redirect_controls_contact_bank();
								jQuery(".user_info_fields,.pricing_fields,.layout_fields,.security_fields,.miscellaneous_fields").slideUp();
								jQuery(".common_fields_cb, .common_fields_cb_pro, .user_info_fields, .user_info_fields_pro, .pricing_fields, .layout_fields, .security_fields, .miscellaneous_fields").slideDown();
								jQuery(".contact_bank_draggable").draggable({
									cancel: "a.ui-icon",
									revert: true,
									helper: "clone",
									cursor: "move",
									revertDuration: 0
								});
								jQuery('.droppable').droppable({
									accept: ".contact_bank_draggable,.result_hover",
									activeClass: "ui-state-highlight",
									drop: function (event, ui) {
										var draggableId = ui.draggable.attr("data-timestamp");
										if(draggableId === undefined)
										{
											var draggableId = ui.draggable.attr("id");
											contact_bank_field_fill(draggableId);
										}
										else
										{
											contact_bank_sort_timestamp();
										}
									}
								});
								jQuery("#sortable").sortable({});
								jQuery("#sortable").disableSelection();
								jQuery(".ux_div_widget_content").hide();
								jQuery("#sortable_available, #sortable_selected").sortable({connectWith: '.sortable_connected', placeholder: 'placeholder'});
						<?php
						if ( count( $form_unserialized_meta_value['controls'] ) > 0 ) {
							foreach ( $form_unserialized_meta_value['controls'] as $controls ) {
								?>
										var timestamp = <?php echo isset( $controls['timestamp'] ) ? esc_attr( $controls['timestamp'] ) : ''; ?>;
										var control_name = '<?php echo isset( $controls['control_type'] ) ? esc_attr( $controls['control_type'] ) : ''; ?>';
										var html_control_type = '<?php echo isset( $controls['html_editor_type'] ) ? esc_attr( $controls['html_editor_type'] ) : ''; ?>';
										jQuery("#ux_ddl_required_"+timestamp).val("<?php echo isset( $controls['required_type'] ) ? esc_attr( $controls['required_type'] ) : ''; ?>");
										jQuery("#ux_ddl_limit_input_"+timestamp).val("<?php echo isset( $controls['input_validation_type'] ) ? esc_attr( $controls['input_validation_type'] ) : ''; ?>");
										jQuery("#ux_ddl_label_placement_"+timestamp).val("<?php echo( isset( $controls['label_placement'] ) ) ? esc_attr( $controls['label_placement'] ) : ''; ?>");
										jQuery("#ux_ddl_mathmatical_operations_"+timestamp).val("<?php echo( isset( $controls['logical_captcha_mathmatical_operations'] ) ) ? esc_attr( $controls['logical_captcha_mathmatical_operations'] ) : ''; ?>");
										jQuery("#ux_ddl_default_current_date_"+timestamp).val("<?php echo( isset( $controls['default_current_date'] ) ) ? esc_attr( $controls['default_current_date'] ) : ''; ?>");
										jQuery("#ux_ddl_time_format_"+timestamp).val("<?php echo( isset( $controls['time_format'] ) ) ? esc_attr( $controls['time_format'] ) : ''; ?>");
										jQuery("#ux_ddl_date_format_"+timestamp).val("<?php echo isset( $controls['date_format'] ) ? esc_attr( $controls['date_format'] ) : ''; ?>");
										jQuery("#ux_ddl_product_"+timestamp).val("<?php echo isset( $controls['product_name'] ) ? esc_attr( $controls['product_name'] ) : ''; ?>");
										jQuery("#ux_ddl_default_current_time_"+timestamp).val("<?php echo( isset( $controls['current_time'] ) ) ? esc_attr( $controls['current_time'] ) : ''; ?>");
										jQuery("#ux_ddl_multiple_upload_"+timestamp).val("<?php echo( isset( $controls['multiple_upload'] ) ) ? esc_attr( $controls['multiple_upload'] ) : ''; ?>");
										jQuery("#ux_ddl_attach_email_"+timestamp).val("<?php echo( isset( $controls['attach_to_email'] ) ) ? esc_attr( $controls['attach_to_email'] ) : ''; ?>");
										jQuery("#ux_ddl_required_"+timestamp).val("<?php echo( isset( $controls['required_type'] ) ) ? esc_attr( $controls['required_type'] ) : ''; ?>");
										jQuery("#ux_ddl_autocomplete_"+timestamp).val("<?php echo( isset( $controls['autocomplete_type'] ) ) ? esc_attr( $controls['autocomplete_type'] ) : ''; ?>");
										jQuery("#ux_ddl_disable_input_"+timestamp).val("<?php echo( isset( $controls['disable_input'] ) ) ? esc_attr( $controls['disable_input'] ) : ''; ?>");
										jQuery("#ux_ddl_input_mask_"+timestamp).val("<?php echo( isset( $controls['input_mask_type'] ) ) ? esc_attr( $controls['input_mask_type'] ) : ''; ?>");
										var mathematical_operation_type = '<?php echo isset( $values['logical_captcha_mathmatical_operations'] ) ? $values['logical_captcha_mathmatical_operations'] : '';// WPCS: XSS ok. ?>';
										contact_bank_control_ids.push(timestamp);
										change_label_placement_contact_bank("ux_ddl_label_placement_"+timestamp, timestamp);
										apply_input_masking_contact_bank("ux_txt_singal_line_text_" + timestamp, "ux_ddl_input_mask_" + timestamp, "ux_div_custom_mask_settings_" + timestamp, timestamp);
										if(control_name === "select" || control_name === "checkbox-list" || control_name === "radio-list")
										{
											var arr = [], $select = jQuery("#ux_ddl_options_required_" + timestamp);
											$select.find("option").each(function() {
												arr[arr.length] = { text: this.text, value: this.value };
											});
											jQuery("#ux_hidden_options_values_" + timestamp).val(JSON.stringify(arr));
											if(control_name === "select")
											{
												jQuery("#ux_txt_default_value_" + timestamp).val("<?php echo isset( $controls['default_value'] ) ? esc_attr( $controls['default_value'] ) : ''; ?>");
												jQuery("#ux_txt_singal_line_text_" + timestamp).val("<?php echo isset( $controls['default_value'] ) ? esc_attr( $controls['default_value'] ) : ''; ?>");
												drag_drop_radio_button_contact_bank("select")
											}
											control_name === "checkbox-list" ? drag_drop_radio_button_contact_bank("checkbox") : (control_name === "radio-list" ? drag_drop_radio_button_contact_bank("radio") : "");
										}
										<?php
							}
						}
								?>
							});
							// Toggle div
							function show_hide_text_field_options(random_id) {
								jQuery("#ux_div_widget_content_" + random_id).animate({
									height: 'toggle'
								});
								var sidebar_load_interval = setInterval(load_sidebar_content_contact_bank, 1000);
								setTimeout(function () {
									clearInterval(sidebar_load_interval);
								}, 5000);
							}
							function delete_select_options_contact_bank(dynamic_id, dynamicId) {
								var value = jQuery("#ux_txt_ddl_value_" + dynamic_id).val();
								var confirm_delete = confirm(<?php echo wp_json_encode( $cb_confirm_data ); ?>);
								if(confirm_delete === true)
								{
									jQuery("#ux_div_full_control_radio_"+dynamic_id).remove();
									jQuery("#ux_txt_singal_line_text_"+dynamicId + " option[value=\"" + value + "\"]").remove();
									jQuery("#ux_ddl_options_required_"+dynamicId + " option[value=\"" + value + "\"]").remove();
									jQuery("#ux_txt_default_value_"+dynamicId + " option[value=\"" + value + "\"]").remove();

									var arr = [], $select = jQuery("#ux_ddl_options_required_" + dynamicId);
									$select.find("option").each(function() {
										arr[arr.length] = { text: this.text, value: this.value  };
									});
									jQuery("#ux_hidden_options_values_" + dynamicId).val(JSON.stringify(arr));
									if (jQuery("#ux_ddl_options_required_"+dynamicId).val() === null) {
										jQuery("#ux_drop_down_value_" + dynamicId).css("display", "none");
									}
								}
							}
							function select_option_value_change_contact_bank(dynamicId)
							{
								var arr = [];
								var line = "";
								var element_class = jQuery("#ux_txt_element_class_"+dynamicId).val();
								jQuery("#ux_ddl_options_required_"+dynamicId).empty();
								jQuery(".sub_div").find("#field_labels_"+dynamicId).each(function(){
									jQuery(this).children("#ux_txt_singal_line_text_"+dynamicId).remove();
								});
								jQuery("#ux_div_append_input_radio_" + dynamicId).find("div").each(function() {
									var options = jQuery(this).children("input:eq(1)").val();
									var values = jQuery(this).children("input:eq(2)").val();
									line += options+"^"+values+";";
									arr[arr.length] = { text: options , value: values };
									jQuery("#ux_txt_singal_line_text_"+dynamicId).attr("value", values).text(options);
								});
								var lines = line.split(";");
								for (var i=0; i < lines.length; i++) {
									if (/\S/.test(lines[i])) {
									var value = lines[i].split("^");
									jQuery("#ux_ddl_options_required_" + dynamicId).append("<option value=\"" + value[1] + "\">" + value[0] + "</option>");
									jQuery("#ux_txt_singal_line_text_" + dynamicId).append("<option value=\"" + value[1] + "\">" + value[0] + "</option>");
									jQuery("#ux_txt_default_value_" + dynamicId).append("<option value=\"" + value[1] + "\">" + value[0] + "</option>");
									}
								}
								jQuery("#ux_hidden_options_values_" + dynamicId).val(JSON.stringify(arr));
							}
							function add_select_options_contact_bank(dynamicId, type) {
								var ddl_options = jQuery("#ux_txt_add_form_option_" + dynamicId).val();
								var ddl_values = jQuery("#ux_txt_add_form_values_"+dynamicId).val();
								if (ddl_options === "" && ddl_values === "") {
									var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
									toastr[shortCutFunction](<?php echo wp_json_encode( $cb_add_fill_option_value ); ?>);
								} else if(ddl_options !== "" && ddl_values === "") {
									var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
									toastr[shortCutFunction](<?php echo wp_json_encode( $cb_add_fill_option_value ); ?>);
								} else if(ddl_options === "" && ddl_values !== "") {
									var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
									toastr[shortCutFunction](<?php echo wp_json_encode( $cb_add_fill_option_value ); ?>);
								} else {
									id++;
									var dynamic_id = dynamicId+"_"+id;
									jQuery("#ux_drop_down_value_" + dynamicId).append("<div id=ux_div_append_input_radio_"+dynamicId+" class=append_input_radio_"+dynamicId+">");
									jQuery("#ux_div_append_input_radio_" + dynamicId).css("margin-top", "10px");
									jQuery("#ux_div_append_input_radio_" + dynamicId).append("<div id=ux_div_full_control_radio_"+dynamic_id+" class=full_control_radio_"+dynamicId+"><input type=radio id=ux_txt_radio_add_button_"+dynamic_id+" name=ux_txt_radio_add_button_"+dynamicId+" style='margin-right:8px;' class=radio_add_button_"+dynamicId+"><input type=text style='margin-left:2px;' id=ux_txt_option_value_"+dynamic_id+" class=txt_option_value_"+dynamicId+" value=\"" + ddl_options + "\"><input type=text style='margin-left:3px;' id=ux_txt_ddl_value_"+dynamic_id+" class=txt_ddl_value_"+dynamicId+" value=\"" + ddl_values + "\"><i class=icon-custom-minus id=ux_btn_delete_option_"+dynamic_id+"></i></div>");
									jQuery("#ux_btn_delete_option_" +dynamic_id).addClass("cb-radio-minus");
									jQuery("#ux_div_full_control_radio_"+dynamic_id).addClass("radio-drag").css("margin-bottom","5px");
									jQuery("#ux_btn_delete_option_"+dynamic_id).attr("onclick", "delete_select_options_contact_bank('"+ dynamic_id + "','" + dynamicId + "')").css("margin-left", "9px");
									jQuery("#ux_btn_delete_option_"+dynamic_id).addClass("cb-radio-minus");

									jQuery(".txt_option_value_"+dynamicId).attr("onchange", "select_option_value_change_contact_bank('"+ dynamicId + "')");
									jQuery(".txt_ddl_value_"+dynamicId).attr("onchange", "select_option_value_change_contact_bank('"+ dynamicId + "')");

									jQuery("#ux_ddl_options_required_" + dynamicId).append("<option value=\"" + ddl_values + "\">" + ddl_options + "</option>");
									jQuery("#ux_txt_singal_line_text_" + dynamicId).append("<option value=\"" + ddl_values + "\">" + ddl_options + "</option>");
									jQuery("#ux_txt_default_value_" + dynamicId).append("<option value=\"" + ddl_values + "\">" + ddl_options + "</option>");
									jQuery("#ux_drop_down_value_" + dynamicId).css("display", "");
									jQuery("#ux_txt_add_form_option_"+dynamicId).val("");
									jQuery("#ux_txt_add_form_values_"+dynamicId).val("");
									jQuery("#ux_ddl_options_required_" + dynamicId).hide();
									var arr = [], $select = jQuery("#ux_ddl_options_required_" + dynamicId);
									$select.find("option").each(function() {
										arr[arr.length] = { text: this.text, value: this.value  };
									});
									jQuery("#ux_hidden_options_values_" + dynamicId).val(JSON.stringify(arr));

									var arr = [], $select = jQuery("#ux_ddl_options_required_" + dynamicId);
									$select.find("option").each(function() {
										arr[arr.length] = { text: this.text, value: this.value };
									});
									jQuery("#ux_hidden_options_values_" + dynamicId).val(JSON.stringify(arr));
									if(type == "select")
									{
										drag_drop_radio_button_contact_bank("select");
									}
								}
							}
							function import_select_options_contact_bank(dynamicId, type) {
								var lines = jQuery("#ux_txt_textarea_"+dynamicId).val().split(/\n/);
								if(lines != "") {
									for (var i=0; i < lines.length; i++) {
										if (/\S/.test(lines[i])) {
										var value = lines[i].split(",");
										id++;
										var dynamic_id = dynamicId+"_"+id;
										if(value[1] !== undefined) {
											jQuery("#ux_ddl_options_required_" + dynamicId).append("<option value=\"" + value[1] + "\">" + value[0] + "</option>");
											jQuery("#ux_ddl_options_required_" + dynamicId).hide();
											jQuery("#ux_drop_down_value_" + dynamicId).append("<div id=ux_div_append_input_radio_"+dynamicId+" class=append_input_radio_"+dynamicId+">");
											jQuery("#ux_div_append_input_radio_" + dynamicId).css("margin-top", "10px");
											jQuery("#ux_div_append_input_radio_" + dynamicId).append("<div id=ux_div_full_control_radio_"+dynamic_id+" class=full_control_radio_"+dynamicId+"><input type=radio id=ux_txt_radio_add_button_"+dynamic_id+" style='margin-left:1px' name=ux_txt_radio_add_button_"+dynamicId+" style='margin-right:8px;'  class=radio_add_button_"+dynamicId+"><input type=text style='margin-left:4px;' id=ux_txt_option_value_"+dynamic_id+" style='margin-left:4px' class=txt_option_value_"+dynamicId+" value=\"" + value[0] + "\"><input type=text style='margin-left:3px;' id=ux_txt_ddl_value_"+dynamic_id+" class=txt_ddl_value_"+dynamicId+" style='margin-left:4px' value=\"" + value[1] + "\"><i class=icon-custom-minus id=ux_btn_delete_option_"+dynamic_id+"></i></div>");
											jQuery("#ux_btn_delete_option_" +dynamic_id).addClass("cb-radio-minus");
											jQuery("#ux_div_full_control_radio_"+dynamic_id).addClass("radio-drag").css("margin-bottom","5px");
											jQuery("#ux_btn_delete_option_"+dynamic_id).attr("onclick", "delete_radio_options_contact_bank('"+ dynamic_id + "','" + dynamicId + "')").css("margin-left", "9px");
											jQuery("#ux_btn_delete_option_"+dynamic_id).addClass("cb-radio-minus");

											jQuery("#ux_txt_singal_line_text_" + dynamicId).append("<option value=\"" + value[1] + "\">" + value[0] + "</option>");
											jQuery("#ux_txt_default_value_" + dynamicId).append("<option value=\"" + value[1] + "\">" + value[0] + "</option>");
										} else {
											jQuery("#ux_ddl_options_required_" + dynamicId).append("<option value=\"" + value[0] + "\">" + value[0] + "</option>");
											jQuery("#ux_ddl_options_required_" + dynamicId).hide();
											jQuery("#ux_drop_down_value_" + dynamicId).append("<div id=ux_div_append_input_radio_"+dynamicId+" class=append_input_radio_"+dynamicId+">");
											jQuery("#ux_div_append_input_radio_" + dynamicId).css("margin-top", "10px");
											jQuery("#ux_div_append_input_radio_" + dynamicId).append("<div id=ux_div_full_control_radio_"+dynamic_id+" class=full_control_radio_"+dynamicId+"><input type=radio id=ux_txt_radio_add_button_"+dynamic_id+" style='margin-left:1px' name=ux_txt_radio_add_button_"+dynamicId+" style='margin-right:8px;'  class=radio_add_button_"+dynamicId+"><input type=text style='margin-left:4px;' id=ux_txt_option_value_"+dynamic_id+" style='margin-left:4px' class=txt_option_value_"+dynamicId+" value=\"" + value[0] + "\"><input type=text style='margin-left:3px;' id=ux_txt_ddl_value_"+dynamic_id+" class=txt_ddl_value_"+dynamicId+" style='margin-left:4px' value=\"" + value[0] + "\"><i class=icon-custom-minus id=ux_btn_delete_option_"+dynamic_id+"></i></div>");
											jQuery("#ux_btn_delete_option_" +dynamic_id).addClass("cb-radio-minus");
											jQuery("#ux_div_full_control_radio_"+dynamic_id).addClass("radio-drag").css("margin-bottom","5px");
											jQuery("#ux_btn_delete_option_"+dynamic_id).attr("onclick", "delete_radio_options_contact_bank('"+ dynamic_id + "','" + dynamicId + "')").css("margin-left", "9px");
											jQuery("#ux_btn_delete_option_"+dynamic_id).addClass("cb-radio-minus");

											jQuery("#ux_txt_singal_line_text_" + dynamicId).append("<option value=\"" + value[0] + "\">" + value[0] + "</option>");
											jQuery("#ux_txt_default_value_" + dynamicId).append("<option value=\"" + value[0] + "\">" + value[0] + "</option>");
										}
										}
									}
									jQuery("#ux_txt_textarea_"+dynamicId).val("");
									var arr = [], $select = jQuery("#ux_ddl_options_required_" + dynamicId);
										$select.find("option").each(function() {
											arr[arr.length] = { text: this.text, value: this.value };
									});
									jQuery("#ux_hidden_options_values_" + dynamicId).val(JSON.stringify(arr));
									jQuery("#ux_drop_down_value_" + dynamicId).css("display", "block");
								}
								var targeted_popup_class = "ux_open_popup_translator_"+dynamicId
								jQuery('[data-popup="' + targeted_popup_class + '"]').fadeOut(350);
								if(type == "select")
								{
									drag_drop_radio_button_contact_bank("select");
								}
							}
							function contact_bank_open_popup(random_id) {
								var targeted_popup_class = "ux_open_popup_translator_"+random_id;
								jQuery('[data-popup="' + targeted_popup_class + '"]').fadeIn(350);
							}
							function contact_bank_close_popup_box(random_id) {
								var confirm_close = confirm(<?php echo wp_json_encode( $cb_confirm_data ); ?>);
								if (confirm_close === true) {
									var targeted_popup_class = "ux_open_popup_translator_"+random_id;
									jQuery('[data-popup="' + targeted_popup_class + '"]').fadeOut(350);
								}
							}
							function set_default_value_contact_bank(dynamicId) {
								var drop_down_value = jQuery("#ux_txt_default_value_"+dynamicId).val();
								jQuery("#ux_txt_singal_line_text_" + dynamicId).val(drop_down_value);
							}
							function delete_controls_contact_bank(control, random_id) {
								var confirm_delete = confirm(<?php echo wp_json_encode( $cb_confirm_data ); ?>);
								if (confirm_delete === true) {
									contact_bank_control_ids.splice(jQuery.inArray(random_id, contact_bank_control_ids), 1);
									jQuery("#" + control).remove();
								}
							}
							function change_label_name_contact_bank(label_id, value) {
								jQuery("#" + label_id).text(value);
							}
							function select_all_content_contact_bank(event, id) {
								if (event.keyCode === 65 && event.ctrlKey) {
									jQuery("#" + id).select();
								}
							}
							function change_tootltip_content_contact_bank(label_id, value) {
								jQuery("#" + label_id).attr("data-original-title", value);
							}
							function change_placeholder_content_contact_bank(id, value) {
								jQuery("#" + id).attr("placeholder", value);
							}
							function control_default_value_contact_bank(id, value) {
								jQuery("#" + id).attr("value", value);
							}
							function append_class_contact_bank(id, value, untitled_class, field_class, control_label_class, random_id, type) {
								if((jQuery("#" + id).hasClass("field_label") && jQuery("#" + id).hasClass("control-label")) || jQuery("#" + id).hasClass("hasDatepicker")) {
									jQuery("#" + id).attr("class", value).addClass(untitled_class).addClass(field_class).addClass(control_label_class);
								} else {
									if(type != "radio-list" && type != "checkbox-list")
									{
										jQuery("#" + id).attr("class", value).addClass(untitled_class);
									} else {

										jQuery(".checkbox_class_" + random_id).attr("class", value).addClass(untitled_class);
									}
								}
							}
							function enable_disable_required_contact_bank(id, required_id) {
								var type = jQuery("#" + id).val();
								switch (type) {
									case "enable":
										jQuery("#" + required_id).css("display", "");
										break;
									case "disable":
										jQuery("#" + required_id).css("display", "none");
										break;
								}
							}
							function enable_disable_autocomplete_contact_bank(input_id, id) {
								var type = jQuery("#" + id).val();
								switch (type) {
									case "enable":
										jQuery("#" + input_id).attr("autocomplete", "off");
										break;
									case "disable":
										jQuery("#" + input_id).attr("autocomplete", "on");
										break;
								}
							}
							function disable_fields_contact_bank(input_id, id) {
								var type = jQuery("#" + id).val();
								switch (type) {
									case "enable":
										jQuery("#" + input_id).attr("disabled", "disabled");
										break;
									case "disable":
										jQuery("#" + input_id).removeAttr("disabled");
										break;
								}
							}
							function apply_input_masking_contact_bank(input_id, id, custom_id, random_id) {
								var input_mask_type = jQuery("#" + id).val();
								switch (input_mask_type) {
									case "none":
										jQuery("#ux_txt_singal_line_text_" + random_id).unmask();
										jQuery("#" + custom_id).css("display", "none");
										break;
									case "us_phone":
										jQuery("#" + custom_id).css("display", "none");
										jQuery("#ux_txt_singal_line_text_" + random_id).unmask();
										jQuery("#ux_txt_singal_line_text_" + random_id).mask("(999)999-9999");
										break;
									case "date":
										jQuery("#" + custom_id).css("display", "none");
										jQuery("#ux_txt_singal_line_text_" + random_id).unmask();
										jQuery("#ux_txt_singal_line_text_" + random_id).mask("99/99/9999");
										break;
									case "custom":
										jQuery("#ux_txt_singal_line_text_" + random_id).unmask();
										var custom_mask_value = jQuery("#ux_txt_custom_mask_" + random_id).val();
										jQuery("#ux_txt_singal_line_text_" + random_id).mask(custom_mask_value);
										jQuery("#" + custom_id).css("display", "block");
										break;
								}
							}
							function change_error_message_content_contact_bank(input_id, value) {
								jQuery("#" + input_id).text(value).addClass("field_label");
							}
							function limit_input_event_contact_bank(random_id) {
								var type = jQuery("#ux_ddl_limit_input_" + random_id).val();
								switch (type) {
									case "characters":
										jQuery("#ux_txt_singal_line_text_" + random_id).removeAttr("onkeypress");
										jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeyup", "only_characters_contact_bank(event," + random_id + ");");
										break;
									case "digits":
										jQuery("#ux_txt_singal_line_text_" + random_id).removeAttr("onkeyup");
										jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeypress", "only_digits_contact_bank(event," + random_id + ");");
										break;
								}
							}
							function number_settings_contact_bank(random_id,event) {
								var step_number_cb = parseInt(jQuery("#ux_txt_step_"+random_id).val());
								var count = 0;
								var step_count = 0;
								var min_number = parseInt(jQuery("#ux_txt_min_number_"+random_id).val());
								var max_number = parseInt(jQuery("#ux_txt_max_number_"+random_id).val());
								var input_number = parseInt(jQuery("#ux_txt_singal_line_text_"+random_id).val());
								jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");
								if (min_number !== "" && max_number !== "" && jQuery("#ux_txt_singal_line_text_"+random_id).val() != "") {
									if((input_number >= min_number) && (input_number <= max_number))
									{
										jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");
									}
									else
									{
										count = 1;
									}
								}
								if(input_number  % step_number_cb !== 0 && step_number_cb !== "") {
									step_count = 1;
								}
								if(count === 1 && step_count === 1) {
									jQuery("#ux_text_appear_after_counter_"+random_id).css("display","block").html(<?php echo wp_json_encode( $cb_number_enter_between_message ); ?> +min_number+" and "+max_number+  <?php echo wp_json_encode( $cb_number_increment_by_message ); ?> + step_number_cb).addClass("field_label");
								}
								else if(step_count === 1) {
									jQuery("#ux_text_appear_after_counter_"+random_id).css("display","block").html(<?php echo wp_json_encode( $cb_number_increment_by_message ); ?> + step_number_cb).addClass("field_label");
								} else if(count === 1) {
									jQuery("#ux_text_appear_after_counter_"+random_id).css("display","block").html(<?php echo wp_json_encode( $cb_number_enter_between_message ); ?>+min_number+" and "+max_number+"").addClass("field_label");
								}
								if(jQuery("#ux_txt_singal_line_text_"+random_id).val() === "") {
									jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");
								}
							}
							function duplicate_fields_contact_bank(type, last_random_id) {
								var confirm_duplicate = confirm(<?php echo wp_json_encode( $cb_confirm_data ); ?>);
								if (confirm_duplicate === true) {
									var random_id = new Date().getTime();
									var last_random_id_index = contact_bank_control_ids.indexOf(last_random_id);
									var random_id_index = parseInt(last_random_id_index)+1;
									contact_bank_control_ids.splice(random_id_index, 0, random_id);
									switch (type) {
										case "text":
											jQuery("#ux_div_single_line_text_" + last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id).attr("name", "ux_div_widget_" + random_id);
											jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("text");
											jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('text'," + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");
											jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id);
											jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
											jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
											jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#ux_sub_div_" + random_id).find("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");
											jQuery("#ux_sub_div_" + random_id).find("input").attr("name", "ux_txt_singal_line_text_" + random_id);
											var validation_type = jQuery("#ux_ddl_limit_input_" + last_random_id).val();
											if (validation_type === "digits") {
												jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeypress", "only_digits_contact_bank(event," + random_id + ");");
											} else {
												jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeyup", "only_characters_contact_bank(event," + random_id + ");");
											}
											jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
											jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
											jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);

											jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "#ux_control_label_placeholder_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("name", "ux_txt_label_field_" + random_id).attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)");
											jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "#ux_control_label_description_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("name", "ux_txt_description_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
											jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).val(jQuery("#ux_ddl_label_placement_" + last_random_id).val()).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")").attr("name", "ux_ddl_label_placement_" + random_id);
											jQuery("#general_" + random_id).find(".date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings,.html_editor,.logical_captcha_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
											jQuery("#apperance_" + random_id).find(".placeholder_settings").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');").attr("name", "ux_txt_custom_validation_field_" + random_id);
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".rows_number,.card_number_placeholder_settings, .expiry_date_placeholder_settings, .card_cvv_number_placeholder_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
											jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id).val(jQuery("#ux_ddl_required_" + last_random_id).val());
											jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("input").attr("name", "ux_txt_limit_input_" + random_id).attr("id", "ux_txt_limit_input_" + random_id).attr("onkeypress","enter_only_digits_for_price(event)").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_limit_input_" + random_id + "');");
											jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("select").attr("name", "ux_ddl_limit_input_" + random_id).attr("id", "ux_ddl_limit_input_" + random_id).val(jQuery("#ux_ddl_limit_input_" + last_random_id).val()).attr("onchange", "limit_input_event_contact_bank(" + random_id + ");");
											jQuery("#restriction_" + random_id).find(".text_appear_settings").children("input").attr("id", "ux_txt_text_appear_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_text_appear_" + random_id + "');").attr("name", "ux_txt_text_appear_" + random_id).attr("onkeyup", "change_error_message_content_contact_bank('ux_text_appear_after_counter_" + random_id + "',this.value);");
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).val(jQuery("#ux_ddl_autocomplete_" + last_random_id).val()).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');").attr("name", "ux_ddl_autocomplete_" + random_id);
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("name", "ux_ddl_disable_input_" + random_id).attr("id", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").val(jQuery("#ux_ddl_disable_input_" + last_random_id).val());
											jQuery("#restriction_" + random_id).find(".custom_mask_settings").attr("id", "ux_div_custom_mask_settings_" + random_id).attr("name", "ux_div_custom_mask_settings_" + random_id);
											jQuery("#restriction_" + random_id).find(".custom_mask_settings").children("input").attr("id", "ux_txt_custom_mask_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_mask_" + random_id + "');").attr("name", "ux_txt_custom_mask_" + random_id).attr("onblur", "apply_input_masking_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_input_mask_" + random_id + "','ux_div_custom_mask_settings_" + random_id + "'," + random_id + ");");
											jQuery("#restriction_" + random_id).find(".input_mask_settings").children("select").attr("id", "ux_ddl_input_mask_" + random_id).val(jQuery("#ux_ddl_input_mask_" + last_random_id).val()).attr("onchange", "apply_input_masking_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_input_mask_" + random_id + "','ux_div_custom_mask_settings_" + random_id + "'," + random_id + ");").attr("name", "ux_ddl_input_mask_" + random_id);
											if(jQuery("#ux_ddl_input_mask_"+random_id).val() != "custom") {
												jQuery("#restriction_" + random_id).find(".custom_mask_settings").css("display", "none");
											}
											jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "single_line_text_field_key_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("name", "ux_txt_default_value_" + random_id).attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
											break;
										case "paragraph":
											jQuery("#ux_div_single_line_text_" + last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id).attr("name", "ux_div_widget_" + random_id);
											jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("paragraph");
											jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('paragraph'," + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");
											jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id);
											jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
											jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
											jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#ux_sub_div_" + random_id).find("textarea").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");
											jQuery("#ux_txt_singal_line_text_" + random_id).css("vertical-align","middle");
											jQuery("#ux_sub_div_" + random_id).find("textarea").attr("name", "ux_txt_singal_line_text_" + random_id);
											var validation_type = jQuery("#ux_ddl_limit_input_" + last_random_id).val();
											if (validation_type === "digits") {
												jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeypress", "only_digits_contact_bank(event," + random_id + ");");
											} else {
												jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeyup", "only_characters_contact_bank(event," + random_id + ");");
											}
											jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
											jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
											jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);

											jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("name", "ux_txt_label_field_" + random_id).attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)");
											jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("name", "ux_txt_description_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
											jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).val(jQuery("#ux_ddl_label_placement_" + last_random_id).val()).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")").attr("name", "ux_ddl_label_placement_" + random_id);
											jQuery("#general_" + random_id).find(".date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings,.html_editor,.logical_captcha_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
											jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');").attr("name", "ux_txt_custom_validation_field_" + random_id);
											jQuery("#apperance_" + random_id).find(".rows_number").children("input").attr("id", "ux_txt_no_of_rows_" + random_id).attr("name", "ux_txt_no_of_rows_" + random_id).attr("onkeyup","change_textarea_rows_contact_bank("+random_id+");").val(jQuery("#ux_txt_no_of_rows_"+random_id)).val(jQuery("#ux_txt_no_of_rows_"+last_random_id).val());
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
											jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id).val(jQuery("#ux_ddl_required_" + last_random_id).val());
											jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("input").attr("name", "ux_txt_limit_input_" + random_id).attr("id", "ux_txt_limit_input_" + random_id).attr("onkeypress","enter_only_digits_for_price(event)").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_limit_input_" + random_id + "');");
											jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("select").attr("name", "ux_ddl_limit_input_" + random_id).attr("id", "ux_ddl_limit_input_" + random_id).val(jQuery("#ux_ddl_limit_input_" + last_random_id).val()).attr("onchange", "limit_input_event_contact_bank(" + random_id + ");");
											jQuery("#restriction_" + random_id).find(".text_appear_settings").children("input").attr("id", "ux_txt_text_appear_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_text_appear_" + random_id + "');").attr("name", "ux_txt_text_appear_" + random_id).attr("onkeyup", "change_error_message_content_contact_bank('ux_text_appear_after_counter_" + random_id + "',this.value);");
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).val(jQuery("#ux_ddl_autocomplete_" + last_random_id).val()).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');").attr("name", "ux_ddl_autocomplete_" + random_id);
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").attr("name", "ux_ddl_disable_input_" + random_id).val(jQuery("#ux_ddl_disable_input_" + last_random_id).val());
											jQuery("#restriction_" + random_id).find(".input_mask_settings,.custom_mask_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "paragraph_text_field_key_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("name", "ux_txt_default_value_" + random_id).attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + last_random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
											break;
										case "select":
											jQuery("#ux_div_single_line_text_"+last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id","ux_div_widget_"+random_id);
											jQuery("#ux_div_widget_"+random_id).children("div:eq(0)").attr("id","ux_header_title_"+random_id).attr("name","ux_header_title_"+random_id);
											jQuery("#ux_header_title_"+random_id).children("div:eq(0)").attr("name","ux_header_title_left_"+random_id).attr("id","ux_header_title_left_"+random_id).html("<b>Select</b>");
											jQuery("#ux_header_title_"+random_id).children("input").attr("id","ux_control_type_"+random_id).attr("name","ux_control_type_"+random_id).val("select");
											jQuery("#ux_header_title_"+random_id).children("div:eq(1)").attr("id","ux_header_title_right_"+random_id).attr("name","ux_header_title_right_"+random_id);
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(0)").attr("id","ux_expand_edit_fields_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(1)").attr("id","ux_duplicate_fields_"+random_id).attr("onclick","duplicate_fields_contact_bank('select',"+random_id+");");
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(2)").attr("id","ux_delete_fields_"+random_id).attr("onclick","delete_controls_contact_bank('ux_div_single_line_text_"+random_id+"');");
											jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
											jQuery("#ux_sub_div_"+random_id).children("label").attr("id","field_label_"+random_id).attr("name","field_label_"+random_id);
											jQuery("#field_label_"+random_id).children("span:eq(0)").attr("id","ux_label_title_"+random_id).attr("name","ux_label_title_"+random_id);
											jQuery("#field_label_"+random_id).children("i").attr("id","ux_tooltip_title_"+random_id).attr("name","ux_tooltip_title_"+random_id);
											jQuery("#field_label_"+random_id).children("span:eq(1)").remove();
											jQuery("#ux_sub_div_"+random_id).children("span:eq(0)").attr("id","ux_text_appear_after_counter_"+random_id).attr("name","ux_text_appear_after_counter_"+random_id);
											jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");
											jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#ux_sub_div_"+random_id).find("select").attr("id","ux_txt_singal_line_text_"+random_id);
											jQuery("#ux_txt_singal_line_text_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
											if(jQuery("#ux_txt_default_value_"+last_random_id).val() != null) {
												jQuery("#ux_txt_singal_line_text_"+random_id).val(jQuery("#ux_txt_default_value_"+last_random_id).val());
											}
											jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
											jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
											jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);

											jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("name","ux_txt_label_field_"+random_id).attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)");
											jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("name","ux_txt_description_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
											jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("id","ux_ddl_label_placement_"+random_id).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")").attr("name","ux_ddl_label_placement_"+random_id).val(jQuery("#ux_ddl_label_placement_"+last_random_id).val());
											jQuery("#general_"+random_id).find(".expiry_date_placeholder_settings,.expiry_date_placeholder_settings,.card_number_placeholder_settings,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings,.html_editor,.logical_captcha_settings").remove();

											jQuery("#ux_div_single_line_text_"+random_id).find(".options_settings").children("a").attr("href","#option_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".options_settings").attr("id","option_"+random_id).attr("name","option_"+random_id);
											jQuery("#option_"+random_id).find("input:eq(0)").attr("id","ux_txt_add_form_option_"+random_id).attr("name","ux_txt_add_form_option_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_option_"+random_id+"');");
											jQuery("#option_"+random_id).find("input:eq(1)").attr("id","ux_txt_add_form_values_"+random_id).attr("name","ux_txt_add_form_values_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_values_"+random_id+"');");
											jQuery("#option_"+random_id).find("input:eq(2)").attr("id","ux_btn_add_options_"+random_id).attr("name","ux_btn_add_options_"+random_id).attr("onclick","add_select_options_contact_bank("+random_id+", 'select')");
											jQuery("#option_"+random_id).find("input:eq(3)").attr("id","ux_btn_add_import_"+random_id);
											jQuery("#option_"+random_id).find("input:eq(4)").attr("id","ux_hidden_options_values_"+random_id).attr("name","ux_hidden_options_values_"+random_id);
											jQuery("#option_"+random_id).find("div:eq(4)").attr("id","ux_drop_down_value_"+random_id);
											jQuery("#option_"+random_id).find("select:eq(0)").attr("id","ux_ddl_options_required_"+random_id).val(jQuery("#ux_ddl_options_required_"+last_random_id).val()).attr("name","ux_ddl_options_required_"+random_id);
											if(jQuery("#ux_ddl_options_required_"+last_random_id).val() ===  null) {
												jQuery("#ux_drop_down_value_"+random_id).css("display","none");
											}
											jQuery("#ux_drop_down_value_"+random_id).find(".append_input_radio_"+last_random_id).remove();
											var arr = [], $select = jQuery("#ux_ddl_options_required_" + random_id);
											$select.find("option").each(function() {
												id++;
												var unique_id = random_id+"_"+id;
												jQuery("#ux_drop_down_value_" + random_id).append("<div id=ux_div_append_input_radio_"+random_id+" class=append_input_radio_"+random_id+">");
												jQuery("#ux_div_append_input_radio_" + random_id).css("margin-top", "10px");
												jQuery("#ux_div_append_input_radio_" + random_id).append("<div id=ux_div_full_control_radio_"+unique_id+" class=full_control_radio_"+random_id+"><input type=radio id=ux_txt_radio_add_button_"+unique_id+" name=ux_txt_radio_add_button_"+random_id+" style='margin-right:8px;'  class=radio_add_button_"+random_id+"><input type=text style='margin-left:2px;' id=ux_txt_option_value_"+unique_id+" class=txt_option_value_"+random_id+" value=\"" + this.text + "\"><input type=text style='margin-left:3px;' id=ux_txt_ddl_value_"+unique_id+" class=txt_ddl_value_"+random_id+" value=\"" + this.value + "\"><i class=icon-custom-minus id=ux_btn_delete_option_"+unique_id+"></i></div>");
												jQuery("#ux_div_full_control_radio_"+unique_id).addClass("radio-drag").css("margin-bottom","5px");
												jQuery("#ux_btn_delete_option_"+unique_id).attr("onclick", "delete_select_options_contact_bank('"+ unique_id + "','" + random_id + "')").css("margin-left", "9px");
												jQuery("#ux_btn_delete_option_"+unique_id).addClass("cb-radio-minus");
												jQuery("#ux_txt_option_value_"+unique_id).attr("onchange", "select_option_value_change_contact_bank('"+ random_id + "')");
												jQuery("#ux_txt_ddl_value_"+unique_id).attr("onchange", "select_option_value_change_contact_bank('"+ random_id + "')");
											});
											drag_drop_radio_button_contact_bank("select");
											jQuery("#ux_btn_add_import_"+random_id).attr("onclick","contact_bank_open_popup("+random_id+");").attr("data-popup-open","ux_open_popup_translator_"+random_id);
											jQuery("#option_"+random_id).find("textarea").attr("id","ux_txt_textarea_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_textarea_"+random_id+"');");
											jQuery("#option_"+random_id).find(".popup").attr("data-popup","ux_open_popup_translator_"+random_id);
											jQuery("#option_"+random_id).find(".popup").find(".btn:eq(0)").attr("id","ux_txt_popup_import_"+random_id);
											jQuery("#option_"+random_id).find(".popup").find(".btn:eq(1)").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
											jQuery("#ux_txt_popup_import_"+random_id).attr("onclick","import_select_options_contact_bank("+random_id+", 'select')").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
											jQuery("#option_"+random_id).find(".modal-footer").find("input:eq(1)").attr("onclick","contact_bank_close_popup_box("+random_id+")");

											jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
											jQuery("#apperance_"+random_id).find(".expiry_date_placeholder_settings,.expiry_date_placeholder_settings,.card_number_placeholder_settings,.card_cvv_number_placeholder_settings,.placeholder_settings").remove();
											jQuery("#apperance_"+random_id).find(".rows_number,.custom_validation_settings").remove();
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");

											jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").attr("href","#restriction_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".restrictions_settings").attr("id","restriction_"+random_id).attr("name","restriction_"+random_id);
											jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id","ux_ddl_autocomplete_"+random_id).attr("onchange","enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_autocomplete_"+random_id+"');").attr("name","ux_ddl_autocomplete_"+random_id).val(jQuery("#ux_ddl_autocomplete_"+last_random_id).val());
											jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id","ux_ddl_disable_input_"+random_id).attr("onchange","disable_fields_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_disable_input_"+random_id+"');").attr("name","ux_ddl_disable_input_"+random_id).val(jQuery("#ux_ddl_disable_input_"+last_random_id).val());
											jQuery("#restriction_"+random_id).find(".required_settings,.custom_mask_settings,.input_mask_settings,.limit_input_number_settings,.text_appear_settings").remove();

											jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
											jQuery("#advanced_"+random_id).find("div:eq(0)").children("input").attr("id","single_line_text_field_key_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'single_line_text_field_key_"+random_id+"');").attr("name","single_line_text_field_key_"+random_id).attr("value","select_field_key_"+random_id);
											jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(0) .form-group").find("select").attr("id","ux_txt_default_value_"+random_id).val(jQuery("#ux_txt_default_value_"+last_random_id).val()).attr("name","ux_txt_default_value_"+random_id).attr("onchange","set_default_value_contact_bank("+random_id+")");
											jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_admin_label_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_admin_label_"+random_id+"');").attr("name","ux_txt_admin_label_"+random_id);
											break;
										case "first_name":
											jQuery("#ux_div_single_line_text_"+last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id","ux_div_widget_"+random_id).attr("name","ux_div_widget_"+random_id);
											jQuery("#ux_div_widget_"+random_id).children("div:eq(0)").attr("id","ux_header_title_"+random_id).attr("name","ux_header_title_"+random_id);
											jQuery("#ux_header_title_"+random_id).children("div:eq(0)").attr("id","ux_header_title_left_"+random_id).html("<b>First Name</b>").attr("name","ux_header_title_left_"+random_id);
											jQuery("#ux_header_title_"+random_id).children("input").attr("id","ux_control_type_"+random_id).attr("name","ux_control_type_"+random_id).val("first_name");
											jQuery("#ux_header_title_"+random_id).children("div:eq(1)").attr("id","ux_header_title_right_"+random_id).attr("name","ux_header_title_right_"+random_id);
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(0)").attr("id","ux_expand_edit_fields_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(1)").attr("id","ux_duplicate_fields_"+random_id).attr("onclick","duplicate_fields_contact_bank('first_name',"+random_id+");");
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(2)").attr("id","ux_delete_fields_"+random_id).attr("onclick","delete_controls_contact_bank('ux_div_single_line_text_"+random_id+"',"+random_id+");");

											jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
											jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
											jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).children("label").attr("id","field_label_"+random_id).attr("name","field_label_"+random_id);
											jQuery("#field_label_"+random_id).children("span:eq(0)").attr("id","ux_label_title_"+random_id).attr("name","ux_label_title_"+random_id);
											jQuery("#field_label_"+random_id).children("i").attr("id","ux_tooltip_title_"+random_id).attr("name","ux_tooltip_title_"+random_id);
											jQuery("#field_label_"+random_id).children("span:eq(1)").attr("id","ux_required_"+random_id).attr("name","ux_required_"+random_id);
											jQuery("#ux_sub_div_"+random_id).children("span:eq(0)").attr("id","ux_text_appear_after_counter_"+random_id).attr("name","ux_text_appear_after_counter_"+random_id);
											jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");

											jQuery("#ux_sub_div_"+random_id).find("input").attr("id","ux_txt_singal_line_text_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_singal_line_text_"+random_id+"');").attr("name","ux_txt_singal_line_text_"+random_id);
											jQuery("#ux_txt_singal_line_text_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
											jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
											jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
											jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);

											jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("name","ux_txt_label_field_"+random_id).attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)");
											jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("name","ux_txt_description_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
											jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("id","ux_ddl_label_placement_"+random_id).val(jQuery("#ux_ddl_label_placement_"+last_random_id).val()).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")").attr("name","ux_ddl_label_placement_"+random_id);
											jQuery("#general_"+random_id).find(".logical_captcha_settings,.html_editor,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();

											jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
											jQuery("#apperance_"+random_id).find(".rows_number,.expiry_date_placeholder_settings,.expiry_date_placeholder_settings,.card_number_placeholder_settings,.card_cvv_number_placeholder_settings").remove();
											jQuery("#apperance_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_placeholder_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_placeholder_field_"+random_id+"');").attr("name","ux_txt_placeholder_field_"+random_id).attr("onkeyup","change_placeholder_content_contact_bank('ux_txt_singal_line_text_"+random_id+"',this.value);");
											jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_"+random_id+"');").attr("name", "ux_txt_custom_validation_field_" + random_id);
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');").attr("onkeyup","append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name","ux_txt_container_class_"+random_id);
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_element_class_"+random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name","ux_txt_element_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_element_class_"+random_id+"');");

											jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").attr("href","#restriction_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".restrictions_settings").attr("id","restriction_"+random_id).attr("name","restriction_"+random_id);
											jQuery("#restriction_"+random_id).find("div:eq(0)").children("select").attr("id","ux_ddl_required_"+random_id).val(jQuery("#ux_ddl_required_" + last_random_id).val()).attr("onchange","enable_disable_required_contact_bank('ux_ddl_required_"+random_id+"','ux_required_"+random_id+"');").attr("name","ux_ddl_required_"+random_id);
											jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id","ux_ddl_autocomplete_"+random_id).val(jQuery("#ux_ddl_autocomplete_"+last_random_id).val()).attr("onchange","enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_autocomplete_"+random_id+"');").attr("name","ux_ddl_autocomplete_"+random_id);
											jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id","ux_ddl_disable_input_"+random_id).attr("onchange","disable_fields_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_disable_input_"+random_id+"');").attr("name","ux_ddl_disable_input_"+random_id);
											jQuery("#ux_ddl_disable_input_"+random_id).val(jQuery("#ux_ddl_disable_input_"+last_random_id).val());
											jQuery("#restriction_"+random_id).find(".text_appear_settings,.limit_input_number_settings,.input_mask_settings,.custom_mask_settings").remove();
											jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
											jQuery("#advanced_"+random_id).find("div:eq(0)").children("input").attr("id","single_line_text_field_key_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'single_line_text_field_key_"+random_id+"');").attr("name","single_line_text_field_key_"+random_id).attr("value","first_name_field_key_"+random_id);
											jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_default_value_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_default_value_"+random_id+"');").attr("name","ux_txt_default_value_"+random_id).attr("onkeyup","control_default_value_contact_bank('ux_txt_singal_line_text_"+random_id+"',this.value);");
											jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_admin_label_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_admin_label_"+random_id+"');").attr("name","ux_txt_admin_label_"+random_id);
											break;
										case "last_name":
											jQuery("#ux_div_single_line_text_" + last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id).attr("name", "ux_div_widget_" + random_id);
											jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).html("<b>Last Name</b>").attr("name", "ux_header_title_left_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("last_name");
											jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('last_name'," + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

											jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
											jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id);
											jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
											jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");

											jQuery("#ux_sub_div_" + random_id).find("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');").attr("name", "ux_txt_singal_line_text_" + random_id);
											jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
											jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
											jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("name", "ux_txt_label_field_" + random_id).attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)");
											jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("name", "ux_txt_description_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
											jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).val(jQuery("#ux_ddl_label_placement_" + last_random_id).val()).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")").attr("name", "ux_ddl_label_placement_" + random_id);
											jQuery("#general_" + random_id).find(".logical_captcha_settings,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
											jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);").attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');").attr("name", "ux_txt_custom_validation_field_" + random_id);
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');").attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id);
											jQuery("#apperance_"+random_id).find(".rows_number,.expiry_date_placeholder_settings,.expiry_date_placeholder_settings,.card_number_placeholder_settings,.card_cvv_number_placeholder_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
											jQuery("#restriction_" + random_id).find(".required_settings").children("select").attr("id", "ux_ddl_required_" + random_id).val(jQuery("#ux_ddl_required_" + last_random_id).val()).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id);
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).val(jQuery("#ux_ddl_autocomplete_" + last_random_id).val()).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');").attr("name", "ux_ddl_autocomplete_" + random_id);
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").attr("name", "ux_ddl_disable_input_" + random_id);
											jQuery("#ux_ddl_disable_input_" + random_id).val(jQuery("#ux_ddl_disable_input_" + last_random_id).val());
											jQuery("#restriction_"+random_id).find(".text_appear_settings,.limit_input_number_settings,.input_mask_settings,.custom_mask_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "last_name_field_key_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("name", "ux_txt_default_value_" + random_id).attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
											break;
										case "email":
											jQuery("#ux_div_single_line_text_"+last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id","ux_div_widget_"+random_id).attr("name","ux_div_widget_"+random_id);
											jQuery("#ux_div_widget_"+random_id).children("div:eq(0)").attr("id","ux_header_title_"+random_id).attr("name","ux_header_title_"+random_id);
											jQuery("#ux_header_title_"+random_id).children("div:eq(0)").attr("id","ux_header_title_left_"+random_id).attr("name","ux_header_title_left_"+random_id).html("<b>Email Address</b>");
											jQuery("#ux_header_title_"+random_id).children("input").attr("id","ux_control_type_"+random_id).attr("name","ux_control_type_"+random_id).val("email");
											jQuery("#ux_header_title_"+random_id).children("div:eq(1)").attr("id","ux_header_title_right_"+random_id).attr("name","ux_header_title_right_"+random_id);
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(0)").attr("id","ux_expand_edit_fields_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(1)").attr("id","ux_duplicate_fields_"+random_id).attr("onclick","duplicate_fields_contact_bank('email',"+random_id+");");
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(2)").attr("id","ux_delete_fields_"+random_id).attr("onclick","delete_controls_contact_bank('ux_div_single_line_text_"+random_id+"',"+random_id+");");
											jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
											jQuery("#ux_sub_div_"+random_id).children("label").attr("id","field_label_"+random_id).attr("name","field_label_"+random_id);
											jQuery("#field_label_"+random_id).children("span:eq(0)").attr("id","ux_label_title_"+random_id).attr("name","ux_label_title_"+random_id);
											jQuery("#field_label_"+random_id).children("i").attr("id","ux_tooltip_title_"+random_id).attr("name","ux_tooltip_title_"+random_id);
											jQuery("#field_label_"+random_id).children("span:eq(1)").attr("id","ux_required_"+random_id).attr("name","ux_required_"+random_id);
											jQuery("#ux_sub_div_"+random_id).children("span:eq(0)").attr("id","ux_text_appear_after_counter_"+random_id).attr("name","ux_text_appear_after_counter_"+random_id);
											jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");
											jQuery("#ux_sub_div_"+random_id).find("input").attr("id","ux_txt_singal_line_text_"+random_id).attr("name","ux_txt_singal_line_text_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_singal_line_text_"+random_id+"');");
											jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#ux_txt_singal_line_text_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
											jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
											jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
											jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("name","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)");
											jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("name","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
											jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("id","ux_ddl_label_placement_"+random_id).attr("name","ux_ddl_label_placement_"+random_id).val(jQuery("#ux_ddl_label_placement_"+last_random_id).val()).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")");
											jQuery("#general_"+random_id).find(".logical_captcha_settings,.html_editor,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();
											jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
											jQuery("#apperance_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_placeholder_field_"+random_id).attr("name","ux_txt_placeholder_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_placeholder_field_"+random_id+"');").attr("onkeyup","change_placeholder_content_contact_bank('ux_txt_singal_line_text_"+random_id+"',this.value);");
											jQuery("#apperance_"+random_id).find(".custom_validation_settings").children("input").attr("id","ux_txt_custom_validation_field_"+random_id).attr("name","ux_txt_custom_validation_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_custom_validation_field_"+random_id+"');");
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("name","ux_txt_container_class_"+random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');");
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_element_class_"+random_id).attr("name","ux_txt_element_class_"+random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_element_class_"+random_id+"');");
											jQuery("#apperance_" + random_id).find(".rows_number,.card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings").remove();
											jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").attr("href","#restriction_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".restrictions_settings").attr("id","restriction_"+random_id).attr("name","restriction_"+random_id);
											jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).val(jQuery("#ux_ddl_required_" +last_random_id).val()).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id);
											jQuery("#restriction_"+random_id).find(".limit_input_number_settings,.text_appear_settings,.autocomplete_settings,.input_mask_settings,.custom_mask_settings").remove();
											jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
											jQuery("#advanced_"+random_id).find("div:eq(0)").children("input").attr("id","single_line_text_field_key_"+random_id).attr("name","single_line_text_field_key_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'single_line_text_field_key_"+random_id+"');").attr("value","email_address_field_key_"+random_id);
											jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_default_value_"+random_id).attr("name","ux_txt_default_value_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_default_value_"+random_id+"');").attr("onkeyup","control_default_value_contact_bank('ux_txt_singal_line_text_"+random_id+"',this.value);");
											jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_admin_label_"+random_id).attr("name","ux_txt_admin_label_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_admin_label_"+random_id+"');");
											break;
											case "phone":
											jQuery("#ux_div_single_line_text_" + last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("name", "ux_div_widget_" + random_id);
											jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id);
											jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("name", "ux_header_title_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).html("<b>Phone</b>");
											jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("name", "ux_header_title_left_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("phone");
											jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('phone'," + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

											jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id);
											jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
											jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
											jQuery("#ux_sub_div_" + random_id).find("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');").attr("name", "ux_txt_singal_line_text_" + random_id);
											var validation_type = jQuery("#ux_ddl_limit_input_" + last_random_id).val();
											if (validation_type === "digits") {
												jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeypress", "only_digits_contact_bank(event," + random_id + ");");
											} else {
												jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeyup", "only_characters_contact_bank(event," + random_id + ");");
											}
											jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
											jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
											jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);

											jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("name", "ux_txt_label_field_" + random_id).attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)");
											jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("name", "ux_txt_description_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
											jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).val(jQuery("#ux_ddl_label_placement_" + last_random_id).val()).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")").attr("name", "ux_ddl_label_placement_" + random_id).val(jQuery("#ux_ddl_label_placement_"+last_random_id).val());
											jQuery("#general_" + random_id).find(".logical_captcha_settings,.html_editor,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
											jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');").attr("name", "ux_txt_custom_validation_field_" + random_id);
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".rows_number,.card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
											jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id).val(jQuery("#ux_ddl_required_"+last_random_id).val());
											jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("input").attr("id", "ux_txt_limit_input_" + random_id).val("10").attr("onkeypress","enter_only_digits_for_price(event)").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_limit_input_" + random_id + "');").attr("name", "ux_txt_limit_input_" + random_id);
											jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("select").attr("id", "ux_ddl_limit_input_" + random_id).val(jQuery("#ux_ddl_limit_input_" + last_random_id).val()).attr("onchange", "limit_input_event_contact_bank(" + random_id + ");").attr("name", "ux_ddl_limit_input_" + random_id).val(jQuery("#ux_ddl_limit_input_"+last_random_id).val());
											jQuery("#restriction_" + random_id).find(".text_appear_settings").children("input").attr("id", "ux_txt_text_appear_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_text_appear_" + random_id + "');").attr("name", "ux_txt_text_appear_" + random_id).attr("onkeyup", "change_error_message_content_contact_bank('ux_text_appear_after_counter_" + random_id + "',this.value);");
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).val(jQuery("#ux_ddl_autocomplete_" + last_random_id).val()).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');").attr("name", "ux_ddl_autocomplete_" + random_id).val(jQuery("#ux_ddl_autocomplete_" + last_random_id).val());
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").attr("name", "ux_ddl_disable_input_" + random_id).val(jQuery("#ux_ddl_disable_input_" + last_random_id).val());
											jQuery("#restriction_" + random_id).find(".custom_mask_settings").attr("id", "ux_div_custom_mask_settings_" + random_id).attr("name", "ux_div_custom_mask_settings_" + random_id);
											jQuery("#restriction_" + random_id).find(".custom_mask_settings").children("input").attr("id", "ux_txt_custom_mask_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_mask_" + random_id + "');").attr("name", "ux_txt_custom_mask_" + random_id).attr("onblur", "apply_input_masking_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_input_mask_" + random_id + "','ux_div_custom_mask_settings_" + random_id + "'," + random_id + ");");
											jQuery("#restriction_" + random_id).find(".input_mask_settings").children("select").attr("id", "ux_ddl_input_mask_" + random_id).val(jQuery("#ux_ddl_input_mask_" + last_random_id).val()).attr("onchange", "apply_input_masking_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_input_mask_" + random_id + "','ux_div_custom_mask_settings_" + random_id + "'," + random_id + ");").attr("name", "ux_ddl_input_mask_" + random_id);
											if(jQuery("#ux_ddl_input_mask_"+random_id).val() != "custom") {
												jQuery("#restriction_" + random_id).find(".custom_mask_settings").css("display", "none");
											}
											jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "phone_field_key_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("name", "ux_txt_default_value_" + random_id).attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
											break;
										case "website_url":
											jQuery("#ux_div_single_line_text_" + last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id).attr("name", "ux_div_widget_" + random_id);
											jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id).html("<b>Website URL</b>");
											jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("website_url");
											jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('website_url'," + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

											jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id);
											jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
											jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
											jQuery("#ux_sub_div_" + random_id).find("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("name", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");
											jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
											jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
											jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("name", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)");
											jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("name", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);");
											jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).attr("name", "ux_ddl_label_placement_" + random_id).val(jQuery("#ux_ddl_label_placement_" + last_random_id).val()).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")");
											jQuery("#general_" + random_id).find(".logical_captcha_settings,.html_editor,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();
											jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
											jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("name", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".rows_number").remove();
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("name", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("name", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");
											jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
											jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("name", "ux_ddl_required_" + random_id).val(jQuery("#ux_ddl_required_" +last_random_id).val()).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');");
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).val(jQuery("#ux_ddl_autocomplete_" + last_random_id).val()).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');");
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("name", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").val(jQuery("#ux_ddl_disable_input_" + last_random_id).val());
											jQuery("#restriction_" + random_id).find(".custom_mask_settings,.input_mask_settings,.text_appear_settings,.limit_input_number_settings").remove();
											jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("name", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("value", "website_url_field_key_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("name", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("name", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');");
											break;
										case "number":
											jQuery("#ux_div_single_line_text_" + last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id).attr("name", "ux_div_widget_" + random_id);
											jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("number");
											jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('number'," + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

											jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id);
											jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
											jQuery("#ux_text_appear_after_counter_" + random_id).css("display", jQuery("ux_text_appear_after_counter_"+last_random_id)).val();
											jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#ux_sub_div_" + random_id).find("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("name", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");

											jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");").attr("onkeyup", "number_settings_contact_bank(" + random_id + ",event);");
											jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
											jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
											jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);

											jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
											jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("name", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("id", "ux_txt_label_field_" + random_id).attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)");
											jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
											jQuery("#general_" + random_id).find(".number_settings").find("div:eq(2)").children("input").attr("id", "ux_txt_min_number_" + random_id).attr("name", "ux_txt_min_number_" + random_id).val(jQuery("#ux_txt_min_number_"+last_random_id).val()).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_min_number_" + random_id + "');");
											jQuery("#general_" + random_id).find(".number_settings").find("div:eq(4)").children("input").attr("id", "ux_txt_max_number_" + random_id).attr("name", "ux_txt_max_number_" + random_id).val(jQuery("#ux_txt_max_number_"+last_random_id).val()).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_max_number_" + random_id + "');");
											jQuery("#general_" + random_id).find(".number_settings").find("div:eq(5)").children("input").attr("id", "ux_txt_step_" + random_id).attr("name", "ux_txt_step_" + random_id).val(jQuery("#ux_txt_step_"+last_random_id).val()).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_step_" + random_id + "');");
											jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("name", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
											jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).attr("name", "ux_ddl_label_placement_" + random_id).val(jQuery("#ux_ddl_label_placement_" + last_random_id).val()).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")");
											jQuery("#general_" + random_id).find(".html_editor,.date_settings,.time_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings,.logical_captcha_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
											jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("name", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');");
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');").attr("name","ux_txt_container_class_"+random_id).attr("onkeyup","append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');");
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_element_class_"+random_id).attr("onkeyup","append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name","ux_txt_element_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_element_class_"+random_id+"');");
											jQuery("#apperance_" + random_id).find(".rows_number,.card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
											jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id).val(jQuery("#ux_ddl_required_" + last_random_id).val());
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).attr("name", "ux_ddl_autocomplete_" + random_id).val(jQuery("#ux_ddl_autocomplete_" + last_random_id).val()).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');");
											jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("name", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").val(jQuery("#ux_ddl_disable_input_" + last_random_id).val());
											jQuery("#restriction_" + random_id).find(".custom_mask_settings,.input_mask_settings,.text_appear_settings,.limit_input_number_settings").remove();
											jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("name", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("value", "number_field_key_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("name", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("name", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');");
											break;
										case "checkbox":
											jQuery("#ux_div_single_line_text_" + last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("name", "ux_div_single_line_text_" + random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id);
											jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id).html("<b>Checkbox</b>");
											jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("checkbox");
											jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('checkbox'," + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");
											jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id);
											jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
											jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
											jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
											jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#ux_sub_div_" + random_id).find("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("name", "ux_txt_singal_line_text_" + random_id);
											jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
											jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
											jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);

											jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)").attr("name","ux_txt_label_field_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("name","ux_txt_description_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
											jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("id","ux_ddl_label_placement_"+random_id).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")").attr("name","ux_ddl_label_placement_"+random_id).val(jQuery("#ux_ddl_label_placement_"+last_random_id).val());
											jQuery("#general_"+random_id).find(".html_editor,.field_description_settings,.quantity_settings,.date_settings,.time_settings,.number_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.html_editor,.logical_captcha_settings").remove();

											jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
											jQuery("#apperance_" + random_id).find(".rows_number,.placeholder_settings, .card_number_placeholder_settings, .expiry_date_placeholder_settings, .card_cvv_number_placeholder_settings").remove();
											jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');").attr("name", "ux_txt_custom_validation_field_" + random_id);
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
											jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'checkbox_class', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");

											jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
											jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
											jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id).val(jQuery("#ux_ddl_required_"+last_random_id).val());
											jQuery("#restriction_" + random_id).find(".limit_input_number_settings,.text_appear_settings,.input_mask_settings,.custom_mask_settings").remove();
											jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id","ux_ddl_autocomplete_"+random_id).attr("onchange","enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_autocomplete_"+random_id+"');").attr("name","ux_ddl_autocomplete_"+random_id).val(jQuery("#ux_ddl_autocomplete_"+last_random_id).val());
											jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id","ux_ddl_disable_input_"+random_id).attr("onchange","disable_fields_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_disable_input_"+random_id+"');").attr("name","ux_ddl_disable_input_"+random_id).val(jQuery("#ux_ddl_disable_input_"+last_random_id).val());

											jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
											jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "checkbox_field_key_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(1)").find(".admin_label_settings").find("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
											jQuery("#advanced_" + random_id).find(".admin_label_settings").removeClass("col-md-6").addClass("col-md-12");
											jQuery("#advanced_" + random_id).find(".default_value_settings").remove();
											break;
										case "checkbox-list":
											jQuery("#ux_div_single_line_text_"+last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("name","ux_div_single_line_text_" + random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id","ux_div_widget_"+random_id);
											jQuery("#ux_div_widget_"+random_id).children("div:eq(0)").attr("id","ux_header_title_"+random_id).attr("name","ux_header_title_"+random_id);
											jQuery("#ux_div_widget_"+random_id).find('b').replaceWith('<b> Checkbox List</b>');
											jQuery("#ux_header_title_"+random_id).children("div:eq(0)").attr("id","ux_header_title_left_"+random_id).attr("name","ux_header_title_left_"+random_id);
											jQuery("#ux_header_title_"+random_id).children("input").attr("id","ux_control_type_"+random_id).attr("name","ux_control_type_"+random_id).val("checkbox-list");
											jQuery("#ux_header_title_"+random_id).children("div:eq(1)").attr("id","ux_header_title_right_"+random_id).attr("name","ux_header_title_right_"+random_id);
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(0)").attr("id","ux_expand_edit_fields_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(1)").attr("id","ux_duplicate_fields_"+random_id).attr("onclick","duplicate_fields_contact_bank('checkbox-list',"+random_id+");");
											jQuery("#ux_header_title_right_"+random_id).children("a:eq(2)").attr("id","ux_delete_fields_"+random_id).attr("onclick","delete_controls_contact_bank('ux_div_single_line_text_"+random_id+"');");
											jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
											jQuery("#ux_sub_div_"+random_id).children("label").attr("id","field_label_"+random_id).attr("name","field_label_"+random_id);
											jQuery("#field_label_"+random_id).children("span:eq(0)").attr("id","ux_label_title_"+random_id).attr("name","ux_label_title_"+random_id);
											jQuery("#field_label_"+random_id).children("i").attr("id","ux_tooltip_title_"+random_id).attr("name","ux_tooltip_title_"+random_id);
											jQuery("#field_label_"+random_id).children("span:eq(1)").attr("id","ux_required_"+random_id).attr("name","ux_required_"+random_id);

											jQuery("#ux_sub_div_"+random_id).find("input").attr("id","ux_txt_singal_line_text_"+random_id).attr("name","ux_txt_singal_line_text_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
											jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#ux_sub_div_"+random_id).find(".checkbox-label").attr("id","ux_txt_check_box_"+random_id).attr("name","ux_txt_check_box_"+random_id);
											jQuery("#ux_sub_div_"+random_id).find("#field_labels_"+last_random_id).attr("id","field_labels_"+random_id).attr("name","field_labels_"+random_id);
											jQuery("#field_labels_"+random_id).find("input").attr("name","ux_txt_check_box_lists_"+random_id).attr("id","ux_txt_check_box_lists_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+")").removeClass("checkbox_class_" + last_random_id).addClass("checkbox_class_" + random_id);
											jQuery("#field_labels_"+random_id).find("label").attr("id","ux_chk_label_lists_"+random_id).attr("name","ux_chk_label_lists_"+random_id);

											jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
											jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
											jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("name","ux_txt_label_field_"+random_id).attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)");
											jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("name","ux_txt_description_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
											jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("id","ux_ddl_label_placement_"+random_id).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")").attr("name","ux_ddl_label_placement_"+random_id).val(jQuery("#ux_ddl_label_placement_"+last_random_id).val());
											jQuery("#general_"+random_id).find(".field_description_settings,.quantity_settings,.date_settings,.time_settings,.number_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.html_editor,.logical_captcha_settings").remove();

											jQuery("#ux_div_single_line_text_"+random_id).find(".options_settings").children("a").attr("href","#option_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".options_settings").attr("id","option_"+random_id).attr("name","option_"+random_id);
											jQuery("#option_"+random_id).find("input:eq(0)").attr("id","ux_txt_add_form_option_"+random_id).attr("name","ux_txt_add_form_option_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_option_"+random_id+"');");
											jQuery("#option_"+random_id).find("input:eq(1)").attr("id","ux_txt_add_form_values_"+random_id).attr("name","ux_txt_add_form_values_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_values_"+random_id+"');");
											jQuery("#option_"+random_id).find("input:eq(2)").attr("id","ux_btn_add_options_"+random_id).attr("name","ux_btn_add_options_"+random_id).attr("onclick","add_control_options_contact_bank("+random_id+",'checkbox');");
											jQuery("#option_"+random_id).find("input:eq(3)").attr("id","ux_btn_add_import_"+random_id);
											jQuery("#option_"+random_id).find("input:eq(4)").attr("id","ux_hidden_options_values_"+random_id).attr("name","ux_hidden_options_values_"+random_id);
											jQuery("#option_"+random_id).find("div:eq(4)").attr("id","ux_drop_down_value_"+random_id);
											if(jQuery("#ux_ddl_options_required_"+last_random_id).val() ===  null) {
												jQuery("#ux_drop_down_value_"+random_id).css("display","none");
											}
											jQuery("#option_"+random_id).find("select:eq(0)").attr("id","ux_ddl_options_required_"+random_id).attr("name","ux_ddl_options_required_"+random_id);
											jQuery("#ux_drop_down_value_"+random_id).find(".append_input_radio_"+last_random_id).remove();
											var arr = [], $select = jQuery("#ux_ddl_options_required_" + random_id);
											$select.find("option").each(function() {
												id++;
												var unique_id = random_id+"_"+id;
												jQuery("#ux_drop_down_value_" + random_id).append("<div id=ux_div_append_input_radio_"+random_id+" class=append_input_radio_"+random_id+">");
												jQuery("#ux_div_append_input_radio_" + random_id).css("margin-top", "10px");
												jQuery("#ux_div_append_input_radio_" + random_id).append("<div id=ux_div_full_control_radio_"+unique_id+" class=full_control_radio_"+random_id+"><input type=radio id=ux_txt_radio_add_button_"+unique_id+" name=ux_txt_radio_add_button_"+random_id+" style='margin-right:8px;'  class=radio_add_button_"+random_id+"><input type=text style='margin-left:2px;' id=ux_txt_option_value_"+unique_id+" class=txt_option_value_"+random_id+" value=\"" + this.text + "\"><input type=text style='margin-left:3px;' id=ux_txt_ddl_value_"+unique_id+" class=txt_ddl_value_"+random_id+" value=\"" + this.value + "\"><i class=icon-custom-minus id=ux_btn_delete_option_"+unique_id+"></i></div>");
												jQuery("#ux_div_full_control_radio_"+unique_id).addClass("radio-drag").css("margin-bottom","5px");
												jQuery("#ux_btn_delete_option_"+unique_id).attr("onclick", "delete_radio_options_contact_bank('"+ unique_id + "','" + random_id + "')").css("margin-left", "9px");
												jQuery("#ux_btn_delete_option_"+unique_id).addClass("cb-radio-minus");
												jQuery("#ux_txt_option_value_"+unique_id).attr("onchange", "radio_option_value_change_contact_bank('"+ random_id + "', 'checkbox')");
												jQuery("#ux_txt_ddl_value_"+unique_id).attr("onchange", "radio_option_value_change_contact_bank('"+ random_id + "', 'checkbox')");
											});
											drag_drop_radio_button_contact_bank("checkbox");
											jQuery("#ux_btn_add_import_"+random_id).attr("onclick","contact_bank_open_popup("+random_id+");").attr("data-popup-open","ux_open_popup_translator_"+random_id);
											jQuery("#option_"+random_id).find("textarea").attr("id","ux_txt_textarea_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_textarea_"+random_id+"');");
											jQuery("#option_"+random_id).find(".popup").attr("data-popup","ux_open_popup_translator_"+random_id);
											jQuery("#option_"+random_id).find(".popup").find(".btn:eq(0)").attr("id","ux_txt_popup_import_"+random_id);
											jQuery("#option_"+random_id).find(".popup").find(".btn:eq(1)").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
											jQuery("#ux_txt_popup_import_"+random_id).attr("onclick","import_controls_values_contact_bank("+random_id+",'checkbox')").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
											jQuery("#option_"+random_id).find(".modal-footer").find("input:eq(1)").attr("onclick","contact_bank_close_popup_box("+random_id+")");

											jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
											jQuery("#apperance_"+random_id).find(".card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings,.rows_number,.placeholder_settings").remove();
											jQuery("#apperance_"+random_id).find(".custom_validation_settings").find("input").attr("id","ux_txt_custom_validation_field_"+random_id).attr("name","ux_txt_custom_validation_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_custom_validation_field_"+random_id+"');");
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');").attr("name","ux_txt_container_class_"+random_id).attr("onkeyup","append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');");
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_element_class_"+random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');").attr("onkeyup","append_class_contact_bank('ux_txt_check_box_lists_" + random_id + "',this.value, 'checkbox_class_" + random_id + "', '', '', "+random_id+", 'checkbox-list');").attr("name","ux_txt_element_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_element_class_"+random_id+"');");

											jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").attr("href","#restriction_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".restrictions_settings").attr("id","restriction_"+random_id).attr("name","restriction_"+random_id);
											jQuery("#restriction_"+random_id).find("div:eq(0)").children("select").attr("id","ux_ddl_required_"+random_id).attr("onchange","enable_disable_required_contact_bank('ux_ddl_required_"+random_id+"','ux_required_"+random_id+"');").attr("name","ux_ddl_required_"+random_id).val(jQuery("#ux_ddl_required_"+last_random_id).val());
											jQuery("#restriction_"+random_id).find(".autocomplete_settings,.limit_input_number_settings,.custom_mask_settings,.text_appear_settings,.input_mask_settings").remove();

											jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
											jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "checkbox_list_key_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
											jQuery("#advanced_" + random_id).find(".admin_label_settings").removeClass("col-md-6").addClass("col-md-12");
											jQuery("#advanced_" + random_id).find(".default_value_settings").remove();
											break;
										case "radio-list":
											jQuery("#ux_div_single_line_text_" + last_random_id).clone(false).attr("id", "ux_div_single_line_text_" + random_id).insertAfter("#ux_div_single_line_text_" + last_random_id);
											jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
											jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id).attr("name", "ux_div_widget_" + random_id);
											jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id);
											jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("radio-list");
											jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('radio-list'," + random_id + ");");
											jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

											jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
											jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
											jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
											jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
											jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id);
											jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
											jQuery("#ux_sub_div_"+random_id).find("input").attr("id","ux_txt_singal_line_text_"+random_id);
											jQuery("#ux_sub_div_"+random_id).find(".checkbox-label").attr("id","ux_txt_check_box_"+random_id).attr("name","ux_txt_check_box_"+random_id);
											jQuery("#ux_sub_div_"+random_id).find("#field_labels_"+last_random_id).attr("id","field_labels_"+random_id).attr("name","field_labels_"+random_id);
											jQuery("#field_labels_"+random_id).find("input").attr("name","ux_txt_check_box_lists_"+random_id).attr("id","ux_txt_check_box_lists_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+")").removeClass("checkbox_class_" + last_random_id).addClass("checkbox_class_" + random_id);
											jQuery("#field_labels_"+random_id).find("label").attr("id","ux_chk_label_lists_"+random_id).attr("name","ux_chk_label_lists_"+random_id);
											jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
											jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
											jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
											jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("name","ux_txt_label_field_"+random_id).attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)");
											jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
											jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("name","ux_txt_description_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
											jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("id","ux_ddl_label_placement_"+random_id).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")").attr("name","ux_ddl_label_placement_"+random_id).val(jQuery("#ux_ddl_label_placement_"+last_random_id).val());
											jQuery("#general_"+random_id).find(".field_description_settings,.quantity_settings,.date_settings,.time_settings,.number_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.html_editor,.logical_captcha_settings").remove();

											jQuery("#ux_div_single_line_text_"+random_id).find(".options_settings").children("a").attr("href","#option_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".options_settings").attr("id","option_"+random_id).attr("name","option_"+random_id);
											jQuery("#option_"+random_id).find("input:eq(0)").attr("id","ux_txt_add_form_option_"+random_id).attr("name","ux_txt_add_form_option_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_option_"+random_id+"');");
											jQuery("#option_"+random_id).find("input:eq(1)").attr("id","ux_txt_add_form_values_"+random_id).attr("name","ux_txt_add_form_values_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_values_"+random_id+"');");
											jQuery("#option_"+random_id).find("input:eq(2)").attr("id","ux_btn_add_options_"+random_id).attr("name","ux_btn_add_options_"+random_id).attr("onclick","add_control_options_contact_bank("+random_id+",'radio');");
											jQuery("#option_"+random_id).find("input:eq(3)").attr("id","ux_btn_add_import_"+random_id);
											jQuery("#option_"+random_id).find("input:eq(4)").attr("id","ux_hidden_options_values_"+random_id).attr("name","ux_hidden_options_values_"+random_id);
											jQuery("#option_"+random_id).find("div:eq(4)").attr("id","ux_drop_down_value_"+random_id);
											jQuery("#option_"+random_id).find("select:eq(0)").attr("id","ux_ddl_options_required_"+random_id).attr("name","ux_ddl_options_required_"+random_id);
											if(jQuery("#ux_ddl_options_required_"+last_random_id).val() ==  null) {
												jQuery("#ux_drop_down_value_"+random_id).css("display","none");
											}
											jQuery("#ux_drop_down_value_"+random_id).find(".append_input_radio_"+last_random_id).remove();
											var arr = [], $select = jQuery("#ux_ddl_options_required_" + random_id);
											$select.find("option").each(function() {
												id++;
												var unique_id = random_id+"_"+id;
												jQuery("#ux_drop_down_value_" + random_id).append("<div id=ux_div_append_input_radio_"+random_id+" class=append_input_radio_"+random_id+">");
												jQuery("#ux_div_append_input_radio_" + random_id).css("margin-top", "10px");
												jQuery("#ux_div_append_input_radio_" + random_id).append("<div id=ux_div_full_control_radio_"+unique_id+" class=full_control_radio_"+random_id+"><input type=radio id=ux_txt_radio_add_button_"+unique_id+" name=ux_txt_radio_add_button_"+random_id+" style='margin-right:8px;'  class=radio_add_button_"+random_id+"><input type=text style='margin-left:2px;' id=ux_txt_option_value_"+unique_id+" class=txt_option_value_"+random_id+" value=\"" + this.text + "\"><input type=text style='margin-left:3px;' id=ux_txt_ddl_value_"+unique_id+" class=txt_ddl_value_"+random_id+" value=\"" + this.value + "\"><i class=icon-custom-minus id=ux_btn_delete_option_"+unique_id+"></i></div>");
												jQuery("#ux_div_full_control_radio_"+unique_id).addClass("radio-drag").css("margin-bottom","5px");
												jQuery("#ux_btn_delete_option_"+unique_id).attr("onclick", "delete_radio_options_contact_bank('"+ unique_id + "','" + random_id + "')").css("margin-left", "9px");
												jQuery("#ux_btn_delete_option_"+unique_id).addClass("cb-radio-minus");
												jQuery("#ux_txt_option_value_"+unique_id).attr("onchange", "radio_option_value_change_contact_bank('"+ random_id + "', 'radio')");
												jQuery("#ux_txt_ddl_value_"+unique_id).attr("onchange", "radio_option_value_change_contact_bank('"+ random_id + "', 'radio')");

											});
											drag_drop_radio_button_contact_bank("radio");
											jQuery("#ux_drop_down_value_"+random_id).find("input:eq(0)").attr("id","ux_btn_delete_option_"+random_id);
											jQuery("#option_"+random_id).find("textarea").attr("id","ux_txt_textarea_"+random_id).attr("name","ux_txt_textarea_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_textarea_"+random_id+"');");
											jQuery("#option_"+random_id).find(".popup").find(".btn:eq(0)").attr("id","ux_txt_popup_import_"+random_id);
											jQuery("#ux_btn_add_import_"+random_id).attr("onclick","contact_bank_open_popup("+random_id+");").attr("data-popup-open","ux_open_popup_translator_"+random_id);
											jQuery("#option_"+random_id).find("textarea").attr("id","ux_txt_textarea_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_textarea_"+random_id+"');");
											jQuery("#option_"+random_id).find(".popup").attr("data-popup","ux_open_popup_translator_"+random_id);
											jQuery("#option_"+random_id).find(".popup").find(".btn:eq(0)").attr("id","ux_txt_popup_import_"+random_id);
											jQuery("#option_"+random_id).find(".popup").find(".btn:eq(1)").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
											jQuery("#ux_txt_popup_import_"+random_id).attr("onclick","import_controls_values_contact_bank("+random_id+",'radio')").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
											jQuery("#option_"+random_id).find(".modal-footer").find("input:eq(1)").attr("onclick","contact_bank_close_popup_box("+random_id+")");

											jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
											jQuery("#apperance_"+random_id).find(".custom_validation_settings,.card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings,.rows_number,.placeholder_settings").remove();
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');").attr("name","ux_txt_container_class_"+random_id).attr("onkeyup","append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');");
											jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_element_class_"+random_id).attr("onkeyup","append_class_contact_bank('ux_txt_check_box_lists_" + random_id + "',this.value, 'checkbox_class_" + random_id + "', '', '', "+random_id+", 'radio-list');").attr("name","ux_txt_element_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_element_class_"+random_id+"');");
											jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").remove();

											jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
											jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
											jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "radio_list_key_" + random_id);
											jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
											jQuery("#advanced_" + random_id).find(".admin_label_settings").removeClass("col-md-6").addClass("col-md-12");
											jQuery("#advanced_" + random_id).find(".default_value_settings").remove();
											break;
									}
									jQuery(".tooltips").tooltip_tip({placement: "right"});
								}
							}
							function contact_bank_field_fill(type)
							{
								var random_id = new Date().getTime();
								contact_bank_control_ids.push(random_id);
								switch (type) {
									case "text":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields");
										jQuery("#ux_div_single_line_text_" + random_id).attr("name", "ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id);
										jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("text");
										jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('text'," + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");
										jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id).text("Single Line Text");
										jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
										jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
										jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#ux_sub_div_" + random_id).children("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");
										jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeyup", "only_characters_contact_bank(event," + random_id + ");").attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
										jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
										jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("name", "ux_txt_label_field_" + random_id).attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)").val("Single Line Text");
										jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("name", "ux_txt_description_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
										jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")").attr("name", "ux_ddl_label_placement_" + random_id);
										jQuery("#general_" + random_id).find(".date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings,.html_editor,.logical_captcha_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".options_settings").remove();
										jQuery("#ux_div_tab_contents_" + random_id).children(".options_settings").remove();
										jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
										jQuery("#apperance_" + random_id).find(".placeholder_settings").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');").attr("name", "ux_txt_custom_validation_field_" + random_id);
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".rows_number,.card_number_placeholder_settings, .expiry_date_placeholder_settings, .card_cvv_number_placeholder_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("input").attr("name", "ux_txt_limit_input_" + random_id).attr("id", "ux_txt_limit_input_" + random_id).attr("onkeypress","enter_only_digits_for_price(event)").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_limit_input_" + random_id + "');");
										jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("select").attr("id", "ux_ddl_limit_input_" + random_id).attr("onchange", "limit_input_event_contact_bank(" + random_id + ");").attr("name", "ux_ddl_limit_input_" + random_id);
										jQuery("#restriction_" + random_id).find(".text_appear_settings").children("input").attr("id", "ux_txt_text_appear_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_text_appear_" + random_id + "');").attr("name", "ux_txt_text_appear_" + random_id).attr("onkeyup", "change_error_message_content_contact_bank('ux_text_appear_after_counter_" + random_id + "',this.value);");
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');").attr("name", "ux_ddl_autocomplete_" + random_id);
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").attr("name", "ux_ddl_disable_input_" + random_id);
										jQuery("#restriction_" + random_id).find(".custom_mask_settings").attr("id", "ux_div_custom_mask_settings_" + random_id).attr("name", "ux_div_custom_mask_settings_" + random_id);
										jQuery("#restriction_" + random_id).find(".custom_mask_settings").children("input").attr("id", "ux_txt_custom_mask_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_mask_" + random_id + "');").attr("name", "ux_txt_custom_mask_" + random_id).attr("onblur", "apply_input_masking_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_input_mask_" + random_id + "','ux_div_custom_mask_settings_" + random_id + "'," + random_id + ");");
										jQuery("#restriction_" + random_id).find(".custom_mask_settings").css("display", "none");
										jQuery("#restriction_" + random_id).find(".input_mask_settings").children("select").attr("id", "ux_ddl_input_mask_" + random_id).attr("onchange", "apply_input_masking_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_input_mask_" + random_id + "','ux_div_custom_mask_settings_" + random_id + "'," + random_id + ");").attr("name", "ux_ddl_input_mask_" + random_id);

										jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "single_line_text_field_key_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("name", "ux_txt_default_value_" + random_id).attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
										break;
									case "paragraph":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields");
										jQuery("#ux_div_single_line_text_" + random_id).attr("name", "ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id);
										jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id).html("<b>Paragraph</b>");
										jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("paragraph");
										jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('paragraph'," + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");
										jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id).text("Paragraph");
										jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
										jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
										jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#ux_sub_div_" + random_id).children("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");
										jQuery('#ux_txt_singal_line_text_' + random_id).replaceWith(jQuery('<textarea name=ux_txt_singal_line_text_' + random_id + ' rows=2 id=ux_txt_singal_line_text_' + random_id + ' class=untitled_control>'));
										jQuery("#ux_txt_singal_line_text_" + random_id).css("vertical-align","middle");
										jQuery('#ux_txt_singal_line_text_' + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');")
										jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeyup", "only_characters_contact_bank(event," + random_id + ");").attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
										jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
										jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);

										jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("name", "ux_txt_label_field_" + random_id).attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)").val("Paragraph");
										jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("name", "ux_txt_description_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
										jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")").attr("name", "ux_ddl_label_placement_" + random_id);
										jQuery("#general_" + random_id).find(".date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings,.html_editor,.logical_captcha_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".options_settings").remove();
										jQuery("#ux_div_tab_contents_" + random_id).children(".options_settings").remove();
										jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
										jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');").attr("name", "ux_txt_custom_validation_field_" + random_id);
										jQuery("#apperance_" + random_id).find(".rows_number").children("input").attr("id", "ux_txt_no_of_rows_" + random_id).attr("name", "ux_txt_no_of_rows_" + random_id).attr("onkeyup","change_textarea_rows_contact_bank("+random_id+");").val(jQuery("#ux_txt_no_of_rows_"+random_id)).val("2");
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("input").attr("name", "ux_txt_limit_input_" + random_id).attr("id", "ux_txt_limit_input_" + random_id).attr("onkeypress","enter_only_digits_for_price(event)").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_limit_input_" + random_id + "');");
										jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("select").attr("name", "ux_ddl_limit_input_" + random_id).attr("id", "ux_ddl_limit_input_" + random_id).attr("onchange", "limit_input_event_contact_bank(" + random_id + ");");
										jQuery("#restriction_" + random_id).find(".text_appear_settings").children("input").attr("id", "ux_txt_text_appear_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_text_appear_" + random_id + "');").attr("name", "ux_txt_text_appear_" + random_id).attr("onkeyup", "change_error_message_content_contact_bank('ux_text_appear_after_counter_" + random_id + "',this.value);");
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');").attr("name", "ux_ddl_autocomplete_" + random_id);
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").attr("name", "ux_ddl_disable_input_" + random_id);
										jQuery("#restriction_" + random_id).find(".input_mask_settings,.custom_mask_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "paragraph_text_field_key_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("name", "ux_txt_default_value_" + random_id).attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
										break;
									case "select":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields");
										jQuery("#ux_div_single_line_text_" + random_id).attr("name","ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id","ux_div_widget_"+random_id);
										jQuery("#ux_div_widget_"+random_id).children("div:eq(0)").attr("id","ux_header_title_"+random_id).attr("name","ux_header_title_"+random_id);
										jQuery("#ux_header_title_"+random_id).children("div:eq(0)").attr("id","ux_header_title_left_"+random_id).attr("name","ux_header_title_left_"+random_id).html("<b> Select</b>");
										jQuery("#ux_header_title_"+random_id).children("input").attr("id","ux_control_type_"+random_id).attr("name","ux_control_type_"+random_id).val("select");
										jQuery("#ux_header_title_"+random_id).children("div:eq(1)").attr("id","ux_header_title_right_"+random_id).attr("name","ux_header_title_right_"+random_id);
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(0)").attr("id","ux_expand_edit_fields_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(1)").attr("id","ux_duplicate_fields_"+random_id).attr("onclick","duplicate_fields_contact_bank('select',"+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(2)").attr("id","ux_delete_fields_"+random_id).attr("onclick","delete_controls_contact_bank('ux_div_single_line_text_"+random_id+"');");
										jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
										jQuery("#ux_sub_div_"+random_id).children("label").attr("id","field_label_"+random_id).attr("name","field_label_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(0)").attr("id","ux_label_title_"+random_id).attr("name","ux_label_title_"+random_id).text("Select");
										jQuery("#field_label_"+random_id).children("i").attr("id","ux_tooltip_title_"+random_id).attr("name","ux_tooltip_title_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(1)").remove();
										jQuery("#ux_sub_div_"+random_id).children("span:eq(0)").attr("id","ux_text_appear_after_counter_"+random_id).attr("name","ux_text_appear_after_counter_"+random_id);
										jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");
										jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#ux_sub_div_"+random_id).children("input").attr("id","ux_txt_singal_line_text_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_singal_line_text_"+random_id+"');");
										jQuery('#ux_txt_singal_line_text_'+random_id).replaceWith(jQuery('<select name=ux_txt_singal_line_text_'+random_id+' id=ux_txt_singal_line_text_'+random_id+' class=untitled_control>'));
										jQuery('#ux_txt_singal_line_text_'+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_singal_line_text_"+random_id+"');").attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
										jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
										jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);

										jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("name","ux_txt_label_field_"+random_id).attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)").val("Select");
										jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("name","ux_txt_description_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
										jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("name","ux_ddl_label_placement_"+random_id).attr("id","ux_ddl_label_placement_"+random_id).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")");
										jQuery("#general_"+random_id).find(".date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings,.html_editor,.logical_captcha_settings").remove();

										jQuery("#ux_div_single_line_text_"+random_id).find(".options_settings").children("a").attr("href","#option_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".options_settings").attr("id","option_"+random_id).attr("name","option_"+random_id);
										jQuery("#option_"+random_id).find("input:eq(0)").attr("id","ux_txt_add_form_option_"+random_id).attr("name","ux_txt_add_form_option_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_option_"+random_id+"');");
										jQuery("#option_"+random_id).find("input:eq(1)").attr("id","ux_txt_add_form_values_"+random_id).attr("name","ux_txt_add_form_values_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_values_"+random_id+"');");
										jQuery("#option_"+random_id).find("input:eq(2)").attr("id","ux_btn_add_options_"+random_id).attr("name","ux_btn_add_options_"+random_id).attr("onclick","add_select_options_contact_bank("+random_id+", 'select')");
										jQuery("#option_"+random_id).find("input:eq(3)").attr("id","ux_btn_add_import_"+random_id);
										jQuery("#option_"+random_id).find("input:eq(4)").attr("id","ux_hidden_options_values_"+random_id).attr("name","ux_hidden_options_values_"+random_id);
										jQuery("#option_"+random_id).find("div:eq(4)").attr("id","ux_drop_down_value_"+random_id);
										jQuery("#ux_drop_down_value_"+random_id).css("display","none");

										jQuery("#ux_drop_down_value_"+random_id).find("select:eq(0)").attr("id", "ux_ddl_options_required_"+random_id).attr("name","ux_ddl_options_required_"+random_id);
										jQuery("#ux_drop_down_value_"+random_id).find("input:eq(0)").attr("id","ux_btn_delete_option_"+random_id);
										jQuery("#ux_btn_delete_option_"+random_id).hide();

										jQuery("#option_"+random_id).find("select:eq(0)").attr("id","ux_ddl_options_required_"+random_id).attr("name","ux_ddl_options_required_"+random_id);
										jQuery("#ux_btn_add_import_"+random_id).attr("onclick","contact_bank_open_popup("+random_id+");").attr("data-popup-open","ux_open_popup_translator_"+random_id);
										jQuery("#option_"+random_id).find("textarea").attr("id","ux_txt_textarea_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_textarea_"+random_id+"');");
										jQuery("#option_"+random_id).find(".popup").attr("data-popup","ux_open_popup_translator_"+random_id);
										jQuery("#option_"+random_id).find(".popup").find(".btn:eq(0)").attr("id","ux_txt_popup_import_"+random_id);
										jQuery("#option_"+random_id).find(".popup").find(".btn:eq(1)").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
										jQuery("#ux_txt_popup_import_"+random_id).attr("onclick","import_select_options_contact_bank("+random_id+", 'select')").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
										jQuery("#option_"+random_id).find(".modal-footer").find("input:eq(1)").attr("onclick","contact_bank_close_popup_box("+random_id+")");

										jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
										jQuery("#apperance_"+random_id).find(".expiry_date_placeholder_settings,.expiry_date_placeholder_settings,.card_number_placeholder_settings,.card_cvv_number_placeholder_settings,.placeholder_settings").remove();
										jQuery("#apperance_"+random_id).find(".rows_number,.custom_validation_settings").remove();
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");

										jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").attr("href","#restriction_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".restrictions_settings").attr("id","restriction_"+random_id).attr("name","restriction_"+random_id);
										jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id","ux_ddl_autocomplete_"+random_id).attr("onchange","enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_autocomplete_"+random_id+"');").attr("name","ux_ddl_autocomplete_"+random_id);
										jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id","ux_ddl_disable_input_"+random_id).attr("onchange","disable_fields_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_disable_input_"+random_id+"');").attr("name","ux_ddl_disable_input_"+random_id);
										jQuery("#restriction_"+random_id).find(".custom_mask_settings").attr("id","ux_div_custom_mask_settings_"+random_id).attr("name","ux_div_custom_mask_settings_"+random_id);
										jQuery("#restriction_"+random_id).find(".required_settings,.custom_mask_settings,.input_mask_settings,.limit_input_number_settings,.text_appear_settings").remove();

										jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
										jQuery("#advanced_"+random_id).find("div:eq(0)").children("input").attr("id","single_line_text_field_key_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'single_line_text_field_key_"+random_id+"');").attr("name","single_line_text_field_key_"+random_id).attr("value","select_field_key_"+random_id);
										jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").remove();
										jQuery("#advanced_"+random_id).find(".default_value_settings").find(".us-states,.countries-list").remove();
										jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(0) .form-group").append("<select class='form-control custom-drop-down input-inline'></select>");
										jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(0) .form-group").find("select").attr("id","ux_txt_default_value_"+random_id).attr("name","ux_txt_default_value_"+random_id).attr("onchange","set_default_value_contact_bank("+random_id+")");
										jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_admin_label_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_admin_label_"+random_id+"');").attr("name","ux_txt_admin_label_"+random_id);
										break;
									case "first_name":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields").attr("name","ux_div_single_line_text_" + random_id);
										jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id","ux_div_widget_"+random_id);
										jQuery("#ux_div_widget_"+random_id).children("div:eq(0)").attr("id","ux_header_title_"+random_id).attr("name","ux_header_title_"+random_id);
										jQuery("#ux_header_title_"+random_id).children("div:eq(0)").attr("id","ux_header_title_left_"+random_id).html('<b>First Name</b>').attr("name","ux_header_title_left_"+random_id);
										jQuery("#ux_header_title_"+random_id).children("input").attr("id","ux_control_type_"+random_id).attr("name","ux_control_type_"+random_id).val("first_name");
										jQuery("#ux_header_title_"+random_id).children("div:eq(1)").attr("id","ux_header_title_right_"+random_id).attr("id","ux_header_title_right_"+random_id).attr("name","ux_header_title_right_"+random_id);
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(0)").attr("id","ux_expand_edit_fields_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(1)").attr("id","ux_duplicate_fields_"+random_id).attr("onclick","duplicate_fields_contact_bank('first_name',"+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(2)").attr("id","ux_delete_fields_"+random_id).attr("onclick","delete_controls_contact_bank('ux_div_single_line_text_"+random_id+"',"+random_id+");");

										jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
										jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#ux_sub_div_"+random_id).children("label").attr("id","field_label_"+random_id).attr("name","field_label_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(0)").attr("id","ux_label_title_"+random_id).attr("name","ux_label_title_"+random_id).text("First Name");
										jQuery("#field_label_"+random_id).children("i").attr("id","ux_tooltip_title_"+random_id).attr("name","ux_tooltip_title_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(1)").attr("id","ux_required_"+random_id).attr("name","ux_required_"+random_id);
										jQuery("#ux_sub_div_"+random_id).children("span:eq(0)").attr("id","ux_text_appear_after_counter_"+random_id).attr("name","ux_text_appear_after_counter_"+random_id);
										jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");

										jQuery("#ux_sub_div_"+random_id).children("input").attr("id","ux_txt_singal_line_text_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_singal_line_text_"+random_id+"');");
										jQuery("#ux_txt_singal_line_text_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
										jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
										jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);

										jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("name","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)").val("First Name");
										jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("name","ux_txt_description_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
										jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("id","ux_ddl_label_placement_"+random_id).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")").attr("name","ux_ddl_label_placement_"+random_id);
										jQuery("#general_"+random_id).find(".logical_captcha_settings,.html_editor,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();

										jQuery("#ux_div_single_line_text_"+random_id).find(".options_settings").remove();
										jQuery("#ux_div_tab_contents_"+random_id).children(".options_settings").remove();

										jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
										jQuery("#apperance_"+random_id).find(".rows_number,.expiry_date_placeholder_settings,.expiry_date_placeholder_settings,.card_number_placeholder_settings,.card_cvv_number_placeholder_settings").remove();
										jQuery("#apperance_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_placeholder_field_"+random_id).attr("name","ux_txt_placeholder_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_placeholder_field_"+random_id+"');").attr("onkeyup","change_placeholder_content_contact_bank('ux_txt_singal_line_text_"+random_id+"',this.value);");
										jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_"+random_id+"');").attr("name", "ux_txt_custom_validation_field_" + random_id);
										jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_element_class_"+random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_element_class_"+random_id+"');");

										jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');").attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name","ux_txt_container_class_"+random_id)
										jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").attr("href","#restriction_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".restrictions_settings").attr("id","restriction_"+random_id).attr("name","restriction_"+random_id);
										jQuery("#restriction_"+random_id).find("div:eq(0)").children("select").attr("id","ux_ddl_required_"+random_id).attr("onchange","enable_disable_required_contact_bank('ux_ddl_required_"+random_id+"','ux_required_"+random_id+"');").attr("name","ux_ddl_required_"+random_id);
										jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id","ux_ddl_autocomplete_"+random_id).attr("onchange","enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_autocomplete_"+random_id+"');").attr("name","ux_ddl_autocomplete_"+random_id);
										jQuery("#restriction_"+random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id","ux_ddl_disable_input_"+random_id).attr("onchange","disable_fields_contact_bank('ux_txt_singal_line_text_"+random_id+"','ux_ddl_disable_input_"+random_id+"');").attr("name","ux_ddl_disable_input_"+random_id);
										jQuery("#restriction_"+random_id).find(".text_appear_settings,.limit_input_number_settings,.input_mask_settings,.custom_mask_settings").remove();

										jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
										jQuery("#advanced_"+random_id).find("div:eq(0)").children("input").attr("id","single_line_text_field_key_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'single_line_text_field_key_"+random_id+"');").attr("name","single_line_text_field_key_"+random_id).attr("value","first_name_field_key_"+random_id);
										jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_default_value_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_default_value_"+random_id+"');").attr("name","ux_txt_default_value_"+random_id).attr("onkeyup","control_default_value_contact_bank('ux_txt_singal_line_text_"+random_id+"',this.value);");
										jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_admin_label_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_admin_label_"+random_id+"');").attr("name","ux_txt_admin_label_"+random_id);
										break;
									case "last_name":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields").attr("name", "ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id);
										jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).html("<b>Last Name</b>").attr("name", "ux_header_title_left_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("last_name");
										jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('last_name'," + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

										jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
										jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
										jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
										jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id).text("Last Name");
										jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
										jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");

										jQuery("#ux_sub_div_" + random_id).children("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");
										jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
										jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
										jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);

										jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("name", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)").val("Last Name");
										jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("name", "ux_txt_description_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
										jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")").attr("name", "ux_ddl_label_placement_" + random_id);
										jQuery("#general_" + random_id).find(".logical_captcha_settings,.html_editor,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".options_settings").remove();
										jQuery("#ux_div_tab_contents_" + random_id).children(".options_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
										jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_"+random_id+"');").attr("name", "ux_txt_custom_validation_field_" + random_id);
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');").attr("onkeyup","append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_custom_validation_field_" + random_id);
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');").attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id);
										jQuery("#apperance_"+random_id).find(".rows_number,.expiry_date_placeholder_settings,.expiry_date_placeholder_settings,.card_number_placeholder_settings,.card_cvv_number_placeholder_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id);
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');").attr("name", "ux_ddl_autocomplete_" + random_id);
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").attr("name", "ux_ddl_disable_input_" + random_id);
										jQuery("#restriction_" +random_id).find(".limit_input_number_settings,.text_appear_settings,.custom_mask_settings,.input_mask_settings").remove();
										jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "last_name_field_key_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("name", "ux_txt_default_value_" + random_id).attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id).attr("name", "ux_txt_admin_label_" + random_id);
										break;
										case "email":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields");
										jQuery("#ux_div_single_line_text_" + random_id).attr("name","ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id","ux_div_widget_"+random_id);
										jQuery("#ux_div_widget_"+random_id).children("div:eq(0)").attr("id","ux_header_title_"+random_id).attr("name","ux_header_title_"+random_id);
										jQuery("#ux_header_title_"+random_id).children("div:eq(0)").attr("id","ux_header_title_left_"+random_id).attr("name","ux_header_title_left_"+random_id).html("<b>Email Address</b>");
										jQuery("#ux_header_title_"+random_id).children("input").attr("id","ux_control_type_"+random_id).attr("name","ux_control_type_"+random_id).val("email");
										jQuery("#ux_header_title_"+random_id).children("div:eq(1)").attr("id","ux_header_title_right_"+random_id).attr("name","ux_header_title_right_"+random_id);
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(0)").attr("id","ux_expand_edit_fields_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(1)").attr("id","ux_duplicate_fields_"+random_id).attr("onclick","duplicate_fields_contact_bank('email',"+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(2)").attr("id","ux_delete_fields_"+random_id).attr("onclick","delete_controls_contact_bank('ux_div_single_line_text_"+random_id+"',"+random_id+");");
										jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
										jQuery("#ux_sub_div_"+random_id).children("label").attr("id","field_label_"+random_id).attr("name","field_label_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(0)").attr("id","ux_label_title_"+random_id).attr("name","ux_label_title_"+random_id).text("Email");
										jQuery("#field_label_"+random_id).children("i").attr("id","ux_tooltip_title_"+random_id).attr("name","ux_tooltip_title_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(1)").attr("id","ux_required_"+random_id).attr("name","ux_required_"+random_id);
										jQuery("#ux_sub_div_"+random_id).children("span:eq(0)").attr("id","ux_text_appear_after_counter_"+random_id).attr("name","ux_text_appear_after_counter_"+random_id);
										jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");
										jQuery("#ux_sub_div_"+random_id).children("input").attr("id","ux_txt_singal_line_text_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_singal_line_text_"+random_id+"');");
										jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#ux_txt_singal_line_text_"+random_id).removeAttr("autocomplete");
										jQuery("#ux_txt_singal_line_text_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
										jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
										jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("name","ux_txt_label_field_"+random_id).attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)").val("Email");
										jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("name","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
										jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("id","ux_ddl_label_placement_"+random_id).attr("name","ux_ddl_label_placement_"+random_id).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")");
										jQuery("#general_"+random_id).find(".logical_captcha_settings,.html_editor,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();
										jQuery("#ux_div_single_line_text_"+random_id).find(".options_settings").remove();
										jQuery("#ux_div_tab_contents_"+random_id).children(".options_settings").remove();
										jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
										jQuery("#apperance_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_placeholder_field_"+random_id).attr("name","ux_txt_placeholder_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_placeholder_field_"+random_id+"');");
										jQuery("#apperance_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_placeholder_field_"+random_id).attr("onkeyup","change_placeholder_content_contact_bank('ux_txt_singal_line_text_"+random_id+"',this.value);");
										jQuery("#apperance_"+random_id).find(".custom_validation_settings").children("input").attr("id","ux_txt_custom_validation_field_"+random_id).attr("name","ux_txt_custom_validation_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_custom_validation_field_"+random_id+"');");
										jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("name","ux_txt_container_class_"+random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');");
										jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_element_class_"+random_id).attr("name","ux_txt_element_class_"+random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_element_class_"+random_id+"');");
										jQuery("#apperance_" + random_id).find(".rows_number,.card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings").remove();
										jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").attr("href","#restriction_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".restrictions_settings").attr("id","restriction_"+random_id).attr("name","restriction_"+random_id);
										jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id);
										jQuery("#restriction_"+random_id).find(".limit_input_number_settings,.custom_mask_settings,.text_appear_settings,.autocomplete_settings,.input_mask_settings").remove();
										jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
										jQuery("#advanced_"+random_id).find("div:eq(0)").children("input").attr("id","single_line_text_field_key_"+random_id).attr("name","single_line_text_field_key_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'single_line_text_field_key_"+random_id+"');").attr("value","email_address_field_key_"+random_id);
										jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_default_value_"+random_id).attr("name","ux_txt_default_value_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_default_value_"+random_id+"');").attr("onkeyup","control_default_value_contact_bank('ux_txt_singal_line_text_"+random_id+"',this.value);");
										jQuery("#advanced_"+random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_admin_label_"+random_id).attr("name","ux_txt_admin_label_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_admin_label_"+random_id+"');");
										break;
									case "website_url":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields");
										jQuery("#ux_div_single_line_text_" + random_id).attr("name", "ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id);
										jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id).html("<b>Website URL</b>");
										jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("website_url");
										jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('website_url'," + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

										jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id).text("Website Url");
										jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
										jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
										jQuery("#ux_sub_div_" + random_id).children("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");
										jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
										jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
										jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("name", "ux_txt_label_field_" + random_id).attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)").val("Website Url");
										jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("name", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
										jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).attr("name", "ux_ddl_label_placement_" + random_id).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")");
										jQuery("#general_" + random_id).find(".logical_captcha_settings,.html_editor,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".options_settings").remove();
										jQuery("#ux_div_tab_contents_" + random_id).children(".options_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
										jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("name", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("name", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("name", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".rows_number,.card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings").remove();
										jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("select").attr("id", "ux_ddl_limit_input_" + random_id).attr("name", "ux_ddl_limit_input_" + random_id).attr("onchange", "limit_input_event_contact_bank(" + random_id + ");");
										jQuery("#restriction_" + random_id).find(".text_appear_settings").children("input").attr("id", "ux_txt_text_appear_" + random_id).attr("name", "ux_txt_text_appear_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_text_appear_" + random_id + "');").attr("onkeyup", "change_error_message_content_contact_bank('ux_text_appear_after_counter_" + random_id + "',this.value);");
										jQuery("#restriction_" + random_id).find(".text_appear_settings,.limit_input_number_settings,.input_mask_settings,.custom_mask_settings").remove();
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).attr("name", "ux_ddl_autocomplete_" + random_id).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');");
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("name", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');");
										jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("name", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("value", "website_url_field_key_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("name", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("name", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');");
										break;
									case "phone":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields");
										jQuery("#ux_div_single_line_text_" + random_id).attr("name", "ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id);
										jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id);
										jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("name", "ux_header_title_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).html("<b>Phone</b>");
										jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("name", "ux_header_title_left_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("input").attr("name", "ux_control_type_" + random_id).val("phone");
										jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("name", "ux_header_title_right_" + random_id);
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('phone'," + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

										jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id).text("Phone");
										jQuery("#ux_div_widget_" + random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
										jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");

										jQuery("#ux_sub_div_" + random_id).children("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");
										jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeyup", "only_characters_contact_bank(event," + random_id + ");").attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
										jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
										jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);

										jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)").attr("name", "ux_txt_label_field_" + random_id).val("Phone");
										jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("name", "ux_txt_description_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
										jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")").attr("name", "ux_ddl_label_placement_" + random_id);
										jQuery("#general_" + random_id).find(".logical_captcha_settings,.html_editor,.date_settings,.time_settings,.number_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".options_settings").remove();
										jQuery("#ux_div_tab_contents_" + random_id).children(".options_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
										jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_"+random_id+"');").attr("name", "ux_txt_custom_validation_field_" + random_id);
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".rows_number,.card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("input").attr("id", "ux_txt_limit_input_" + random_id).val("10").attr("onkeypress","enter_only_digits_for_price(event)").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_limit_input_" + random_id + "');").attr("name", "ux_txt_limit_input_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("select").attr("id", "ux_ddl_limit_input_" + random_id).attr("onchange", "limit_input_event_contact_bank(" + random_id + ");").attr("name", "ux_ddl_limit_input_" + random_id);
										jQuery("#restriction_" + random_id).find(".text_appear_settings").children("input").attr("id", "ux_txt_text_appear_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_text_appear_" + random_id + "');").attr("name", "ux_txt_text_appear_" + random_id).attr("onkeyup", "change_error_message_content_contact_bank('ux_text_appear_after_counter_" + random_id + "',this.value);");
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');").attr("name", "ux_ddl_autocomplete_" + random_id);
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');").attr("name", "ux_ddl_disable_input_" + random_id);
										jQuery("#restriction_" + random_id).find(".custom_mask_settings").attr("id", "ux_div_custom_mask_settings_" + random_id).attr("name", "ux_div_custom_mask_settings_" + random_id);
										jQuery("#restriction_" + random_id).find(".custom_mask_settings").children("input").attr("id", "ux_txt_custom_mask_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_mask_" + random_id + "');").attr("name", "ux_txt_custom_mask_" + random_id).attr("onblur", "apply_input_masking_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_input_mask_" + random_id + "','ux_div_custom_mask_settings_" + random_id + "'," + random_id + ");");
										jQuery("#restriction_" + random_id).find(".custom_mask_settings").css("display", "none");
										jQuery("#restriction_" + random_id).find(".input_mask_settings").children("select").attr("id", "ux_ddl_input_mask_" + random_id).attr("onchange", "apply_input_masking_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_input_mask_" + random_id + "','ux_div_custom_mask_settings_" + random_id + "'," + random_id + ");").attr("name", "ux_ddl_input_mask_" + random_id);

										jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "phone_field_key_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("name", "ux_txt_default_value_" + random_id).attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
										break;
									case "number":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields");
										jQuery("#ux_div_single_line_text_" + random_id).attr("name", "ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id);
										jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).html("<b>Number</b>").attr("name", "ux_header_title_left_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("number");
										jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('number'," + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

										jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id).text("Number");
										jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltip_title_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
										jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
										jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();

										jQuery("#ux_sub_div_" + random_id).children("input").attr("id", "ux_txt_singal_line_text_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_singal_line_text_" + random_id + "');");
										jQuery("#ux_txt_singal_line_text_" + random_id).attr("onkeyup", "number_settings_contact_bank(" + random_id + ",event);").attr("onkeypress","enter_only_digits_for_price(event);").attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
										jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
										jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("name", "ux_txt_label_field_" + random_id).attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)").val("Number");
										jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
										jQuery("#general_" + random_id).find(".number_settings").find("div:eq(2)").children("input").attr("id", "ux_txt_min_number_" + random_id).attr("name", "ux_txt_min_number_" + random_id).val(jQuery("#ux_txt_min_number_"+random_id)).val("10").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_min_number_" + random_id + "');");
										jQuery("#general_" + random_id).find(".number_settings").find("div:eq(4)").children("input").attr("id", "ux_txt_max_number_" + random_id).attr("name", "ux_txt_max_number_" + random_id).val(jQuery("#ux_txt_max_number_"+random_id)).val("20").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_max_number_" + random_id + "');");
										jQuery("#general_" + random_id).find(".number_settings").find("div:eq(5)").children("input").attr("id", "ux_txt_step_" + random_id).attr("name", "ux_txt_step_" + random_id).val(jQuery("#ux_txt_step_"+random_id)).val("2").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_step_" + random_id + "');");
										jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("name", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
										jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).attr("name", "ux_ddl_label_placement_" + random_id).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")");
										jQuery("#general_" + random_id).find(".html_editor,.date_settings,.time_settings,.quantity_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.field_description_settings,.logical_captcha_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".options_settings").remove();
										jQuery("#ux_div_tab_contents_" + random_id).children(".options_settings").remove();
										jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
										jQuery("#apperance_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_placeholder_field_" + random_id).attr("name", "ux_txt_placeholder_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_placeholder_field_" + random_id + "');").attr("onkeyup", "change_placeholder_content_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("name", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');");
										jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');").attr("name","ux_txt_container_class_"+random_id).attr("onkeyup","append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');");
										jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id","ux_txt_element_class_"+random_id).attr("onkeyup","append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'untitled_control', '', '', '', '');").attr("name","ux_txt_element_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_element_class_"+random_id+"');");
										jQuery("#apperance_" + random_id).find(".rows_number,.card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("name", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');");
										jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("input").attr("id", "ux_txt_limit_input_" + random_id).attr("onkeypress","enter_only_digits_for_price(event)").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_limit_input_" + random_id + "');").attr("name", "ux_txt_limit_input_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(1)").find(".row .col-md-6").children("select").attr("id", "ux_ddl_limit_input_" + random_id).attr("name", "ux_ddl_limit_input_" + random_id).attr("onchange", "limit_input_event_contact_bank(" + random_id + ");");
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(0) .form-group").children("select").attr("id", "ux_ddl_autocomplete_" + random_id).attr("name", "ux_ddl_autocomplete_" + random_id).attr("onchange", "enable_disable_autocomplete_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_autocomplete_" + random_id + "');");
										jQuery("#restriction_" + random_id).find(".autocomplete_settings").find("div:eq(2) .form-group").children("select").attr("id", "ux_ddl_disable_input_" + random_id).attr("name", "ux_ddl_disable_input_" + random_id).attr("onchange", "disable_fields_contact_bank('ux_txt_singal_line_text_" + random_id + "','ux_ddl_disable_input_" + random_id + "');");
										jQuery("#restriction_" + random_id).find(".limit_input_number_settings,.text_appear_settings,.autocomplete_settings,.input_mask_settings,.custom_mask_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("name", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("value", "number_field_key_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_default_value_" + random_id).attr("name", "ux_txt_default_value_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_default_value_" + random_id + "');").attr("onkeyup", "control_default_value_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value);");
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("name", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');");
										break;
									case "checkbox":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields");
										jQuery("#ux_div_single_line_text_" + random_id).attr("name", "ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id", "ux_div_widget_" + random_id);
										jQuery("#ux_div_widget_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_" + random_id).attr("name", "ux_header_title_" + random_id);
										jQuery("#ux_header_title_" + random_id).children("div:eq(0)").attr("id", "ux_header_title_left_" + random_id).attr("name", "ux_header_title_left_" + random_id).html("<b>Checkbox</b>");
										jQuery("#ux_header_title_" + random_id).children("input").attr("id", "ux_control_type_" + random_id).attr("name", "ux_control_type_" + random_id).val("checkbox");
										jQuery("#ux_header_title_" + random_id).children("div:eq(1)").attr("id", "ux_header_title_right_" + random_id).attr("name", "ux_header_title_right_" + random_id);
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(0)").attr("id", "ux_expand_edit_fields_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(1)").attr("id", "ux_duplicate_fields_" + random_id).attr("onclick", "duplicate_fields_contact_bank('checkbox'," + random_id + ");");
										jQuery("#ux_header_title_right_" + random_id).children("a:eq(2)").attr("id", "ux_delete_fields_" + random_id).attr("onclick", "delete_controls_contact_bank('ux_div_single_line_text_" + random_id + "'," + random_id + ");");

										jQuery("#ux_div_widget_" + random_id).children("div:eq(1)").attr("id", "ux_sub_div_" + random_id).attr("name", "ux_sub_div_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("label").attr("id", "field_label_" + random_id).attr("name", "field_label_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(0)").attr("id", "ux_label_title_" + random_id).attr("name", "ux_label_title_" + random_id).text("Checkbox");
										jQuery("#field_label_" + random_id).children("i").attr("id", "ux_tooltip_title_" + random_id).attr("name", "ux_tooltux_txt_label_field_ip_title_" + random_id);
										jQuery("#field_label_" + random_id).children("span:eq(1)").attr("id", "ux_required_" + random_id).attr("name", "ux_required_" + random_id);
										jQuery("#ux_sub_div_" + random_id).children("span:eq(0)").attr("id", "ux_text_appear_after_counter_" + random_id).attr("name", "ux_text_appear_after_counter_" + random_id);
										jQuery("#ux_text_appear_after_counter_" + random_id).css("display", "none");
										jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#ux_sub_div_" + random_id).children("input").attr("id", "ux_txt_singal_line_text_" + random_id);
										jQuery('#ux_txt_singal_line_text_' + random_id).replaceWith(jQuery('<input type=checkbox name=ux_txt_singal_line_text_' + random_id + ' id=ux_txt_singal_line_text_' + random_id + ' class=checkbox_class>'));
										jQuery("#ux_txt_singal_line_text_" + random_id).attr("onclick", "show_hide_text_field_options(" + random_id + ");");
										jQuery("#ux_div_single_line_text_" + random_id).children(".ux_div_widget_content").attr("id", "ux_div_widget_content_" + random_id).attr("name", "ux_div_widget_content_" + random_id);
										jQuery(".add_fields #ux_div_single_line_text_" + random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_" + random_id).find(".general_settings").children("a").attr("href", "#general_" + random_id);
										jQuery("#ux_div_widget_content_" + random_id).children("div:eq(0)").children("div:eq(0)").attr("id", "ux_div_tab_contents_" + random_id).attr("name", "ux_div_tab_contents_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".general_settings").attr("id", "general_" + random_id).attr("name", "general_" + random_id);

										jQuery("#general_" + random_id).find("div:eq(0)").children("label").attr("id", "ux_control_label_placeholder_" + random_id).attr("name", "ux_control_label_placeholder_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(0)").children("input").attr("id", "ux_txt_label_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_label_field_" + random_id + "');").attr("onkeyup", "change_label_name_contact_bank('ux_label_title_" + random_id + "',this.value)").attr("name", "ux_txt_label_field_" + random_id).val("Checkbox");
										jQuery("#general_" + random_id).find("div:eq(1)").children("label").attr("id", "ux_control_label_description_" + random_id).attr("name", "ux_control_label_description_" + random_id);
										jQuery("#general_" + random_id).find("div:eq(1)").children("input").attr("id", "ux_txt_description_field_" + random_id).attr("onkeyup", "change_tootltip_content_contact_bank('ux_tooltip_title_" + random_id + "',this.value);").attr("name", "ux_txt_description_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');").attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_description_field_" + random_id + "');");
										jQuery("#general_" + random_id).find("div:eq(2)").children("select").attr("id", "ux_ddl_label_placement_" + random_id).attr("onchange", "change_label_placement_contact_bank('ux_ddl_label_placement_" + random_id + "'," + random_id + ")").attr("name", "ux_ddl_label_placement_" + random_id);
										jQuery("#general_" + random_id).find(".html_editor,.field_description_settings,.quantity_settings,.date_settings,.time_settings,.number_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.html_editor,.logical_captcha_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".options_settings").remove();
										jQuery("#ux_div_tab_contents_" + random_id).children(".options_settings").remove();
										jQuery("#ux_div_single_line_text_" + random_id).find(".appearance_settings").children("a").attr("href", "#apperance_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".appearance_settings").attr("id", "apperance_" + random_id).attr("name", "apperance_" + random_id);
										jQuery("#apperance_" + random_id).find(".rows_number,.placeholder_settings, .card_number_placeholder_settings, .expiry_date_placeholder_settings, .card_cvv_number_placeholder_settings").remove();
										jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("id", "ux_txt_custom_validation_field_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_custom_validation_field_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".custom_validation_settings").children("input").attr("name", "ux_txt_custom_validation_field_" + random_id);
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id", "ux_txt_container_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');").attr("name", "ux_txt_container_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_container_class_" + random_id + "');");
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'checkbox_class', '', '', '', '');").attr("name", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');");

										jQuery("#ux_div_single_line_text_" + random_id).find(".restrictions_settings").children("a").attr("href", "#restriction_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".restrictions_settings").attr("id", "restriction_" + random_id).attr("name", "restriction_" + random_id);
										jQuery("#restriction_" + random_id).find("div:eq(0)").children("select").attr("id", "ux_ddl_required_" + random_id).attr("onchange", "enable_disable_required_contact_bank('ux_ddl_required_" + random_id + "','ux_required_" + random_id + "');").attr("name", "ux_ddl_required_" + random_id);
										jQuery("#restriction_" + random_id).find(".autocomplete_settings,.limit_input_number_settings,.text_appear_settings,.custom_mask_settings,.input_mask_settings").remove();

										jQuery("#ux_div_single_line_text_" + random_id).find(".advanced_settings").children("a").attr("href", "#advanced_" + random_id);
										jQuery("#ux_div_tab_contents_" + random_id).children(".advanced_settings").attr("id", "advanced_" + random_id).attr("name", "advanced_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "checkbox_field_key_" + random_id);
										jQuery("#advanced_" + random_id).find(".admin_label_settings").find("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
										jQuery("#advanced_" + random_id).find(".admin_label_settings").removeClass("col-md-6").addClass("col-md-12");
										jQuery("#advanced_" + random_id).find(".default_value_settings").remove();
										break;
									case "checkbox-list":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields").attr("name","ux_div_single_line_text_" + random_id);
										jQuery("#ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id","ux_div_widget_"+random_id);
										jQuery("#ux_div_widget_"+random_id).children("div:eq(0)").attr("id","ux_header_title_"+random_id).attr("name","ux_header_title_"+random_id);
										jQuery("#ux_header_title_"+random_id).children("div:eq(0)").attr("id","ux_header_title_left_"+random_id).attr("name","ux_header_title_left_"+random_id).html("<b>Checkbox List</b>");
										jQuery("#ux_header_title_"+random_id).children("input").attr("id","ux_control_type_"+random_id).attr("name","ux_control_type_"+random_id).val("checkbox-list");
										jQuery("#ux_header_title_"+random_id).children("div:eq(1)").attr("id","ux_header_title_right_"+random_id).attr("name","ux_header_title_right_"+random_id);
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(0)").attr("id","ux_expand_edit_fields_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(1)").attr("id","ux_duplicate_fields_"+random_id).attr("onclick","duplicate_fields_contact_bank('checkbox-list',"+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(2)").attr("id","ux_delete_fields_"+random_id).attr("onclick","delete_controls_contact_bank('ux_div_single_line_text_"+random_id+"');");
										jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
										jQuery("#ux_sub_div_"+random_id).children("label").attr("id","field_label_"+random_id).attr("name","field_label_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(0)").attr("id","ux_label_title_"+random_id).attr("name","ux_label_title_"+random_id).text("Checkbox List");
										jQuery("#field_label_"+random_id).children("i").attr("id","ux_tooltip_title_"+random_id).attr("name","ux_tooltip_title_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(1)").attr("id","ux_required_"+random_id).attr("name","ux_required_"+random_id);
										jQuery("#ux_sub_div_"+random_id).children("span:eq(0)").attr("id","ux_text_appear_after_counter_"+random_id).attr("name","ux_text_appear_after_counter_"+random_id);
										jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");

										jQuery("#ux_sub_div_"+random_id).find("input").attr("id","ux_txt_singal_line_text_"+random_id).attr("onkeyup","append_class_contact_bank('ux_txt_singal_line_text_" + random_id + "',this.value, 'checkbox_class_" + random_id + "', '', '', " + random_id + ", 'checkbox-list');");
										jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#ux_div_single_line_text_" + random_id).find(".sub_div").find('#ux_txt_singal_line_text_' + random_id).before("<span id=ux_txt_check_box_"+random_id+" name=ux_txt_check_box_"+random_id+" class=checkbox-label></span>");
										jQuery("#ux_div_single_line_text_" + random_id).find(".sub_div").find("#ux_txt_check_box_"+random_id).append("<label id=field_labels_"+random_id+" name=field_labels_"+random_id+"></label>");
										jQuery('#ux_txt_singal_line_text_'+random_id).replaceWith(jQuery('<input type=checkbox name=ux_txt_singal_line_text_'+random_id+' id=ux_txt_singal_line_text_'+random_id+' class=checkbox_class>'));
										jQuery("#ux_txt_singal_line_text_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
										jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
										jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("name","ux_txt_label_field_"+random_id).attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)").val("Checkbox List");
										jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("name","ux_txt_description_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
										jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("name","ux_ddl_label_placement_"+random_id).attr("id","ux_ddl_label_placement_"+random_id).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")");
										jQuery("#general_"+random_id).find(".field_description_settings,.quantity_settings,.date_settings,.time_settings,.number_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.html_editor,.logical_captcha_settings").remove();

										jQuery("#ux_div_single_line_text_"+random_id).find(".options_settings").children("a").attr("href","#option_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".options_settings").attr("id","option_"+random_id).attr("name","option_"+random_id);
										jQuery("#option_"+random_id).find("input:eq(0)").attr("id","ux_txt_add_form_option_"+random_id).attr("name","ux_txt_add_form_option_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_option_"+random_id+"');");
										jQuery("#option_"+random_id).find("input:eq(1)").attr("id","ux_txt_add_form_values_"+random_id).attr("name","ux_txt_add_form_values_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_values_"+random_id+"');");
										jQuery("#option_"+random_id).find("input:eq(2)").attr("id","ux_btn_add_options_"+random_id).attr("name","ux_btn_add_options_"+random_id).attr("onclick","add_control_options_contact_bank("+random_id+",'checkbox');");
										jQuery("#option_"+random_id).find("input:eq(3)").attr("id","ux_btn_add_import_"+random_id);
										jQuery("#option_"+random_id).find("input:eq(4)").attr("id","ux_hidden_options_values_"+random_id).attr("name","ux_hidden_options_values_"+random_id);
										jQuery("#option_"+random_id).find("div:eq(4)").attr("id","ux_drop_down_value_"+random_id);
										jQuery("#ux_drop_down_value_"+random_id).css("display","none");

										jQuery("#option_"+random_id).find("select:eq(0)").attr("id","ux_ddl_options_required_"+random_id).attr("name","ux_ddl_options_required_"+random_id);
										jQuery("#ux_drop_down_value_"+random_id).find("input:eq(0)").attr("id","ux_btn_delete_option_"+random_id);
										jQuery("#ux_btn_delete_option_"+random_id).hide();

										jQuery("#ux_btn_add_import_"+random_id).attr("onclick","contact_bank_open_popup("+random_id+");").attr("data-popup-open","ux_open_popup_translator_"+random_id);
										jQuery("#option_"+random_id).find("textarea").attr("id","ux_txt_textarea_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_textarea_"+random_id+"');");
										jQuery("#option_"+random_id).find(".popup").attr("data-popup","ux_open_popup_translator_"+random_id);
										jQuery("#option_"+random_id).find(".popup").find(".btn:eq(0)").attr("id","ux_txt_popup_import_"+random_id);
										jQuery("#option_"+random_id).find(".popup").find(".btn:eq(1)").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
										jQuery("#ux_txt_popup_import_"+random_id).attr("onclick","import_controls_values_contact_bank("+random_id+",'checkbox')").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
										jQuery("#option_"+random_id).find(".modal-footer").find("input:eq(1)").attr("onclick","contact_bank_close_popup_box("+random_id+")");

										jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
										jQuery("#apperance_"+random_id).find(".card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings,.rows_number,.placeholder_settings").remove();
										jQuery("#apperance_"+random_id).find(".custom_validation_settings").find("input").attr("id","ux_txt_custom_validation_field_"+random_id).attr("name","ux_txt_custom_validation_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_custom_validation_field_"+random_id+"');");
										jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');").attr("name","ux_txt_container_class_"+random_id).attr("onkeyup","append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');");
										jQuery("#apperance_" + random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_element_class_" + random_id + "');").attr("onkeyup", "append_class_contact_bank('ux_txt_check_box_lists_" + random_id + "',this.value, 'checkbox_class_"+random_id+"', '', '', "+random_id+", 'checkbox-list');").attr("name", "ux_txt_element_class_" + random_id);

										jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").attr("href","#restriction_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".restrictions_settings").attr("id","restriction_"+random_id).attr("name","restriction_"+random_id);
										jQuery("#restriction_"+random_id).find("div:eq(0)").children("select").attr("name","ux_ddl_required_"+random_id).attr("id","ux_ddl_required_"+random_id).attr("onchange","enable_disable_required_contact_bank('ux_ddl_required_"+random_id+"','ux_required_"+random_id+"');");
										jQuery("#restriction_"+random_id).find(".autocomplete_settings,.limit_input_number_settings,.custom_mask_settings,.text_appear_settings,.input_mask_settings").remove();

										jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
										jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "checkbox_list_key_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
										jQuery("#advanced_" + random_id).find(".admin_label_settings").removeClass("col-md-6").addClass("col-md-12");
										jQuery("#advanced_" + random_id).find(".default_value_settings").remove();
										break;
									case "radio-list":
										jQuery("#ux_div_single_line_text").clone(false).attr("id", "ux_div_single_line_text_" + random_id).appendTo(".add_fields");
										jQuery("#ux_div_single_line_text_" + random_id).attr("name","ux_div_single_line_text_" + random_id).attr("data-timestamp",random_id);
										jQuery("#ux_div_single_line_text_" + random_id).children("div").attr("id","ux_div_widget_"+random_id);
										jQuery("#ux_div_widget_"+random_id).children("div:eq(0)").attr("id","ux_header_title_"+random_id).attr("name","ux_header_title_"+random_id);
										jQuery("#ux_header_title_"+random_id).children("div:eq(0)").attr("id","ux_header_title_left_"+random_id).attr("name","ux_header_title_left_"+random_id).html("<b>Radio List</b>");
										jQuery("#ux_header_title_"+random_id).children("input").attr("id","ux_control_type_"+random_id).attr("name","ux_control_type_"+random_id).val("radio-list");
										jQuery("#ux_header_title_"+random_id).children("div:eq(1)").attr("id","ux_header_title_right_"+random_id).attr("name","ux_header_title_right_"+random_id);
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(0)").attr("id","ux_expand_edit_fields_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(1)").attr("id","ux_duplicate_fields_"+random_id).attr("onclick","duplicate_fields_contact_bank('radio-list',"+random_id+");");
										jQuery("#ux_header_title_right_"+random_id).children("a:eq(2)").attr("id","ux_delete_fields_"+random_id).attr("onclick","delete_controls_contact_bank('ux_div_single_line_text_"+random_id+"');");
										jQuery("#ux_div_widget_"+random_id).children("div:eq(1)").attr("id","ux_sub_div_"+random_id).attr("name","ux_sub_div_"+random_id);
										jQuery("#ux_sub_div_"+random_id).children("label").attr("id","field_label_"+random_id).attr("name","field_label_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(0)").attr("id","ux_label_title_"+random_id).attr("name","ux_label_title_"+random_id).text("Radio List");
										jQuery("#field_label_"+random_id).children("i").attr("id","ux_tooltip_title_"+random_id).attr("name","ux_tooltip_title_"+random_id);
										jQuery("#field_label_"+random_id).children("span:eq(1)").remove();
										jQuery("#ux_sub_div_"+random_id).children("span:eq(0)").attr("id","ux_text_appear_after_counter_"+random_id).attr("name","ux_text_appear_after_counter_"+random_id);
										jQuery("#ux_text_appear_after_counter_"+random_id).css("display","none");

										jQuery("#ux_sub_div_"+random_id).children("input").attr("id","ux_txt_singal_line_text_"+random_id);
										jQuery("#ux_div_widget_"+random_id).find(".sub_div_credit_card,.sub_div_section_break").remove();
										jQuery("#ux_sub_div_"+random_id).find("#ux_ddl_us_states,#ux_ddl_country,.default_text").remove();
										jQuery("#ux_div_single_line_text_" + random_id).find(".sub_div").find('#ux_txt_singal_line_text_' + random_id).before("<span id=ux_txt_check_box_"+random_id+" name=ux_txt_check_box_"+random_id+" class=checkbox-label></span>");
										jQuery("#ux_div_single_line_text_" + random_id).find(".sub_div").find("#ux_txt_check_box_"+random_id).append("<label id=field_labels_"+random_id+" name=field_labels_"+random_id+"></label>");
										jQuery('#ux_txt_singal_line_text_'+random_id).replaceWith(jQuery('<input type=radio name=ux_txt_singal_line_text_'+random_id+' id=ux_txt_singal_line_text_'+random_id+' class=checkbox_class>'));
										jQuery("#ux_txt_singal_line_text_"+random_id).attr("onclick","show_hide_text_field_options("+random_id+");");
										jQuery("#ux_div_single_line_text_"+random_id).children(".ux_div_widget_content").attr("id","ux_div_widget_content_"+random_id).attr("name","ux_div_widget_content_"+random_id);
										jQuery(".add_fields #ux_div_single_line_text_"+random_id).css({"display": "block", "border": "1px solid #fff", "padding": "5px"});
										jQuery("#ux_div_single_line_text_"+random_id).find(".general_settings").children("a").attr("href","#general_"+random_id);
										jQuery("#ux_div_widget_content_"+random_id).children("div:eq(0)").children("div:eq(0)").attr("id","ux_div_tab_contents_"+random_id).attr("name","ux_div_tab_contents_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".general_settings").attr("id","general_"+random_id).attr("name","general_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(0)").children("label").attr("id","ux_control_label_placeholder_"+random_id).attr("name","ux_control_label_placeholder_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(0)").children("input").attr("id","ux_txt_label_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_label_field_"+random_id+"');").attr("name","ux_txt_label_field_"+random_id).attr("onkeyup","change_label_name_contact_bank('ux_label_title_"+random_id+"',this.value)").val("Radio List");
										jQuery("#general_"+random_id).find("div:eq(1)").children("label").attr("id","ux_control_label_description_"+random_id).attr("name","ux_control_label_description_"+random_id);
										jQuery("#general_"+random_id).find("div:eq(1)").children("input").attr("id","ux_txt_description_field_"+random_id).attr("onkeyup","change_tootltip_content_contact_bank('ux_tooltip_title_"+random_id+"',this.value);").attr("name","ux_txt_description_field_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_description_field_"+random_id+"');");
										jQuery("#general_"+random_id).find("div:eq(2)").children("select").attr("name","ux_ddl_label_placement_"+random_id).attr("id","ux_ddl_label_placement_"+random_id).attr("onchange","change_label_placement_contact_bank('ux_ddl_label_placement_"+random_id+"',"+random_id+")");
										jQuery("#general_"+random_id).find(".field_description_settings,.quantity_settings,.date_settings,.time_settings,.number_settings,.file_upload_settings,.anti_spam_settings,.product_settings,.shipping_settings,.credit_card_settings,.star_rating,.html_editor,.logical_captcha_settings").remove();

										jQuery("#ux_div_single_line_text_"+random_id).find(".options_settings").children("a").attr("href","#option_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".options_settings").attr("id","option_"+random_id).attr("name","option_"+random_id);
										jQuery("#option_"+random_id).find("input:eq(0)").attr("id","ux_txt_add_form_option_"+random_id).attr("name","ux_txt_add_form_option_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_option_"+random_id+"');");
										jQuery("#option_"+random_id).find("input:eq(1)").attr("id","ux_txt_add_form_values_"+random_id).attr("name","ux_txt_add_form_values_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_add_form_values_"+random_id+"');");
										jQuery("#option_"+random_id).find("input:eq(2)").attr("id","ux_btn_add_options_"+random_id).attr("name","ux_btn_add_options_"+random_id).attr("onclick","add_control_options_contact_bank("+random_id+",'radio');");
										jQuery("#option_"+random_id).find("input:eq(3)").attr("id","ux_btn_add_import_"+random_id);
										jQuery("#option_"+random_id).find("input:eq(4)").attr("id","ux_hidden_options_values_"+random_id).attr("name","ux_hidden_options_values_"+random_id);
										jQuery("#option_"+random_id).find("div:eq(4)").attr("id","ux_drop_down_value_"+random_id);
										jQuery("#ux_drop_down_value_"+random_id).css("display","none");

										jQuery("#ux_drop_down_value_"+random_id).find("select:eq(0)").attr("id", "ux_ddl_options_required_"+random_id).attr("name","ux_ddl_options_required_"+random_id);
										jQuery("#ux_drop_down_value_"+random_id).find("input:eq(0)").attr("id","ux_btn_delete_option_"+random_id);
										jQuery("#ux_btn_delete_option_"+random_id).hide();
										jQuery("#ux_btn_add_import_"+random_id).attr("onclick","contact_bank_open_popup("+random_id+");").attr("data-popup-open","ux_open_popup_translator_"+random_id);
										jQuery("#option_"+random_id).find("textarea").attr("id","ux_txt_textarea_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_textarea_"+random_id+"');");
										jQuery("#option_"+random_id).find(".popup").attr("data-popup","ux_open_popup_translator_"+random_id);
										jQuery("#option_"+random_id).find(".popup").find(".btn:eq(0)").attr("id","ux_txt_popup_import_"+random_id);
										jQuery("#option_"+random_id).find(".popup").find(".btn:eq(1)").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
										jQuery("#ux_txt_popup_import_"+random_id).attr("onclick","import_controls_values_contact_bank("+random_id+",'radio')").attr("data-popup-close-translator","ux_open_popup_translator_"+random_id);
										jQuery("#option_"+random_id).find(".modal-footer").find("input:eq(1)").attr("onclick","contact_bank_close_popup_box("+random_id+")");

										jQuery("#ux_div_single_line_text_"+random_id).find(".appearance_settings").children("a").attr("href","#apperance_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".appearance_settings").attr("id","apperance_"+random_id).attr("name","apperance_"+random_id);
										jQuery("#apperance_"+random_id).find(".custom_validation_settings,.card_number_placeholder_settings,.expiry_date_placeholder_settings,.card_cvv_number_placeholder_settings,.rows_number,.placeholder_settings").remove();
										jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(0) .form-group").children("input").attr("id","ux_txt_container_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_container_class_"+random_id+"');").attr("name","ux_txt_container_class_"+random_id).attr("onkeyup","append_class_contact_bank('ux_sub_div_" + random_id + "',this.value, 'sub_div', 'field_label', 'control-label', '', '');");
										jQuery("#apperance_"+random_id).find(".class_settings").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_element_class_" + random_id).attr("onkeyup", "append_class_contact_bank('ux_txt_check_box_lists_" + random_id + "',this.value, 'checkbox_class_"+random_id+"', '', '', "+random_id+", 'radio-list');").attr("name", "ux_txt_element_class_" + random_id).attr("name","ux_txt_element_class_"+random_id).attr("onkeydown","select_all_content_contact_bank(event,'ux_txt_element_class_"+random_id+"');");
										jQuery("#ux_div_single_line_text_"+random_id).find(".restrictions_settings").children("a").remove();

										jQuery("#ux_div_single_line_text_"+random_id).find(".advanced_settings").children("a").attr("href","#advanced_"+random_id);
										jQuery("#ux_div_tab_contents_"+random_id).children(".advanced_settings").attr("id","advanced_"+random_id).attr("name","advanced_"+random_id);
										jQuery("#advanced_" + random_id).find("div:eq(0)").children("input").attr("id", "single_line_text_field_key_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'single_line_text_field_key_" + random_id + "');").attr("name", "single_line_text_field_key_" + random_id).attr("value", "radio_list_key_" + random_id);
										jQuery("#advanced_" + random_id).find("div:eq(1)").find("div:eq(2) .form-group").children("input").attr("id", "ux_txt_admin_label_" + random_id).attr("onkeydown", "select_all_content_contact_bank(event,'ux_txt_admin_label_" + random_id + "');").attr("name", "ux_txt_admin_label_" + random_id);
										jQuery("#advanced_" + random_id).find(".admin_label_settings").removeClass("col-md-6").addClass("col-md-12");
										jQuery("#advanced_" + random_id).find(".default_value_settings").remove();
										break;
								}
								jQuery(".tooltips").tooltip_tip({placement: "right"});
								return random_id;
							}
							function contact_bank_move_to_second_step() {
								jQuery("#ux_div_first_step").addClass("first-step-helper");
								contact_bank_validate_settings();
							}
							function contact_bank_move_to_first_step() {
								jQuery("#ux_div_first_step").removeClass("first-step-helper");
								jQuery("#ux_div_first_step").css("display", "block");
								jQuery("#ux_div_second_step").css("display", "none");
								jQuery("#ux_div_step_progres_bar_width").css("width", "50%");
								jQuery("#ux_div_frm_wizard li:eq(1)").removeClass("active");
							}
							function contact_bank_move_to_third_step() {
								jQuery("#ux_div_first_step").removeClass("first-step-helper");
								contact_bank_validate_settings();
							}
							function contact_bank_second_step_settings() {
								jQuery("#ux_div_first_step").removeClass("first-step-helper");
								jQuery("#ux_div_first_step").css("display", "none");
								jQuery("#ux_div_second_step").css("display", "block");
								jQuery("#ux_div_step_progres_bar_width").css("width", "100%");
								jQuery("#ux_div_frm_wizard li:eq(1)").addClass("active");
								jQuery("#ux_div_frm_wizard li:eq(2)").removeClass("active");
							}
							function add_class_active_contact_bank(class_name) {
								jQuery(".template-contact-bank").removeClass("cb-active");
								jQuery("." + class_name).addClass("cb-active");
							}
							function contact_bank_validate_settings() {
								jQuery("#ux_frm_add_new_forms").validate({
									rules: {
										ux_txt_form_title: {
											required: true
										},
										ux_txt_submission_limit: {
											required: true
										},
										ux_txt_submission_limit_message: {
											required: true
										},
										ux_txt_success_message: {
											required: true
										},
										ux_txt_url_redirect: {
											required: true,
											url: true
										}
									},
									errorPlacement: function (error, element) {
									},
									highlight: function (element) {
										jQuery(element).closest(".form-group").removeClass("has-success").addClass("has-error");
									},
									success: function (label, element) {
										jQuery(element).closest(".form-group").removeClass("has-error").addClass("has-success");
									},
									submitHandler: function () {
										if (jQuery("#ux_div_first_step").hasClass("first-step-helper")) {
											if (jQuery(".template-contact-bank").hasClass("cb-active")) {
												var template = jQuery(".cb-active").attr("value");
												var form_id= "<?php echo isset( $_REQUEST['form_id'] ) ? intval( $_REQUEST['form_id'] ) : '';// WPCS: input var ok, CSRF ok. ?>";
												if(template === "layout_settings_blank_form_template") {
													contact_bank_second_step_settings();
												}
												else {
													var param = "";
													var nonce = "";
													if(template === "layout_settings_contact_us_form_template")
													{
														param = "cb_add_form_contact_us_template";
														nonce = "<?php echo esc_attr( $cb_add_form_contact_us_template_nonce ); ?>";
														submit_handler_common_contact_bank(form_id, "#ux_frm_add_new_forms", "", param, nonce, "", "cb_add_new_form&form_id="+form_id+"&mode=edit", template, "");
													} else if(template === "layout_settings_quote_request_form_template" || template === "layout_settings_event_form_registration_template" )
													{
														premium_edition_notification_contact_bank();
													}
												}
											} else {
												var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
												toastr[shortCutFunction](<?php echo wp_json_encode( $cb_select_form_message ); ?>);
											}
										} else{
											if (window.CKEDITOR) {
												jQuery("#ux_txtarea_add_form_heading_content").val(CKEDITOR.instances["ux_heading_content"].getData());
											} else if (jQuery("#wp-ux_heading_content-wrap").hasClass("tmce-active")) {
												jQuery("#ux_txtarea_add_form_heading_content").val(tinyMCE.get("ux_heading_content").getContent());
											} else {
												jQuery("#ux_txtarea_add_form_heading_content").val(jQuery("#ux_heading_content").val());
											}
											var template = jQuery(".cb-active").attr("value");
											var form_id = "<?php echo isset( $_REQUEST['form_id'] ) ? intval( $_REQUEST['form_id'] ) : 0;// WPCS: input var ok,CSRF ok. ?>";
											submit_handler_common_contact_bank(form_id, "#ux_frm_add_new_forms", "", "add_form_module", "<?php echo esc_attr( $add_new_form_module ); ?>", <?php echo wp_json_encode( $cb_saved_settings ); ?>, "contact_dashboard", template, contact_bank_control_ids);
										}
									}
								});
							}
							var sidebar_load_interval = setInterval(load_sidebar_content_contact_bank, 1000);
							setTimeout(function () {
								clearInterval(sidebar_load_interval);
							}, 5000);
						<?php
					}
					break;
				case 'cb_layout_settings':
					?>
						jQuery("#ux_li_layout_settings").addClass("active");
					<?php
					if ( LAYOUT_SETTINGS_CONTACT_BANK === '1' ) {
						?>
							jQuery(document).ready(function () {
								<?php
								if ( isset( $_REQUEST['form_id'] ) ) {// WPCS: input var ok, CSRF ok.
									?>
										jQuery("#ux_div_choose_template").css("display", "block");
									<?php
								}
								?>
								jQuery("#ux_ddl_choose_template").val("<?php echo isset( $_REQUEST['form_id'] ) ? intval( $_REQUEST['form_id'] ) : '';// WPCS: input var ok, CSRF ok. ?>");
								jQuery("#ux_ddl_form_design_form_position").val("<?php echo( isset( $layout_settings_data['layout_settings_form_design_position'] ) ) ? esc_attr( $layout_settings_data['layout_settings_form_design_position'] ) : 'left'; ?>");
								jQuery("#ux_ddl_form_design_title_html_tag").val("<?php echo( isset( $layout_settings_data['layout_settings_form_design_title_html_tag'] ) ) ? esc_attr( $layout_settings_data['layout_settings_form_design_title_html_tag'] ) : 'h1'; ?>");
								jQuery("#ux_ddl_form_design_title_form_position").val("<?php echo( isset( $layout_settings_data['layout_settings_form_design_title_alignment'] ) ) ? esc_attr( $layout_settings_data['layout_settings_form_design_title_alignment'] ) : 'left'; ?>");
								jQuery("#ux_ddl_form_design_title_font_family").val("<?php echo( isset( $layout_settings_data['layout_settings_form_design_title_font_family'] ) ) ? htmlspecialchars_decode( $layout_settings_data['layout_settings_form_design_title_font_family'] ) : 'Roboto Condensed';// WPCS: XSS ok. ?>");
								jQuery("#ux_ddl_form_design_description_html_tag").val("<?php echo( isset( $layout_settings_data['layout_settings_form_design_description_html_tag'] ) ) ? esc_attr( $layout_settings_data['layout_settings_form_design_description_html_tag'] ) : 'h1'; ?>");
								jQuery("#ux_ddl_form_design_description_form_position").val("<?php echo( isset( $layout_settings_data['layout_settings_form_design_description_alignment'] ) ) ? esc_attr( $layout_settings_data['layout_settings_form_design_description_alignment'] ) : 'left'; ?>");
								jQuery("#ux_ddl_form_design_description_font_family").val("<?php echo( isset( $layout_settings_data['layout_settings_form_design_description_font_family'] ) ) ? htmlspecialchars_decode( $layout_settings_data['layout_settings_form_design_description_font_family'] ) : 'Roboto Condensed';// WPCS: XSS ok. ?>");
								jQuery("#ux_ddl_label_field_text_alignment").val("<?php echo isset( $layout_settings_data['layout_settings_label_field_text_alignment'] ) ? esc_attr( $layout_settings_data['layout_settings_label_field_text_alignment'] ) : 'left'; ?>");
								jQuery("#ux_ddl_input_field_text_alignment").val("<?php echo isset( $layout_settings_data['layout_settings_input_field_text_alignment'] ) ? esc_attr( $layout_settings_data['layout_settings_input_field_text_alignment'] ) : 'left'; ?>");
								jQuery("#ux_ddl_input_field_radio_button_alignment").val("<?php echo isset( $layout_settings_data['layout_settings_input_field_radio_button_alignment'] ) ? esc_attr( $layout_settings_data['layout_settings_input_field_radio_button_alignment'] ) : 'single_row'; ?>");
								jQuery("#ux_ddl_input_field_checkbox_alignment").val("<?php echo isset( $layout_settings_data['layout_settings_input_field_checkbox_alignment'] ) ? esc_attr( $layout_settings_data['layout_settings_input_field_checkbox_alignment'] ) : 'single_row'; ?>");
								jQuery("#ux_ddl_input_field_border_style_thickness").val("<?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?>");
								jQuery("#ux_ddl_input_field_font_family").val("<?php echo( isset( $layout_settings_data['layout_settings_input_field_font_family'] ) ) ? htmlspecialchars_decode( $layout_settings_data['layout_settings_input_field_font_family'] ) : 'Roboto Condensed';// WPCS: XSS ok. ?>");
								jQuery("#ux_ddl_button_text_alignment").val("<?php echo isset( $layout_settings_data['layout_settings_button_text_alignment'] ) ? esc_attr( $layout_settings_data['layout_settings_button_text_alignment'] ) : 'left'; ?>");
								jQuery("#ux_ddl_button_border_style_thickness").val("<?php echo esc_attr( $layout_settings_button_border_style[1] ); ?>");
								jQuery("#ux_ddl_button_title_font_family").val("<?php echo isset( $layout_settings_data['layout_settings_button_font_family'] ) ? htmlspecialchars_decode( $layout_settings_data['layout_settings_button_font_family'] ) : 'Roboto Condensed';// WPCS: XSS ok. ?>");
								jQuery("#ux_ddl_label_field_font_family").val("<?php echo( isset( $layout_settings_data['layout_settings_label_field_font_family'] ) ) ? htmlspecialchars_decode( $layout_settings_data['layout_settings_label_field_font_family'] ) : 'Roboto Condensed';// WPCS: XSS ok. ?>");
								jQuery("#ux_ddl_contact_messages_font_family").val("<?php echo( isset( $layout_settings_data['layout_settings_messages_font_family'] ) ) ? htmlspecialchars_decode( $layout_settings_data['layout_settings_messages_font_family'] ) : 'Roboto Condensed';// WPCS: XSS ok. ?>");
								jQuery("#ux_ddl_messages_text_alignment").val("<?php echo isset( $layout_settings_data['layout_settings_messages_text_alignment'] ) ? esc_attr( $layout_settings_data['layout_settings_messages_text_alignment'] ) : 'left'; ?>");
								jQuery("#ux_ddl_error_messages_font_family").val("<?php echo( isset( $layout_settings_data['layout_settings_error_messages_font_family'] ) ) ? htmlspecialchars_decode( $layout_settings_data['layout_settings_error_messages_font_family'] ) : 'Roboto Slab';// WPCS: XSS ok. ?>");
							});
							function layout_settings_data() {
								var form_id = jQuery("#ux_ddl_choose_template").val();
								if (form_id !== "") {
									window.location.href = "admin.php?page=cb_layout_settings&form_id=" + form_id;
								}
								else
								{
									window.location.href = "admin.php?page=cb_layout_settings";
								}
							}
							var form_id= "<?php echo isset( $_REQUEST['form_id'] ) ? intval( $_REQUEST['form_id'] ) : '';// WPCS: input var ok, CSRF ok. ?>";
							jQuery("#ux_frm_layout_settings").validate({
								submitHandler: function () {
									premium_edition_notification_contact_bank();
								}
							});
							var sidebar_load_interval = setInterval(load_sidebar_content_contact_bank, 1000);
							setTimeout(function () {
								clearInterval(sidebar_load_interval);
							}, 5000);
						<?php
					}
					break;
				case 'cb_custom_css':
					?>
						jQuery("#ux_li_custom_settings").addClass("active");
					<?php
					if ( CUSTOM_CSS_CONTACT_BANK === '1' ) {
						?>
							jQuery("#ux_frm_custom_css").validate({
								submitHandler: function () {
									submit_handler_common_contact_bank("", "#ux_frm_custom_css", "", "custom_css_module", "<?php echo esc_attr( $custom_css_nonce ); ?>", <?php echo wp_json_encode( $cb_saved_settings ); ?>, "cb_custom_css", "", "");
								}
							});
							var sidebar_load_interval = setInterval(load_sidebar_content_contact_bank, 1000);
							setTimeout(function () {
								clearInterval(sidebar_load_interval);
							}, 5000);
						<?php
					}
					break;
				case 'cb_email_templates':
					?>
						jQuery("#ux_li_email_templates").addClass("active");
						jQuery("#ux_li_manage_email_templates").addClass("active");

					<?php
					if ( EMAIL_TEMPLATES_CONTACT_BANK === '1' ) {
						?>
							var oTable = contact_bank_manage_datatable("#ux_table_manage_email_templates");
							function contact_bank_show_hide_layout() {
								var data = jQuery("#ux_ddl_send_to").val();
								switch (data) {
									case "send_to_email" :
										jQuery("#ux_send_to_field").css("display", "none");
										jQuery("#ux_send_to_email").css("display", "block");
										break;
									case "select_field" :
										jQuery("#ux_send_to_email").css("display", "none");
										jQuery("#ux_send_to_field").css("display", "block");
										break;
								}
							}
							jQuery(document).ready(function () {
								jQuery("#ux_ddl_forms").val("<?php echo isset( $_REQUEST['form_id'] ) ? esc_attr( wp_unslash( $_REQUEST['form_id'] ) ) : '';// WPCS: input var ok, CSRF ok, sanitization ok. ?>");
								jQuery("#ux_ddl_email_templates").val("<?php echo isset( $_REQUEST['template_type'] ) ? esc_attr( wp_unslash( $_REQUEST['template_type'] ) ) : 'form_admin_notification_email';// WPCS: input var ok, CSRF ok, sanitization ok. ?>");
								jQuery("#ux_ddl_send_to").val("<?php echo isset( $unserialized_data_forms[ $template_type ]['template_send_to'] ) ? esc_attr( $unserialized_data_forms[ $template_type ]['template_send_to'] ) : 'send_to_email'; ?>")
								var form_id = jQuery("#ux_ddl_forms").val();
								if (form_id !== "") {
									jQuery("#email_template_layout").css("display", "block");
								} else {
									jQuery("#email_template_layout").css("display", "none");
								}
								contact_bank_show_hide_layout();
							});
							function append_control_shortcode_contact_bank(ddl_id, input_id)
							{
								var dynamicId = jQuery("#" + ddl_id).val();
								var label = jQuery("#" + ddl_id + " option:selected").text();
								if (dynamicId != "")
								{
									var selected_fields = jQuery("#" + input_id).val();
									var fields_shortCodes = selected_fields + "[control_"+dynamicId+"]";
									jQuery("#" + input_id).val(fields_shortCodes);
									jQuery("#" + ddl_id).val("");
								}
							}
							function append_form_message_field_control_contact_bank(ddl_id)
							{
								var dynamicId = jQuery("#" + ddl_id).val();
								var label = jQuery("#" + ddl_id + " option:selected").text();
								if (dynamicId != "")
								{
									if(jQuery("#wp-ux_heading_content-wrap").hasClass("tmce-active"))
									{
										var selected_fields = tinyMCE.get("ux_heading_content").getContent();
										if(label === "Credit Card")
										{
											var fields_shortCodes = "<strong>" + selected_fields + "Credit Card Number " + "</strong> : [control_card_number_" + dynamicId + "]<br /><br /> <strong>" + "Card Expiry Date " + "</strong> : [control_expiry_date_" + dynamicId + "]<br /><br /> <strong>" + "CVV Number " + "</strong> : [control_cvv_number_" + dynamicId + "]<br />";
										}
										else
										{
											var fields_shortCodes = "<strong>" + selected_fields + label + "</strong> : [control_" + dynamicId + "]<br />";
										}
										tinyMCE.get("ux_heading_content").setContent(fields_shortCodes);
									} else
									{
									var selected_fields = jQuery("#ux_heading_content").val();
									if(label === "Credit Card")
									{
										var fields_shortCodes = selected_fields + "Credit Card Number " + " : [control_card_number_" + dynamicId + "]<br /> " + "Card Expiry Date " + " : [control_expiry_date_" + dynamicId + "]<br /> " + "CVV Number " + " : [control_cvv_number_" + dynamicId + "]<br />";
									}
									else
									{
										var fields_shortCodes = selected_fields + label + " : [control_" + dynamicId + "]<br />";
									}
									jQuery("#ux_heading_content").val(fields_shortCodes);
									}
									jQuery("#" + ddl_id).val("");
								}
							}
							function email_templates_redirect_data() {
								var form_id = jQuery("#ux_ddl_forms").val();
								var template_type = jQuery("#ux_ddl_email_templates").val();
								if (form_id !== "" && template_type !== "") {
									window.location.href = "admin.php?page=cb_email_templates&form_id=" + form_id + "&template_type=" + template_type;
								} else {
									window.location.href = "admin.php?page=cb_email_templates";
								}
							}
							jQuery("#ux_frm_manage_email_templates").validate({
								rules:
										{
											ux_txt_send_to_email: {
														required: true
													},
											ux_txt_send_to_field: {
														required: true
													},
											ux_txt_subject: {
														required: true
													}
										},
								errorPlacement: function (error, element) {
								},
								highlight: function (element) {
									jQuery(element).closest(".form-group").removeClass("has-success").addClass("has-error");
								},
								success: function (label, element) {
									jQuery(element).closest(".form-group").removeClass("has-error").addClass("has-success");
								},
								submitHandler: function () {
									if(jQuery("#ux_ddl_forms").val() === "")
									{
										var shortCutFunction = jQuery("#toastTypeGroup_error input:checked").val();
										toastr[shortCutFunction](<?php echo wp_json_encode( $cb_select_form_error_message ); ?>);
									}
									else
									{
										if (window.CKEDITOR) {
										jQuery("#ux_txtarea_email_template_heading_content").val(CKEDITOR.instances["ux_heading_content"].getData());
										} else if (jQuery("#wp-ux_heading_content-wrap").hasClass("tmce-active")) {
											jQuery("#ux_txtarea_email_template_heading_content").val(tinyMCE.get("ux_heading_content").getContent());
										} else {
											jQuery("#ux_txtarea_email_template_heading_content").val(jQuery("#ux_heading_content").val());
										}
										var form_id = "<?php echo isset( $_REQUEST['form_id'] ) ? intval( $_REQUEST['form_id'] ) : 0;// WPCS: input var ok, CSRF ok. ?>";
										var template_type = "<?php echo isset( $_REQUEST['template_type'] ) ? esc_attr( wp_unslash( $_REQUEST['template_type'] ) ) : 'form_admin_notification_email';// WPCS: input var ok, CSRF ok, sanitization o. ?>";
										submit_handler_common_contact_bank("", "#ux_frm_manage_email_templates", "", "email_templates_module", "<?php echo esc_attr( $email_templates_nonce ); ?>", <?php echo wp_json_encode( $cb_saved_settings ); ?>, "cb_email_templates&form_id="+form_id+"&template_type="+template_type, "", "");
									}
								}
							});
						<?php
					}
					break;
				case 'cb_general_settings':
					?>
						jQuery("#ux_li_general_settings").addClass("active");
					<?php
					if ( GENERAL_SETTINGS_CONTACT_BANK === '1' ) {
						?>
							jQuery(document).ready(function () {
								jQuery("#ux_ddl_general_settings").val("<?php echo isset( $details_general_settings['automatic_updates'] ) ? esc_attr( $details_general_settings['automatic_updates'] ) : 'enable'; ?>");
								jQuery("#ux_ddl_remove_table").val("<?php echo isset( $details_general_settings['remove_tables_at_uninstall'] ) ? esc_attr( $details_general_settings['remove_tables_at_uninstall'] ) : 'enable'; ?>");
								jQuery("#ux_ddl_default_currency").val("<?php echo isset( $details_general_settings['default_currency'] ) ? esc_attr( $details_general_settings['default_currency'] ) : 'USD'; ?>");
								jQuery("#ux_ddl_language_direction").val("<?php echo isset( $details_general_settings['language_direction'] ) ? esc_attr( $details_general_settings['language_direction'] ) : 'left_to_right'; ?>");
								jQuery("#ux_ddl_gdpr_compliance").val("<?php echo isset( $details_general_settings['gdpr_compliance'] ) ? esc_attr( $details_general_settings['gdpr_compliance'] ) : 'enable'; ?>");
								gdpr_compliance_contact_bank();
							});
							jQuery("#ux_frm_general_settings").validate ({
										submitHandler: function (form) {
											submit_handler_common_contact_bank("", "#ux_frm_general_settings", "", "general_settings_module", "<?php echo esc_attr( $general_settings_nonce ); ?>",<?php echo wp_json_encode( $cb_saved_settings ); ?>, "cb_general_settings", "");
										}
									});
						<?php
					}
					break;
				case 'cb_submissions':
					?>
					jQuery("#ux_li_submissions").addClass("active");
					<?php
					if ( SUBMISSIONS_CONTACT_BANK === '1' ) {
						?>
						var oTable = jQuery("#ux_table_submissions").dataTable({
							"pagingType": "full_numbers",
							"language": {
								"emptyTable": "No data available in table",
								"info": "Showing _START_ to _END_ of _TOTAL_ entries",
								"infoEmpty": "No entries found",
								"infoFiltered": "(filtered1 from _MAX_ total entries)",
								"lengthMenu": "Show _MENU_ entries",
								"search": "Search:",
								"zeroRecords": "No matching records found"
							},
							"bSort": true,
							"pageLength": 10,
							"aoColumnDefs": [{"bSortable": false, "aTargets": [0]}],
							dom: "lBfrtip",
							buttons: [
								{
									extend: "excelHtml5",
									action: function ()
									{
											this.disable();
										}
								}
								]
						});
						jQuery(".dt-button").click(function ()
						{
							premium_edition_notification_contact_bank();
						});
						jQuery("#ux_chk_all_forms").click(function ()
						{
							jQuery("input[type=checkbox]", oTable.fnGetFilteredNodes()).attr("checked", this.checked);
						});
						function submissions_redirect_data_contact_bank()
						{
							var form_id = jQuery("#ux_ddl_manage_email").val();
							if (form_id !== "") {
								window.location.href = "admin.php?page=cb_submissions&form_id=" + form_id;
							}
							else
							{
								window.location.href = "admin.php?page=cb_submissions";
							}
						}
						function prevent_datepicker_contact_bank(id)
						{
							jQuery(id).keypress(function (event)
							{
								event.preventDefault();
							});
						}
						jQuery(document).ready(function()
						{
							jQuery("#ux_txt_start_date").datepicker
							({
								dateFormat: "mm/dd/yy",
								numberOfMonths: 1,
								changeMonth: true,
								changeYear: true,
								yearRange: "1970:2039",
								onSelect: function (selected)
								{
									jQuery("#ux_txt_end_date").datepicker("option", "minDate", selected);
								}
							});
							jQuery("#ux_txt_end_date").datepicker
							({
								dateFormat: "mm/dd/yy",
								numberOfMonths: 1,
								changeMonth: true,
								changeYear: true,
								yearRange: "1970:2039",
								onSelect: function (selected)
								{
									jQuery("#ux_txt_start_date").datepicker("option", "maxDate", selected);
								}
							});
							jQuery("#ux_ddl_manage_email").val("<?php echo isset( $_REQUEST['form_id'] ) ? intval( $_REQUEST['form_id'] ) : '';// WPCS: input var ok, CSRF ok. ?>");
							<?php
							if ( isset( $_REQUEST['form_id'] ) ) {// WPCS: input var ok, CSRF ok.
								?>
								jQuery("#ux_div_submissions").css("display","block");
								<?php
							}
							?>
						});
						jQuery("#ux_frm_submissions_layout").validate
						({
								rules:
								{
									ux_txt_start_date:
									{
										required: true
									},
									ux_txt_end_date:
									{
										required: true
									}
								},
								errorPlacement: function ()
								{
								},
								highlight: function (element)
								{
									jQuery(element).closest(".form-group").removeClass("has-success").addClass("has-error");
								},
								success: function (label, element)
								{
									jQuery(element).closest(".form-group").removeClass("has-error").addClass("has-success");
								},
								submitHandler: function ()
								{
									premium_edition_notification_contact_bank();
								}
							});
							var sidebar_load_interval = setInterval(load_sidebar_content_contact_bank, 1000);
							setTimeout(function () {
								clearInterval(sidebar_load_interval);
							}, 5000);
						<?php
					}
					break;
				case 'cb_roles_and_capabilities':
					?>
						jQuery("#ux_li_roles_and_capabilities").addClass("active");
					<?php
					if ( ROLES_AND_CAPABILITIES_CONTACT_BANK === '1' ) {
						?>
							function show_roles_capabilities_contact_bank(id, div_id) {
								jQuery(id).prop("checked") ? jQuery("#" + div_id).css("display", "block") : jQuery("#" + div_id).css("display", "none");
							}
							function full_control_function_contact_bank(id, div_id) {
								var checkbox_id = jQuery(id).prop("checked");
								jQuery("#" + div_id + " input[type=checkbox]").each(function () {
									if (checkbox_id) {
										jQuery(this).attr("checked", "checked");
										if (jQuery(id).attr("id") !== jQuery(this).attr("id")) {
											jQuery(this).attr("disabled", "disabled");
										}
									} else {
										if (jQuery(id).attr("id") !== jQuery(this).attr("id")) {
											jQuery(this).removeAttr("disabled");
											jQuery("#ux_chk_other_capabilities_manage_options,#ux_chk_other_capabilities_read").attr("disabled", "disabled");
										}
									}
								});
							}
							jQuery(document).ready(function () {
								jQuery("#ux_ddl_contact_bank_menu").val("<?php echo isset( $details_roles_capabilities['show_contact_bank_top_bar_menu'] ) ? esc_attr( $details_roles_capabilities['show_contact_bank_top_bar_menu'] ) : 'enable'; ?>");
								show_roles_capabilities_contact_bank("#ux_chk_author", "ux_div_author_roles");
								full_control_function_contact_bank("#ux_chk_full_control_author", "ux_div_author_roles");
								show_roles_capabilities_contact_bank("#ux_chk_editor", "ux_div_editor_roles");
								full_control_function_contact_bank("#ux_chk_full_control_editor", "ux_div_editor_roles");
								show_roles_capabilities_contact_bank("#ux_chk_contributor", "ux_div_contributor_roles");
								full_control_function_contact_bank("#ux_chk_full_control_contributor", "ux_div_contributor_roles");
								show_roles_capabilities_contact_bank("#ux_chk_subscriber", "ux_div_subscriber_roles");
								full_control_function_contact_bank("#ux_chk_full_control_subscriber", "ux_div_subscriber_roles");
								show_roles_capabilities_contact_bank("#ux_chk_others_privileges", "ux_div_other_privileges_roles");
								full_control_function_contact_bank("#ux_chk_full_control_others", "ux_div_other_privileges_roles");
							});
							jQuery("#ux_frm_roles_and_capabilities").validate({
								submitHandler: function () {
									premium_edition_notification_contact_bank();
								}
							});
						<?php
					}
					break;
				case 'cb_system_information':
					?>
						jQuery("#ux_li_system_information").addClass("active");
					<?php
					if ( SYSTEM_INFORMATION_CONTACT_BANK === '1' ) {
						?>
							jQuery.getSystemReport = function (strDefault, stringCount, string, location) {
								var o = strDefault.toString();
								if (!string) {
									string = "0";
								}
								while (o.length < stringCount) {
									if (location === "undefined") {
										o = string + o;
									} else {
										o = o + string;
									}
								}
								return o;
							};
							jQuery(".system-report").click(function () {
								var report = "";
								jQuery(".custom-form-body").each(function () {
									jQuery("h3.form-section", jQuery(this)).each(function () {
										report = report + "\n### " + jQuery.trim(jQuery(this).text()) + " ###\n\n";
									});
									jQuery("tbody > tr", jQuery(this)).each(function () {
										var the_name = jQuery.getSystemReport(jQuery.trim(jQuery(this).find("strong").text()), 25, " ");
										var the_value = jQuery.trim(jQuery(this).find("span").text());
										var value_array = the_value.split(", ");
										if (value_array.length > 1) {
											var temp_line = "";
											jQuery.each(value_array, function (key, line) {
												var tab = (key === 0) ? 0 : 25;
												temp_line = temp_line + jQuery.getSystemReport("", tab, " ", "f") + line + "\n";
											});
											the_value = temp_line;
										}
										report = report + "" + the_name + the_value + "\n";
									});
								});
								try {
									jQuery("#ux_system_information").slideDown();
									jQuery("#ux_system_information textarea").val(report).focus().select();
									return false;
								} catch (e) {
									console.log(e);
								}
								return false;
							});
							jQuery("#ux_btn_system_information").click(function () {
								if (jQuery("#ux_btn_system_information").text() === "Close System Information!") {
									jQuery("#ux_system_information").slideUp();
									jQuery("#ux_btn_system_information").html("Get System Information!");
								} else {
									jQuery("#ux_btn_system_information").html("Close System Information!");
									jQuery("#ux_btn_system_information").removeClass("system-information");
									jQuery("#ux_btn_system_information").addClass("close-information");
								}
							});
							var sidebar_load_interval = setInterval(load_sidebar_content_contact_bank, 1000);
							setTimeout(function () {
								clearInterval(sidebar_load_interval);
							}, 5000);
						<?php
					}
					break;
			}
		}
		?>
		</script>
		<?php
	}
}
