<?php
/**
 * Archive Template
 * This template is used when an archive page is shown.
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package WordPress
 * @subpackage Krusze
 */
get_header(); ?>

	<?php do_action( 'krusze_container_before' ); ?>
	
	<section class="container">
		<div class="row">

			<?php do_action( 'krusze_main_before' ); ?>
			
			<main id="main" class="site-main" role="main">
			
			<?php do_action( 'krusze_main_top' ); ?>
					
			<?php if ( have_posts() ) : ?>
				
				<header class="page-header">
					<?php
						the_archive_title( '<h1 class="page-title">', '</h1>' );
						the_archive_description( '<div class="taxonomy-description">', '</div>' );
					?>
				</header><!-- .page-header -->
					
				<?php
				// Start the Loop.
				while ( have_posts() ) : the_post();

					// Include the Post Format specific template for the content.
					get_template_part( 'content', get_post_format() );

				// End the loop.
				endwhile;
			
				// Previous/Next page navigation.
				krusze_posts_pagination();
			
			// If no posts found, include the content-none.php template.
			else : 
				get_template_part( 'content', 'none' );

			endif;
		
			do_action( 'krusze_main_bottom' ); ?>
				
			</main><!-- #main -->
			
			<?php do_action( 'krusze_main_after' ); ?>
		
			<?php get_sidebar(); ?>

		</div><!-- .row -->
	</section><!-- .container -->
	
	<?php do_action( 'krusze_container_after' ); ?>

<?php get_footer(); ?>
