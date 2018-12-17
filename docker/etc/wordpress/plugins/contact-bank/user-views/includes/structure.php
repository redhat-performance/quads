<?php
/**
 * This file is used for includes all files.
 *
 * @author Tech Banker
 * @package contact-bank/user-views/includes
 * @version 3.1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
wp_enqueue_script( 'jquery-ui-datepicker' );
wp_enqueue_script( 'contact-bank-jquery.validate.js', plugins_url( 'assets/global/plugins/validation/jquery.validate.js', dirname( dirname( __FILE__ ) ) ) );
wp_enqueue_script( 'contact-bank-colpick.js', plugins_url( 'assets/global/plugins/colorpicker/colpick.js', dirname( dirname( __FILE__ ) ) ) );
wp_enqueue_script( 'contact-bank-toastr.js', plugins_url( 'assets/global/plugins/toastr/toastr.js', dirname( dirname( __FILE__ ) ) ) );
wp_enqueue_script( 'contact-bank-input-masking.min.js', plugins_url( 'assets/global/plugins/input-masking/masking-input.js', dirname( dirname( __FILE__ ) ) ), null, null, true );
wp_enqueue_style( 'contact-bank-simple-line-icons.css', plugins_url( 'assets/global/plugins/icons/icons.css', dirname( dirname( __FILE__ ) ) ) );
wp_enqueue_style( 'contact-bank-components.css', plugins_url( 'assets/global/css/components.css', dirname( dirname( __FILE__ ) ) ) );
if ( is_rtl() ) {
		wp_enqueue_style( 'contact-bank-bootstrap.css', plugins_url( 'assets/global/plugins/custom/css/custom-rtl.css', dirname( dirname( __FILE__ ) ) ) );
		wp_enqueue_style( 'contact-bank-layout.css', plugins_url( 'assets/admin/layout/css/layout-rtl.css', dirname( dirname( __FILE__ ) ) ) );
		wp_enqueue_style( 'contact-bank-custom.css', plugins_url( 'assets/admin/layout/css/tech-banker-custom-rtl.css', dirname( dirname( __FILE__ ) ) ) );
} else {
		wp_enqueue_style( 'contact-bank-bootstrap.css', plugins_url( 'assets/global/plugins/custom/css/custom.css', dirname( dirname( __FILE__ ) ) ) );
		wp_enqueue_style( 'contact-bank-layout.css', plugins_url( 'assets/admin/layout/css/layout.css', dirname( dirname( __FILE__ ) ) ) );
		wp_enqueue_style( 'contact-bank-custom.css', plugins_url( 'assets/admin/layout/css/tech-banker-custom.css', dirname( dirname( __FILE__ ) ) ) );
}
wp_enqueue_style( 'contact-bank.css', plugins_url( 'assets/admin/layout/css/contact-bank.css', dirname( dirname( __FILE__ ) ) ) );
wp_enqueue_style( 'contact-bank-default.css', plugins_url( 'assets/admin/layout/css/themes/default.css', dirname( dirname( __FILE__ ) ) ) );
wp_enqueue_style( 'contact-bank-toastr.min.css', plugins_url( 'assets/global/plugins/toastr/toastr.css', dirname( dirname( __FILE__ ) ) ) );
wp_enqueue_style( 'contact-bank-jquery-ui.css', plugins_url( 'assets/global/plugins/datepicker/jquery-ui.css', dirname( dirname( __FILE__ ) ) ), false, '2.0', false );
wp_enqueue_style( 'contact-bank-colpick.css', plugins_url( 'assets/global/plugins/colorpicker/colpick.css', dirname( dirname( __FILE__ ) ) ) );
// Exit if accessed directly.
global $wpdb;
$random = rand( 100, 10000 );
if ( file_exists( CONTACT_BANK_USER_VIEWS_PATH . 'includes/queries.php' ) ) {
	include CONTACT_BANK_USER_VIEWS_PATH . 'includes/queries.php';
}

if ( file_exists( CONTACT_BANK_USER_VIEWS_PATH . 'includes/style-sheet.php' ) ) {
	include CONTACT_BANK_USER_VIEWS_PATH . 'includes/style-sheet.php';
}

if ( file_exists( CONTACT_BANK_USER_VIEWS_PATH . 'layouts/form.php' ) ) {
	include CONTACT_BANK_USER_VIEWS_PATH . 'layouts/form.php';
}

if ( file_exists( CONTACT_BANK_USER_VIEWS_PATH . 'includes/footer.php' ) ) {
	include CONTACT_BANK_USER_VIEWS_PATH . 'includes/footer.php';
}
