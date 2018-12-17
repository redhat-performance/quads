<?php
/**
 * This Template is used for Wizard
 *
 * @author  Tech Banker
 * @package contact-bank/views/wizard
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
		$contact_bank_check_status = wp_create_nonce( 'contact_bank_check_status' );
		?>
		<html>
			<body>
				<div><div><div>
				<div class="page-container header-wizard">
					<div class="page-content">
						<div class="row row-custom row-bg">
							<div class="col-md-1">
							</div>
							<div class="col-md-4 center">
								<b>
									<i class="dashicons dashicons-wordpress cb-dashicons-wordpress"></i>
								</b>
							</div>
							<div class="col-md-2 center">
								<i class="dashicons dashicons-plus cb-dashicons-plus"></i>
							</div>
							<div class="col-md-4 center">
								<img src="<?php echo esc_attr( plugins_url( 'assets/global/img/wizard-icon.png', dirname( dirname( __FILE__ ) ) ) ); ?>" height="110" width="110">
							</div>
							<div class="col-md-1">
							</div>
						</div>
						<div class="row row-custom">
							<div class="col-md-12 textalign">
								<p><?php echo esc_attr( __( 'Hi there!', 'contact-bank' ) ); ?></p>
								<p><?php echo esc_attr( __( 'Don\'t ever miss an opportunity to opt in for Email Notifications / Announcements about exciting New Features and Update Releases.', 'contact-bank' ) ); ?></p>
								<p><?php echo esc_attr( __( 'Contribute in helping us making our plugin compatible with most plugins and themes by allowing to share non-sensitive information about your website.', 'contact-bank' ) ); ?></p>
								<p><?php echo esc_attr( __( 'If you opt in, some data about your usage of Contact Bank Plugin will be sent to our servers for Compatiblity Testing Purposes and Email Notifications.', 'contact-bank' ) ); ?></p>
							</div>
						</div>
						<div class="row row-custom">
							<div class="col-md-12">
								<div style="padding-left: 40px;">
									<label class="control-label" style="font-size: 16px;">
										<?php echo 'Email Address for Notifications'; ?> :
									</label>
									<span id="ux_txt_validation_gdpr_contact_bank" style="display:none;vertical-align:middle;">*</span>
									<input type="text" style="width: 90%;" class="form-control" name="ux_txt_email_address_notifications" id="ux_txt_email_address_notifications" value="<?php echo esc_attr( get_option( 'admin_email' ) ); ?>">
								</div>
								<div class="textalign">
									<p><?php echo esc_attr( __( 'If you\'re not ready to Opt-In, that\'s ok too!', 'contact-bank' ) ); ?></p>
									<p><strong><?php echo esc_attr( __( 'Contact Bank will still work fine', 'contact-bank' ) ); ?></strong></p>
								</div>
							</div>
							<div class="col-md-12">
								<a class="permissions" onclick="show_hide_details_contact_bank();"><?php echo esc_attr( __( 'What permissions are being granted?', 'contact-bank' ) ); ?></a>
							</div>
							<div class="col-md-12" style="display:none;" id="ux_div_wizard_set_up">
								<div class="col-md-6">
									<ul>
										<li>
											<i class="dashicons dashicons-admin-users cb-dashicons-admin-users"></i>
											<div class="admin">
												<span><strong><?php echo esc_attr( __( 'User Details', 'contact-bank' ) ); ?></strong></span>
												<p><?php echo esc_attr( __( 'Name and Email Address', 'contact-bank' ) ); ?></p>
											</div>
										</li>
									</ul>
								</div>
								<div class="col-md-6 align align2">
									<ul>
										<li>
											<i class="dashicons dashicons-admin-plugins cb-dashicons-admin-plugins"></i>
											<div class="admin-plugins">
												<span><strong><?php echo esc_attr( __( 'Current Plugin Status', 'contact-bank' ) ); ?></strong></span>
												<p><?php echo esc_attr( __( 'Activation, Deactivation and Uninstall', 'contact-bank' ) ); ?></p>
											</div>
										</li>
									</ul>
								</div>
								<div class="col-md-6">
									<ul>
										<li>
											<i class="dashicons dashicons-testimonial cb-dashicons-testimonial"></i>
											<div class="testimonial">
												<span><strong><?php echo esc_attr( __( 'Notifications', 'contact-bank' ) ); ?></strong></span>
												<p><?php echo esc_attr( __( 'Updates &amp; Announcements', 'contact-bank' ) ); ?></p>
											</div>
										</li>
									</ul>
								</div>
								<div class="col-md-6 align2">
									<ul>
										<li>
											<i class="dashicons dashicons-welcome-view-site cb-dashicons-welcome-view-site"></i>
											<div class="settings">
												<span><strong><?php echo esc_attr( __( 'Website Overview', 'contact-bank' ) ); ?></strong></span>
												<p><?php echo esc_attr( __( 'Site URL, WP Version, PHP Info, Plugins &amp; Themes Info', 'contact-bank' ) ); ?></p>
											</div>
										</li>
									</ul>
								</div>
							</div>
							<div class="col-md-12 allow">
								<div class="tech-banker-actions">
									<a onclick="plugin_stats_contact_bank('opt_in');" class="button button-primary-wizard">
										<strong><?php echo esc_attr( __( 'Opt-In &amp; Continue', 'contact-bank' ) ); ?> </strong>
										<i class="dashicons dashicons-arrow-right-alt cb-dashicons-arrow-right-alt"></i>
									</a>
									<a onclick="plugin_stats_contact_bank('skip');" class="button button-secondary-wizard" tabindex="2">
										<strong><?php echo esc_attr( __( 'Skip &amp; Continue', 'contact-bank' ) ); ?> </strong>
										<i class="dashicons dashicons-arrow-right-alt cb-dashicons-arrow-right-alt"></i>
									</a>
									<div class="clearfix"></div>
								</div>
							</div>
							<div class="col-md-12 terms">
								<a href="https://contact-bank.tech-banker.com/privacy-policy/" target="_blank"><?php echo esc_attr( __( 'Privacy Policy', 'contact-bank' ) ); ?></a>
								<span> - </span>
								<a href="https://contact-bank.tech-banker.com/terms-conditions/" target="_blank"><?php echo esc_attr( __( 'Terms &amp; Conditions', 'contact-bank' ) ); ?></a>
							</div>
						</div>
					</div>
				</div>
			</body>
		</html>
		<?php
	}
}
