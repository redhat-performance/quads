<?php
/**
 * This file is used for displaying admin bar menus.
 *
 * @author   Tech Banker
 * @package  contact-bank/lib
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
		$flag                                = 0;
		$role_capabilities                   = $wpdb->get_var(
			$wpdb->prepare(
				'SELECT meta_value from ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s', 'roles_and_capabilities'
			)
		);// WPCS: db call ok, cache ok.
		$roles_and_capabilities_unserialized = maybe_unserialize( $role_capabilities );
		$capabilities                        = explode( ',', isset( $roles_and_capabilities_unserialized['roles_and_capabilities'] ) ? esc_attr( $roles_and_capabilities_unserialized['roles_and_capabilities'] ) : '1,1,1,0,0,0' );

		if ( is_super_admin() ) {
			$cb_role = 'administrator';
		} else {
			$cb_role = check_user_roles_contact_bank( $current_user );
		}
		switch ( $cb_role ) {
			case 'administrator':
				$flag = $capabilities[0];
				break;

			case 'author':
				$flag = $capabilities[1];
				break;

			case 'editor':
				$flag = $capabilities[2];
				break;

			case 'contributor':
				$flag = $capabilities[3];
				break;

			case 'subscriber':
				$flag = $capabilities[4];
				break;
		}

		if ( '1' === $flag ) {
			$wp_admin_bar->add_menu(
				array(
					'id'    => 'contact_bank',
					'title' => '<img style="width:16px; height:16px; vertical-align:middle; margin-right:3px;" src=' . plugins_url( 'assets/global/img/icon.png', dirname( __FILE__ ) ) . '> ' . $cb_contact_bank,
					'href'  => admin_url( 'admin.php?page=contact_dashboard' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_forms',
					'title'  => $cb_forms,
					'href'   => admin_url( 'admin.php?page=contact_dashboard' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_layout_settings',
					'title'  => $cb_layout_settings,
					'href'   => admin_url( 'admin.php?page=cb_layout_settings' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_custom_css',
					'title'  => $cb_custom_css,
					'href'   => admin_url( 'admin.php?page=cb_custom_css' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_email_templates',
					'title'  => $cb_email_templates,
					'href'   => admin_url( 'admin.php?page=cb_email_templates' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_general_settings',
					'title'  => $cb_general_settings,
					'href'   => admin_url( 'admin.php?page=cb_general_settings' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_submissions',
					'title'  => $cb_submissions,
					'href'   => admin_url( 'admin.php?page=cb_submissions' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_roles_and_capabilities',
					'title'  => $cb_roles_and_capabilities,
					'href'   => admin_url( 'admin.php?page=cb_roles_and_capabilities' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_feedback',
					'title'  => $cb_ask_for_help,
					'href'   => 'https://wordpress.org/support/plugin/contact-bank',
					'meta'   => array( 'target' => '_blank' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_system_information',
					'title'  => $cb_system_information,
					'href'   => admin_url( 'admin.php?page=cb_system_information' ),
				)
			);

			$wp_admin_bar->add_menu(
				array(
					'parent' => 'contact_bank',
					'id'     => 'cb_licensing_page',
					'title'  => $cb_premium_edition,
					'href'   => 'https://contact-bank.tech-banker.com/pricing/',
					'meta'   => array( 'target' => '_blank' ),
				)
			);
		}
	}
}
