<?php
/**
 * Custom template tags for Krusze.
 *
 * @package WordPress
 * @subpackage Krusze
 */

if ( ! function_exists( 'krusze_comment_nav' ) ) :
/**
 * Display navigation to next/previous comments.
 */
function krusze_comment_nav() {
	// Are there comments to navigate through?
	if ( get_comment_pages_count() > 1 && get_option( 'page_comments' ) ) :
	?>
	<div class="navigation comment-navigation" role="navigation">
		<h2 class="screen-reader-text sr-only"><?php _e( 'Comment navigation', 'krusze' ); ?></h2>
		<div class="nav-links">
			<div class="nav-previous"><?php previous_comments_link( __( 'Older Comments', 'krusze' ) ); ?></div>
			<div class="nav-next"><?php next_comments_link( __( 'Newer Comments', 'krusze' ) ); ?></div>
		</div><!-- .nav-links -->
	</div><!-- .comment-navigation -->
	<?php
	endif;
}
endif; // krusze_comment_nav

if ( ! function_exists( 'krusze_excerpt_more' ) && ! is_admin() ) :
/**
 * Replace "[...]" with 'Continue reading' prepended with an ellipsis.
 */
function krusze_excerpt_more( $more ) {
	$link = sprintf( '<a href="%1$s" class="read-more">%2$s %3$s</a>',
		esc_url( get_permalink( get_the_ID() ) ),
		__( 'Continue reading', 'krusze' ),
		'<span class="screen-reader-text sr-only">' . get_the_title( get_the_ID() ) . '</span>'
		);
	return ' &hellip; ' . $link;
}
add_filter( 'excerpt_more', 'krusze_excerpt_more' );
endif; // krusze_excerpt_more

if ( ! function_exists( 'krusze_get_header_class' ) ) :
/**
 * Retrieve the classes for the header element as an array.
 *
 * @param string|array $class One or more classes to add to the class list.
 * @return array Array of classes.
 */
function krusze_get_header_class( $class = '' ) {
	$classes = array();

	$classes[] = 'site-header';
	$classes[] = 'navbar';
	$classes[] = 'navbar-static-top';

	if ( ! empty( $class ) ) {
		if ( !is_array( $class ) )
			$class = preg_split( '#\s+#', $class );
		$classes = array_merge( $classes, $class );
	} else {
		// Ensure that we always coerce class to being an array.
		$class = array();
	}

	$classes = array_map( 'esc_attr', $classes );

	/**
	 * Filter the list of CSS header classes.
	 *
	 * @param array  $classes An array of header classes.
	 * @param string $class   A comma-separated list of additional classes added to the header.
	 */
	$classes = apply_filters( 'krusze_header_class', $classes, $class );

	return array_unique( $classes );
}
endif; // krusze_get_header_class

if ( ! function_exists( 'krusze_get_link_url' ) ) :
/**
 * Return the post URL if no link URL is found in the post.
 */
function krusze_get_link_url() {
	$has_url = get_url_in_content( get_the_content() );

	return $has_url ? $has_url : apply_filters( 'the_permalink', get_permalink() );
}
endif; // krusze_get_link_url

if ( ! function_exists( 'krusze_header_class' ) ) :
/**
 * Display the classes for the header element.
 *
 * @param string|array $class One or more classes to add to the class list.
 */
function krusze_header_class( $class = '' ) {
	// Separates classes with a single space, collates classes for header element
	echo 'class="' . join( ' ', krusze_get_header_class( $class ) ) . '"';
}
endif; // krusze_header_class

if ( ! function_exists( 'krusze_entry_footer' ) ) :
/**
 * Prints HTML with entry footer.
 */
function krusze_entry_footer() {
	if ( is_single() ) { ?>
	
	<footer class="entry-footer">
	
	<?php
	// entry attachment dimensions
	krusze_entry_attachment_dimensions();

	// entry format
	krusze_entry_format();
	
	// entry categories
	krusze_entry_categories();

	// entry tags
	krusze_entry_tags();
	
	// edit_post_link
	edit_post_link( __( 'Edit', 'krusze' ) . ' <span class="screen-reader-text sr-only">' . get_the_title() . '</span>', '<span class="edit-link">', '</span>' );	

	// krusze entry author info
	krusze_entry_author_info();
	?>
	
	</footer><!-- .entry-footer -->
	
	<?php
	} // is_single
}
endif; // krusze_entry_footer

if ( ! function_exists( 'krusze_entry_header' ) ) :
/**
 * Prints HTML with entry header.
 */
function krusze_entry_header() { ?>
	
	<header class="entry-header">
	
	<?php
	// entry title
	krusze_title();
	
	// entry date
	krusze_entry_date();

	// entry author
	krusze_entry_author();
	
	// entry comments
	krusze_entry_comments();
	?>
	
	</header><!-- .entry-header -->
	
	<?php

}
endif; // krusze_entry_header

if ( ! function_exists( 'krusze_entry_attachment_dimensions' ) ) :
/**
 * Prints HTML with attachment dimensions.
 */
function krusze_entry_attachment_dimensions() {
	if ( is_attachment() && wp_attachment_is_image() ) {
		$metadata = wp_get_attachment_metadata();
		
		printf( '<span class="meta-dimensions"><span class="meta-dimensions-prep">%1$s </span><a href="%2$s" title="%3$s">%4$s &times; %5$s</a></span>',
			__( 'Original dimensions', 'krusze' ),
			esc_url( wp_get_attachment_url() ),
			esc_attr( __( 'Link to image', 'krusze' ) ),
			$metadata['width'],
			$metadata['height']
		);
	}
}
endif; // krusze_entry_attachment_dimensions

if ( ! function_exists( 'krusze_entry_author' ) ) :
/**
 * Prints HTML with entry footer.
 */
function krusze_entry_author() {
	if ( is_single() ) {
		printf( '<span class="meta-author"><span class="author vcard"><span class="meta-author-prep">%1$s </span><a href="%2$s" class="url fn n" title="%3$s">%4$s</a></span></span>',
			__( 'Author', 'krusze' ),
			esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ),
			sprintf( esc_attr__( 'View all posts by %s', 'krusze' ), get_the_author() ),
			get_the_author()
		);
	}
}
endif; // krusze_entry_author

if ( ! function_exists( 'krusze_entry_author_info' ) ) :
/**
 * Prints HTML with entry author info.
 */
function krusze_entry_author_info() {
	if ( is_single() && get_the_author_meta( 'description' ) ) { ?>
	
	<div class="author-info">
		<div class="author-avatar">
			<?php
			$author_bio_avatar_size = apply_filters( 'krusze_author_bio_avatar_size', 64 );
			echo get_avatar( get_the_author_meta( 'user_email' ), $author_bio_avatar_size );
			?>
		</div><!-- .author-avatar -->
		<div class="author-description">
			<h3 class="author-title"><?php the_author(); ?></h3>
			<p class="author-bio">
				<?php the_author_meta( 'description' ); ?>
				<a href="<?php echo esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ); ?>" class="author-link" rel="author">
					<?php printf( __( 'View all posts by %s', 'krusze' ), get_the_author() ); ?>
				</a>
			</p>
		</div><!-- .author-description -->
	</div><!-- .meta-author-info -->
	
	<?php 
	}
}
endif; // krusze_entry_author_info

if ( ! function_exists( 'krusze_entry_categories' ) ) :
/**
 * Prints HTML with entry categories.
 */
function krusze_entry_categories() {
	$categories_list = get_the_category_list( ', ' );
	if ( $categories_list ) {
		printf( '<span class="meta-categories"><span class="meta-categories-prep">%1$s </span>%2$s</span>',
			__( 'Categories', 'krusze' ),
			$categories_list
		);
	}
}
endif; // krusze_entry_categories

if ( ! function_exists( 'krusze_entry_comments' ) ) :
/**
 * Prints HTML with entry footer.
 */
function krusze_entry_comments() {
	if ( is_single() ) {
		if ( comments_open() && ! post_password_required() && ( comments_open() || get_comments_number() ) ) :
			echo '<span class="meta-comments">';
				comments_popup_link( __( 'Leave a comment', 'krusze' ), __( '1 Comment', 'krusze' ), __( '% Comments', 'krusze' ), 'meta-comments-link' );
			echo '</span>';
		endif;
	}
}
endif; // krusze_entry_comments

if ( ! function_exists( 'krusze_entry_date' ) ) :
/**
 * Prints HTML with entry date.
 */
function krusze_entry_date() {
	if ( is_single() ) { 
		printf('<span class="meta-date"><span class="meta-date-prep">' . __( 'Published on', 'krusze' ) . '</span> %1$s',
			sprintf( '<time datetime="%1$s">%2$s</time></span> ',
				esc_attr( get_the_date( 'c' ) ),
				get_the_date()
			)
		);
	} else {
		printf('<span class="meta-date"><span class="meta-date-prep">' . __( 'Published on', 'krusze' ) . '</span> %1$s',
			sprintf( '<a href="%1$s" rel="bookmark"><time datetime="%2$s">%3$s</time></a></span> ',
				get_permalink(),
				esc_attr( get_the_date( 'c' ) ),
				get_the_date()
			)
		);
	}
}
endif; // krusze_entry_date

if ( ! function_exists( 'krusze_entry_format' ) ) :
/**
 * Prints HTML with entry format.
 */
function krusze_entry_format() {
	$format = get_post_format();
	if ( current_theme_supports( 'post-formats', $format ) ) {
		printf( '<span class="meta-format">%1$s<a href="%2$s">%3$s</a></span>',
			sprintf( '<span class="meta-format-prep">%s </span>', __( 'Format', 'krusze' ) ),
			esc_url( get_post_format_link( $format ) ),
			get_post_format_string( $format )
		);
	}
}
endif; // krusze_entry_format

if ( ! function_exists( 'krusze_entry_tags' ) ) :
/**
 * Prints HTML with entry tags.
 */
function krusze_entry_tags() {
	$tags_list = get_the_tag_list( '', ', ' );
	if ( $tags_list ) {
		printf( '<span class="meta-tags"><span class="meta-tags-prep">%1$s </span>%2$s</span>',
			__( 'Tags', 'krusze' ),
			$tags_list
		);
	}
}
endif; // krusze_entry_tags

if ( ! function_exists( 'krusze_post_navigation' ) ) :
/**
 * Custom previous/next post navigation.
 */
function krusze_post_navigation() {
	if ( is_attachment() && wp_attachment_is_image() ) : ?>

		<nav class="navigation image-navigation" role="navigation">
			<h2 class="screen-reader-text sr-only"><?php _e( 'Navigation', 'krusze' ); ?></h2>
			<div class="nav-links">
				<div class="nav-previous"><?php previous_image_link( false, __( 'Previous', 'krusze' ) ); ?></div>
				<div class="nav-next"><?php next_image_link( false, __( 'Next', 'krusze' ) ); ?></div>
			</div><!-- .nav-links -->
		</nav><!-- .image-navigation -->
	
	<?php
	elseif ( is_attachment() ) :
	
		the_post_navigation( array(
				'prev_text' => '<span class="meta-nav">' . __( 'Published in', 'krusze' ) . '</span> <span class="post-title">%title</span>',
		) );
		
	elseif ( is_single() ) :
	
		the_post_navigation( array(
			'next_text' => '<span class="meta-nav" aria-hidden="true">' . __( 'Next', 'krusze' ) . '</span> ' .
				'<span class="screen-reader-text sr-only">' . __( 'Next post:', 'krusze' ) . '</span> ' .
				'<span class="post-title">%title</span>',
			'prev_text' => '<span class="meta-nav" aria-hidden="true">' . __( 'Previous', 'krusze' ) . '</span> ' .
				'<span class="screen-reader-text sr-only">' . __( 'Previous post:', 'krusze' ) . '</span> ' .
				'<span class="post-title">%title</span>',
		) ); 
			
	endif;
}
endif; // krusze_post_navigation

if ( ! function_exists( 'krusze_post_thumbnail' ) ) :
/**
 * Custom post thumbnail.
 */
function krusze_post_thumbnail() {
	if ( ! has_post_thumbnail() || is_attachment() || post_password_required() ) {
		return;
	}

	if ( is_singular() ) :
	?>

	<div class="post-thumbnail">
		<?php the_post_thumbnail( 'krusze-large' ); ?>
	</div><!-- .post-thumbnail -->

	<?php else : ?>

	<a href="<?php the_permalink(); ?>" class="post-thumbnail" title="<?php the_title_attribute(); ?>" rel="bookmark" aria-hidden="true">
		<?php
			the_post_thumbnail( 'krusze-large', array( 'alt' => get_the_title() ) );
		?>
	</a>

	<?php 
	endif;
}
endif; // krusze_post_thumbnail

if ( ! function_exists( 'krusze_posts_pagination' ) ) :
/**
 * Custom output of links to the previous and next pages of posts.
 */
function krusze_posts_pagination() {
	
	if ( function_exists('wp_pagenavi') ) { 
		wp_pagenavi(); 
		
	} else { 
		// pagination arguments
		// @link https://developer.wordpress.org/themes/functionality/pagination/#numerical-pagination
		the_posts_pagination( array(
			'prev_text'          => __( 'Previous', 'krusze' ),
			'next_text'          => __( 'Next', 'krusze' ),
			'before_page_number' => '<span class="meta-nav screen-reader-text sr-only">' . __( 'Page', 'krusze' ) . ' </span>',
		) );
	}
		
}
endif; // krusze_posts_pagination

if ( ! function_exists( 'krusze_title' ) ) :
/**
 * Custom post title.
 */
function krusze_title() {
	$format = get_post_format();
	
	if ( is_single() || is_page() ) {
		the_title( '<h1 class="entry-title">', '</h1>' );
		
	} elseif ( current_theme_supports( 'post-formats', $format ) && $format === 'link' ) {
		the_title( sprintf( '<h2 class="entry-title"><a href="%s">', esc_url( krusze_get_link_url() ) ), '</a></h2>' );
	
	} else {
		the_title( sprintf( '<h2 class="entry-title"><a href="%s" rel="bookmark">', esc_url( get_permalink() ) ), '</a></h2>' );
	}
		
}
endif; // krusze_title
