<?php
/**
 * Template for update and view settings in Roles and Capabilities.
 *
 * @author  Tech Banker
 * @package contact-bank/views/roles-and-capabilities
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
	} elseif ( ROLES_AND_CAPABILITIES_CONTACT_BANK === '1' ) {
		$roles_and_capabilities = explode( ',', isset( $details_roles_capabilities ) ? $details_roles_capabilities['roles_and_capabilities'] : '1,1,1,0,0,0' );
		$author                 = explode( ',', isset( $details_roles_capabilities ) ? $details_roles_capabilities['author_privileges'] : '0,1,1,0,0,0,1,0,0,0,1,0' );
		$editor                 = explode( ',', isset( $details_roles_capabilities ) ? $details_roles_capabilities['editor_privileges'] : '0,0,0,0,0,0,1,0,1,0,0,0' );
		$contributor            = explode( ',', isset( $details_roles_capabilities ) ? $details_roles_capabilities['contributor_privileges'] : '0,0,0,1,0,0,1,0,0,0,0,0' );
		$subscriber             = explode( ',', isset( $details_roles_capabilities ) ? $details_roles_capabilities['subscriber_privileges'] : '0,0,0,0,0,0,0,0,0,0,0,0' );
		$other_capability       = explode( ',', isset( $details_roles_capabilities ) ? $details_roles_capabilities['other_privileges'] : '0,0,0,0,0,0,0,0,0,0,0,0' );
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
						<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-users"></i>
							<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
						</div>
						<p class="premium-editions">
							<?php echo esc_attr( $cb_upgrade_need_help ); ?><a href="https://contact-bank.tech-banker.com/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_documentation ); ?></a><?php echo esc_attr( $cb_read_and_check ); ?><a href="https://contact-bank.tech-banker.com/frontend-demos/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_demos_section ); ?></a>
						</p>
					</div>
					<div class="portlet-body form">
						<form id="ux_frm_roles_and_capabilities">
							<div class="form-body">
								<div class="form-actions">
									<div class="pull-right">
										<input type="submit" class="btn vivid-green" name="ux_btn_add_tag"  id="ux_btn_add_tag" value="<?php echo esc_attr( $cb_save_changes ); ?>">
									</div>
								</div>
								<div class="line-separator"></div>
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_roles_capabilities_show_menu ); ?> :
										<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
									</label>
									<table class="table table-striped table-bordered table-margin-top" id="ux_tbl_contact_bank">
										<thead>
											<tr>
												<th>
													<input type="checkbox" name="ux_chk_administrator" id="ux_chk_administrator" value="1" checked="checked" disabled="disabled" <?php echo '1' === $roles_and_capabilities[0] ? 'checked = checked' : ''; ?>>
													<?php echo esc_attr( $cb_roles_capabilities_administrator ); ?>
												</th>
												<th>
													<input type="checkbox" name="ux_chk_author" id="ux_chk_author" value="1" onclick="show_roles_capabilities_contact_bank(this, 'ux_div_author_roles');" <?php echo '1' === $roles_and_capabilities[1] ? 'checked = checked' : ''; ?>>
													<?php echo esc_attr( $cb_roles_capabilities_author ); ?>
												</th>
												<th>
													<input type="checkbox" name="ux_chk_editor" id="ux_chk_editor" value="1" onclick="show_roles_capabilities_contact_bank(this, 'ux_div_editor_roles');" <?php echo '1' === $roles_and_capabilities[2] ? 'checked = checked' : ''; ?>>
													<?php echo esc_attr( $cb_roles_capabilities_editor ); ?>
												</th>
												<th>
													<input type="checkbox" name="ux_chk_contributor" id="ux_chk_contributor" value="1" onclick="show_roles_capabilities_contact_bank(this, 'ux_div_contributor_roles');" <?php echo '1' === $roles_and_capabilities[3] ? 'checked = checked' : ''; ?>>
													<?php echo esc_attr( $cb_roles_capabilities_contributor ); ?>
												</th>
												<th>
													<input type="checkbox" name="ux_chk_subscriber" id="ux_chk_subscriber" value="1" onclick="show_roles_capabilities_contact_bank(this, 'ux_div_subscriber_roles');" <?php echo '1' === $roles_and_capabilities[4] ? 'checked = checked' : ''; ?>>
													<?php echo esc_attr( $cb_roles_capabilities_subscriber ); ?>
												</th>
												<th>
													<input type="checkbox"  name="ux_chk_others_privileges" id="ux_chk_others_privileges" value="1" onclick="show_roles_capabilities_contact_bank(this, 'ux_div_other_privileges_roles');" <?php echo '1' === $roles_and_capabilities[5] ? 'checked = checked' : ''; ?>>
													<?php echo esc_attr( $cb_roles_capabilities_others ); ?>
												</th>
											</tr>
										</thead>
									</table>
									<i class="controls-description"><?php echo esc_attr( $cb_roles_capabilities_show_menu_tooltip ); ?></i>
								</div>
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_roles_capabilities_topbar_menu ); ?> :
										<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
									</label>
									<select name="ux_ddl_contact_bank_menu" id="ux_ddl_contact_bank_menu" class="form-control">
										<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
										<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
									</select>
								</div>
								<i class="controls-description"><?php echo esc_attr( $cb_roles_capabilities_topbar_menu_tooltip ); ?></i>
								<div class="line-separator"></div>
								<div class="form-group">
									<div id="ux_div_administrator_roles">
										<label class="control-label">
											<?php echo esc_attr( $cb_roles_capabilities_administrator_role ); ?> :
											<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
										</label>
										<div class="table-margin-top">
											<table class="table table-striped table-bordered table-hover" id="ux_tbl_administrator">
												<thead>
													<tr>
														<th style="width: 40% !important;">
															<input type="checkbox" name="ux_chk_full_control_administrator" id="ux_chk_full_control_administrator" checked="checked" disabled="disabled" value="1">
															<?php echo esc_attr( $cb_roles_capabilities_full_control ); ?>
														</th>
													</tr>
												</thead>
												<tbody>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_forms_admin" disabled="disabled" checked="checked" id="ux_chk_forms_admin" value="1">
															<?php echo esc_attr( $cb_forms ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_layout_settings_admin" disabled="disabled" checked="checked" id="ux_chk_layout_settings_admin" value="1">
															<?php echo esc_attr( $cb_layout_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_custom_css_admin" disabled="disabled" checked="checked" id="ux_chk_custom_css_admin" value="1">
															<?php echo esc_attr( $cb_custom_css ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_email_templates_admin" disabled="disabled" checked="checked" id="ux_chk_email_templates_admin" value="1">
															<?php echo esc_attr( $cb_email_templates ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_general_settings_admin" disabled="disabled" checked="checked" id="ux_chk_general_settings_admin" value="1">
															<?php echo esc_attr( $cb_general_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_submissions_admin" disabled="disabled" checked="checked" id="ux_chk_submissions_admin" value="1">
															<?php echo esc_attr( $cb_submissions ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_roles_admin" disabled="disabled" checked="checked" id="ux_chk_roles_admin" value="1">
															<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_system_information_admin" disabled="disabled" checked="checked" id="ux_chk_system_information_admin" value="1">
															<?php echo esc_attr( $cb_system_information ); ?>
														</td>
														<td>
														</td>
													</tr>
												</tbody>
											</table>
											<i class="controls-description"><?php echo esc_attr( $cb_roles_capabilities_administrator_role_tooltip ); ?></i>
										</div>
										<div class="line-separator"></div>
									</div>
								</div>
								<div class="form-group">
									<div id="ux_div_author_roles">
										<label class="control-label">
											<?php echo esc_attr( $cb_roles_capabilities_author_role ); ?> :
											<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
										</label>
										<div class="table-margin-top">
											<table class="table table-striped table-bordered table-hover" id="ux_tbl_author">
												<thead>
													<tr>
														<th style="width: 40% !important;">
															<input type="checkbox" name="ux_chk_full_control_author" id="ux_chk_full_control_author" value="1" onclick="full_control_function_contact_bank(this, 'ux_div_author_roles');" <?php echo isset( $author ) && '1' === $author[0] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_capabilities_full_control ); ?>
														</th>
													</tr>
												</thead>
												<tbody>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_forms_author" id="ux_chk_forms_author" value="1" <?php echo isset( $author ) && '1' === $author[1] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_forms ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_layout_settings_author" id="ux_chk_layout_settings_author" value="1" <?php echo isset( $author ) && '1' === $author[2] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_layout_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_custom_css_author" id="ux_chk_custom_css_author" value="1" <?php echo isset( $author ) && '1' === $author[3] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_custom_css ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_email_templates_author" id="ux_chk_email_templates_author" value="1" <?php echo isset( $author ) && '1' === $author[4] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_email_templates ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_general_settings_author" id="ux_chk_general_settings_author" value="1" <?php echo isset( $author ) && '1' === $author[5] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_general_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_submissions_author" id="ux_chk_submissions_author" value="1" <?php echo isset( $author ) && '1' === $author[6] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_submissions ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_roles_author" id="ux_chk_roles_author" value="1" <?php echo isset( $author ) && '1' === $author[7] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_system_information_author" id="ux_chk_system_information_author" value="1" <?php echo isset( $author ) && '1' === $author[8] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_system_information ); ?>
														</td>
														<td>
														</td>
													</tr>
												</tbody>
											</table>
										</div>
										<i class="controls-description"><?php echo esc_attr( $cb_roles_capabilities_author_role_tooltip ); ?></i>
										<div class="line-separator"></div>
									</div>
								</div>
								<div class="form-group">
									<div id="ux_div_editor_roles">
										<label class="control-label">
											<?php echo esc_attr( $cb_roles_capabilities_editor_role ); ?> :
											<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
										</label>
										<div class="table-margin-top">
											<table class="table table-striped table-bordered table-hover" id="ux_tbl_editor">
												<thead>
													<tr>
														<th style="width: 40% !important;">
															<input type="checkbox" name="ux_chk_full_control_editor" id="ux_chk_full_control_editor" value="1" onclick="full_control_function_contact_bank(this, 'ux_div_editor_roles');" <?php echo isset( $editor ) && '1' === $editor[0] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_capabilities_full_control ); ?>
														</th>
													</tr>
												</thead>
												<tbody>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_forms_editor" id="ux_chk_forms_editor" value="1" <?php echo isset( $editor ) && '1' === $editor[1] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_forms ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_layout_settings_editor" id="ux_chk_layout_settings_editor" value="1" <?php echo isset( $editor ) && '1' === $editor[2] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_layout_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_custom_css_editor" id="ux_chk_custom_css_editor" value="1" <?php echo isset( $editor ) && '1' === $editor[3] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_custom_css ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_email_templates_editor" id="ux_chk_email_templates_editor" value="1" <?php echo isset( $editor ) && '1' === $editor[4] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_email_templates ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_general_settings_editor" id="ux_chk_general_settings_editor" value="1" <?php echo isset( $editor ) && '1' === $editor[5] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_general_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_submissions_editor" id="ux_chk_submissions_editor" value="1" <?php echo isset( $editor ) && '1' === $editor[6] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_submissions ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_roles_editor" id="ux_chk_roles_editor" value="1" <?php echo isset( $editor ) && '1' === $editor[7] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_system_information_editor" id="ux_chk_system_information_editor" value="1" <?php echo isset( $editor ) && '1' === $editor[8] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_system_information ); ?>
														</td>
														<td>
														</td>
													</tr>
												</tbody>
											</table>
										</div>
										<i class="controls-description"><?php echo esc_attr( $cb_roles_capabilities_editor_role_tooltip ); ?></i>
										<div class="line-separator"></div>
									</div>
								</div>
								<div class="form-group">
									<div id="ux_div_contributor_roles">
										<label class="control-label">
											<?php echo esc_attr( $cb_roles_capabilities_contributor_role ); ?> :
											<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
										</label>
										<div class="table-margin-top">
											<table class="table table-striped table-bordered table-hover" id="ux_tbl_contributor">
												<thead>
													<tr>
														<th style="width: 40% !important;">
															<input type="checkbox" name="ux_chk_full_control_contributor" id="ux_chk_full_control_contributor" value="1" onclick="full_control_function_contact_bank(this, 'ux_div_contributor_roles');" <?php echo isset( $contributor ) && $contributor[0] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_capabilities_full_control ); ?>
														</th>
													</tr>
												</thead>
												<tbody>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_forms_contributor" id="ux_chk_forms_contributor" value="1" <?php echo isset( $contributor ) && '1' === $contributor[1] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_forms ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_layout_settings_contributor" id="ux_chk_layout_settings_contributor" value="1" <?php echo isset( $contributor ) && '1' === $contributor[2] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_layout_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_custom_css_contributor" id="ux_chk_custom_css_contributor" value="1" <?php echo isset( $contributor ) && '1' === $contributor[3] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_custom_css ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_email_templates_contributor" id="ux_chk_email_templates_contributor" value="1" <?php echo isset( $contributor ) && '1' === $contributor[4] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_email_templates ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_general_settings_contributor" id="ux_chk_general_settings_contributor" value="1" <?php echo isset( $contributor ) && '1' === $contributor[5] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_general_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_submissions_contributor" id="ux_chk_submissions_contributor" value="1" <?php echo isset( $contributor ) && '1' === $contributor[6] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_submissions ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_roles_contributor" id="ux_chk_roles_contributor" value="1" <?php echo isset( $contributor ) && '1' === $contributor[7] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_system_information_contributor" id="ux_chk_system_information_contributor" value="1" <?php echo isset( $contributor ) && '1' === $contributor[8] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_system_information ); ?>
														</td>
														<td>
														</td>
													</tr>
												</tbody>
											</table>
										</div>
										<i class="controls-description"><?php echo esc_attr( $cb_roles_capabilities_contributor_role_tooltip ); ?></i>
										<div class="line-separator"></div>
									</div>
								</div>
								<div class="form-group">
									<div id="ux_div_subscriber_roles">
										<label class="control-label">
											<?php echo esc_attr( $cb_roles_capabilities_subscriber_role ); ?> :
											<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
										</label>
										<div class="table-margin-top">
											<table class="table table-striped table-bordered table-hover" id="ux_tbl_subscriber">
												<thead>
													<tr>
														<th style="width: 40% !important;">
															<input type="checkbox" name="ux_chk_full_control_subscriber" id="ux_chk_full_control_subscriber" value="1" onclick="full_control_function_contact_bank(this, 'ux_div_subscriber_roles');" <?php echo isset( $subscriber ) && '1' === $subscriber[0] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_capabilities_full_control ); ?>
														</th>
													</tr>
												</thead>
												<tbody>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_forms_subscriber" id="ux_chk_forms_subscriber" value="1" <?php echo isset( $subscriber ) && '1' === $subscriber[1] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_forms ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_layout_settings_subscriber" id="ux_chk_layout_settings_subscriber" value="1" <?php echo isset( $subscriber ) && '1' === $subscriber[2] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_layout_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_custom_css_subscriber" id="ux_chk_custom_css_subscriber" value="1" <?php echo isset( $subscriber ) && '1' === $subscriber[3] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_custom_css ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_email_templates_subscriber" id="ux_chk_email_templates_subscriber" value="1" <?php echo isset( $subscriber ) && '1' === $subscriber[4] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_email_templates ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_general_settings_subscriber" id="ux_chk_general_settings_subscriber" value="1" <?php echo isset( $subscriber ) && '1' === $subscriber[5] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_general_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_submissions_subscriber" id="ux_chk_submissions_subscriber" value="1" <?php echo isset( $subscriber ) && '1' === $subscriber[6] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_submissions ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_roles_subscriber" id="ux_chk_roles_subscriber" value="1" <?php echo isset( $subscriber ) && '1' === $subscriber[7] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_system_information_subscriber" id="ux_chk_system_information_subscriber" value="1" <?php echo isset( $subscriber ) && '1' === $subscriber[8] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_system_information ); ?>
														</td>
														<td>
														</td>
													</tr>
												</tbody>
											</table>
											<i class="controls-description"><?php echo esc_attr( $cb_roles_capabilities_subscriber_role_tooltip ); ?></i>
										</div>
										<div class="line-separator"></div>
									</div>
								</div>
								<div class="form-group">
									<div id="ux_div_other_privileges_roles">
										<label class="control-label">
											<?php echo esc_attr( $cb_roles_capabilities_other_role ); ?> :
											<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
										</label>
										<div class="table-margin-top">
											<table class="table table-striped table-bordered table-hover" id="ux_tbl_subscriber">
												<thead>
													<tr>
														<th style="width: 40% !important;">
															<input type="checkbox" name="ux_chk_full_control_others" id="ux_chk_full_control_others" value="1" onclick="full_control_function_contact_bank(this, 'ux_div_other_privileges_roles');" <?php echo isset( $other_capability ) && '1' === $other_capability[0] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_capabilities_full_control ); ?>
														</th>
													</tr>
												</thead>
												<tbody>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_forms_others" id="ux_chk_forms_others" value="1" <?php echo isset( $other_capability ) && '1' === $other_capability[1] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_forms ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_layout_settings_others" id="ux_chk_layout_settings_others" value="1" <?php echo isset( $other_capability ) && '1' === $other_capability[2] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_layout_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_custom_css_others" id="ux_chk_custom_css_others" value="1" <?php echo isset( $other_capability ) && '1' === $other_capability[3] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_custom_css ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_email_templates_others" id="ux_chk_email_templates_others" value="1" <?php echo isset( $other_capability ) && '1' === $other_capability[4] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_email_templates ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_general_settings_others" id="ux_chk_general_settings_others" value="1" <?php echo isset( $other_capability ) && '1' === $other_capability[5] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_general_settings ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_submissions_others" id="ux_chk_submissions_others" value="1" <?php echo isset( $other_capability ) && '1' === $other_capability[6] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_submissions ); ?>
														</td>
													</tr>
													<tr>
														<td>
															<input type="checkbox" name="ux_chk_roles_others" id="ux_chk_roles_others" value="1" <?php echo isset( $other_capability ) && '1' === $other_capability[7] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
														</td>
														<td>
															<input type="checkbox" name="ux_chk_system_information_others" id="ux_chk_system_information_others" value="1" <?php echo isset( $other_capability ) && '1' === $other_capability[8] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_system_information ); ?>
														</td>
														<td>
														</td>
													</tr>
												</tbody>
											</table>
										</div>
										<i class="controls-description"><?php echo esc_attr( $cb_roles_capabilities_other_role_tooltip ); ?></i>
										<div class="line-separator"></div>
									</div>
								</div>
								<div class="form-group">
									<div id="ux_div_other_roles">
										<label class="control-label">
											<?php echo esc_attr( $cb_roles_capabilities_other_roles_capabilities ); ?> :
											<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
										</label>
										<div class="table-margin-top">
											<table class="table table-striped table-bordered table-hover" id="ux_tbl_other_roles">
												<thead>
													<tr>
														<th style="width: 40% !important;">
															<input type="checkbox" name="ux_chk_full_control_other_roles" id="ux_chk_full_control_other_roles" value="1" onclick="full_control_function_contact_bank(this, 'ux_div_other_roles');" <?php echo isset( $details_roles_capabilities['others_full_control_capability'] ) && '1' === $details_roles_capabilities['others_full_control_capability'] ? 'checked = checked' : ''; ?>>
															<?php echo esc_attr( $cb_roles_capabilities_full_control ); ?>
														</th>
													</tr>
												</thead>
												<tbody>
													<?php
													$flag              = 0;
													$user_capabilities = get_others_capabilities_contact_bank();
													foreach ( $user_capabilities as $key => $value ) {
														$other_roles = in_array( $value, $other_roles_array, true ) ? 'checked=checked' : '';
														$flag++;
														if ( 0 === $key % 3 ) {
															?>
															<tr>
																<?php
														}
															?>
															<td>
																<input type="checkbox" name="ux_chk_other_capabilities_<?php echo esc_attr( $value ); ?>" id="ux_chk_other_capabilities_<?php echo esc_attr( $value ); ?>" value="<?php echo esc_attr( $value ); ?>" <?php echo esc_attr( $other_roles ); ?>>
																<?php echo esc_attr( $value ); ?>
															</td>
															<?php
															if ( count( $user_capabilities ) === $flag && 1 === $flag % 3 ) {
																?>
																<td>
																</td>
																<td>
																</td>
																<?php
															}
															?>
															<?php
															if ( count( $user_capabilities ) === $flag && 2 === $flag % 3 ) {
																?>
																<td>
																</td>
																<?php
															}
															?>
															<?php
															if ( 0 === $flag % 3 ) {
																?>
															</tr>
															<?php
															}
													}
													?>
												</tbody>
											</table>
										</div>
										<i class="controls-description"><?php echo esc_attr( $cb_roles_capabilities_other_roles_capabilities_tooltip ); ?></i>
										<div class="line-separator"></div>
									</div>
								</div>
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
						<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-users"></i>
								<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
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
