<?php
/**
 * Index Page Template
 * This template is used to display a page when nothing more specific matches a query.
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
			
				<?php if ( is_home() && ! is_front_page() ) : ?>
					<header class="page-header">
						<h1 class="page-title screen-reader-text sr-only"><?php single_post_title(); ?></h1>
					</header><!-- .page-header -->
				<?php endif; ?>
				
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
	
<?php do_action( 'krusze_container_after' );

get_footer(); ?>
