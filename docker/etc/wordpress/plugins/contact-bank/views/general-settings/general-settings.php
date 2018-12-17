<?php
/**
 * Template for general settings.
 *
 * @author  Tech Banker
 * @package contact-bank/views/general-settings
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
	} elseif ( GENERAL_SETTINGS_CONTACT_BANK === '1' ) {
		$general_settings_nonce = wp_create_nonce( 'general_settings_nonce' );
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
						<?php echo esc_attr( $cb_general_settings ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-frame"></i>
							<?php echo esc_attr( $cb_general_settings ); ?>
						</div>
						<p class="premium-editions">
							<?php echo esc_attr( $cb_upgrade_need_help ); ?><a href="https://contact-bank.tech-banker.com/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_documentation ); ?></a><?php echo esc_attr( $cb_read_and_check ); ?><a href="https://contact-bank.tech-banker.com/frontend-demos/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_demos_section ); ?></a>
						</p>
					</div>
					<div class="portlet-body form">
						<form id="ux_frm_general_settings">
							<div class="form-body">
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_general_settings_remove_table_at_uninstall_title ); ?> :
										<span class="required" aria-required="true">*</span>
									</label>
									<select id="ux_ddl_remove_table" name="ux_ddl_remove_table" class="form-control">
										<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
										<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
									</select>
									<i class="controls-description"><?php echo esc_attr( $cb_general_settings_remove_table_at_uninstall_tooltip ); ?></i>
								</div>
								<div class="row">
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_default_currency ); ?> :
												<span class="required" aria-required="true">*</span>
											</label>
											<select id="ux_ddl_default_currency" name="ux_ddl_default_currency" class="form-control">
												<option value="USD"><?php echo esc_attr( $cb_us_dollars ); ?></option>
												<option value="AUD"><?php echo esc_attr( $cb_australian_dollars ); ?></option>
												<option value="CAD"><?php echo esc_attr( $cb_canadian_dollars ); ?></option>
												<option value="CZK"><?php echo esc_attr( $cb_crech_koruna ); ?></option>
												<option value="DKK"><?php echo esc_attr( $cb_danish_krone ); ?></option>
												<option value="EUR"><?php echo esc_attr( $cb_euros ); ?></option>
												<option value="HKD"><?php echo esc_attr( $cb_hong_kong_dollars ); ?></option>
												<option value="HUF"><?php echo esc_attr( $cb_hungarian_forints ); ?></option>
												<option value="ILS"><?php echo esc_attr( $cb_israeli_new_sheqels ); ?></option>
												<option value="JPY"><?php echo esc_attr( $cb_japanese_yen ); ?></option>
												<option value="MXN"><?php echo esc_attr( $cb_mexican_pesos ); ?></option>
												<option value="NOK"><?php echo esc_attr( $cb_norwegian_krone ); ?></option>
												<option value="NZD"><?php echo esc_attr( $cb_new_zealanddollars ); ?></option>
												<option value="PHP"><?php echo esc_attr( $cb_philippine_pesos ); ?></option>
												<option value="PLN"><?php echo esc_attr( $cb_polish_zloty ); ?></option>
												<option value="GBP"><?php echo esc_attr( $cb_british_pounds_sterling ); ?></option>
												<option value="SGD"><?php echo esc_attr( $cb_singapore_dollars ); ?></option>
												<option value="SEK"><?php echo esc_attr( $cb_swedish_krona ); ?></option>
												<option value="CHF"><?php echo esc_attr( $cb_swiss_franc ); ?></option>
												<option value="TWD"><?php echo esc_attr( $cb_taiwan_new_dollars ); ?></option>
												<option value="THB"><?php echo esc_attr( $cb_thai_baht ); ?></option>
												<option value="INR"><?php echo esc_attr( $cb_indian_rupee ); ?></option>
											</select>
											<i class="controls-description"><?php echo esc_attr( $cb_default_currency_tooltip ); ?></i>
										</div>
									</div>
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_language_direction ); ?> :
												<span class="required" aria-required="true">*</span>
											</label>
											<select id="ux_ddl_language_direction" name="ux_ddl_language_direction" class="form-control">
												<option value="right_to_left"><?php echo esc_attr( $cb_right_to_left ); ?></option>
												<option value="left_to_right"><?php echo esc_attr( $cb_left_to_right ); ?></option>
											</select>
											<i class="controls-description"><?php echo esc_attr( $cb_language_direction_tooltip ); ?></i>
										</div>
									</div>
								</div>
								<div class="row">
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_recaptcha_public_key ); ?> :
												<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
											</label>
											<input type="text" name="ux_txt_recaptcha_public_key" id="ux_txt_recaptcha_public_key" placeholder="<?php echo esc_attr( $cb_recaptcha_public_key_placeholder ); ?>" class="form-control" value="<?php echo isset( $details_general_settings['recaptcha_public_key'] ) ? esc_attr( $details_general_settings['recaptcha_public_key'] ) : ''; ?>">
											<i class="controls-description"><?php echo esc_attr( $cb_recaptcha_public_key_tooltip ); ?></i>
										</div>
									</div>
									<div class="col-md-6">
										<div class="form-group">
											<label class="control-label">
												<?php echo esc_attr( $cb_recaptcha_private_key ); ?> :
												<span class="required" aria-required="true">* ( <?php echo esc_attr( $cb_premium_edition ); ?> )</span>
											</label>
											<input type="text" name="ux_txt_recaptcha_private_key" id="ux_txt_recaptcha_private_key" placeholder="<?php echo esc_attr( $cb_recaptcha_private_key_placeholder ); ?>" class="form-control"  value="<?php echo isset( $details_general_settings['recaptcha_private_key'] ) ? esc_attr( $details_general_settings['recaptcha_private_key'] ) : ''; ?>">
											<i class="controls-description"><?php echo esc_attr( $cb_recaptcha_private_key_tooltip ); ?></i>
										</div>
									</div>
								</div>
								<div class="form-group">
									<label class="control-label">
										<?php echo esc_attr( $cb_gdpr_compliance ); ?> :
										<span class="required" aria-required="true">*</span>
									</label>
									<select id="ux_ddl_gdpr_compliance" name="ux_ddl_gdpr_compliance" class="form-control" onchange="gdpr_compliance_contact_bank();">
										<option value="enable"><?php echo esc_attr( $cb_enable ); ?></option>
										<option value="disable"><?php echo esc_attr( $cb_disable ); ?></option>
									</select>
									<i class="controls-description"><?php echo esc_attr( $cb_gdpr_compliance_tooltip ); ?></i>
								</div>
								<div class="form-group" id="ux_div_gdpr_compliance_text">
									<label class="control-label">
										<?php echo esc_attr( $cb_gdpr_compliance_text ); ?> :
										<span class="required" aria-required="true">*</span>
									</label>
									<textarea name="ux_txt_gdpr_compliance_text" id="ux_txt_gdpr_compliance_text" class="form-control" placeholder="<?php echo esc_attr( $cb_gdpr_compliance_text_placeholder ); ?>"><?php echo isset( $details_general_settings['gdpr_compliance_text'] ) ? esc_attr( $details_general_settings['gdpr_compliance_text'] ) : 'By using this form you agree with the storage and handling of your data by this website'; ?></textarea>
									<i class="controls-description"><?php echo esc_attr( $cb_gdpr_compliance_text_tooltip ); ?></i>
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
						<?php echo esc_attr( $cb_general_settings ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-frame"></i>
							<?php echo esc_attr( $cb_general_settings ); ?>
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
