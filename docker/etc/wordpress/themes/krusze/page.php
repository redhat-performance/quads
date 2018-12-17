<?php
/**
 * All Pages Template
 * This template is used when a page is shown.
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/#page
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
		
			<?php while ( have_posts() ) : the_post(); ?>
			
				<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
				
					<header class="entry-header">
						<?php krusze_title(); ?>
					</header><!-- .entry-header -->
					
					<div class="entry-content">
					<?php 
						the_content();
						wp_link_pages( array( 'before' => '<div class="page-links"><span class="page-links-prep">' . __( 'Pages:', 'krusze' ) . '</span>', 'after' => '</div>', 'link_before' => '<span class="page-numbers">', 'link_after'  => '</span>' ) );
					?>
					</div><!-- .entry-content -->
					
					<?php edit_post_link( __( 'Edit', 'krusze' ) . ' <span class="screen-reader-text sr-only">' . get_the_title() . '</span>', '<footer class="entry-footer"><span class="edit-link">', '</span></footer><!-- .entry-footer -->' ); ?>

				</article><!-- #post-## -->
				
				<?php
					// Load the comment template if comments are open or there is at least one comment.
					if ( comments_open() || get_comments_number() ) :
						comments_template();
					endif;
				?>
			
			<?php endwhile; ?>
		
			<?php do_action('krusze_main_bottom'); ?>
			
		</main><!-- #main -->
		
		<?php do_action('krusze_main_after'); ?>
		
		<?php get_sidebar(); ?>

		</div><!-- .row -->
	</div><!-- .container -->
	
	<?php do_action('krusze_container_after'); ?>
	
<?php get_footer(); ?>
