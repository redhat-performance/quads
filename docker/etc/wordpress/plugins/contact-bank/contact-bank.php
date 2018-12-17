<?php // @codingStandardsIgnoreLine.
/**
 * Plugin Name: Contact Bank
 * Plugin URI: https://contact-bank.tech-banker.com/
 * Description: Contact Bank is a user-friendly form builder plugin. This form builder lets you create contact forms and other forms in seconds with ease.
 * Author: Tech-Banker
 * Author URI: https://contact-bank.tech-banker.com
 * Version: 3.0.22
 * License: GPLv3
 * Text Domain: contact-bank
 * Domain Path: /languages
 *
 * @package contact-bank
 */

if ( ! defined( 'ABSPATH' ) ) {
		exit;
} // Exit if accessed directly

if ( ! defined( 'CONTACT_BANK_LOCAL_TIME' ) ) {
		define( 'CONTACT_BANK_LOCAL_TIME', strtotime( date_i18n( 'Y-m-d H:i:s' ) ) );
}
if ( ! defined( 'CONTACT_BANK_PLUGIN_DIR_PATH' ) ) {
		define( 'CONTACT_BANK_PLUGIN_DIR_PATH', plugin_dir_path( __FILE__ ) );
}
if ( ! defined( 'CONTACT_BANK_FILE' ) ) {
		define( 'CONTACT_BANK_FILE', 'contact-bank/contact-bank.php' );
}
if ( ! defined( 'CONTACT_BANK_PLUGIN_DIRNAME' ) ) {
		define( 'CONTACT_BANK_PLUGIN_DIRNAME', plugin_basename( dirname( __FILE__ ) ) );
}
if ( ! defined( 'CONTACT_BANK_USER_VIEWS_PATH' ) ) {
		define( 'CONTACT_BANK_USER_VIEWS_PATH', CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/' );
}
if ( ! defined( 'CONTACT_BANK_MAIN_DIR' ) ) {
		define( 'CONTACT_BANK_MAIN_DIR', dirname( dirname( dirname( __FILE__ ) ) ) . '/contact-bank/' );
}
if ( ! defined( 'CONTACT_BANK_PLUGIN_URL' ) ) {
		define( 'CONTACT_BANK_PLUGIN_URL', plugin_dir_url( __FILE__ ) );
}
if ( ! defined( 'CONTACT_BANK_WIZARD_VERSION_NUMBER' ) ) {
		define( 'CONTACT_BANK_WIZARD_VERSION_NUMBER', '3.0.22' );
}
if ( ! defined( 'TECH_BANKER_STATS_URL' ) ) {
		define( 'TECH_BANKER_STATS_URL', 'http://stats.tech-banker-services.org' );
}
if ( ! defined( 'CONTACT_BANK_LOCAL_TIME' ) ) {
		define( 'CONTACT_BANK_LOCAL_TIME', strtotime( date_i18n( 'Y-m-d H:i:s' ) ) );
}
if ( is_ssl() ) {
	if ( ! defined( 'TECH_BANKER_URL' ) ) {
			define( 'TECH_BANKER_URL', 'https://tech-banker.com' );
	}
	if ( ! defined( 'TECH_BANKER_BETA_URL' ) ) {
			define( 'TECH_BANKER_BETA_URL', 'https://contact-bank.tech-banker.com/' );
	}
} else {
	if ( ! defined( 'TECH_BANKER_URL' ) ) {
			define( 'TECH_BANKER_URL', 'http://tech-banker.com' );
	}
	if ( ! defined( 'TECH_BANKER_BETA_URL' ) ) {
			define( 'TECH_BANKER_BETA_URL', 'http://contact-bank.tech-banker.com/' );
	}
}
$memory_limit_contact_bank = intval( ini_get( 'memory_limit' ) );
if ( ! extension_loaded( 'suhosin' ) && $memory_limit_contact_bank < 512 ) {
		@ini_set( 'memory_limit', '1024M' );// @codingStandardsIgnoreLine.
}
if ( ! is_dir( CONTACT_BANK_MAIN_DIR ) ) {
		wp_mkdir_p( CONTACT_BANK_MAIN_DIR );
}
/**
 * This function is used to include install script for contact bank.
 */
function install_script_for_contact_bank() {
		global $wpdb;
	if ( is_multisite() ) {
			$blog_ids = $wpdb->get_col( "SELECT blog_id FROM $wpdb->blogs" );// WPCS: db call ok, no-cache ok.
		foreach ( $blog_ids as $blog_id ) {
				switch_to_blog( $blog_id );// @codingStandardsIgnoreLine.
				$version = get_option( 'contact-bank-version-number' );
			if ( $version < '3.0.1' ) {
				if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/class-dbhelper-install-script-contact-bank.php' ) ) {
						include CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/class-dbhelper-install-script-contact-bank.php';
				}
			}
				restore_current_blog();
		}
	} else {
			$version = get_option( 'contact-bank-version-number' );
		if ( $version < '3.0.1' ) {
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/class-dbhelper-install-script-contact-bank.php' ) ) {
					include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/class-dbhelper-install-script-contact-bank.php';
			}
		}
	}
}

/**
 * This function is used for creating a parent table.
 */
function contact_bank() {
	global $wpdb;
	return $wpdb->prefix . 'contact_bank';
}

/**
 * This function is used for creating a meta table.
 */
function contact_bank_meta() {
		global $wpdb;
		return $wpdb->prefix . 'contact_bank_meta';
}

/**
 * This function is used for checking roles of different users.
 *
 * @param string $user .
 */
function check_user_roles_contact_bank( $user = null ) {
		$user = $user ? new WP_User( $user ) : wp_get_current_user();
		return $user->roles ? $user->roles[0] : false;
}

/**
 * This function is used to get all the roles available in WordPress
 */
function get_others_capabilities_contact_bank() {
		$user_capabilities = array();
	if ( function_exists( 'get_editable_roles' ) ) {
		foreach ( get_editable_roles() as $role_name => $role_info ) {
			foreach ( $role_info['capabilities'] as $capability => $values ) {
				if ( ! in_array( $capability, $user_capabilities, true ) ) {
						array_push( $user_capabilities, $capability );
				}
			}
		}
	} else {
			$user_capabilities = array(
				'manage_options',
				'edit_plugins',
				'edit_posts',
				'publish_posts',
				'publish_pages',
				'edit_pages',
				'read',
			);
	}
		return $user_capabilities;
}

/**
 * This function is used to call css and js for contact bank frontend
 */
function shortcode_js_css_contact_bank() {
		wp_enqueue_style( 'contact-bank-popup.css', plugins_url( 'assets/admin/layout/css/contact-bank-popup.css', __FILE__ ) );
}

/**
 * This function used for calling admin function fired on admin_init hook.
 */
function admin_functions_contact_form() {
		shortcode_js_css_contact_bank();
		install_script_for_contact_bank();
		contact_bank_redirect();
}

$version = get_option( 'contact-bank-version-number' );
if ( '3.0.1' === $version ) {
	if ( is_admin() ) {
		/**
		 * This is used for calling a js and css backend function.
		 *
		 * @param string $hook .
		 */
		function backend_js_css_for_contact_bank( $hook ) {
				$pages_contact_bank = array(
					'cb_wizard_contact_bank',
					'contact_dashboard',
					'cb_layout_settings',
					'cb_custom_css',
					'cb_email_templates',
					'cb_general_settings',
					'cb_submissions',
					'cb_roles_and_capabilities',
					'cb_system_information',
					'cb_add_new_form',
				);
			if ( isset( $_REQUEST['page'] ) ) {
					$page_url = sanitize_text_field( wp_unslash( $_REQUEST['page'] ) );// WPCS: Input var ok, CSRF ok.
				if ( in_array( $page_url, $pages_contact_bank, true ) ) {
						wp_enqueue_script( 'jquery' );
						wp_enqueue_script( 'jquery-ui-droppable' );
						wp_enqueue_script( 'jquery-ui-sortable' );
						wp_enqueue_script( 'jquery-ui-datepicker' );
						wp_enqueue_script( 'contact-bank-bootstrap.js', plugins_url( 'assets/global/plugins/custom/js/custom.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-jquery.validate.js', plugins_url( 'assets/global/plugins/validation/jquery.validate.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-jquery.datatables.js', plugins_url( 'assets/global/plugins/datatables/media/js/jquery.datatables.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-clipboard.js', plugins_url( 'assets/global/plugins/clipboard/clipboard.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-colpick.js', plugins_url( 'assets/global/plugins/colorpicker/colpick.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-jquery.fngetfilterednodes.js', plugins_url( 'assets/global/plugins/datatables/media/js/fngetfilterednodes.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-toastr.js', plugins_url( 'assets/global/plugins/toastr/toastr.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-buttons.html5.js', plugins_url( 'assets/global/plugins/datatables/media/js/buttons.html5.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-datatables.buttons.js', plugins_url( 'assets/global/plugins/datatables/media/js/datatables.buttons.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-jszip.min.js', plugins_url( 'assets/global/plugins/datatables/media/js/jszip.min.js', __FILE__ ) );
						wp_enqueue_script( 'contact-bank-input-masking.min.js', plugins_url( 'assets/global/plugins/input-masking/masking-input.js', __FILE__ ), null, null, true );
						wp_enqueue_style( 'contact-bank-simple-line-icons.css', plugins_url( 'assets/global/plugins/icons/icons.css', __FILE__ ) );
						wp_enqueue_style( 'contact-bank-components.css', plugins_url( 'assets/global/css/components.css', __FILE__ ) );
					if ( is_rtl() ) {
							wp_enqueue_style( 'contact-bank-bootstrap.css', plugins_url( 'assets/global/plugins/custom/css/custom-rtl.css', __FILE__ ) );
							wp_enqueue_style( 'contact-bank-layout.css', plugins_url( 'assets/admin/layout/css/layout-rtl.css', __FILE__ ) );
							wp_enqueue_style( 'contact-bank-custom.css', plugins_url( 'assets/admin/layout/css/tech-banker-custom-rtl.css', __FILE__ ) );
					} else {
							wp_enqueue_style( 'contact-bank-bootstrap.css', plugins_url( 'assets/global/plugins/custom/css/custom.css', __FILE__ ) );
							wp_enqueue_style( 'contact-bank-layout.css', plugins_url( 'assets/admin/layout/css/layout.css', __FILE__ ) );
							wp_enqueue_style( 'contact-bank-custom.css', plugins_url( 'assets/admin/layout/css/tech-banker-custom.css', __FILE__ ) );
					}
						wp_enqueue_style( 'contact-bank.css', plugins_url( 'assets/admin/layout/css/contact-bank.css', __FILE__ ) );
						wp_enqueue_style( 'contact-bank-default.css', plugins_url( 'assets/admin/layout/css/themes/default.css', __FILE__ ) );
						wp_enqueue_style( 'contact-bank-toastr.min.css', plugins_url( 'assets/global/plugins/toastr/toastr.css', __FILE__ ) );
						wp_enqueue_style( 'contact-bank-jquery-ui.css', plugins_url( 'assets/global/plugins/datepicker/jquery-ui.css', __FILE__ ), false, '2.0', false );
						wp_enqueue_style( 'contact-bank-datatables.foundation.css', plugins_url( 'assets/global/plugins/datatables/media/css/datatables.foundation.css', __FILE__ ) );
						wp_enqueue_style( 'contact-bank-colpick.css', plugins_url( 'assets/global/plugins/colorpicker/colpick.css', __FILE__ ) );
				}
			}
		}
		add_action( 'admin_enqueue_scripts', 'backend_js_css_for_contact_bank' );
	}

	/**
	 * This function is used to get users capabilities.
	 */
	function get_users_capabilities_contact_bank() {
			global $wpdb;
			$capabilities              = $wpdb->get_var(
				$wpdb->prepare(
					'SELECT meta_value FROM ' . $wpdb->prefix . 'contact_bank_meta
																WHERE meta_key = %s', 'roles_and_capabilities'
				)
			);// WPCS: db call ok, no-cache ok.
			$core_roles                = array(
				'manage_options',
				'edit_plugins',
				'edit_posts',
				'publish_posts',
				'publish_pages',
				'edit_pages',
			);
			$unserialized_capabilities = maybe_unserialize( $capabilities );
			return isset( $unserialized_capabilities['capabilities'] ) ? $unserialized_capabilities['capabilities'] : $core_roles;
	}

	/**
	 * This function is used to call helper file for contact bank
	 */
	function helper_file_for_contact_form() {
			global $wpdb, $current_user;
			$user_role_permission = get_users_capabilities_contact_bank();
		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/class-dbhelper-contact-bank.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/class-dbhelper-contact-bank.php';
		}
	}

	/**
	 * This is used for calling a sidebar menu function.
	 */
	function sidebar_menu_for_contact_bank() {
			global $wpdb, $current_user;
			$user_role_permission = get_users_capabilities_contact_bank();
		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
		}

		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/sidebar-menu.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/sidebar-menu.php';
		}
	}

	/**
	 * This is used for calling a top bar menu function.
	 */
	function top_bar_menu_for_contact_bank() {
			global $wpdb, $current_user, $wp_admin_bar;
			$user_role_permission         = get_users_capabilities_contact_bank();
			$role_capabilities            = $wpdb->get_var(
				$wpdb->prepare(
					'SELECT meta_value from ' . $wpdb->prefix . 'contact_bank_meta
																				WHERE ' . $wpdb->prefix . 'contact_bank_meta. meta_key = %s', 'roles_and_capabilities'
				)
			);// WPCS: db call ok, no-cache ok.
			$role_capabilities_serialized = maybe_unserialize( $role_capabilities );
		if ( 'enable' === $role_capabilities_serialized['show_contact_bank_top_bar_menu'] ) {

			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
					include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/admin-bar-menu.php' ) ) {
					include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/admin-bar-menu.php';
			}
		}
	}

	/**
	 * This function is used to load languages.
	 */
	function plugin_load_textdomain_contact_bank() {
		if ( function_exists( 'load_plugin_textdomain' ) ) {
				load_plugin_textdomain( 'contact-bank', false, CONTACT_BANK_PLUGIN_DIRNAME . '/languages' );
		}
	}

	/**
	 * This function is used to register ajax for contact bank
	 */
	function main_ajax_file_for_contact_bank() {
			global $wpdb, $current_user;
			$user_role_permission = get_users_capabilities_contact_bank();
		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
		}
		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/action-library.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/action-library.php';
		}
	}
	/**
	 * This function is used for calling the frontend functions.
	 */
	function user_functions_contact_bank() {
			plugin_load_textdomain_contact_bank();
			helper_file_for_contact_bank_frontend();
			global $wpdb;
			$get_general_settings = $wpdb->get_var(
				$wpdb->prepare(
					'SELECT meta_value from ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s', 'general_settings'
				)
			);// WPCS: db call ok, no-cache ok.
	}

	if ( isset( $_REQUEST['cb_preview_form'] ) ) {// WPCS: Input var ok, CSRF ok.
		/**
		 * This function is used for preview the content.
		 */
		function preview_form_contact_bank() {
			if ( ! is_user_logged_in() ) {
					echo '<strong>You must be logged in to preview a form.</strong>';
			} else {
					global $wpdb, $current_user;
					$user_role_permission = get_users_capabilities_contact_bank();
					$random               = rand( 100, 10000 );
				if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
						include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
				}
				if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
						include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
				}
				if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/includes/style-sheet.php' ) ) {
						include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/includes/style-sheet.php';
				}
				if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'views/preview-page/preview-page.php' ) ) {
						include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'views/preview-page/preview-page.php';
				}
				if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/includes/footer.php' ) ) {
						include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/includes/footer.php';
				}
			}
		}

			add_filter( 'the_content', 'preview_form_contact_bank' );
			add_action( 'init', 'preview_form_js_css_for_contact_bank' );
	}
	/**
	 * This function is used to call css and js for preview form
	 */
	function preview_form_js_css_for_contact_bank() {
			wp_enqueue_script( 'jquery-ui-datepicker' );
			wp_enqueue_script( 'contact-bank-bootstrap.js', plugins_url( 'assets/global/plugins/custom/js/custom.js', __FILE__ ) );
			wp_enqueue_script( 'contact-bank-jquery.validate.js', plugins_url( 'assets/global/plugins/validation/jquery.validate.js', __FILE__ ) );
			wp_enqueue_script( 'contact-bank-colpick.js', plugins_url( 'assets/global/plugins/colorpicker/colpick.js', __FILE__ ) );
			wp_enqueue_script( 'contact-bank-toastr.js', plugins_url( 'assets/global/plugins/toastr/toastr.js', __FILE__ ) );
			wp_enqueue_script( 'contact-bank-input-masking.min.js', plugins_url( 'assets/global/plugins/input-masking/masking-input.js', __FILE__ ), null, null, true );
			wp_enqueue_style( 'contact-bank-simple-line-icons.css', plugins_url( 'assets/global/plugins/icons/icons.css', __FILE__ ) );
			wp_enqueue_style( 'contact-bank-components.css', plugins_url( 'assets/global/css/components.css', __FILE__ ) );
		if ( is_rtl() ) {
				wp_enqueue_style( 'contact-bank-bootstrap.css', plugins_url( 'assets/global/plugins/custom/css/custom-rtl.css', __FILE__ ) );
				wp_enqueue_style( 'contact-bank-layout.css', plugins_url( 'assets/admin/layout/css/layout-rtl.css', __FILE__ ) );
				wp_enqueue_style( 'contact-bank-custom.css', plugins_url( 'assets/admin/layout/css/tech-banker-custom-rtl.css', __FILE__ ) );
		} else {
				wp_enqueue_style( 'contact-bank-bootstrap.css', plugins_url( 'assets/global/plugins/custom/css/custom.css', __FILE__ ) );
				wp_enqueue_style( 'contact-bank-layout.css', plugins_url( 'assets/admin/layout/css/layout.css', __FILE__ ) );
				wp_enqueue_style( 'contact-bank-custom.css', plugins_url( 'assets/admin/layout/css/tech-banker-custom.css', __FILE__ ) );
		}
			wp_enqueue_style( 'contact-bank.css', plugins_url( 'assets/admin/layout/css/contact-bank.css', __FILE__ ) );
			wp_enqueue_style( 'contact-bank-default.css', plugins_url( 'assets/admin/layout/css/themes/default.css', __FILE__ ) );
			wp_enqueue_style( 'contact-bank-toastr.min.css', plugins_url( 'assets/global/plugins/toastr/toastr.css', __FILE__ ) );
			wp_enqueue_style( 'contact-bank-jquery-ui.css', plugins_url( 'assets/global/plugins/datepicker/jquery-ui.css', __FILE__ ), false, '2.0', false );
			wp_enqueue_style( 'contact-bank-colpick.css', plugins_url( 'assets/global/plugins/colorpicker/colpick.css', __FILE__ ) );
	}

	/**
	 * This function is used to call js file in frontend
	 */
	function frontend_js_files_contact_bank() {
		wp_enqueue_script( 'jquery' );
		wp_enqueue_script( 'contact-bank-bootstrap.js', plugins_url( 'assets/global/plugins/custom/js/custom.js', __FILE__ ) );
	}

	/**
	 * This function is used to call helper file for contact bank frontend
	 */
	function helper_file_for_contact_bank_frontend() {
		global $wpdb;
		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/lib/class-user-helper-contact-bank.php' ) ) {
			include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/lib/class-user-helper-contact-bank.php';
		}
	}

	/**
	 * This function is used to parse contents.
	 *
	 * @param array $content .
	 */
	function parse_shortcode_content_contact_bank( $content ) {

			/* Parse nested shortcodes and add formatting. */
			$content = trim( do_shortcode( shortcode_unautop( $content ) ) );

			/* Remove '' from the start of the string. */
		if ( '' === substr( $content, 0, 4 ) ) {
					$content = substr( $content, 4 );
		}

			/* Remove '' from the end of the string. */
		if ( '' === substr( $content, -3, 3 ) ) {
				$content = substr( $content, 0, -3 );
		}

			/* Remove any instances of ''. */
			$content = str_replace( array( '<p></p>' ), '', $content );
			$content = str_replace( array( '<p>  </p>' ), '', $content );

			return $content;
	}

	/**
	 * It is used for a creating shortcode for contact bank.
	 *
	 * @param array $atts .
	 * @param array $content .
	 */
	function contact_bank_shortcode( $atts, $content ) {
			extract(// @codingStandardsIgnoreLine.
				shortcode_atts(
					array(
						'form_id'          => '',
						'form_title'       => '',
						'form_description' => '',
						'show_title'       => '',
						'show_desc'        => '',
					), $atts
				)
			);
		if ( isset( $show_title ) && '' !== $show_title ) {
				$form_title       = 'true' === $show_title ? 'show' : 'hide';
				$form_description = 'true' === $show_desc ? 'show' : 'hide';
		}
		if ( ! is_feed() ) {
			if ( ! class_exists( 'SiteOrigin_Panels' ) && ! class_exists( 'ckeditor_wordpress' ) && ! class_exists( 'Tinymce_Advanced' ) ) {
					ob_start();
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/includes/structure.php' ) ) {
					include CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/includes/structure.php';
			}

			if ( class_exists( 'SiteOrigin_Panels' ) || class_exists( 'ckeditor_wordpress' ) || class_exists( 'Tinymce_Advanced' ) ) {
					$content = parse_shortcode_content_contact_bank( $content );
					return $content;
			} else {
					$contact_bank_output = ob_get_clean();
					wp_reset_query();// @codingStandardsIgnoreLine.
					return $contact_bank_output;
			}
		}
	}

	/**
	 * This function is used for button show on frontend.
	 *
	 * @param string $context .
	 */
	function add_contact_form_shortcode_button( $context ) {
			add_thickbox();
			$context .= '<a href="#TB_inline?width=300&height=400&inlineId=contact-bank"  class="button thickbox"  title="' . __( 'Add Contact Bank Form', 'contact-bank' ) . '">
						<span class="contact_bank_icon"></span> Add Contact Bank Form</a>';
			return $context;
	}

	/**
	 * This function is used for popup show on frontend.
	 */
	function add_contact_form_mce_popup() {
			global $wpdb;
			$user_role_permission = get_users_capabilities_contact_bank();
			add_thickbox();
		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
				include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
		}
		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/shortcode-button.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/shortcode-button.php';
		}
	}

	/**
	 * This function is used for including the frontend ajax file.
	 */
	function frontend_ajax_call_contact_bank() {
			global $wpdb;
		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/lib/frontend-ajax.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/lib/frontend-ajax.php';
		}
	}

	/**
	 * This class is used to add widget.
	 */
	class Contact_Bank_Widget extends WP_Widget {
		/**
		 * Public Constructor
		 */
		public function __construct() {
				parent::__construct(
					'contact_bank_widget', __( 'Contact Bank', 'contact-bank' ), array( 'description' => __( 'Build Complex, Powerful Contact Forms in Just Seconds.', 'contact-bank' ) )
				);
		}
		/**
		 * This function is used to add widget form.
		 *
		 * @param array $instance .
		 */
		public function form( $instance ) {
				global $wpdb;
				$user_role_permission = get_users_capabilities_contact_bank();
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php' ) ) {
					include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/queries.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php' ) ) {
					include CONTACT_BANK_PLUGIN_DIR_PATH . 'includes/translations.php';
			}
			if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/includes/widget-form.php' ) ) {
					include CONTACT_BANK_PLUGIN_DIR_PATH . 'user-views/includes/widget-form.php';
			}
		}

		/**
		 * This function is used to display widget.
		 *
		 * @param array $args .
		 * @param array $instance .
		 */
		public function widget( $args, $instance ) {
				extract( $args, EXTR_SKIP );// @codingStandardsIgnoreLine.
				echo $before_widget;// WPCS: XSS ok.
			if ( isset( $instance['title'] ) ) {
					$form_id = $instance['form_id'];
					echo do_shortcode( "[contact_bank form_id=\"$form_id\" form_title=\"show\" form_description=\"hide\"][/contact_bank]" );
			} else {
					$shortcode_data = empty( $instance['form_name'] ) ? ' ' : apply_filters( 'widget_contact_bank_shortcode', $instance['form_name'] );
				if ( ! empty( $shortcode_data ) ) {
						$form_name        = $instance['form_name'];
						$form_title       = $instance['form_title'];
						$form_description = $instance['form_description'];
						echo do_shortcode( "[contact_bank form_id=\"$form_name\" form_title=\"$form_title\" form_description=\"$form_description\"][/contact_bank]" );
				}
			}
			echo $after_widget;// WPCS: XSS ok.
		}

		/**
		 * This function is used to update widget.
		 *
		 * @param array $new_instance .
		 * @param array $old_instance .
		 */
		public function update( $new_instance, $old_instance ) {
				$instance                     = $old_instance;
				$instance['form_name']        = $new_instance['ux_ddl_shortcode_form_name'];
				$instance['form_title']       = $new_instance['ux_ddl_shortcode_form_title'];
				$instance['form_description'] = $new_instance['ux_ddl_shortcode_form_description'];
				return $instance;
		}
	}

	/**
	 * This function is used for executing the code on deactivation.
	 */
	function deactivation_function_for_contact_bank() {
			delete_option( 'contact-bank-wizard-set-up' );
	}
	/**
	 * This function is used to create link for Pro Editions.
	 *
	 * @param string $plugin_link passes paramater as plugin link.
	 */
	function contact_bank_action_links( $plugin_link ) {
		$plugin_link[] = '<a href="https://contact-bank.tech-banker.com/" style="color: red; font-weight: bold;" target="_blank">Go Pro!</a>';
		return $plugin_link;
	}
	/**
	 * This function is used to add a widget to the dashboard.
	 */
	function add_dashboard_widgets_contact_bank() {
			wp_add_dashboard_widget(
				'cb_dashboard_widget', // Widget slug.
				'Contact Bank Statistics', // Title.
				'dashboard_widget_function_contact_bank'// Display function.
			);
	}

	/**
	 * This function is used to to output the contents of our Dashboard Widget.
	 */
	function dashboard_widget_function_contact_bank() {
		global $wpdb;
		if ( file_exists( CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/dashboard-widget.php' ) ) {
				include_once CONTACT_BANK_PLUGIN_DIR_PATH . 'lib/dashboard-widget.php';
		}
	}
	// Hooks.
	/**
	 * This hook is used for calling a function of sidebar menu
	 */
	add_action( 'admin_menu', 'sidebar_menu_for_contact_bank' );
	add_action( 'network_admin_menu', 'sidebar_menu_for_contact_bank' );

	/**
	 * This hook is used for calling a function of top bar menu.
	 */
	add_action( 'admin_bar_menu', 'top_bar_menu_for_contact_bank', 100 );

	/**
	 * This hook is used for calling all the frontend functions
	 */
	add_action( 'init', 'user_functions_contact_bank' );

	/**
	 * This hook is used for calling backend ajax function
	 */
	add_action( 'wp_ajax_contact_bank_action_module', 'main_ajax_file_for_contact_bank' );

	/**
	 * This hook is used for calling the function of add to button.
	 */
	add_action( 'media_buttons_context', 'add_contact_form_shortcode_button', 1 );

	/**
	 *This hook is used for calling the function of show popup.
	 */
	add_action( 'admin_footer', 'add_contact_form_mce_popup' );

	/**
	 * This function for shortcode.
	 */
	add_shortcode( 'contact_bank', 'contact_bank_shortcode' );

	/**
	 * This function for calling js file in frontend.
	 */
	add_action( 'init', 'frontend_js_files_contact_bank' );

	/**
	 * This hook is used for calling frontend ajax function
	 */
	add_action( 'wp_ajax_contact_bank_frontend_ajax_call', 'frontend_ajax_call_contact_bank' );
	add_action( 'wp_ajax_nopriv_contact_bank_frontend_ajax_call', 'frontend_ajax_call_contact_bank' );

	/**
	 * This function is used for initiate Widget.
	 */
	function register_foo_widget_contact_bank() {
		register_widget( 'Contact_Bank_Widget' );
	}

	/**
	 * This hook is used for initiate Widget.
	 */
	add_action( 'widgets_init', 'register_foo_widget_contact_bank' );

	/**
	 * This hook is used for apply the shortcode for Widget.
	 */
	add_filter( 'widget_text', 'do_shortcode' );

	/*
	Add_filter create Go Pro link for Contact Bank
	Description: This hook is used for create link for premium Editions.
	Created On: 25-09-2017 12:21
	Created by: Tech Banker Team
	*/

	add_filter( 'plugin_action_links_' . plugin_basename( __FILE__ ), 'contact_bank_action_links' );
	/**
	 * This hook is used to add widget on dashboard.
	 */
		add_action( 'wp_dashboard_setup', 'add_dashboard_widgets_contact_bank' );

	/**
	 * This hook is used for calling the helper file.
	 */
		add_action( 'admin_init', 'helper_file_for_contact_form' );
}
/**
 * This hook is used to call install script
 */
register_activation_hook( __FILE__, 'install_script_for_contact_bank' );

/**
 * This hook is used for calling all the backend functions
 */
add_action( 'admin_init', 'admin_functions_contact_form' );

/**
 *This hook is used to sets the deactivation hook for a plugin.
 */
register_deactivation_hook( __FILE__, 'deactivation_function_for_contact_bank' );

/**
 * This function is used to create the object of admin notices.
 */
function contact_bank_admin_notice_class() {
	global $wpdb;
	/**
	 * This class is used to add admin notices.
	 */
	 class Contact_Bank_Admin_Notices {// @codingStandardsIgnoreLine.
		/**
		 * The $promo_link of this plugin.
		 *
		 * @access   protected
		 * @var      string    $promo_link  .
		 */
		protected $promo_link = '';
		/**
		 * This is $config variable.
		 *
		 * @access public
		 * @var    string    $config .
		 */
		public $config;
		/**
		 * This is $notice_spam variable.
		 *
		 * @access   public
		 * @var      integer    $notice_spam .
		 */
		public $notice_spam = 0;
		/**
		 * This is $notice_spam_max variable.
		 *
		 * @access   public
		 * @var      integer    $notice_spam_max .
		 */
		public $notice_spam_max = 2;
			/**
			 * Public Constructor
			 *
			 * @param array $config .
			 */
		public function __construct( $config = array() ) {
				// Runs the admin notice ignore function incase a dismiss button has been clicked.
				add_action( 'admin_init', array( $this, 'cb_admin_notice_ignore' ) );
				// Runs the admin notice temp ignore function incase a temp dismiss link has been clicked.
				add_action( 'admin_init', array( $this, 'cb_admin_notice_temp_ignore' ) );
				add_action( 'admin_notices', array( $this, 'cb_display_admin_notices' ) );
		}

		/**
		 * Checks to ensure notices aren't disabled and the user has the correct permissions.
		 */
		public function cb_admin_notices() {
				$settings = get_option( 'cb_admin_notice' );
			if ( ! isset( $settings['disable_admin_notices'] ) || ( isset( $settings['disable_admin_notices'] ) && 0 === $settings['disable_admin_notices'] ) ) {
				if ( current_user_can( 'manage_options' ) ) {
						return true;
				}
			}
				return false;
		}

		/**
		 * Primary notice function that can be called from an outside function sending necessary variables.
		 *
		 * @param string $admin_notices .
		 */
		public function change_admin_notice_contact_bank( $admin_notices ) {
				// Check options.
			if ( ! $this->cb_admin_notices() ) {
					return false;
			}
			foreach ( $admin_notices as $slug => $admin_notice ) {
					// Call for spam protection.
				if ( $this->cb_anti_notice_spam() ) {
						return false;
				}
					// Check for proper page to display on.
				if ( isset( $admin_notices[ $slug ]['pages'] ) && is_array( $admin_notices[ $slug ]['pages'] ) ) {
					if ( ! $this->cb_admin_notice_pages( $admin_notices[ $slug ]['pages'] ) ) {
							return false;
					}
				}
					// Check for required fields.
				if ( ! $this->cb_required_fields( $admin_notices[ $slug ] ) ) {
						// Get the current date then set start date to either passed value or current date value and add interval.
						$current_date = current_time( 'm/d/Y' );
						$start        = ( isset( $admin_notices[ $slug ]['start'] ) ? $admin_notices[ $slug ]['start'] : $current_date );
						$start        = date( 'm/d/Y' );
						$interval     = ( isset( $admin_notices[ $slug ]['int'] ) ? $admin_notices[ $slug ]['int'] : 0 );
						$date         = strtotime( '+' . $interval . ' days', strtotime( $start ) );
						$start        = date( 'm/d/Y', $date );

						// This is the main notices storage option.
						$admin_notices_option = get_option( 'cb_admin_notice', array() );
						// Check if the message is already stored and if so just grab the key otherwise store the message and its associated date information.
					if ( ! array_key_exists( $slug, $admin_notices_option ) ) {
							$admin_notices_option[ $slug ]['start'] = date( 'm/d/Y' );
							$admin_notices_option[ $slug ]['int']   = $interval;
							update_option( 'cb_admin_notice', $admin_notices_option );
					}

						// Sanity check to ensure we have accurate information.
						// New date information will not overwrite old date information.
						$admin_display_check    = ( isset( $admin_notices_option[ $slug ]['dismissed'] ) ? $admin_notices_option[ $slug ]['dismissed'] : 0 );
						$admin_display_start    = ( isset( $admin_notices_option[ $slug ]['start'] ) ? $admin_notices_option[ $slug ]['start'] : $start );
						$admin_display_interval = ( isset( $admin_notices_option[ $slug ]['int'] ) ? $admin_notices_option[ $slug ]['int'] : $interval );
						$admin_display_msg      = ( isset( $admin_notices[ $slug ]['msg'] ) ? $admin_notices[ $slug ]['msg'] : '' );
						$admin_display_title    = ( isset( $admin_notices[ $slug ]['title'] ) ? $admin_notices[ $slug ]['title'] : '' );
						$admin_display_link     = ( isset( $admin_notices[ $slug ]['link'] ) ? $admin_notices[ $slug ]['link'] : '' );
						$output_css             = false;

						// Ensure the notice hasn't been hidden and that the current date is after the start date.
					if ( 0 === $admin_display_check && strtotime( $admin_display_start ) <= strtotime( $current_date ) ) {
							// Get remaining query string.
							$query_str = ( isset( $admin_notices[ $slug ]['later_link'] ) ? $admin_notices[ $slug ]['later_link'] : esc_url( add_query_arg( 'cb_admin_notice_ignore', $slug ) ) );
						if ( strpos( $slug, 'promo' ) === false ) {
								// Admin notice display output.
								echo '<div class="update-nag cb-admin-notice" style="width:95%!important;">
																	<div></div>
																	 <strong><p>' . $admin_display_title . '</p></strong>
																	 <strong><p style="font-size:14px !important">' . $admin_display_msg . '</p></strong>
																	 <strong><ul>' . $admin_display_link . '</ul></strong>
																 </div>';// WPCS: XSS ok.
						} else {
							echo '<div class="admin-notice-promo">';
							echo $admin_display_msg;// WPCS: XSS ok.
							echo '<ul class="notice-body-promo blue">
																			 ' . $admin_display_link . '
																		 </ul>';// WPCS: XSS ok.
							echo '</div>';
						}
								$this->notice_spam += 1;
								$output_css         = true;
					}
				}
			}
		}

		/**
		 * Spam protection check
		 */
		public function cb_anti_notice_spam() {
			if ( $this->notice_spam >= $this->notice_spam_max ) {
					return true;
			}
				return false;
		}

		/**
		 * Ignore function that gets ran at admin init to ensure any messages that were dismissed get marked.
		 */
		public function cb_admin_notice_ignore() {
				// If user clicks to ignore the notice, update the option to not show it again.
			if ( isset( $_GET['cb_admin_notice_ignore'] ) ) {// WPCS: CSRF ok, input var ok.
					$admin_notices_option = get_option( 'cb_admin_notice', array() );
					$admin_notices_option[ $_GET['cb_admin_notice_ignore'] ]['dismissed'] = 1;// WPCS: CSRF ok, input var ok, sanitization ok.
					update_option( 'cb_admin_notice', $admin_notices_option );
					$query_str = remove_query_arg( 'cb_admin_notice_ignore' );
					wp_safe_redirect( $query_str );
					exit;
			}
		}

		/**
		 * Ignore function that gets ran at admin init to ensure any messages that were dismissed get marked
		 */
		public function cb_admin_notice_temp_ignore() {
			// If user clicks to temp ignore the notice, update the option to change the start date - default interval of 7 days.
			if ( isset( $_GET['cb_admin_notice_temp_ignore'] ) ) {// WPCS: CSRF ok, input var ok.
					$admin_notices_option = get_option( 'cb_admin_notice', array() );
					$current_date         = current_time( 'm/d/Y' );
					$interval             = ( isset( $_GET['int'] ) ? intval( wp_unslash( $_GET['int'] ) ) : 7 );// WPCS: CSRF ok, input var ok.
					$date                 = strtotime( '+' . $interval . ' days', strtotime( $current_date ) );
					$new_start            = date( 'm/d/Y', $date );

					$admin_notices_option[ $_GET['cb_admin_notice_temp_ignore'] ]['start']     = $new_start;// WPCS: CSRF ok, input var ok, sanitization ok.
					$admin_notices_option[ $_GET['cb_admin_notice_temp_ignore'] ]['dismissed'] = 0;// WPCS: CSRF ok, input var ok, sanitization ok.
					update_option( 'cb_admin_notice', $admin_notices_option );
					$query_str = remove_query_arg( array( 'cb_admin_notice_temp_ignore', 'int' ) );
					wp_safe_redirect( $query_str );
					exit;
			}
		}
		/**
		 * Display admin notice on pages.
		 *
		 * @param array $pages .
		 */
		public function cb_admin_notice_pages( $pages ) {
			foreach ( $pages as $key => $page ) {
				if ( is_array( $page ) ) {
					if ( isset( $_GET['page'] ) && $_GET['page'] === $page[0] && isset( $_GET['tab'] ) && $_GET['tab'] === $page[1] ) {// WPCS: CSRF ok, input var ok.
							return true;
					}
				} else {
					if ( 'all' === $page ) {
							return true;
					}
					if ( get_current_screen()->id === $page ) {
							return true;
					}
					if ( isset( $_GET['page'] ) && $_GET['page'] === $page ) {// WPCS: CSRF ok, input var ok.
							return true;
					}
				}
					return false;
			}
		}

		/**
		 * Required fields check.
		 *
		 * @param array $fields .
		 */
		public function cb_required_fields( $fields ) {
			if ( ! isset( $fields['msg'] ) || ( isset( $fields['msg'] ) && empty( $fields['msg'] ) ) ) {
					return true;
			}
			if ( ! isset( $fields['title'] ) || ( isset( $fields['title'] ) && empty( $fields['title'] ) ) ) {
					return true;
			}
				return false;
		}

		/**
		 * Display Content in admin notice.
		 */
		public function cb_display_admin_notices() {
				$two_week_review_ignore     = add_query_arg( array( 'cb_admin_notice_ignore' => 'two_week_review' ) );
				$two_week_review_temp       = add_query_arg(
					array(
						'cb_admin_notice_temp_ignore' => 'two_week_review',
						'int'                         => 7,
					)
				);
				$notices['two_week_review'] = array(
					'title'      => __( 'Leave A Review For Contact Bank ?', 'contact-bank' ),
					'msg'        => __( 'We love and care about you. Contact Bank Team is putting our maximum efforts to provide you the best functionalities.<br> We would really appreciate if you could spend a couple of seconds to give a Nice Review to the plugin for motivating us!', 'contact-bank' ),
					'link'       => '<span class="dashicons dashicons-external contact-bank-admin-notice"></span><span class="contact-bank-admin-notice"><a href="https://wordpress.org/support/plugin/contact-bank/reviews/?filter=5" target="_blank" class="contact-bank-admin-notice-link">' . __( 'Sure! I\'d love to!', 'contact-bank' ) . '</a></span>
									<span class="dashicons dashicons-smiley contact-bank-admin-notice"></span><span class="contact-bank-admin-notice"><a href="' . $two_week_review_ignore . '" class="contact-bank-admin-notice-link"> ' . __( 'I\'ve already left a review', 'contact-bank' ) . '</a></span>
									<span class="dashicons dashicons-calendar-alt contact-bank-admin-notice"></span><span class="contact-bank-admin-notice"><a href="' . $two_week_review_temp . '" class="contact-bank-admin-notice-link">' . __( 'Maybe Later', 'contact-bank' ) . '</a></span>',
					'later_link' => $two_week_review_temp,
					'int'        => 7,
				);
				$this->change_admin_notice_contact_bank( $notices );
		}

	}

		$plugin_info_contact_bank = new Contact_Bank_Admin_Notices();
}

/**
 * This Hook is used for displaying admin notice.
 */
add_action( 'init', 'contact_bank_admin_notice_class' );

/**
 * This function is used to add option on plugin activation.
 */
function plugin_activate_contact_bank() {
	add_option( 'contact_bank_do_activation_redirect', true );
}

/**
 * This function is used to redirect to manage maps menu.
 */
function contact_bank_redirect() {
	if ( get_option( 'contact_bank_do_activation_redirect', false ) ) {
			delete_option( 'contact_bank_do_activation_redirect' );
			wp_safe_redirect( admin_url( 'admin.php?page=contact_dashboard' ) );
			exit;
	}
}

/**
 * This Hook is used for redirecting to main menu after activation.
 */
register_activation_hook( __FILE__, 'plugin_activate_contact_bank' );
/**
 * Add Pop on deactivation.
 */
function add_popup_on_deactivation_contact_bank() {
	global $wpdb;
	/**
	 * This class is used to add Pop on deactivation.
	 */
	class Contact_Bank_Deactivation_Form {// @codingStandardsIgnoreLine.
		/**
		 * Public Constructor.
		 */
		function __construct() {
				add_action( 'wp_ajax_post_user_feedback_contact_bank', array( $this, 'post_user_feedback_contact_bank' ) );
				global $pagenow;
			if ( 'plugins.php' === $pagenow ) {
							add_action( 'admin_enqueue_scripts', array( $this, 'feedback_form_js_contact_bank' ) );
							add_action( 'admin_head', array( $this, 'add_form_layout_contact_bank' ) );
							add_action( 'admin_footer', array( $this, 'add_deactivation_dialog_form_contact_bank' ) );
			}
		}
		/**
		 * Add css and js files.
		 */
		function feedback_form_js_contact_bank() {
				wp_enqueue_style( 'wp-jquery-ui-dialog' );
				wp_register_script( 'contact-bank-post-feedback', plugins_url( 'assets/global/plugins/deactivation/deactivate-popup.js', __FILE__ ), array( 'jquery', 'jquery-ui-core', 'jquery-ui-dialog' ), false, true );
				wp_localize_script( 'contact-bank-post-feedback', 'post_feedback', array( 'admin_ajax' => admin_url( 'admin-ajax.php' ) ) );
				wp_enqueue_script( 'contact-bank-post-feedback' );
		}
		/**
		 * This function is used to post user feedback.
		 */
		function post_user_feedback_contact_bank() {
					$contact_bank_deactivation_reason = isset( $_POST['reason'] ) ? esc_attr( wp_unslash( $_POST['reason'] ) ) : '';// WPCS: Input var ok, CSRF ok, sanitization ok.
					$type                             = get_option( 'contact-bank-wizard-set-up' );
					$user_admin_email                 = get_option( 'contact-bank-admin-email' );
					$plugin_info_contact_bank         = new Plugin_Info_Contact_Bank();
					global $wp_version, $wpdb;
					$url           = TECH_BANKER_STATS_URL . '/wp-admin/admin-ajax.php';
					$theme_details = array();

			if ( $wp_version >= 3.4 ) {
					$active_theme                   = wp_get_theme();
					$theme_details['theme_name']    = strip_tags( $active_theme->name );
					$theme_details['theme_version'] = strip_tags( $active_theme->version );
					$theme_details['author_url']    = strip_tags( $active_theme->{'Author URI'} );
			}

					$plugin_stat_data                     = array();
					$plugin_stat_data['plugin_slug']      = 'contact-bank';
					$plugin_stat_data['reason']           = $contact_bank_deactivation_reason;
					$plugin_stat_data['type']             = 'standard_edition';
					$plugin_stat_data['version_number']   = CONTACT_BANK_WIZARD_VERSION_NUMBER;
					$plugin_stat_data['status']           = $type;
					$plugin_stat_data['event']            = 'de-activate';
					$plugin_stat_data['domain_url']       = site_url();
					$plugin_stat_data['wp_language']      = defined( 'WPLANG' ) && WPLANG ? WPLANG : get_locale();
					$plugin_stat_data['email']            = false !== $user_admin_email ? $user_admin_email : get_option( 'admin_email' );
					$plugin_stat_data['wp_version']       = $wp_version;
					$plugin_stat_data['php_version']      = esc_html( phpversion() );
					$plugin_stat_data['mysql_version']    = $wpdb->db_version();
					$plugin_stat_data['max_input_vars']   = ini_get( 'max_input_vars' );
					$plugin_stat_data['operating_system'] = PHP_OS . '  (' . PHP_INT_SIZE * 8 . ') BIT';
					$plugin_stat_data['php_memory_limit'] = ini_get( 'memory_limit' ) ? ini_get( 'memory_limit' ) : 'N/A';
					$plugin_stat_data['extensions']       = get_loaded_extensions();
					$plugin_stat_data['plugins']          = $plugin_info_contact_bank->get_plugin_info_contact_bank();
					$plugin_stat_data['themes']           = $theme_details;

					$response = wp_safe_remote_post(
						$url, array(
							'method'      => 'POST',
							'timeout'     => 45,
							'redirection' => 5,
							'httpversion' => '1.0',
							'blocking'    => true,
							'headers'     => array(),
							'body'        => array(
								'data'    => maybe_serialize( $plugin_stat_data ),
								'site_id' => false !== get_option( 'cb_tech_banker_site_id' ) ? get_option( 'cb_tech_banker_site_id' ) : '',
								'action'  => 'plugin_analysis_data',
							),
						)
					);
			if ( ! is_wp_error( $response ) ) {
					false !== $response['body'] ? update_option( 'cb_tech_banker_site_id', $response['body'] ) : '';
			}
			die( 'success' );
		}
		/**
		 * Add form layout of deactivation form.
		 */
		function add_form_layout_contact_bank() {
					?>
					<style type="text/css">
									.contact-bank-feedback-form .ui-dialog-buttonset {
											float: none !important;
									}
									#contact-bank-feedback-dialog-continue,#contact-bank-feedback-dialog-skip {
											float: right;
									}
									#contact-bank-feedback-cancel{
											float: left;
									}
									#contact-bank-feedback-content p {
											font-size: 1.1em;
									}
									.contact-bank-feedback-form .ui-icon {
											display: none;
									}
									#contact-bank-feedback-dialog-continue.contact-bank-ajax-progress .ui-icon {
											text-indent: inherit;
											display: inline-block !important;
											vertical-align: middle;
											animation: rotate 2s infinite linear;
									}
									#contact-bank-feedback-dialog-continue.contact-bank-ajax-progress .ui-button-text {
											vertical-align: middle;
									}
									@keyframes rotate {
										0%    { transform: rotate(0deg); }
										100%  { transform: rotate(360deg); }
									}
					</style>
					<?php
		}
		/**
		 * Add deactivation dialog form.
		 */
		function add_deactivation_dialog_form_contact_bank() {
			?>
			<div id="contact-bank-feedback-content" style="display: none;">
				<p style="margin-top:-5px"><?php echo esc_attr( _e( 'We feel guilty when anyone stop using Contact Bank', 'contact-bank' ) ); ?></p>
				<p><?php echo esc_attr( _e( 'If Contact Bank isn\'t working for you, others also may not', 'contact-bank' ) ); ?></p>
				<p><?php echo esc_attr( _e( 'We would love to hear your feedback about what went wrong', 'contact-bank' ) ); ?></p>
				<p><?php echo esc_attr( _e( 'We would like to help you in fixing the issue', 'contact-bank' ) ); ?></p>
				<p><?php echo esc_attr( _e( 'If you click Continue, some data would be sent to our servers for Compatiblity Testing Purposes.', 'contact-bank' ) ); ?></p>
				<p><?php echo esc_attr( _e( 'If you Skip, no data would be shared with our servers.', 'contact-bank' ) ); ?></p>
				<form>
			<?php wp_nonce_field(); ?>
				<ul id="contact-bank-deactivate-reasons">
				<li class="contact-bank-reason contact-bank-custom-input">
					<label>
						<span><input value="0" type="radio" name="reason" /></span>
						<span><?php echo esc_attr( _e( 'The Plugin didn\'t work', 'contact-bank' ) ); ?></span>
					</label>
				</li>
				<li class="contact-bank-reason contact-bank-custom-input">
					<label>
						<span><input value="1" type="radio" name="reason" /></span>
						<span><?php echo esc_attr( _e( 'I found a better Plugin', 'contact-bank' ) ); ?></span>
					</label>
				</li>
				<li class="contact-bank-reason">
					<label>
						<span><input value="2" type="radio" name="reason" checked/></span>
						<span><?php echo esc_attr( _e( 'It\'s a temporary deactivation. I\'m just debugging an issue', 'contact-bank' ) ); ?></span>
					</label>
				</li>
				<li class="contact-bank-reason contact-bank-custom-input">
					<label>
						<span><input value="3" type="radio" name="reason" /></span>
						<span><a href="https://wordpress.org/support/plugin/contact-bank" target="_blank"><?php echo esc_attr( _e( 'Open a Support Ticket for me', 'contact-bank' ) ); ?></a></span>
					</label>
				</li>
				</ul>
			</form>
		</div>
			<?php
		}
	}
		$plugin_deactivation_details = new Contact_Bank_Deactivation_Form();
}
add_action( 'plugins_loaded', 'add_popup_on_deactivation_contact_bank' );
/**
 * Insert deactivation link.
 *
 * @param array $links .
 */
function insert_deactivate_link_id_contact_bank( $links ) {
	if ( ! is_multisite() ) {
		$links['deactivate'] = str_replace( '<a', '<a id="contact-bank-plugin-disable-link"', $links['deactivate'] );
	}
		return $links;
}
add_filter( 'plugin_action_links_' . plugin_basename( __FILE__ ), 'insert_deactivate_link_id_contact_bank', 10, 2 );
