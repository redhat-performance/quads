<?php
/**
 * WooCommerce compatibility.
 *
 * @package WordPress
 * @subpackage Krusze
 */

remove_action( 'woocommerce_before_main_content', 'woocommerce_output_content_wrapper', 10);
/**
 * krusze_woocommerce_output_content_wrapper
 */
function krusze_woocommerce_output_content_wrapper() { ?>
	<div class="container">
		<div class="row">
			<main id="main" class="site-main" role="main">
<?php }
add_action('woocommerce_before_main_content', 'krusze_woocommerce_output_content_wrapper', 10);

remove_action( 'woocommerce_after_main_content', 'woocommerce_output_content_wrapper_end', 10);
/**
 * krusze_woocommerce_output_content_wrapper_end
 */
function krusze_woocommerce_output_content_wrapper_end() { ?>
	</main><!-- #main -->
<?php }
add_action('woocommerce_after_main_content', 'krusze_woocommerce_output_content_wrapper_end', 10);

/**
 * krusze_woocommerce_container_start
 */
function krusze_woocommerce_container_start() { ?>
		</div><!-- .row -->
	</div><!-- .container -->
<?php }
add_action( 'woocommerce_sidebar', 'krusze_woocommerce_container_start', 20 );

if( !function_exists( 'krusze_woocommerce_setup' ) ) :
/**
 * WooCommerce setup.
 */
function krusze_woocommerce_setup() {
	/**
	 * Add theme support: WooCommerce
	 * @link http://docs.woothemes.com/document/third-party-custom-theme-compatibility/
	 */
	add_theme_support( 'woocommerce' );
}
endif; // krusze_woocommerce_setup
add_action( 'after_setup_theme', 'krusze_woocommerce_setup' );
