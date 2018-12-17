<?php
/**
 * Template for add new form.
 *
 * @author  Tech Banker
 * @package  contact-bank/includes
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
			global $wpdb;
			$form_id                = isset( $_REQUEST['form_id'] ) ? intval( $_REQUEST['form_id'] ) : '';// WPCS: input var ok, CSRF ok.
			$meta_value             = $wpdb->get_var(
				$wpdb->prepare(
					'SELECT meta_value  FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_id = %d and meta_key = %s', $form_id, 'form_data'
				)
			);// WPCS: db call ok, cache ok.
			$unserialize_meta_value = maybe_unserialize( $meta_value );
		?>
		<div id="ux_div_single_line_text" style="display: none;cursor:pointer;" class="result_hover">
			<div class="main_div">
				<div class="header_title" style="visibility: hidden;">
					<div class="header_title_left" ><b>Single Line Text</b></div>
					<div class="header_title_rigth" style="float: right;margin-right: 10px;">
						<a title="<?php echo esc_attr( $cb_expand_field ); ?>"><i class="icon-custom-note"></i></a>
						<a title="<?php echo esc_attr( $cb_duplicate_field ); ?>" ><i class="icon-custom-docs"></i></a>
						<a title="<?php echo esc_attr( $cb_delete_field ); ?>"><i class="icon-custom-trash"></i></a>
					</div>
					<input type="hidden">
				</div>
				<div class="sub_div" style="padding-bottom:20px;">
					<label class="control-label field_label" style="display:block;">
						<span> <?php echo esc_attr( $cb_untitled_control ); ?></span> :
						<i class="icon-custom-question tooltips" data-original-title="" data-placement="right"></i>
						<span class="required" aria-required="true">*</span>
					</label>
					<input name="ux_txt_singal_line_text" class="untitled_control" type="text" value="" autocomplete="off">
					<div class="form-group default_text" style="display:none; padding: 10px 10px 0px 10px;">
						It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout.
					</div>
					<select name="ux_ddl_us_states" id="ux_ddl_us_states" class="untitled_control" style="display: none;">
					</select>
					<select id="ux_ddl_country" class="untitled_control" style="display:none;">
					</select>
					<span></span>
				</div>
				<div class="sub_div_credit_card" style="padding-bottom:10%; display: none;">
					<div class="form-group">
						<label class="control-label field_label">
							<span> <?php echo esc_attr( $cb_general_credit_card_number ); ?></span> :
							<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_credit_card_number_tooltip ); ?>" data-placement="right"></i>
							<span class="required" aria-required="true">*</span>
						</label>
						<input name="ux_txt_credit_card_number_text_field" class="untitled_control" type="text" value="" autocomplete="off" data-inputmask="'mask': '9999 9999 9999 9999'">
					</div>
					<div class="form-group">
						<label class="control-label field_label">
							<span> <?php echo esc_attr( $cb_general_credit_card_expiry_date ); ?></span> :
							<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_credit_card_expiry_date_tooltip ); ?>" data-placement="right"></i>
							<span class="required" aria-required="true">*</span>
						</label>
						<input name="ux_txt_credit_card_expiry_date" class="untitled_control" type="text" value="" autocomplete="off">
					</div>
					<div class="form-group">
						<label class="control-label field_label">
							<span> <?php echo esc_attr( $cb_general_credit_cvv_number ); ?></span> :
							<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_credit_cvv_number_tooltip ); ?>" data-placement="right"></i>
							<span class="required" aria-required="true">*</span>
						</label>
						<input name="credit_card_cvv_number" class="untitled_control" type="text" value="" autocomplete="off">
					</div>
						<span></span>
				</div>
				<div class="sub_div_section_break" style="padding-bottom:30px; display: none;">
					<label class="control-label field_label">
						<span> <?php echo esc_attr( $cb_untitled_control ); ?></span>
					</label>
					<input name="ux_txt_singal_line_text" class="untitled_control" type="text" value="" autocomplete="off">
					<span></span>
				</div>
			</div>
			<div class="ux_div_widget_content" >
				<div class="tabbable-form-custom">
					<ul class="nav nav-tabs ">
						<li class="active general_settings">
							<a aria-expanded="true" data-toggle="tab">
								<?php echo esc_attr( $cb_general_tab ); ?>
							</a>
						</li>
						<li class="options_settings">
							<a aria-expanded="false" data-toggle="tab">
								<?php echo esc_attr( $cb_options_tab ); ?>
							</a>
						</li>
						<li class="appearance_settings">
							<a aria-expanded="false" data-toggle="tab">
								<?php echo esc_attr( $cb_appearance_tab ); ?>
							</a>
						</li>
						<li class="restrictions_settings">
							<a aria-expanded="false" data-toggle="tab">
								<?php echo esc_attr( $cb_restrictions_tab ); ?>
							</a>
						</li>
						<li class="advanced_settings">
							<a aria-expanded="false" data-toggle="tab">
								<?php echo esc_attr( $cb_advanced_tab ); ?>
							</a>
						</li>
					</ul>
					<div class="tab-content">
						<div class="tab-pane active general_settings" id="general">
							<div class="form-group label_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_label_control ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_label_control_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" name="ux_txt_label_field"  placeholder="<?php echo esc_attr( $cb_label_general_placeholder ); ?>" value="Untitled">
							</div>
							<div class="form-group tooltip_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_tooltip_control ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_tooltip_description ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" name="ux_txt_description_field"  placeholder="<?php echo esc_attr( $cb_general_tootltip_placeholder ); ?>">
							</div>
							<div class="form-group label_placement_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_label_placement_control ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_label_placement ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<select class="form-control">
									<option value="above"><?php echo esc_attr( $cb_label_placement_above ); ?></option>
									<option value="below"><?php echo esc_attr( $cb_label_placement_below ); ?></option>
									<option value="left"><?php echo esc_attr( $cb_label_placement_left ); ?></option>
									<option value="right"><?php echo esc_attr( $cb_label_placement_right ); ?></option>
									<option value="hidden"><?php echo esc_attr( $cb_label_placement_hidden ); ?></option>
								</select>
							</div>
							<div class="form-group logical_captcha_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_general_mathematical_operations ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_logical_captcha ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<select class="form-control" style="margin-bottom:15px !important;">
									<option value="arithmetic"><?php echo esc_attr( $cb_general_arithmetic ); ?></option>
									<option value="relational"><?php echo esc_attr( $cb_general_relational ); ?></option>
									<option value="arrange_order"><?php echo esc_attr( $cb_general_arrange_order ); ?></option>
								</select>
								<div style="display:block;">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_arithmetic_operations ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_arithmetic_operations_tooltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
									<table class="table table-striped table-bordered table-margin-top" id="ux_tbl_arithmetic">
										<thead>
											<tr>
												<th class="control-label add_settings">
													<input type="checkbox" class="custom-chkbox-operation" value="0" ><?php echo esc_attr( $cb_general_arithmeric_addition ); ?>
												</th>
												<th class="control-label sub_settings">
													<input type="checkbox" class="custom-chkbox-operation" value="0"><?php echo esc_attr( $cb_general_arithmeric_subtraction ); ?>
												</th>
												<th class="control-label multi_settings">
													<input type="checkbox" class="custom-chkbox-operation" value="0"><?php echo esc_attr( $cb_general_arithmeric_mutiplication ); ?>
												</th>
												<th class="control-label division_settings">
													<input type="checkbox" class="custom-chkbox-operation" value="0"><?php echo esc_attr( $cb_general_arithmeric_division ); ?>
												</th>
											</tr>
											<input type="hidden" class="artimatic_values" value="[0,0,0,0]">
										</thead>
									</table>
								</div>
								<div  style="display:none;">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_relational_operations ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_relational_operations_tooltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
									<table class="table table-striped table-bordered table-margin-top" id="ux_tbl_relational">
										<thead>
											<tr>
												<th class="control-label larger_number_settings ">
													<input type="checkbox" class="form-control" value="0"><?php echo esc_attr( $cb_general_relational_largest_number ); ?>
												</th>
												<th class="control-label smaller_number_settings">
													<input type="checkbox" class="form-control"  value="0"><?php echo esc_attr( $cb_general_relational_smallest_number ); ?>
												</th>
											</tr>
											<input type="hidden" class="relational_values" value="[0,0]">
										</thead>
									</table>
								</div>
								<div style="display:none;">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_arrange_order ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_arrange_order_tootltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
									<table class="table table-striped table-bordered table-margin-top" id="ux_tbl_arrange">
										<thead>
											<tr>
												<th class="control-label ascending_order_settings">
													<input type="checkbox" class="form-control" value="0"><?php echo 'Ascending Order'; ?>
												</th>
												<th class="control-label decending_order_settings">
													<input type="checkbox" class="form-control" value="0"><?php echo 'Descending Order'; ?>
												</th>
											</tr>
											<input type="hidden" class="arrange_values" value="[0,0]">
										</thead>
									</table>
								</div>
							</div>
							<div class="form-group anti_spam_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_general_answer ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_answer_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" name="ux_txt_answer" id ="ux_txt_answer"  placeholder="<?php echo esc_attr( $cb_general_answer_placeholder ); ?>">
							</div>
							<div class="form-group field_description_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_general_field_description ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_field_description_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<textarea type="text" class="form-control" name="ux_txt_field_description" placeholder="<?php echo esc_attr( $cb_general_field_description_placeholder ); ?>"></textarea>
							</div>
							<div class="html_editor">
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_html_editor_content ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_html_editor_content_tooltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
									<input type="hidden">
									<textarea name="ux_content_heading_content" id="ux_content_heading_content">It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout.</textarea>
									<textarea name="ux_content_heading_content_duplicate" id="ux_content_heading_content_duplicate" style="display: none;"></textarea>
								</div>
							</div>
							<div class="date_settings">
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_date_format ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_date_format_tooltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
									<select class="form-control">
										<option value="F j, Y"> F j, Y </option>
										<option value="Y/m/d"> Y/m/d </option>
										<option value="m/d/Y"> m/d/Y </option>
										<option value="d/m/Y"> d/m/Y </option>
									</select>
<!--                                    <input type="text" class="form-control" name="ux_date_format" value="mm/dd/yy" placeholder="< ?php echo $cb_general_date_format_placeholder;?>">-->
								</div>
								<div class="row">
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_date_start_year ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_date_start_year_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<input type="text" class="form-control" name="ux_txt_start_year" value="1970" placeholder="<?php echo esc_attr( $cb_general_date_start_year_placeholder ); ?>">
										</div>
									</div>
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_date_end_year ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_date_end_year_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<input type="text" class="form-control" name="ux_txt_end_year" value="2017" placeholder="<?php echo esc_attr( $cb_general_date_end_year_placeholder ); ?>">
										</div>
									</div>
								</div>
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_default_current_date ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_default_current_date_tooltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
									<select class="form-control" class="ux_ddl_default_date">
										<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
										<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
									</select>
								</div>
							</div>
							<div class="time_settings">
								<div class="row">
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_time_format ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_time_format_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<select class="form-control">
												<option value="12hour"><?php echo esc_attr( $cb_general_time_format_twelve ); ?></option>
												<option value="24hour"><?php echo esc_attr( $cb_general_time_format_twentyfour ); ?></option>
											</select>
										</div>
									</div>
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_default_current_time ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_default_current_time_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<select class="form-control">
												<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
												<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
											</select>
										</div>
									</div>
								</div>
							</div>
							<div class="form-group quantity_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_general_product ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_product_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<select class="form-control" name="ux_ddl_product_list">
									<option value=""><?php echo esc_attr( $cb_general_select_product ); ?></option>
									<?php
									if ( isset( $unserialize_meta_value['controls'] ) && count( $unserialize_meta_value['controls'] ) > 0 ) {
										foreach ( $unserialize_meta_value['controls'] as $values ) {
											if ( 'product' === $values['control_type'] ) {
												?>
												<option value="<?php echo esc_attr( $values['timestamp'] ); ?>"><?php echo esc_attr( $values['label_name'] ); ?></option>
												<?php
											}
										}
									}
									?>
								</select>
							</div>
							<div class="number_settings">
								<div class="row">
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_min_number ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_min_number_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<input type="text" class="form-control" name="ux_txt_min_number" onkeypress="enter_only_digits_for_price(event);" placeholder="<?php echo esc_attr( $cb_general_min_number_placeholder ); ?>">
										</div>
									</div>
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_max_number ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_max_number_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<input type="text" class="form-control" name="ux_txt_max_number" onkeypress="enter_only_digits_for_price(event);" placeholder="<?php echo esc_attr( $cb_general_max_number_placeholder ); ?>">
										</div>
									</div>
								</div>
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_step ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_step_tooltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
									<input type="text" class="form-control" name="ux_txt_number_step" onkeypress="enter_only_digits_for_price(event);" placeholder="<?php echo esc_attr( $cb_general_step_placeholder ); ?>">
								</div>
							</div>
							<div class="file_upload_settings">
								<div class="row">
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_file_upload_maximum_size ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_file_upload_maximum_size_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<input type="text" class="form-control" value="2mb" placeholder="<?php echo esc_attr( $cb_general_file_upload_maximum_size_placeholder ); ?>">
										</div>
									</div>
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_file_upload_extension ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_file_upload_extension_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<input type="text" class="form-control" value="jpg,png,gif,zip" placeholder="<?php echo esc_attr( $cb_general_file_upload_extension_placeholder ); ?>">
										</div>
									</div>
								</div>
								<div class="row">
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_file_upload_multiple_upload ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_file_upload_multiple_upload_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<select class="form-control">
												<option value="true"><?php echo esc_attr( $cb_enable ); ?></option>
												<option value="false"><?php echo esc_attr( $cb_disable ); ?></option>
											</select>
										</div>
									</div>
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_file_upload_attach_email ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_file_upload_attach_email_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<select class="form-control">
												<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
												<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
											</select>
										</div>
									</div>
								</div>
							</div>
							<div class="product_settings">
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_product_price ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_product_price_tooltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
									<input type="text" class="form-control" name="ux_txt_price" onkeypress="enter_only_digits_for_price(event);" placeholder="<?php echo esc_attr( $cb_general_product_price_placeholder ); ?>" value="0.00">
								</div>
							</div>
							<div class="shipping_settings">
								<div class="form-group">
									<label class="control-label">
											<?php echo esc_attr( $cb_general_shipping_cost ); ?> :
											<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_shipping_cost_tooltip ); ?>" data-placement="right"></i>
											<span class="required" aria-required="true">*</span>
									</label>
									<input type="text" class="form-control" name="ux_txt_cost" onkeypress="enter_only_digits_for_price(event);" placeholder="<?php echo esc_attr( $cb_general_shipping_cost_placeholder ); ?>" value="0.00">
								</div>
							</div>
							<div class="credit_card_settings">
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_credit_card_number ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_credit_card_number_tooltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
									<input type="text" class="form-control" name="ux_txt_credit_card_number" maxlength="16" placeholder="<?php echo esc_attr( $cb_general_credit_card_number_placeholder ); ?>">
								</div>
								<div class="row">
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_credit_card_expiry_date ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_credit_card_expiry_date_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<input type="text" class="form-control" name="ux_txt_expiry_date" placeholder="<?php echo esc_attr( $cb_general_credit_card_expiry_date_placeholder ); ?>">
										</div>
									</div>
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_general_credit_cvv_number ); ?> :
												<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_credit_cvv_number_tooltip ); ?>" data-placement="right"></i>
												<span class="required" aria-required="true">*</span>
											</label>
											<input type="text" class="form-control" name="ux_txt_cvv" maxlength="4" placeholder="<?php echo esc_attr( $cb_general_credit_cvv_number_placeholder ); ?>">
										</div>
									</div>
								</div>
							</div>
							<div class="form-group star_rating">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_number_stars ); ?> :
										<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_general_number_stars_tooltip ); ?>" data-placement="right"></i>
										<span class="required" aria-required="true">*</span>
									</label>
								<input type="text" class="form-control" name="ux_txt_number_of_stars" value="5" placeholder="<?php echo esc_attr( $cb_general_number_stars_placeholder ); ?>">
							</div>
						</div>
						<div class="tab-pane options_settings" id="option">
							<div class="row">
								<div class="col-md-6">
									<?php echo esc_attr( $cb_options_control ); ?>
									<input type="text" class="form-control" name="ux_txt_add_form_option" placeholder="<?php echo esc_attr( $cb_options_control_placeholder ); ?>">
								</div>
								<div class="col-md-6">
									<?php echo esc_attr( $cb_options_value ); ?>
									<input type="text" class="form-control" name="ux_txt_add_form_values" placeholder="<?php echo esc_attr( $cb_options_value_placeholder ); ?>">
								</div>
								<div class="pull-right" style="margin-right:10px;margin-top:5px;">
									<input type="button" class="btn vivid-green" name="ux_btn_add_option" id="ux_btn_add_options" name="ux_btn_add_options" value="<?php echo esc_attr( $cb_add_option ); ?>">
									<input type="button" class="btn vivid-green" name="ux_btn_add_option" id="ux_btn_add_import" value="<?php echo esc_attr( $cb_add_import ); ?>" data-popup-open="ux_open_popup_translator">
									<input type="hidden" class="form-control select-hidden" name="ux_hidden_options_values">
								</div>
							</div>
							<div class="form-group">
								<label class="control-label" style="display:block;">
									<?php echo esc_attr( $cb_options ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_options_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<select class="form-control custom-drop-down input-inline" name="ux_ddl_required">
								</select>
								<input type="button" class="btn vivid-green pull-right"  style="margin-top:8px" name="ux_btn_delete_option"  value="<?php echo esc_attr( $cb_add_delete ); ?>">
							</div>
							<div class="popup" data-popup="ux_open_popup_translator" id="open_popup">
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
														<textarea class="form-control" rows="7" placeholder="<?php echo esc_attr( $cb_popup_query_placeholder ); ?>"></textarea>
													</div>
												</div>
												<div class="modal-footer">
													<div class="form-actions">
														<div class="pull-right">
															<input type="button"  class="btn vivid-green" name="ux_send_query" value="<?php echo esc_attr( $cb_add_import ); ?>" data-popup-close-translator="ux_open_popup_translator">
															<input type="button" data-popup-close-translator="ux_open_popup_translator" class="btn vivid-green" id="ux_btn_close" value="<?php echo esc_attr( $cb_manage_backups_close ); ?>">
														</div>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="tab-pane appearance_settings" id="appearance">
							<div class="form-group placeholder_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_appearance_placeholder_label ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_placeholder_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" name="ux_txt_placeholder_field" placeholder="<?php echo esc_attr( $cb_appearance_placeholder ); ?>">
							</div>
							<div class="form-group card_number_placeholder_settings" style="display:none;">
								<label class="control-label">
									<?php echo esc_attr( $cb_appearance_card_number_placeholder_label ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_card_number_placeholder_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" name="card_number_placeholder" placeholder="<?php echo esc_attr( $cb_appearance_card_number_placeholder ); ?>">
							</div>
							<div class="form-group expiry_date_placeholder_settings" style="display:none;">
								<label class="control-label">
									<?php echo esc_attr( $cb_appearance_expiry_date_placeholder_label ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_expiry_date_placeholder_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" name="expiry_date_placeholder" placeholder="<?php echo esc_attr( $cb_appearance_expiry_date_placeholder ); ?>">
							</div>
							<div class="form-group card_cvv_number_placeholder_settings" style="display:none;">
								<label class="control-label">
									<?php echo esc_attr( $cb_cvv_number_placeholder_label ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_cvv_number_placeholder_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" name="card_cvv_number_placeholder" Placeholder="<?php echo esc_attr( $cb_cvv_number_placeholder ); ?>">
							</div>
							<div class="form-group custom_validation_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_custom_validation_message ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_custom_validation_message_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" placeholder="<?php echo esc_attr( $cb_custom_validation_message_placeholder ); ?>" value="This field is required">
							</div>
							<div class="form-group rows_number">
								<label class="control-label">
									<?php echo esc_attr( $cb_appearance_rows ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_rows_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" onkeypress="enter_only_digits_contact_bank(event);" maxlength="3" placeholder="<?php echo esc_attr( $cb_appearance_rows_placeholder ); ?>">
							</div>
							<div class="row class_settings">
								<div class="col-md-6">
									<div class="form-group">
										<label class="control-label">
											<?php echo esc_attr( $cb_appearance_container_class ); ?> :
											<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_container_class_tooltip ); ?>" data-placement="right"></i>
											<span class="required" aria-required="true">*</span>
										</label>
										<input type="text" class="form-control" placeholder="<?php echo esc_attr( $cb_appearance_container_class_placeholder ); ?>">
									</div>
								</div>
								<div class="col-md-6">
									<div class="form-group">
										<label class="control-label">
											<?php echo esc_attr( $cb_appearance_element_class ); ?> :
											<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_appearance_element_class_tooltip ); ?>" data-placement="right"></i>
											<span class="required" aria-required="true">*</span>
										</label>
										<input type="text" class="form-control" placeholder="<?php echo esc_attr( $cb_appearance_element_class_placeholder ); ?>">
									</div>
								</div>
							</div>
						</div>
						<div class="tab-pane restrictions_settings" id="restriction">
							<div class="form-group required_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_restrictions_required ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_required_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<select class="form-control">
									<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
									<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
								</select>
							</div>
							<div class="form-group limit_input_number_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_restrictions_limit_input_number ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_limit_input_number_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<div class="row">
									<div class="col-md-6">
										<input type="text" class="form-control" value="50" placeholder="<?php echo esc_attr( $cb_restrictions_limit_input_number_placeholder ); ?>">
									</div>
									<div class="col-md-6">
										<select class="form-control">
											<option value="characters"><?php echo esc_attr( $cb_restrictions_characters ); ?></option>
											<option value="digits"><?php echo esc_attr( $cb_restrictions_words ); ?></option>
										</select>
									</div>
								</div>
							</div>
							<div class="form-group text_appear_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_restrictions_text_appear_after_counter ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_text_appear_after_counter_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" value="Characters Left" placeholder="<?php echo esc_attr( $cb_restrictions_text_appear_after_counter_placeholder ); ?>">
							</div>
							<div class="row autocomplete_settings">
								<div class="col-md-6 enable_autocomplete">
									<div class="form-group">
										<label class="control-label">
											<?php echo esc_attr( $cb_restrictions_required_disabled_autocomplete ); ?> :
											<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_required_disabled_autocomplete_tooltip ); ?>" data-placement="right"></i>
											<span class="required" aria-required="true">*</span>
										</label>
										<select class="form-control">
											<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
											<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
										</select>
									</div>
								</div>
								<div class="col-md-6 enable_disable_input">
									<div class="form-group disable_input_settings">
										<label class="control-label">
											<?php echo esc_attr( $cb_restrictions_required_disabled_input ); ?> :
											<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_required_disabled_input_tooltip ); ?>" data-placement="right"></i>
											<span class="required" aria-required="true">*</span>
										</label>
										<select class="form-control" >
											<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
											<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
										</select>
									</div>
								</div>
							</div>
							<div class="form-group input_mask_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_restrictions_input_masking ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_input_masking_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<select class="form-control" >
									<option value="none"><?php echo esc_attr( $cb_restriction_none ); ?></option>
									<option value="us_phone"><?php echo esc_attr( $cb_restriction_us_phone ); ?></option>
									<option value="date"><?php echo esc_attr( $cb_restriction_date ); ?></option>
									<option value="custom"><?php echo esc_attr( $cb_restriction_custom ); ?></option>
								</select>
							</div>
							<div class="form-group custom_mask_settings">
								<label class="control-label">
									<?php echo esc_attr( $cb_restrictions_custom_masking ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_restrictions_custom_masking_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control"  value="999,999,999,999" placeholder="<?php echo esc_attr( $cb_restrictions_custom_masking_placeholder ); ?>">
							</div>
						</div>
						<div class="tab-pane advanced_settings" id="advanced">
							<div class="form-group">
								<label class="control-label">
									<?php echo esc_attr( $cb_advanced_field_key ); ?> :
									<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_advanced_field_key_tooltip ); ?>" data-placement="right"></i>
									<span class="required" aria-required="true">*</span>
								</label>
								<input type="text" class="form-control" placeholder="<?php echo esc_attr( $cb_advanced_field_key_placeholder ); ?>">
							</div>
							<div class="row">
								<div class="col-md-6 default_value_settings">
									<div class="form-group">
										<label class="control-label">
											<?php echo esc_attr( $cb_advanced_default_value ); ?> :
											<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_advanced_default_value_tooltip ); ?>" data-placement="right"></i>
											<span class="required" aria-required="true">*</span>
										</label>
										<input type="text" class="form-control" placeholder="<?php echo esc_attr( $cb_advanced_default_value_placeholder ); ?>">
										<select id="ux_default_state" class="form-control us-states" style="display: none;">
										</select>
										<select id="ux_default_country" class="form-control countries-list" style="display:none;">
										</select>
									</div>
								</div>
								<div class="col-md-6 admin_label_settings">
									<div class="form-group">
										<label class="control-label">
											<?php echo esc_attr( $cb_advanced_admin_label ); ?> :
											<i class="icon-custom-question tooltips" data-original-title="<?php echo esc_attr( $cb_advanced_admin_label_tooltip ); ?>" data-placement="right"></i>
											<span class="required" aria-required="true">*</span>
										</label>
										<input type="text" class="form-control" placeholder="<?php echo esc_attr( $cb_advanced_admin_label_placeholder ); ?>">
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
