<?php
/**
 * Single Post Template
 * This template is used when a single post page is shown.
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/#single-post
 *
 * @package WordPress
 * @subpackage Krusze
 */

get_header(); ?>

	<?php do_action('krusze_container_before'); ?>
	
	<div class="container">
		<div class="row">

		<?php do_action('krusze_main_before'); ?>
		
		<main id="main" class="site-main" role="main">
		
		<?php do_action('krusze_main_top'); ?>
	
		<?php
		// Start the Loop.
		while ( have_posts() ) : the_post();
		
			// Include the Post Format specific template for the content.
			get_template_part('content', get_post_format());
		
			// Previous/next post navigation.
			krusze_post_navigation();

			// Load the comment template if comments are open or there is at least one comment.
			if ( comments_open() || get_comments_number() ) :
				comments_template();
			endif;
	
		// End the loop.
		endwhile;
		?>
	
		<?php do_action('krusze_main_bottom'); ?>
		
		</main><!-- #main -->
		
		<?php do_action('krusze_main_after'); ?>
		
		<?php get_sidebar(); ?>

		</div><!-- .row -->
	</div><!-- .container -->
	
	<?php do_action('krusze_container_after'); ?>

<?php get_footer(); ?>
