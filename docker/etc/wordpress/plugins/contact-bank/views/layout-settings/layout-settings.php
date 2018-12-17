<?php
/**
 * Template to view and update the settings for Layout Setting.
 *
 * @author  Tech Banker
 * @package contact-bank/views/layout-settings
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
	} elseif ( LAYOUT_SETTINGS_CONTACT_BANK === '1' ) {
		$layout_settings_input_field_font_style   = isset( $layout_settings_data['layout_settings_input_field_font_style'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_input_field_font_style'] ) ) : array( 14, '#100000' );
		$layout_settings_input_field_border_style = isset( $layout_settings_data['layout_settings_input_field_border_style'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_input_field_border_style'] ) ) : array( 5, 'none', '#000000' );
		$layout_settings_input_field_margin       = isset( $layout_settings_data['layout_settings_input_field_margin'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_input_field_margin'] ) ) : array( 0, 0, 0, 0 );
		$layout_settings_input_field_padding      = isset( $layout_settings_data['layout_settings_input_field_padding'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_input_field_padding'] ) ) : array( 0, 0, 0, 0 );

		$layout_settings_button_font_style   = isset( $layout_settings_data['layout_settings_button_font_style'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_button_font_style'] ) ) : array( 12, '#000000' );
		$layout_settings_button_border_style = isset( $layout_settings_data['layout_settings_button_border_style'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_button_border_style'] ) ) : array( 5, 'none', '#000000' );
		$layout_settings_button_margin       = isset( $layout_settings_data['layout_settings_button_margin'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_button_margin'] ) ) : array( 0, 0, 0, 0 );
		$layout_settings_button_padding      = isset( $layout_settings_data['layout_settings_button_padding'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_button_padding'] ) ) : array( 0, 0, 0, 0 );

		$form_design_title_font_style         = isset( $layout_settings_data['layout_settings_form_design_title_font_style'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_form_design_title_font_style'] ) ) : array( 24, '#000000' );
		$form_design_description_font_style   = isset( $layout_settings_data['layout_settings_form_design_description_font_style'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_form_design_description_font_style'] ) ) : array( 24, '#000000' );
		$form_design_form_margin              = isset( $layout_settings_data['layout_settings_form_design_form_margin'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_form_design_form_margin'] ) ) : array( 0, 0, 0, 0 );
		$form_design_form_padding             = isset( $layout_settings_data['layout_settings_form_design_form_padding'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_form_design_form_padding'] ) ) : array( 0, 0, 0, 0 );
		$form_design_title_form_margin        = isset( $layout_settings_data['layout_settings_form_design_title_margin'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_form_design_title_margin'] ) ) : array( 0, 0, 0, 0 );
		$form_design_title_form_padding       = isset( $layout_settings_data['layout_settings_form_design_title_padding'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_form_design_title_padding'] ) ) : array( 0, 0, 0, 0 );
		$form_design_description_form_margin  = isset( $layout_settings_data['layout_settings_form_design_description_margin'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_form_design_description_margin'] ) ) : array( 0, 0, 0, 0 );
		$form_design_description_form_padding = isset( $layout_settings_data['layout_settings_form_design_description_padding'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_form_design_description_padding'] ) ) : array( 0, 0, 0, 0 );

		$layout_settings_label_field_font_style = isset( $layout_settings_data['layout_settings_label_field_font_style'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_label_field_font_style'] ) ) : array( 24, '#000000' );
		$layout_settings_label_field_margin     = isset( $layout_settings_data['layout_settings_label_field_margin'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_label_field_margin'] ) ) : array( 0, 0, 0, 0 );
		$layout_settings_label_field_padding    = isset( $layout_settings_data['layout_settings_label_field_padding'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_label_field_padding'] ) ) : array( 0, 0, 0, 0 );

		$layout_settings_messages_font_style = isset( $layout_settings_data['layout_settings_messages_font_style'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_messages_font_style'] ) ) : array( 24, '#000000' );
		$layout_settings_messages_margin     = isset( $layout_settings_data['layout_settings_messages_margin'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_messages_margin'] ) ) : array( 0, 0, 0, 0 );
		$layout_settings_messages_padding    = isset( $layout_settings_data['layout_settings_messages_padding'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_messages_padding'] ) ) : array( 0, 0, 0, 0 );

		$layout_settings_input_field_background_color_transparency = isset( $layout_settings_data['layout_settings_input_field_background_color_transparency'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_input_field_background_color_transparency'] ) ) : array( '#000000', 100 );
		$layout_settings_label_field_background_color_transparency = isset( $layout_settings_data['layout_settings_label_field_background_color_transparency'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_label_field_background_color_transparency'] ) ) : array( '#000000', 100 );
		$layout_settings_messages_background_color_transparency    = isset( $layout_settings_data['layout_settings_messages_background_color_transparency'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_messages_background_color_transparency'] ) ) : array( '#000000', 100 );

		$layout_settings_error_messages_font_style = isset( $layout_settings_data['layout_settings_error_messages_font_style'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_error_messages_font_style'] ) ) : array( 18, '#6aa500' );
		$layout_settings_error_messages_margin     = isset( $layout_settings_data['layout_settings_error_messages_margin'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_error_messages_margin'] ) ) : array( 0, 0, 0, 0 );
		$layout_settings_error_messages_padding    = isset( $layout_settings_data['layout_settings_error_messages_padding'] ) ? explode( ',', esc_attr( $layout_settings_data['layout_settings_error_messages_padding'] ) ) : array( 0, 0, 0, 0 );
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
					<span>
						<?php echo esc_attr( $cb_layout_settings ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-settings"></i>
							<?php echo esc_attr( $cb_layout_settings ); ?>
						</div>
						<p class="premium-editions">
							<?php echo esc_attr( $cb_upgrade_need_help ); ?><a href="https://contact-bank.tech-banker.com/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_documentation ); ?></a><?php echo esc_attr( $cb_read_and_check ); ?><a href="https://contact-bank.tech-banker.com/frontend-demos/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_demos_section ); ?></a>
						</p>
					</div>
					<div class="portlet-body form">
						<form id="ux_frm_layout_settings">
							<div class="form-body">
								<div class="form-actions">
									<div class="pull-right">
										<input type="submit" class="btn vivid-green" name="ux_btn_save_changes" id="ux_btn_save_changes" value="<?php echo esc_attr( $cb_save_changes ); ?>">
									</div>
								</div>
								<div class="line-separator"></div>
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_choose_templates ); ?> :
										<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?> </span>
									</label>
									<select id="ux_ddl_choose_template" name="ux_ddl_choose_template" class="form-control" onchange="layout_settings_data();">
										<option value=""><?php echo esc_attr( $cb_choose_form ); ?></option>
										<?php
										foreach ( $unserialized_layouts_forms_data_array as $data ) {
											?>
											<option value="<?php echo intval( $data['old_form_id'] ); ?>"><?php echo isset( $data['form_title'] ) && '' !== $data['form_title'] ? esc_attr( $data['form_title'] ) : esc_attr( $cb_untitled_form ); ?></option>
											<?php
										}
										?>
									</select>
									<i class="controls-description"><?php echo esc_attr( $cb_choose_templates_tooltip ); ?></i>
								</div>
								<div class="tabbable-custom"  id="ux_div_choose_template" style="display: none;">
									<ul class="nav nav-tabs ">
										<li class="active">
											<a aria-expanded="true" href="#form_design_layout" data-toggle="tab">
												<?php echo esc_attr( $cb_form_design ); ?>
											</a>
										</li>
										<li>
											<a aria-expanded="true" href="#input_fields_layout" data-toggle="tab">
												<?php echo esc_attr( $cb_input_fields ); ?>
											</a>
										</li>
										<li>
											<a aria-expanded="true" href="#label_fields_layout" data-toggle="tab">
												<?php echo esc_attr( $cb_label_fields ); ?>
											</a>
										</li>
										<li>
											<a aria-expanded="true" href="#button_layout" data-toggle="tab">
												<?php echo esc_attr( $cb_buttons ); ?>
											</a>
										</li>
										<li>
											<a aria-expanded="true" href="#messages_layout" data-toggle="tab">
												<?php echo esc_attr( $cb_messages ); ?>
											</a>
										</li>
										<li>
											<a aria-expanded="true" href="#error_fields_layout" data-toggle="tab">
												<?php echo esc_attr( $cb_error_fields ); ?>
											</a>
										</li>
									</ul>
									<div class="tab-content">
										<div class="tab-pane active" id="form_design_layout">
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_form_width ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?> </span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_form_design_form_width" id="ux_txt_form_design_form_width" placeholder="<?php echo esc_attr( $cb_form_width ); ?>"  maxlength="6" onblur="default_value_contact_bank('#ux_txt_form_design_form_width', '100%')" value="<?php echo isset( $layout_settings_data['layout_settings_form_design_width'] ) ? esc_attr( $layout_settings_data['layout_settings_form_design_width'] ) : '100%'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_layout_settings_form_width_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_form_position ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?> </span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_form_design_form_position" id="ux_ddl_form_design_form_position" class="form-control">
																<option value="left"><?php echo esc_attr( $cb_left ); ?></option>
																<option value="center"><?php echo esc_attr( $cb_center ); ?></option>
																<option value="right"><?php echo esc_attr( $cb_right ); ?></option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_form_position_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_background_color ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?> </span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_form_design_background_color" id="ux_txt_form_design_background_color" placeholder="<?php echo esc_attr( $cb_background_color ); ?>" onfocus="color_picker_contact_bank(this, this.value)" value="<?php echo isset( $layout_settings_data['layout_settings_form_design_background_color'] ) ? esc_attr( $layout_settings_data['layout_settings_form_design_background_color'] ) : '#cccccc'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_background_color_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_background_transparency ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_form_design_background_color_transparency" id="ux_txt_form_design_background_color_transparency" maxlength="3" placeholder="<?php echo esc_attr( $cb_background_transparency ); ?>"  onblur="default_value_contact_bank('#ux_txt_form_design_background_color_transparency', 100)" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" onchange="check_opacity_contact_bank(this);" value="<?php echo isset( $layout_settings_data['layout_settings_form_design_background_transparency'] ) ? intval( $layout_settings_data['layout_settings_form_design_background_transparency'] ) : 100; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_background_transparency_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_title_html_tag ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_form_design_title_html_tag" id="ux_ddl_form_design_title_html_tag" class="form-control">
																<option value="h1"><?php echo esc_attr( $cb_h1_tag ); ?></option>
																<option value="h2"><?php echo esc_attr( $cb_h2_tag ); ?></option>
																<option value="h3"><?php echo esc_attr( $cb_h3_tag ); ?></option>
																<option value="h4"><?php echo esc_attr( $cb_h4_tag ); ?></option>
																<option value="h5"><?php echo esc_attr( $cb_h5_tag ); ?></option>
																<option value="h6"><?php echo esc_attr( $cb_h6_tag ); ?></option>
																<option value="blockquote"><?php echo esc_attr( $cb_blockquote_tag ); ?></option>
																<option value="p"><?php echo esc_attr( $cb_paragraph_tag ); ?></option>
																<option value="span"><?php echo esc_attr( $cb_span_tag ); ?></option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_layout_settings_title_html_tag_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_title_alignment ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_form_design_title_form_position" id="ux_ddl_form_design_title_form_position" class="form-control">
																<option value="left"><?php echo esc_attr( $cb_left ); ?></option>
																<option value="center"><?php echo esc_attr( $cb_center ); ?></option>
																<option value="right"><?php echo esc_attr( $cb_right ); ?></option>
																<option value="justify"><?php echo esc_attr( $cb_justify ); ?></option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_alignment_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_title_font_style ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_form_design_title_font_style[]" id="ux_txt_form_design_title_font_size" placeholder="<?php echo esc_attr( $cb_font_size_placeholder ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_title_font_size', 24);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_title_font_style[0] ); ?>">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_form_design_title_font_style[]" id="ux_txt_form_design_title_style_color" onfocus="color_picker_contact_bank(this, this.value)" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo esc_attr( $form_design_title_font_style[1] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_style_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_title_font_family ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_form_design_title_font_family" id="ux_ddl_form_design_title_font_family" class="form-control">
																<?php
																if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php' ) ) {
																	include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php';
																}
																?>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_family_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_description_html_tag ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_form_design_description_html_tag" id="ux_ddl_form_design_description_html_tag" class="form-control">
																<option value="h1"><?php echo esc_attr( $cb_h1_tag ); ?></option>
																<option value="h2"><?php echo esc_attr( $cb_h2_tag ); ?></option>
																<option value="h3"><?php echo esc_attr( $cb_h3_tag ); ?></option>
																<option value="h4"><?php echo esc_attr( $cb_h4_tag ); ?></option>
																<option value="h5"><?php echo esc_attr( $cb_h5_tag ); ?></option>
																<option value="h6"><?php echo esc_attr( $cb_h6_tag ); ?></option>
																<option value="blockquote"><?php echo esc_attr( $cb_blockquote_tag ); ?></option>
																<option value="p"><?php echo esc_attr( $cb_paragraph_tag ); ?></option>
																<option value="span"><?php echo esc_attr( $cb_span_tag ); ?></option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_layout_settings_title_html_tag_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_description_alignment ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_form_design_description_form_position" id="ux_ddl_form_design_description_form_position" class="form-control">
																<option value="left"><?php echo esc_attr( $cb_left ); ?></option>
																<option value="center"><?php echo esc_attr( $cb_center ); ?></option>
																<option value="right"><?php echo esc_attr( $cb_right ); ?></option>
																<option value="justify"><?php echo esc_attr( $cb_justify ); ?></option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_description_alignment_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_description_font_style ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_form_design_description_font_style[]" id="ux_txt_form_design_description_font_size" placeholder="<?php echo esc_attr( $cb_font_size_placeholder ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_description_font_size', 24);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_description_font_style[0] ); ?>">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_form_design_description_font_style[]" id="ux_txt_form_design_description_font_style" onfocus="color_picker_contact_bank(this, this.value)" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo esc_attr( $form_design_description_font_style[1] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_style_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_description_font_family ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_form_design_description_font_family" id="ux_ddl_form_design_description_font_family" class="form-control">
																	<?php
																	if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php' ) ) {
																		include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php';
																	}
																?>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_family_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_form_margin ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_form_margin_text[]" id="ux_txt_form_design_form_margin_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_form_margin_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_form_margin[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_form_margin_text[]" id="ux_txt_form_design_form_margin_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_form_margin_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_form_margin[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_form_margin_text[]" id="ux_txt_form_design_form_margin_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_form_margin_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_form_margin[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_form_margin_text[]" id="ux_txt_form_design_form_margin_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_form_margin_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_form_margin[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_margin_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_form_padding ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_form_padding_text[]" id="ux_txt_form_design_form_padding_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_form_padding_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_form_padding[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_form_padding_text[]" id="ux_txt_form_design_form_padding_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_form_padding_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_form_padding[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_form_padding_text[]" id="ux_txt_form_design_form_padding_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_form_padding_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_form_padding[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_form_padding_text[]" id="ux_txt_form_design_form_padding_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_form_padding_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_form_padding[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_form_padding_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_title_margin ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_title_margin_text[]" id="ux_txt_form_design_title_margin_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_title_margin_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_title_form_margin[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_title_margin_text[]" id="ux_txt_form_design_title_margin_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_title_margin_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_title_form_margin[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_title_margin_text[]" id="ux_txt_form_design_title_margin_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_title_margin_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_title_form_margin[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_title_margin_text[]" id="ux_txt_form_design_title_margin_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_title_margin_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_title_form_margin[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_margin_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_title_padding ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_title_padding_text[]" id="ux_txt_form_design_title_padding_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_title_padding_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_title_form_padding[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_title_padding_text[]" id="ux_txt_form_design_title_padding_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_title_padding_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_title_form_padding[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_title_padding_text[]" id="ux_txt_form_design_title_padding_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_title_padding_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_title_form_padding[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_title_padding_text[]" id="ux_txt_form_design_title_padding_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_title_padding_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_title_form_padding[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_padding_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_description_margin ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_description_margin_text[]" id="ux_txt_form_design_description_margin_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_description_margin_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_description_form_margin[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_description_margin_text[]" id="ux_txt_form_design_description_margin_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_description_margin_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_description_form_margin[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_description_margin_text[]" id="ux_txt_form_design_description_margin_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_description_margin_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_description_form_margin[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_description_margin_text[]" id="ux_txt_form_design_description_margin_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_description_margin_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_description_form_margin[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_margin_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_description_padding ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_description_padding_text[]" id="ux_txt_form_design_description_padding_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_description_padding_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_description_form_padding[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_description_padding_text[]" id="ux_txt_form_design_description_padding_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_description_padding_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_description_form_padding[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_description_padding_text[]" id="ux_txt_form_design_description_padding_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_description_padding_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_description_form_padding[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_form_design_description_padding_text[]" id="ux_txt_form_design_description_padding_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_form_design_description_padding_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $form_design_description_form_padding[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_description_padding_tooltips ); ?></i>
													</div>
												</div>
											</div>
										</div>
										<div class="tab-pane" id="input_fields_layout">
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_input_field_width ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class= "input-icon right">
															<input type="text" class="form-control" name="ux_txt_input_field_width" id="ux_txt_input_field_width" placeholder="<?php echo esc_attr( $cb_input_field_width ); ?>" maxlength="5" onblur="default_value_contact_bank('#ux_txt_input_field_width', '100%')"  onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo isset( $layout_settings_data['layout_settings_input_field_width'] ) ? esc_attr( $layout_settings_data['layout_settings_input_field_width'] ) : '100%'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_layout_settings_form_width_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_input_field_height ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_input_field_height" id="ux_txt_input_field_height" maxlength="5" placeholder="<?php echo esc_attr( $cb_input_field_height ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_height', '100%')"  onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo isset( $layout_settings_data['layout_settings_input_field_height'] ) ? esc_attr( $layout_settings_data['layout_settings_input_field_height'] ) : '100%'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_field_height_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_alignment ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_input_field_text_alignment" id="ux_ddl_input_field_text_alignment" class="form-control">
																<option value="left"><?php echo esc_attr( $cb_left ); ?></option>
																<option value="center"><?php echo esc_attr( $cb_center ); ?></option>
																<option value="right"><?php echo esc_attr( $cb_right ); ?></option>
																<option value="justify"><?php echo esc_attr( $cb_justify ); ?> </option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_alignment_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_input_field_background_color_transparency ); ?> :
															<span class="required" aria-required="true">* </span>
														</label>
														<div class= "input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline valid" name="ux_txt_input_field_background_color_transparency[]" id="ux_txt_input_field_background_color" onfocus="color_picker_contact_bank(this, this.value)" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo isset( $layout_settings_input_field_background_color_transparency[0] ) ? esc_attr( $layout_settings_input_field_background_color_transparency[0] ) : '#cccccc'; ?>">
															<input type="text" class="form-control custom-input-medium input-inline valid" name="ux_txt_input_field_background_color_transparency[]" id="ux_txt_input_field_background_transparency" placeholder="<?php echo esc_attr( $cb_button_bg_transparency ); ?>" value="<?php echo isset( $layout_settings_input_field_background_color_transparency[1] ) ? intval( $layout_settings_input_field_background_color_transparency[1] ) : '100'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_input_field_background_color_transparency_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_input_field_radio_button_alignment ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_input_field_radio_button_alignment" id="ux_ddl_input_field_radio_button_alignment" class="form-control">
																<option value="single_row"><?php echo esc_attr( $cb_single_row ); ?></option>
																<option value="multiple_row"><?php echo esc_attr( $cb_multiple_row ); ?></option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_input_field_radio_button_alignment_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_input_field_checkbox_alignment ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_input_field_checkbox_alignment" id="ux_ddl_input_field_checkbox_alignment" class="form-control">
																<option value="single_row"><?php echo esc_attr( $cb_single_row ); ?></option>
																<option value="multiple_row"><?php echo esc_attr( $cb_multiple_row ); ?></option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_input_field_checkbox_alignment_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_font_style ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_input_field_font_style[]" id="ux_txt_input_field_font_size" placeholder="<?php echo esc_attr( $cb_font_size_placeholder ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_font_size', 14)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_font_style[0] ); ?>">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_input_field_font_style[]" id="ux_txt_input_field_font_color" onfocus="color_picker_contact_bank(this, this.value)" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo esc_attr( $layout_settings_input_field_font_style[1] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_style_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_font_family ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_input_field_font_family" id="ux_ddl_input_field_font_family" class="form-control">
																	<?php
																	if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php' ) ) {
																		include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php';
																	}
																?>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_font_family_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_border_style ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control input-width-25 input-inline" name="ux_txt_input_field_border_style[]" id="ux_txt_input_field_border_style_width" placeholder="<?php echo esc_attr( $cb_button_border_width_placeholder ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_border_style_width', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_border_style[0] ); ?>">
															<select name="ux_txt_input_field_border_style[]" id="ux_ddl_input_field_border_style_thickness" class="form-control input-width-27 input-inline">
																<option value="none"><?php echo esc_attr( $cb_none ); ?></option>
																<option value="solid"><?php echo esc_attr( $cb_solid ); ?></option>
																<option value="dashed"><?php echo esc_attr( $cb_dashed ); ?></option>
																<option value="dotted"><?php echo esc_attr( $cb_dotted ); ?></option>
															</select>
															<input type="text" class="form-control input-normal input-inline" name="ux_txt_input_field_border_style[]" id="ux_txt_input_field_border_style_color" onfocus="color_picker_contact_bank(this, this.value)" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_input_field_border_style_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_border_radius ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_input_field_border_radius" id="ux_txt_input_field_border_radius" placeholder="<?php echo esc_attr( $cb_border_radius ); ?>" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onblur="default_value_contact_bank('#ux_txt_input_field_border_radius', 0)" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo isset( $layout_settings_data['layout_settings_input_field_border_radius'] ) ? intval( $layout_settings_data['layout_settings_input_field_border_radius'] ) : 0; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_input_field_border_radius_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_margin_title ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_input_field_margin[]" id="ux_txt_input_field_margin_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_margin_top', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_margin[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_input_field_margin[]" id="ux_txt_input_field_margin_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_margin_right', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_margin[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_input_field_margin[]" id="ux_txt_input_field_margin_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_margin_bottom', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_margin[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_input_field_margin[]" id="ux_txt_input_field_margin_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_margin_left', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_margin[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_margin_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_padding ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_input_field_padding[]" id="ux_txt_input_field_padding_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_padding_top', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_padding[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_input_field_padding[]" id="ux_txt_input_field_padding_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_padding_right', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_padding[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_input_field_padding[]" id="ux_txt_input_field_padding_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_padding_bottom', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_padding[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_input_field_padding[]" id="ux_txt_input_field_padding_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_input_field_padding_left', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_input_field_padding[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_input_field_padding_tooltip ); ?></i>
													</div>
												</div>
											</div>
										</div>
										<div class="tab-pane" id="label_fields_layout">
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_label_field_width_title ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<input type="text" class="form-control" name="ux_txt_label_field_width" id="ux_txt_label_field_width" value="<?php echo isset( $layout_settings_data['layout_settings_label_field_width'] ) ? esc_attr( $layout_settings_data['layout_settings_label_field_width'] ) : '100%'; ?>" placeholder="<?php echo esc_attr( $cb_label_field_width_title ); ?>" onblur="default_value_contact_bank('#ux_txt_label_field_width', '100%');"  maxlength="5" onfocus="paste_prevent_contact_bank(this.id);">
														<i class="controls-description"><?php echo esc_attr( $cb_layout_settings_form_width_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_label_field_height_title ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<input type="text" class="form-control" name="ux_txt_label_field_height" id="ux_txt_label_field_height" value="<?php echo isset( $layout_settings_data['layout_settings_label_field_height'] ) ? esc_attr( $layout_settings_data['layout_settings_label_field_height'] ) : '100%'; ?>" placeholder="<?php echo esc_attr( $cb_label_field_height_title ); ?>" onblur="default_value_contact_bank('#ux_txt_label_field_height', '100%');"  maxlength="5" onfocus="paste_prevent_contact_bank(this.id);">
														<i class="controls-description"><?php echo esc_attr( $cb_field_height_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_alignment ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<select name="ux_ddl_label_field_text_alignment" id="ux_ddl_label_field_text_alignment" class="form-control">
															<option value="left"><?php echo esc_attr( $cb_left ); ?></option>
															<option value="center"><?php echo esc_attr( $cb_center ); ?></option>
															<option value="right"><?php echo esc_attr( $cb_right ); ?></option>
															<option value="justify"><?php echo esc_attr( $cb_justify ); ?></option>
														</select>
														<i class="controls-description"><?php echo esc_attr( $cb_alignment_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_label_field_background_color_transparency ); ?> :
															<span class="required" aria-required="true">* </span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline valid" name="ux_txt_label_field_background_color_transparency[]" id="ux_txt_label_field_background_color" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" onfocus="color_picker_contact_bank(this, this.value)" value="<?php echo isset( $layout_settings_label_field_background_color_transparency[0] ) ? esc_attr( $layout_settings_label_field_background_color_transparency[0] ) : '#000000'; ?>">
															<input type="text" class="form-control custom-input-medium input-inline valid" name="ux_txt_label_field_background_color_transparency[]" id="ux_txt_label_field_background_transparency" placeholder="<?php echo esc_attr( $cb_button_bg_transparency ); ?>" value="<?php echo isset( $layout_settings_label_field_background_color_transparency[1] ) ? intval( $layout_settings_label_field_background_color_transparency[1] ) : '100'; ?>">
													</div>
													<i class="controls-description"><?php echo esc_attr( $cb_label_field_background_color_tooltips ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_font_style ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_label_field_font_style[]" id="ux_txt_label_field_font_size" placeholder="<?php echo esc_attr( $cb_font_size_placeholder ); ?>" onblur="default_value_contact_bank('#ux_txt_label_field_font_size', 16);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo isset( $layout_settings_label_field_font_style[0] ) ? intval( $layout_settings_label_field_font_style[0] ) : 16; ?>">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_label_field_font_style[]" id="ux_txt_label_field_style_color" onfocus="color_picker_contact_bank(this, this.value)" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo isset( $layout_settings_label_field_font_style[1] ) ? esc_attr( $layout_settings_label_field_font_style[1] ) : '#000000'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_style_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_font_family ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<select name="ux_ddl_label_field_font_family" id="ux_ddl_label_field_font_family" class="form-control">
															<?php
															if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php' ) ) {
																include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php';
															}
																?>
														</select>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_family_tooltips ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_margin_title ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_label_field_margin[]" id="ux_txt_label_field_margin_top_text" placeholder="<?php echo esc_attr( $cb_top ); ?>" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" onblur="default_value_contact_bank('#ux_txt_label_field_margin_top_text', 0);" value="<?php echo intval( $layout_settings_label_field_margin[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_label_field_margin[]" id="ux_txt_label_field_margin_right_text" placeholder="<?php echo esc_attr( $cb_right ); ?>" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" onblur="default_value_contact_bank('#ux_txt_label_field_margin_right_text', 0);" value="<?php echo intval( $layout_settings_label_field_margin[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_label_field_margin[]" id="ux_txt_label_field_margin_bottom_text" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" onblur="default_value_contact_bank('#ux_txt_label_field_margin_bottom_text', 0);"   value="<?php echo intval( $layout_settings_label_field_margin[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_label_field_margin[]" id="ux_txt_label_field_margin_left_text" placeholder="<?php echo esc_attr( $cb_left ); ?>" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" onblur="default_value_contact_bank('#ux_txt_label_field_margin_left_text', 0);"   value="<?php echo intval( $layout_settings_label_field_margin[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_margin_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_padding ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_label_field_padding[]" id="ux_txt_label_field_padding_top_text" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_label_field_padding_top_text', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_label_field_padding[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_label_field_padding[]" id="ux_txt_label_field_padding_right_text" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_label_field_padding_right_text', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_label_field_padding[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_label_field_padding[]" id="ux_txt_label_field_padding_bottom_text" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_label_field_padding_bottom_text', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_label_field_padding[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_label_field_padding[]" id="ux_txt_label_field_padding_left_text" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_label_field_padding_left_text', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_label_field_padding[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_padding_label_field_tooltip ); ?></i>
													</div>
												</div>
											</div>
										</div>
										<div class="tab-pane" id="button_layout">
											<div class="row" >
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_button_width ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_frm_button_width" id="ux_frm_button_width" placeholder="<?php echo esc_attr( $cb_button_width ); ?>" onblur="default_value_contact_bank('#ux_frm_button_width', '100%');" onchange="" maxlength="5"  onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo isset( $layout_settings_data['layout_settings_button_width'] ) ? esc_attr( $layout_settings_data['layout_settings_button_width'] ) : '100%'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_layout_settings_form_width_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_button_height ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_frm_button_height" id="ux_frm_button_height" placeholder="<?php echo esc_attr( $cb_button_height ); ?>" onblur="default_value_contact_bank('#ux_frm_button_height', '100%');" onchange="" maxlength="5" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo isset( $layout_settings_data['layout_settings_button_height'] ) ? esc_attr( $layout_settings_data['layout_settings_button_height'] ) : '100%'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_field_height_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row" >
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_button_text ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_frm_button_text" id="ux_frm_button_text" onblur="default_value_contact_bank('#ux_frm_button_text', 'Submit');" onfocus="paste_prevent_contact_bank(this.id);" placeholder="<?php echo esc_attr( $cb_button_text ); ?>" value="<?php echo isset( $layout_settings_data['layout_settings_button_text'] ) ? esc_attr( $layout_settings_data['layout_settings_button_text'] ) : 'Submit'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_button_text_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_alignment ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_button_text_alignment" id="ux_ddl_button_text_alignment" class="form-control">
																<option value="left"><?php echo esc_attr( $cb_left ); ?></option>
																<option value="center"><?php echo esc_attr( $cb_center ); ?></option>
																<option value="right"><?php echo esc_attr( $cb_right ); ?></option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_alignment_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_button_font_style ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_button_font_style[]" id="ux_txt_button_font_size" onblur="default_value_contact_bank('#ux_txt_button_font_size', 12);" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" placeholder="<?php echo esc_attr( $cb_font_size_placeholder ); ?>" value="<?php echo intval( $layout_settings_button_font_style[0] ); ?>">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_button_font_style[]" id="ux_txt_button_style_color" onfocus="color_picker_contact_bank(this, this.value);" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo esc_attr( $layout_settings_button_font_style[1] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_style_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_button_font_family_title ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_button_title_font_family" id="ux_ddl_button_title_font_family" class="form-control">
																<?php
																if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php' ) ) {
																	include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php';
																}
																?>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_family_tooltips ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_button_bg_color ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_button_bg_color" id="ux_txt_button_bg_color" onfocus="color_picker_contact_bank(this, this.value);" placeholder="<?php echo esc_attr( $cb_button_bg_color_placeholder ); ?>" value="<?php echo isset( $layout_settings_data['layout_settings_button_background_color'] ) ? esc_attr( $layout_settings_data['layout_settings_button_background_color'] ) : '#000000'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_button_bg_color_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_button_bg_transparency ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_button_bg_transparency" id="ux_txt_button_bg_transparency" placeholder="<?php echo esc_attr( $cb_button_bg_transparency ); ?>" value="<?php echo isset( $layout_settings_data['layout_settings_button_background_transparency'] ) ? esc_attr( $layout_settings_data['layout_settings_button_background_transparency'] ) : '100'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_button_bg_transparency_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_button_hover_bg_color ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_button_hover_bg_color" id="ux_txt_button_hover_bg_color" onfocus="color_picker_contact_bank(this, this.value);" placeholder="<?php echo esc_attr( $cb_button_hover_bg_color_placeholder ); ?>" value="<?php echo isset( $layout_settings_data['layout_settings_button_hover_background_color'] ) ? esc_attr( $layout_settings_data['layout_settings_button_hover_background_color'] ) : '#000000'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_button_hover_bg_color_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_button_hover_bg_transparency ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_button_hover_bg_transparency" id="ux_txt_button_hover_bg_transparency" placeholder="<?php echo esc_attr( $cb_button_bg_transparency ); ?>" value="<?php echo isset( $layout_settings_data['layout_settings_button_hover_background_transparency'] ) ? esc_attr( $layout_settings_data['layout_settings_button_hover_background_transparency'] ) : '100'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_button_hover_bg_transparency_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_border_style_title ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control input-width-25 input-inline" name="ux_txt_button_border_style[]" id="ux_txt_button_border_style_width" placeholder="<?php echo esc_attr( $cb_button_border_width_placeholder ); ?>"  onblur="default_value_contact_bank('#ux_txt_button_border_style_width', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_button_border_style[0] ); ?>">
															<select name="ux_txt_button_border_style[]" id="ux_ddl_button_border_style_thickness" class="form-control input-width-27 input-inline">
																<option value="none"><?php echo esc_attr( $cb_none ); ?></option>
																<option value="solid"><?php echo esc_attr( $cb_solid ); ?></option>
																<option value="dashed"><?php echo esc_attr( $cb_dashed ); ?></option>
																<option value="dotted"><?php echo esc_attr( $cb_dotted ); ?></option>
															</select>
															<input type="text" class="form-control input-normal input-inline" name="ux_txt_button_border_style[]" id="ux_txt_button_border_style_color" onfocus="color_picker_contact_bank(this, this.value);"  placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo esc_attr( $layout_settings_button_border_style[2] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_border_style_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_border_radius ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_button_border_radius" id="ux_txt_button_border_radius" placeholder="<?php echo esc_attr( $cb_border_radius ); ?>" onblur="default_value_contact_bank('#ux_txt_button_border_radius', 0);" onchange="" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo isset( $layout_settings_data['layout_settings_button_border_radius'] ) ? intval( $layout_settings_data['layout_settings_button_border_radius'] ) : 0; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_button_border_radius_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="form-group">
												<label class="control-label">
													<?php echo esc_attr( $cb_border_hover_style_title ); ?> :
													<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
												</label>
												<div class="input-icon right">
													<input type="text" class="form-control" name="ux_txt_button_hover_border_color" id="ux_txt_button_hover_border_color" onfocus="color_picker_contact_bank(this, this.value);" placeholder="<?php echo esc_attr( $cb_border_hover_style_title ); ?>" value="<?php echo isset( $layout_settings_data['layout_settings_button_hover_border_color'] ) ? esc_attr( $layout_settings_data['layout_settings_button_hover_border_color'] ) : '#000000'; ?>">
												</div>
												<i class="controls-description"><?php echo esc_attr( $cb_border_hover_style_tooltip ); ?></i>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_margin_title ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_button_margin[]" id="ux_txt_button_margin_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_button_margin_top', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_button_margin[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_button_margin[]" id="ux_txt_button_margin_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_button_margin_right', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_button_margin[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_button_margin[]" id="ux_txt_button_margin_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>"  onblur="default_value_contact_bank('#ux_txt_button_margin_bottom', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_button_margin[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_button_margin[]" id="ux_txt_button_margin_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_button_margin_left', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_button_margin[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_margin_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_padding ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_button_padding[]" id="ux_txt_button_padding_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_button_padding_top', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_button_padding[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_button_padding[]" id="ux_txt_button_padding_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_button_padding_right', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_button_padding[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_button_padding[]" id="ux_txt_button_padding_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_button_padding_bottom', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_button_padding[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_button_padding[]" id="ux_txt_button_padding_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_button_padding_left', 0);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_button_padding[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_padding_tooltip ); ?></i>
													</div>
												</div>
											</div>
										</div>
										<div class="tab-pane" id="messages_layout">
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_alignment ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class= "input-icon right">
															<select name="ux_ddl_messages_text_alignment" id="ux_ddl_messages_text_alignment" class="form-control">
																<option value="left"><?php echo esc_attr( $cb_left ); ?></option>
																<option value="center"><?php echo esc_attr( $cb_center ); ?></option>
																<option value="right"><?php echo esc_attr( $cb_right ); ?></option>
																<option value="justify"><?php echo esc_attr( $cb_justify ); ?> </option>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_alignment_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_messages_background_color_transparency ); ?> :
															<span class="required" aria-required="true">* </span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline valid" name="ux_txt_contact_messages_background_color_transparency[]" id="ux_txt_contact_messages_background_color" placeholder="<?php echo esc_attr( $cb_background_color ); ?>" onfocus="color_picker_contact_bank(this, this.value)" value="<?php echo isset( $layout_settings_messages_background_color_transparency[0] ) ? esc_attr( $layout_settings_messages_background_color_transparency[0] ) : '#000000'; ?>">
															<input type="text" class="form-control custom-input-medium input-inline valid" name="ux_txt_contact_messages_background_color_transparency[]" id="ux_txt_contact_messages_background_transparency" placeholder="<?php echo esc_attr( $cb_button_bg_transparency ); ?>" value="<?php echo isset( $layout_settings_messages_background_color_transparency[1] ) ? intval( $layout_settings_messages_background_color_transparency[1] ) : '100'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_messages_background_color_transparency_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_messages_font_style ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_contact_messages_font_style[]" id="ux_txt_contact_messages_font_size" placeholder="<?php echo esc_attr( $cb_font_size_placeholder ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_font_size', 24);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_messages_font_style[0] ); ?>">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_contact_messages_font_style[]" id="ux_txt_contact_messages_style_color" onfocus="color_picker_contact_bank(this, this.value)" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo esc_attr( $layout_settings_messages_font_style[1] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_style_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_messages_font_family ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_contact_messages_font_family" id="ux_ddl_contact_messages_font_family" class="form-control">
																<?php
																if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php' ) ) {
																	include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php';
																}
																?>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_family_tooltips ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_margin_title ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_contact_messages_margin[]" id="ux_txt_contact_messages_margin_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_margin_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_messages_margin[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_contact_messages_margin[]" id="ux_txt_contact_messages_margin_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_margin_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_messages_margin[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_contact_messages_margin[]" id="ux_txt_contact_messages_margin_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_margin_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_messages_margin[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_contact_messages_margin[]" id="ux_txt_contact_messages_margin_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_margin_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_messages_margin[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_margin_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_padding ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_contact_messages_padding[]" id="ux_txt_contact_messages_padding_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_padding_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_messages_padding[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_contact_messages_padding[]" id="ux_txt_contact_messages_padding_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_padding_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_messages_padding[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_contact_messages_padding[]" id="ux_txt_contact_messages_padding_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_padding_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_messages_padding[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_contact_messages_padding[]" id="ux_txt_contact_messages_padding_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_padding_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_messages_padding[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_messages_padding_tooltip ); ?></i>
													</div>
												</div>
											</div>
										</div>
										<div class="tab-pane" id="error_fields_layout">
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_error_message_background_color ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class= "input-icon right">
															<input type="text" class="form-control" name="ux_txt_error_messages_background_color" id="ux_txt_error_messages_background_color" placeholder="<?php echo esc_attr( $cb_error_message_background_color_placeholder ); ?>" onfocus="color_picker_contact_bank(this, this.value)" value="<?php echo isset( $layout_settings_data['layout_settings_error_messages_background_color'] ) ? esc_attr( $layout_settings_data['layout_settings_error_messages_background_color'] ) : '#ffffff'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_error_message_background_color_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_error_message_background_transparency ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control" name="ux_txt_error_messages_background_transparency" id="ux_txt_error_messages_background_transparency" placeholder="<?php echo esc_attr( $cb_button_bg_transparency ); ?>" value="<?php echo isset( $layout_settings_data['layout_settings_error_messages_background_transparency'] ) ? intval( $layout_settings_data['layout_settings_error_messages_background_transparency'] ) : '50'; ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_error_message_background_transparency_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_error_message_font_style ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_error_messages_font_style[]" id="ux_txt_error_messages_font_size" placeholder="<?php echo esc_attr( $cb_font_size_placeholder ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_font_size', 24);" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_error_messages_font_style[0] ); ?>">
															<input type="text" class="form-control custom-input-medium input-inline" name="ux_txt_error_messages_font_style[]" id="ux_txt_error_messages_style_color" onfocus="color_picker_contact_bank(this, this.value)" placeholder="<?php echo esc_attr( $cb_color_placeholder ); ?>" value="<?php echo esc_attr( $layout_settings_error_messages_font_style[1] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_title_font_style_tooltips ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_error_message_font_family ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<select name="ux_ddl_error_messages_font_family" id="ux_ddl_error_messages_font_family" class="form-control">
																<?php
																if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php' ) ) {
																	include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/web-fonts.php';
																}
																?>
															</select>
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_error_message_font_family_tooltip ); ?></i>
													</div>
												</div>
											</div>
											<div class="row">
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_margin_title ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_error_messages_margin[]" id="ux_txt_error_messages_margin_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_margin_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_error_messages_margin[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_error_messages_margin[]" id="ux_txt_error_messages_margin_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_margin_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_error_messages_margin[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_error_messages_margin[]" id="ux_txt_error_messages_margin_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_margin_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_error_messages_margin[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_error_messages_margin[]" id="ux_txt_error_messages_margin_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_margin_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_error_messages_margin[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_margin_tooltip ); ?></i>
													</div>
												</div>
												<div class="col-md-6">
													<div class="form-group">
														<label class="control-label">
															<?php echo esc_attr( $cb_padding ); ?> :
															<span class="required" aria-required="true">* <?php echo '( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></span>
														</label>
														<div class="input-icon right">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_error_messages_padding[]" id="ux_txt_error_messages_padding_top" placeholder="<?php echo esc_attr( $cb_top ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_padding_top', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_error_messages_padding[0] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_error_messages_padding[]" id="ux_txt_error_messages_padding_right" placeholder="<?php echo esc_attr( $cb_right ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_padding_right', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_error_messages_padding[1] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_error_messages_padding[]" id="ux_txt_error_messages_padding_bottom" placeholder="<?php echo esc_attr( $cb_bottom ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_padding_bottom', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_error_messages_padding[2] ); ?>">
															<input type="text" class="form-control custom-input-xsmall input-inline" name="ux_txt_error_messages_padding[]" id="ux_txt_error_messages_padding_left" placeholder="<?php echo esc_attr( $cb_left ); ?>" onblur="default_value_contact_bank('#ux_txt_contact_messages_padding_left', 0)" maxlength="3" onkeypress="enter_only_digits_contact_bank(event);" onfocus="paste_prevent_contact_bank(this.id);" value="<?php echo intval( $layout_settings_error_messages_padding[3] ); ?>">
														</div>
														<i class="controls-description"><?php echo esc_attr( $cb_error_message_padding_tooltip ); ?></i>
													</div>
												</div>
											</div>
										</div>
										<div class="line-separator"></div>
										<div class="form-actions">
											<div class="pull-right">
												<input type="submit" class="btn vivid-green" name="ux_btn_save_changes" id="ux_btn_save_changes" value="<?php echo esc_attr( $cb_save_changes ); ?>">
											</div>
										</div>
									</div>
								</form>
							</div>
						</div>
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
					<span>
						<?php echo esc_attr( $cb_layout_settings ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-settings"></i>
							<?php echo esc_attr( $cb_layout_settings ); ?>
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
