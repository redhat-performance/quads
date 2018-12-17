<?php
/**
 * 404 Template
 * This template is used when a 404 page is shown.
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/#404-not-found
 *
 * @package WordPress
 * @subpackage Krusze
 */
get_header(); ?>

	<?php do_action( 'krusze_container_before' ); ?>

	<div class="container">
		<div class="row">

			<?php do_action( 'krusze_main_before' ); ?>
			
			<main id="main" class="site-main" role="main">
			
			<?php do_action( 'krusze_main_top' ); ?>
				
				<section class="error-404 not-found">
					<header class="page-header">
						<h1 class="page-title"><?php _e( 'Page not found.', 'krusze' ); ?></h1>
					</header><!-- .page-header -->
					
					<div class="page-content">
						<p><?php _e( 'Sorry, no posts matched your criteria.', 'krusze' ); ?></p>
					</div><!-- .page-content -->
				</section><!-- .error-404 -->
			
			<?php do_action( 'krusze_main_bottom' ); ?>
				
			</main><!-- #main -->
			
			<?php do_action( 'krusze_main_after' ); ?>
		
		</div><!-- .row -->
	</div><!-- .container -->
	
	<?php do_action( 'krusze_container_after' ); ?>

<?php get_footer(); ?>
