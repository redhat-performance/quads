<?php
/**
 * Adds site layout options on posts and pages.
 *
 * @package WordPress
 * @subpackage Krusze
 */
 
// Exit if accessed directly
if ( ! defined( 'ABSPATH' ) ) exit;

/**
 * Adds a box to the side column on the Page and Post edit screens.
 */
function krusze_site_layout_add_meta_box() {
	$post_types = array( 'page', 'post' );
	
	foreach ( $post_types as $post_type ) {
		add_meta_box( 
			'krusze_site_layout', 
			__( 'Site layout', 'krusze' ), 
			'krusze_site_layout_callback', 
			$post_type, 
			'side', 
			'default' 
		);
    }
}
add_action( 'add_meta_boxes', 'krusze_site_layout_add_meta_box' );

/**
 * Prints the box content.
 */
function krusze_site_layout_callback() {
	// Add a nonce field so we can check for it later.
	wp_nonce_field( 'krusze_site_layout', 'krusze_site_layout_nonce' );
	
	global $post;
	$custom        = ( get_post_custom( $post->ID ) ? get_post_custom( $post->ID ) : false );
	$site_layout        = ( isset( $custom['_krusze_site_layout'][0] ) ? $custom['_krusze_site_layout'][0] : 'default' );
	$valid_site_layouts = krusze_valid_site_layouts();
	?>
	<p>
		<label><input type="radio" name="_krusze_site_layout" <?php checked( 'default' == $site_layout ); ?> value="default" />
		<?php esc_html_e( 'Default', 'krusze' ); ?></label><br />
		<?php foreach( $valid_site_layouts as $slug => $name ) { ?>
			<label><input type="radio" name="_krusze_site_layout" <?php checked( $slug == $site_layout ); ?> value="<?php echo esc_attr( $slug ); ?>" />
			<?php echo esc_html( $name ); ?></label><br />
		<?php } ?>
	</p>
<?php
}

/**
 * When the post is saved, saves our custom data.
 */
function krusze_site_layout_save_meta_box_data() {
	// If this is an autosave, our form has not been submitted, so we don't want to do anything.
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}

	// Verify that the nonce is valid.
	if ( ! isset( $_POST['krusze_site_layout_nonce'] ) && ! wp_verify_nonce( $_POST['krusze_site_layout_nonce'] ) ) {
		return;
	}

	// Check the user's permissions.
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}
	
	global $post;
	if( !isset( $post ) || !is_object( $post ) ) {
		return;
	}
	$valid_site_layouts = krusze_valid_site_layouts();
	$site_layout        = ( isset( $_POST['_krusze_site_layout'] ) && array_key_exists( $_POST['_krusze_site_layout'], $valid_site_layouts ) ? $_POST['_krusze_site_layout'] : 'default' );

	update_post_meta( $post->ID, '_krusze_site_layout', $site_layout );
}

// Hook the save site layout post custom meta data into
// publish_{post-type}, draft_{post-type}, and future_{post-type}
add_action( 'publish_post', 'krusze_site_layout_save_meta_box_data' );
add_action( 'publish_page', 'krusze_site_layout_save_meta_box_data' );
add_action( 'draft_post', 'krusze_site_layout_save_meta_box_data' );
add_action( 'draft_page', 'krusze_site_layout_save_meta_box_data' );
add_action( 'future_post', 'krusze_site_layout_save_meta_box_data' );
add_action( 'future_page', 'krusze_site_layout_save_meta_box_data' );


/**
 * Get valid site layouts.
 */
function krusze_valid_site_layouts() {
	$site_layouts = array(
		'layout-boxed' => __( 'Boxed', 'krusze' ),
		'layout-wide' 	=> __( 'Wide', 'krusze' )
	);

	return apply_filters( 'krusze_valid_site_layouts', $site_layouts );
}

/**
 * Get current site layout.
 */
function krusze_get_site_layout() {
	// 404 pages
	if( is_404() ) {
		return 'default';
	}
	$site_layout = '';
	
	$valid_site_layouts = krusze_valid_site_layouts();

	global $post;
	$site_layout_meta_value = ( false != get_post_meta( get_the_ID(), '_krusze_site_layout', true ) ? get_post_meta( get_the_ID(), '_krusze_site_layout', true ) : 'default' );
	$site_layout_meta       = ( array_key_exists( $site_layout_meta_value, $valid_site_layouts ) ? $site_layout_meta_value : 'default' );	
	
	if( 'default' != $site_layout_meta ) {
		$site_layout = $site_layout_meta;
	} else {
		$site_layout = 'default';	
	}

	return apply_filters( 'krusze_get_site_layout', $site_layout );
}

/**
 * Get content classes.
 */
function krusze_site_layout_content_classes() {
	$content_classes = array();
	$site_layout          = krusze_get_site_layout();
	
	if( 'default' == $site_layout ) {
		$content_classes[] = get_theme_mod( 'krusze_site_layout', 'layout-boxed' );
	}
	else {
		if( 'layout-wide' == $site_layout ) {
			$content_classes[] = 'layout-wide';
		}
		else {
			if( 'layout-boxed' == $site_layout ) {
				$content_classes[] = 'layout-boxed';
			}
		}
	}

	return apply_filters( 'krusze_site_layout_content_classes', $content_classes );
}

/**
 * krusze_site_layout_body_class
 */
function krusze_site_layout_body_class( $classes ) {
	
	// add 'class-name' to the $classes array
	$content_class =  implode( ' ', krusze_site_layout_content_classes() );
	$classes[] = $content_class;
	
	// return the $classes array
	return $classes;
}
add_filter( 'body_class', 'krusze_site_layout_body_class', 10 );
