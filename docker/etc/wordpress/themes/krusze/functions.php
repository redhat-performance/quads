<?php
/*
 * Krusze functions and definitions.
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package WordPress
 * @subpackage Krusze
 */

if ( ! function_exists( 'krusze_setup' ) ) :
/**
 * Krusze setup.
 */
function krusze_setup() {

	// Allows theme developers to link a custom stylesheet file to the TinyMCE visual editor.
	add_editor_style( 'css/editor-style.css' );

	// Add default posts and comments RSS feed links to head.
	add_theme_support( 'automatic-feed-links' );

	// Enable support for Custom Background.
	add_theme_support( 'custom-background', array() );
		
	// Allow the use of HTML5 markup.
	add_theme_support( 'html5', array( 'comment-list', 'comment-form', 'search-form', 'gallery', 'caption' ) );
	
	/*
	 * Enable support for Post Formats.
	 *
	 * See: https://developer.wordpress.org/themes/functionality/post-formats/
	 */
	add_theme_support( 'post-formats', array(
		'aside', 'audio', 'chat', 'gallery', 'image', 'link', 'quote', 'status', 'video'
	) );

	/*
	 * Enable support for Post Thumbnails.
	 *
	 * See: https://developer.wordpress.org/themes/functionality/featured-images-post-thumbnails/
	 */
	add_theme_support( 'post-thumbnails' );
	// set default post thumbnails: 150 pixels wide by 150 pixels tall, crop mode
	set_post_thumbnail_size( 150, 150, true );
	// declare 'krusze-large' size
	add_image_size( 'krusze-large', 780, 780, true );
	
	// Let WordPress manage the document title.
	add_theme_support( 'title-tag' );
	
	// Makes Krusze available for translation.
	load_theme_textdomain( 'krusze', get_template_directory() . '/languages' );
	
	// Add support for a navigation menu.
	register_nav_menus( array(
		'site-navigation' 	=> __( 'Navigation', 'krusze' ),
		'menu-navigation' 	=> __( 'Navigation Menu', 'krusze' )
	) );
	
	// Set the content width.
	global $content_width; 
	if ( ! isset( $content_width ) ) { 
		$content_width = 780;
	}		
}
endif; // krusze_setup
add_action( 'after_setup_theme', 'krusze_setup' );

/**
 * Enqueue scripts and styles.
 */
function krusze_enqueue_scripts_and_styles() {
	// Load main stylesheet.
	wp_enqueue_style( 'krusze-style', get_stylesheet_uri(), array( 'bootstrap' ), '0.9.7', 'all' );
	
	/**
	 * Enqueue Respond script.
	 *
	 * A fast & lightweight polyfill for min/max-width CSS3 Media Queries (for IE 6-8, and more).
	 *
	 * @link https://github.com/scottjehl/Respond
	 */
	wp_enqueue_script( 'respond', get_template_directory_uri() . '/js/respond/respond.min.js', array(), '1.4.2', false);
	
	// Support for threaded comments.
	if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
		wp_enqueue_script( 'comment-reply' );
	}
	
	wp_enqueue_script( 'krusze-script', get_template_directory_uri() . '/js/functions.js', array( 'jquery' ), '0.9.7', true );
}
add_action( 'wp_enqueue_scripts', 'krusze_enqueue_scripts_and_styles' );

if ( ! function_exists( '_wp_render_title_tag' ) ) :
/**
 * Add backwards compatibility for wp_title, prior to version 4.1.
 */
function krusze_render_title() { ?>
<title><?php wp_title( '|', true, 'right' ); ?></title>
<?php 
}
add_action( 'wp_head', 'krusze_render_title' );
endif; // krusze_render_title

/**
 * Register widget areas.
 */
function krusze_widgets_init() {
	// Sidebar
	register_sidebar( array(
		'name' 			=> __( 'Sidebar', 'krusze' ),
		'id' 			=> 'sidebar-1',
		'description' 	=> __( 'Sidebar', 'krusze' ),
		'before_widget' => '<aside id="%1$s" class="widget-container %2$s">',
		'after_widget' 	=> '</aside>',
		'before_title' 	=> '<h3 class="widget-title">',
		'after_title' 	=> '</h3>',
	) );
	
	// Header
	register_sidebar( array(
		'name' 			=> __( 'Header', 'krusze' ),
		'id' 			=> 'header',
		'description' 	=> __( 'Header', 'krusze' ),
		'before_widget' => '<aside id="%1$s" class="widget-container %2$s">',
		'after_widget' 	=> '</aside>',
		'before_title' 	=> '<h3 class="widget-title">',
		'after_title' 	=> '</h3>',
	) );
	
	// Footer
	register_sidebar( array(
		'name' 			=> __( 'Footer', 'krusze' ),
		'id' 			=> 'footer',
		'description' 	=> __( 'Footer', 'krusze' ),
		'before_widget' => '<aside id="%1$s" class="widget-container %2$s">',
		'after_widget' 	=> '</aside>',
		'before_title' 	=> '<h3 class="widget-title">',
		'after_title' 	=> '</h3>',
	) );

	// Colophon
	register_sidebar( array(
		'name' 			=> __( 'Colophon', 'krusze' ),
		'id' 			=> 'colophon',
		'description' 	=> __( 'Colophon', 'krusze' ),
		'before_widget' => '<aside id="%1$s" class="widget-container %2$s">',
		'after_widget' 	=> '</aside>',
		'before_title' 	=> '<h3 class="widget-title">',
		'after_title' 	=> '</h3>',
	) );
}
add_action( 'widgets_init', 'krusze_widgets_init' );

/**
 * Implement Bootstrap.
 */
require( get_template_directory() . '/inc/bootstrap/bootstrap.php' );

/**
 * WooCommerce ready.
 */
require( get_template_directory() . '/inc/plugins/woocommerce/woocommerce.php' );

/**
 * Implement the Custom Header feature.
 */
require( get_template_directory() . '/inc/custom-header.php' );

/**
 * Implement Customizer.
 */
require( get_template_directory() . '/inc/customizer.php' );

/**
 * Add post custom meta: post layout.
 */
require( get_template_directory() . '/inc/post-custom-meta-post-layout.php' );

/**
 * Add post custom meta: site layout.
 */
require( get_template_directory() . '/inc/post-custom-meta-site-layout.php' );

/**
 * Template tags.
 */
require( get_template_directory() . '/inc/template-tags.php' );
