<?php
/**
 * Template for manage form.
 *
 * @author  Tech Banker
 * @package contact-bank/views/forms
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
	} elseif ( FORMS_CONTACT_BANK === '1' ) {
		$cb_contact_bank_bulk_delete_nonce    = wp_create_nonce( 'cb_bulk_delete_forms' );
		$cb_contact_bank_bulk_duplicate_nonce = wp_create_nonce( 'cb_bulk_duplicate_forms' );
		$cb_delete_all_forms_nonce            = wp_create_nonce( 'cb_delete_all_forms_nonce' );
		$cb_contact_bank_delete_nonce         = wp_create_nonce( 'contact_forms_delete_nonce' );
		$cb_contact_form_duplicate_data       = wp_create_nonce( 'contact_form_duplicate_nonce' );
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
						<?php echo esc_attr( $cb_manage_forms ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-grid"></i>
							<?php echo esc_attr( $cb_manage_forms ); ?>
						</div>
						<p class="premium-editions">
							<?php echo esc_attr( $cb_upgrade_need_help ); ?><a href="https://contact-bank.tech-banker.com/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_documentation ); ?></a><?php echo esc_attr( $cb_read_and_check ); ?><a href="https://contact-bank.tech-banker.com/frontend-demos/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_demos_section ); ?></a>
						</p>
					</div>
					<div class="portlet-body form">
						<form id="ux_frm_manage_forms">
							<div class="form-body">
								<div class="table-top-margin">
									<select name="ux_ddl_bulk_action" id="ux_ddl_bulk_action">
										<option value=""><?php echo esc_attr( $cb_bulk_action ); ?></option>
										<option value="delete" style="color:red;"><?php echo esc_attr( $cb_bulk_delete ) . ' ( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></option>
										<option value="duplicate" style="color:red;"><?php echo esc_attr( $cb_bulk_duplicate ) . ' ( ' . esc_attr( $cb_premium_edition ) . ' )'; ?></option>
									</select>
									<input type="button" class="btn vivid-green" name="ux_btn_apply_manage_forms" id="ux_btn_apply_manage_forms" value="<?php echo esc_attr( $cb_apply ); ?>" onclick="premium_edition_notification_contact_bank();">
									<a href="javascript:;" onclick="add_new_form_contact_bank()" class="btn vivid-green"><?php echo esc_attr( $cb_add_form ); ?></a>
								</div>
								<div class="line-separator"></div>
								<table class="table table-striped table-bordered table-hover" id="ux_table_manage_forms">
									<thead class="align-thead-left">
										<tr>
											<th style="text-align:center; width: 5%;" class="chk-action">
												<input type="checkbox" name="ux_chk_all_forms" id="ux_chk_all_forms">
											</th>
											<th style="width: 70%" class="custom-table-th-right">
												<?php echo esc_attr( $cb_details ); ?>
											</th>
											<th class="chk-action" style="width: 20%;">
												<?php echo esc_attr( $cb_actions ); ?>
											</th>
										</tr>
									</thead>
									<tbody>
										<?php
										foreach ( $unserialized_forms_data_array as $row ) {
											$form_id = $cb_form_id . ' ' . intval( $row['meta_id'] );
											?>
											<tr>
												<td style="width: 5%; text-align:center;" class="chk-action">
													<input type="checkbox" name="ux_chk_manage_forms" id="ux_chk_manage_forms"  onclick="check_all_contact_bank('#ux_chk_all_forms');" value="<?php echo intval( $row['meta_id'] ); ?>">
												</td>
												<td>
													<?php echo isset( $row['form_title'] ) && '' !== $row['form_title'] ? '<p>' . esc_attr( $row['form_title'] ) . ' - ( <strong>' . esc_attr( $form_id ) . '</strong> ) </p>' : '<p>' . esc_attr( $cb_untitled_form ) . ' - ( <strong>' . esc_attr( $form_id ) . '</strong> ) </p>'; ?>
													<?php echo isset( $row['form_description'] ) && '' !== $row['form_description'] ? '<p>' . htmlspecialchars_decode( $row['form_description'] ) . '</p>' : '<p></p>'; // WPCS:XSS ok. ?>
													<strong><?php echo 'Shortcode'; ?> :</strong>
													<div class="icon-custom-docs tooltips pull-right" style="font-size:18px;" data-original-title="<?php echo esc_attr( $cb_shortcode_copy_to_clipboard ); ?>" data-placement="left" data-clipboard-action="copy" data-clipboard-target="#ux_txtarea_generate_shortcodes_<?php echo intval( $row['old_form_id'] ); ?>"></div>
													<textarea class="form-control" readonly name="ux_txtarea_generate_shortcodes_<?php echo intval( $row['old_form_id'] ); ?>" id="ux_txtarea_generate_shortcodes_<?php echo intval( $row['old_form_id'] ); ?>" rows="1">[contact_bank form_id="<?php echo intval( $row['old_form_id'] ); ?>" form_title="show" form_description="show"][/contact_bank]</textarea>
												</td>
												<td class="custom-alternative">
													<a href="admin.php?page=cb_add_new_form&form_id=<?php echo intval( $row['old_form_id'] ); ?>&mode=edit" class="button-contact-bank" style="width:146px;">
														<i class="icon-custom-pencil manage-form-icon-contact-bank"></i>
														<?php echo esc_attr( $cb_edit ); ?>
													</a>
													<a href="javascript:void(0);" class="button-contact-bank" style="width:146px;" onclick="confirm_delete_contact_bank('<?php echo intval( $row['meta_id'] ); ?>','<?php echo esc_attr( $cb_delete_message ); ?>','contact_dashboard','delete_contact_forms');" data-placement="right">
														<i class="icon-custom-trash manage-form-icon-contact-bank"></i>
														<?php echo esc_attr( $cb_delete ); ?>
													</a>
													<a href="<?php echo esc_url( home_url( '/?cb_preview_form=' . $row['old_form_id'] ) ); ?>" target="_blank" name="ux_btn_preview_changes" id="ux_btn_preview_changes" class="button-contact-bank" style="width:146px;">
														<i class="icon-custom-eye manage-form-icon-contact-bank"></i>
														<?php echo esc_attr( $cb_preview ); ?>
													</a>
													<a href="javascript:void(0);" class="button-contact-bank" style="width:146px;" onclick="premium_edition_notification_contact_bank();" data-placement="right">
														<i class="icon-custom-docs manage-form-icon-contact-bank" ></i>
														<?php echo esc_attr( $cb_duplicate ); ?>
													</a>
													<a href="admin.php?page=cb_email_templates&form_id=<?php echo intval( $row['meta_id'] ); ?>" class="button-contact-bank" style="width:146px;">
														<i class="icon-custom-envelope manage-form-icon-contact-bank"></i>
														<?php echo esc_attr( $cb_email_settings ); ?>
													</a>
													<a href="admin.php?page=cb_submissions&form_id=<?php echo intval( $row['old_form_id'] ); ?>" class="button-contact-bank" style="width:146px;">
														<i class="icon-custom-grid manage-form-icon-contact-bank"></i>
														<?php echo esc_attr( $cb_form_entries ); ?>
													</a>
												</td>
											</tr>
											<?php
										}
										?>
									</tbody>
								</table>
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
					<a href="admin.php?page=contact_dashboard">
						<?php echo esc_attr( $cb_forms ); ?>
					</a>
					<span>></span>
				</li>
				<li>
					<span>
						<?php echo esc_attr( $cb_manage_forms ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-grid"></i>
							<?php echo esc_attr( $cb_manage_forms ); ?>
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
