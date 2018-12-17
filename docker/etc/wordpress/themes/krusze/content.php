<?php
/**
 * Content Template
 * This template is used for displaying content for 
 * both single and index/archive/search pages.
 *
 * @link https://developer.wordpress.org/themes/basics/linking-theme-files-directories/
 *
 * @package WordPress
 * @subpackage Krusze
 */
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<?php
		// Custom post thumbnail.
		krusze_post_thumbnail(); 
	?>
	
	<?php krusze_entry_header(); ?>
		
	<?php if ( is_single() || is_page() ) : ?>
	<div class="entry-content">
		<?php
			the_content();
			wp_link_pages( array( 
				'before' => '<div class="page-links"><span class="page-links-prep">' . __( 'Pages:', 'krusze' ) . '</span>',
				'after' => '</div>',
				'link_before' => '<span class="page-numbers">',
				'link_after'  => '</span>'
			) );
		?>
	</div><!-- .entry-content -->
	
	<?php else : ?>
	
	<div class="entry-summary">
		<?php
			the_excerpt(); 
		?>
	</div><!-- .entry-summary -->
	
	<?php endif; ?>
	
	<?php krusze_entry_footer(); ?>
	
</article><!-- #post-## -->
