<?php
/**
 * This file is used for displaying sidebar menus.
 *
 * @author   Tech Banker
 * @package  contact-bank/includes
 * @version  3.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}
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
		?>
		<div class="page-sidebar-wrapper-tech-banker">
			<div class="page-sidebar-tech-banker navbar-collapse collapse">
				<div class="sidebar-menu-tech-banker">
					<ul class="page-sidebar-menu-tech-banker" data-slide-speed="200">
						<div class="sidebar-search-wrapper" style="padding:20px;text-align:center">
							<a class="plugin-logo" href="<?php echo esc_attr( TECH_BANKER_BETA_URL ); ?>" target="_blank">
								<img src="<?php echo esc_attr( plugins_url( 'assets/global/img/logo.png', dirname( __FILE__ ) ) ); ?>"/>
							</a>
						</div>
						<li id="ux_li_forms">
							<a href="javascript:;">
								<i class="icon-custom-docs"></i>
								<span class="title">
									<?php echo esc_attr( $cb_forms ); ?>
								</span>
							</a>
							<ul class="sub-menu">
								<li id="ux_li_manage_forms">
									<a href="admin.php?page=contact_dashboard">
										<i class="icon-custom-grid"></i>
										<span class="title">
											<?php echo esc_attr( $cb_manage_forms ); ?>
										</span>
									</a>
								</li>
								<li id="ux_li_add_new_forms">
									<a href="javascript:;" onclick="add_new_form_contact_bank();">
										<i class="icon-custom-plus"></i>
										<span class="title">
											<?php echo esc_attr( $cb_add_new_form ); ?>
										</span>
									</a>
								</li>
							</ul>
						</li>
						<li id="ux_li_layout_settings">
							<a href="admin.php?page=cb_layout_settings">
								<i class="icon-custom-settings"></i>
								<span class="title">
									<?php echo esc_attr( $cb_layout_settings ); ?>
									<span class="badge">Pro</span>
								</span>
							</a>
						</li>
						<li id="ux_li_custom_settings">
							<a href="admin.php?page=cb_custom_css">
								<i class="icon-custom-pencil"></i>
								<span class="title">
									<?php echo esc_attr( $cb_custom_css ); ?>
								</span>
							</a>
						</li>
						<li id="ux_li_email_templates">
							<a href="admin.php?page=cb_email_templates">
								<i class="icon-custom-grid"></i>
								<?php echo esc_attr( $cb_email_templates ); ?>
							</a>
						</li>
						<li id="ux_li_general_settings">
							<a href="admin.php?page=cb_general_settings">
								<i class="icon-custom-frame"></i>
								<span class="title">
									<?php echo esc_attr( $cb_general_settings ); ?>
								</span>
							</a>
						</li>
						<li id="ux_li_submissions">
							<a href="admin.php?page=cb_submissions">
								<i class="icon-custom-note"></i>
								<span class="title">
									<?php echo esc_attr( $cb_submissions ); ?>
								</span>
							</a>
						</li>
						<li id="ux_li_roles_and_capabilities">
							<a href="admin.php?page=cb_roles_and_capabilities">
								<i class="icon-custom-users"></i>
								<span class="title">
									<?php echo esc_attr( $cb_roles_and_capabilities ); ?>
									<span class="badge">Pro</span>
								</span>
							</a>
						</li>
						<li id="ux_li_cb_feedback">
							<a href='https://wordpress.org/support/plugin/contact-bank' target='_blank'>
								<i class="icon-custom-call-out"></i>
								<span class="title">
									<?php echo esc_attr( $cb_ask_for_help ); ?>
								</span>
							</a>
						</li>
						<li id="ux_li_system_information">
							<a href="admin.php?page=cb_system_information">
								<i class="icon-custom-screen-desktop"></i>
								<span class="title">
									<?php echo esc_attr( $cb_system_information ); ?>
								</span>
							</a>
						</li>
						<li id="ux_li_licensing">
							<a href='https://contact-bank.tech-banker.com/pricing/' target='_blank'>
								<i class="icon-custom-briefcase"></i>
								<span class="title">
									<strong style='color:yellow;'>
									<?php echo esc_attr( $cb_premium_edition ); ?>
								</strong>
								</span>
							</a>
						</li>
				</div>
			</div>
		</div>
		<div class="page-content-wrapper">
			<div class="page-content">
				<?php
	}
}
