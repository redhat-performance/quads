<?php
/*
 * Krusze customizer functionality.
 *
 * @link https://developer.wordpress.org/themes/advanced-topics/customizer-api/
 *
 * @package WordPress
 * @subpackage Krusze
 */

/**
 * krusze_customize_register
 */
function krusze_customize_register( $wp_customize ) {
	$theme_name = wp_get_theme();
	
	/**
	 * Google Font
	 */
	$wp_customize->add_section( 'krusze_google_font', array(
		'title'			=> $theme_name . ' ' . esc_html__( 'Google Font', 'krusze' ),
		'priority'		=> 130,
		'description'   => 'Integrate the fonts into your CSS. All you need to do is add the font name to your CSS styles. For example: "font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif; If You want to add more than one font just separate them with pipe "|", for example: "Open Sans:400|Inconsolata:400,700". Default subset is "latin,latin-ext"',
	) );
	
    $wp_customize->add_setting( 'krusze_google_font_family', array(
		'default' 			=> 'Open Sans:400',
		'sanitize_callback' => 'sanitize_text_field',
    ) );
	
   $wp_customize->add_control( 'krusze_google_font_family', array(
		'label'		=> esc_html__( 'Google Font family', 'krusze' ),
        'section' => 'krusze_google_font',
        'type'    => 'text',
    ) );
	
    $wp_customize->add_setting( 'krusze_google_font_subset', array(
		'default' 			=> 'latin,latin-ext',
		'sanitize_callback' => 'sanitize_text_field',
    ) );
	
   $wp_customize->add_control( 'krusze_google_font_subset', array(
		'label'	  => esc_html__( 'Google Font subset', 'krusze' ),
        'section' => 'krusze_google_font',
        'type'    => 'text',
    ) );
	

	/**
	 * Layout
	 */
	$wp_customize->add_section( 'krusze_layout', array(
		'title'			=> $theme_name . ' ' . esc_html__( 'Layout', 'krusze' ),
		'priority'		=> 140,
	) );
	
	// Site layout
	$wp_customize->add_setting( 'krusze_site_layout', array(
		'default' 			=> 'layout-boxed',
		'sanitize_callback' => 'krusze_sanitize_site_layout',
	) );
	 
	$wp_customize->add_control(
		'krusze_site_layout',
		array(
			'type' => 'radio',
			'label' => esc_html__( 'Site layout', 'krusze' ),
			'section' => 'krusze_layout',
			'choices' => array(
				'layout-boxed' => esc_html__( 'Boxed', 'krusze' ),
				'layout-wide'  => esc_html__( 'Wide', 'krusze' ),
			),
		)
	);	
	
	// Post layout
	$wp_customize->add_setting( 'krusze_post_layout', array(
		'default' 			=> 'two-columns-right-sidebar',
		'sanitize_callback' => 'krusze_sanitize_post_layout',
	) );
	 
	$wp_customize->add_control(
		'krusze_post_layout',
		array(
			'type' => 'radio',
			'label' => esc_html__( 'Post layout', 'krusze' ),
			'section' => 'krusze_layout',
			'choices' => array(
				'one-column' => esc_html__( 'One column', 'krusze' ),
				'two-columns-right-sidebar' => esc_html__( 'Two columns, right sidebar', 'krusze' ),
				'two-columns-left-sidebar'=> esc_html__( 'Two columns, left sidebar', 'krusze' ),
			),
		)
	);
}
add_action( 'customize_register', 'krusze_customize_register' );

if ( ! function_exists( 'krusze_sanitize_post_layout' ) ) :
/**
 * Sanitize post layout.
 */
function krusze_sanitize_post_layout( $post_layout ) {
	if ( ! in_array( $post_layout, array( 'one-column', 'two-columns-right-sidebar', 'two-columns-left-sidebar' ), true ) ) {
		$post_layout = 'two-columns-right-sidebar';
	}

	return $post_layout;
}
endif; // krusze_sanitize_post_layout

if ( ! function_exists( 'krusze_sanitize_site_layout' ) ) :
/**
 * Sanitize site layout.
 */
function krusze_sanitize_site_layout( $site_layout ) {
	if ( ! in_array( $site_layout, array( 'layout-boxed', 'layout-wide' ), true ) ) {
		$site_layout = 'layout-boxed';
	}

	return $site_layout;
}
endif; // krusze_sanitize_site_layout

if ( !function_exists( 'krusze_customizer_google_fonts_url' ) ) :
/**
 * Google Font URL.
 */
function krusze_customizer_google_fonts_url() {
	$fonts_url = '';
	$fonts = get_theme_mod( 'krusze_google_font_family' );
	$subsets = get_theme_mod( 'krusze_google_font_subset' );
		
	if (! empty ( $subsets ) ) {
		$query_args = array(
			'family' => urlencode( $fonts  ),
			'subset' => urlencode( $subsets ),
		);
	} else {
		$query_args = array(
			'family' => urlencode( $fonts  ),
		);		
	}

	if ( $fonts ) {
		$fonts_url = add_query_arg( $query_args, "//fonts.googleapis.com/css" );
	}

	return $fonts_url;
}
endif; // krusze_customizer_google_fonts_url

/**
 * Enqueue Google Font style.
 */
function krusze_enqueue_style_google_font_url() {
    wp_enqueue_style( 'krusze-google-font', krusze_customizer_google_fonts_url(), array(), null );
}
add_action( 'wp_enqueue_scripts', 'krusze_enqueue_style_google_font_url' );

/**
 * Adding Google Font to the editor.
 */
function krusze_add_editor_style_customizer_google_fonts_url() {
    add_editor_style( krusze_customizer_google_fonts_url() );
}
add_action( 'after_setup_theme', 'krusze_add_editor_style_customizer_google_fonts_url' );

/**
 * Adding Google font to the Custom Header screen.
 */
function krusze_enqueue_style_google_font_custom_header() {
    wp_enqueue_style( 'krusze-google-font', krusze_customizer_google_fonts_url(), array(), null );
}
add_action( 'admin_print_styles-appearance_page_custom-header', 'krusze_enqueue_style_google_font_custom_header' );
