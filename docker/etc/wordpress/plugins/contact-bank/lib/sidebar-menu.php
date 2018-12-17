<?php
/**
 * This file is used for sidebar menus.
 *
 * @author   Tech Banker
 * @package  contact-bank/lib
 * @version 3.0
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
		$flag = 0;

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
				$privileges = 'administrator_privileges';
				$flag       = $capabilities[0];
				break;

			case 'author':
				$privileges = 'author_privileges';
				$flag       = $capabilities[1];
				break;

			case 'editor':
				$privileges = 'editor_privileges';
				$flag       = $capabilities[2];
				break;

			case 'contributor':
				$privileges = 'contributor_privileges';
				$flag       = $capabilities[3];
				break;

			case 'subscriber':
				$privileges = 'subscriber_privileges';
				$flag       = $capabilities[4];
				break;

			default:
				$privileges = 'other_privileges';
				$flag       = $capabilities[5];
		}
		$privileges_value = '0,0,0,0,0,0,0,0,0,0,0,0';
		foreach ( $roles_and_capabilities_unserialized as $key => $value ) {
			if ( $privileges === $key ) {
				$privileges_value = $value;
				break;
			}
		}
		$full_control = explode( ',', $privileges_value );
		if ( ! defined( 'FULL_CONTROL' ) ) {
			define( 'FULL_CONTROL', "$full_control[0]" );
		}
		if ( ! defined( 'FORMS_CONTACT_BANK' ) ) {
			define( 'FORMS_CONTACT_BANK', "$full_control[1]" );
		}
		if ( ! defined( 'LAYOUT_SETTINGS_CONTACT_BANK' ) ) {
			define( 'LAYOUT_SETTINGS_CONTACT_BANK', "$full_control[2]" );
		}
		if ( ! defined( 'CUSTOM_CSS_CONTACT_BANK' ) ) {
			define( 'CUSTOM_CSS_CONTACT_BANK', "$full_control[3]" );
		}
		if ( ! defined( 'EMAIL_TEMPLATES_CONTACT_BANK' ) ) {
			define( 'EMAIL_TEMPLATES_CONTACT_BANK', "$full_control[4]" );
		}
		if ( ! defined( 'GENERAL_SETTINGS_CONTACT_BANK' ) ) {
			define( 'GENERAL_SETTINGS_CONTACT_BANK', "$full_control[5]" );
		}
		if ( ! defined( 'SUBMISSIONS_CONTACT_BANK' ) ) {
			define( 'SUBMISSIONS_CONTACT_BANK', "$full_control[6]" );
		}
		if ( ! defined( 'ROLES_AND_CAPABILITIES_CONTACT_BANK' ) ) {
			define( 'ROLES_AND_CAPABILITIES_CONTACT_BANK', "$full_control[7]" );
		}
		if ( ! defined( 'SYSTEM_INFORMATION_CONTACT_BANK' ) ) {
			define( 'SYSTEM_INFORMATION_CONTACT_BANK', "$full_control[8]" );
		}
		$check_contact_bank_wizard = get_option( 'contact-bank-wizard-set-up' );
		if ( '1' === $flag ) {
			$icon = CONTACT_BANK_PLUGIN_URL . 'assets/global/img/icon.png';
			if ( $check_contact_bank_wizard ) {
				add_menu_page( $cb_contact_bank, $cb_contact_bank, 'read', 'contact_dashboard', '', $icon );
			} else {
				add_menu_page( $cb_contact_bank, $cb_contact_bank, 'read', 'cb_wizard_contact_bank', '', plugins_url( 'assets/global/img/icon.png', dirName( __FILE__ ) ) );
				add_submenu_page( $cb_contact_bank, $cb_contact_bank, '', 'read', 'cb_wizard_contact_bank', 'cb_wizard_contact_bank' );
			}
			add_submenu_page( 'contact_dashboard', $cb_forms, $cb_forms, 'read', 'contact_dashboard', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'contact_dashboard' );
			add_submenu_page( 'contact_dashboard', $cb_layout_settings, $cb_layout_settings, 'read', 'cb_layout_settings', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'cb_layout_settings' );
			add_submenu_page( 'contact_dashboard', $cb_custom_css, $cb_custom_css, 'read', 'cb_custom_css', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'cb_custom_css' );
			add_submenu_page( 'contact_dashboard', $cb_email_templates, $cb_email_templates, 'read', 'cb_email_templates', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'cb_email_templates' );
			add_submenu_page( 'contact_dashboard', $cb_general_settings, $cb_general_settings, 'read', 'cb_general_settings', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'cb_general_settings' );
			add_submenu_page( 'contact_dashboard', $cb_submissions, $cb_submissions, 'read', 'cb_submissions', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'cb_submissions' );
			add_submenu_page( 'contact_dashboard', $cb_roles_and_capabilities, $cb_roles_and_capabilities, 'read', 'cb_roles_and_capabilities', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'cb_roles_and_capabilities' );
			add_submenu_page( 'contact_dashboard', $cb_ask_for_help, $cb_ask_for_help, 'read', 'https://wordpress.org/support/plugin/contact-bank' );
			add_submenu_page( 'contact_dashboard', $cb_system_information, $cb_system_information, 'read', 'cb_system_information', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'cb_system_information' );
			add_submenu_page( $cb_forms, $cb_add_new_form, '', 'read', 'cb_add_new_form', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'cb_add_new_form' );
			add_submenu_page( $cb_email_templates, $cb_add_new_email_template, '', 'read', 'cb_add_new_email_template', false === $check_contact_bank_wizard ? 'cb_wizard_contact_bank' : 'cb_add_new_email_template' );
			add_submenu_page( 'contact_dashboard', $cb_premium_edition, $cb_premium_edition, 'read', 'https://contact-bank.tech-banker.com/pricing/' );
		}

		/**
		 * Function Name: cb_wizard_contact_bank
		 * Parameters: No
		 * Description: This function is used for creating cb_wizard_contact_bank menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_wizard_contact_bank() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/wizard/wizard.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/wizard/wizard.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: contact_dashboard
		 * Parameters: No
		 * Description: This function is used for manage-forms menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function contact_dashboard() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/forms/manage-forms.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/forms/manage-forms.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: cb_add_new_form
		 * Parameters: No
		 * Description: This function is used for cb_add_new_form menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_add_new_form() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/contact-bank-controls-list.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/contact-bank-controls-list.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/forms/add-new-forms.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/forms/add-new-forms.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: cb_layout_settings
		 * Parameters: No
		 * Description: This function is used for cb_layout_settings menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_layout_settings() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}

			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/layout-settings/layout-settings.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/layout-settings/layout-settings.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: cb_custom_css
		 * Parameters: No
		 * Description: This function is used for cb_custom_css menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_custom_css() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/custom-css/custom-css.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/custom-css/custom-css.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: cb_email_templates
		 * Parameters: No
		 * Description: This function is used for manage-email menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_email_templates() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/email-templates/email-templates.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/email-templates/email-templates.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: cb_add_new_email_template
		 * Parameters: No
		 * Description: This function is used for manage-email menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_add_new_email_template() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/email-templates/add-new-email-template.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/email-templates/add-new-email-template.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: cb_general_settings
		 * Parameters: No
		 * Description: This function is used for cb_general_settings menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_general_settings() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/general-settings/general-settings.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/general-settings/general-settings.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: cb_submissions
		 * Parameters: No
		 * Description: This function is used for cb_submissions menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_submissions() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/submissions/submissions.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/submissions/submissions.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: cb_roles_and_capabilities
		 * Parameters: No
		 * Description: This function is used for cb_roles_and_capabilities menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_roles_and_capabilities() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/roles-and-capabilities/roles-and-capabilities.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/roles-and-capabilities/roles-and-capabilities.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}

		/**
		 * Function Name: cb_system_information
		 * Parameters: No
		 * Description: This function is used for cb_system_information menu.
		 * Created On: 04-09-2017 04:57
		 * Created By: Tech Banker Team
		 */
		function cb_system_information() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/header.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/sidebar.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/system-information/system-information.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/system-information/system-information.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/footer.php';
			}
		}
	}
}
