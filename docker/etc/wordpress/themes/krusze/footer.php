<?php
/**
 * Footer Template
 * The area of the page that contains the footer.
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package WordPress
 * @subpackage Krusze
 */
?>

		<?php do_action( 'krusze_content_bottom' ); ?>
		
	</div><!-- #content -->
	
	<?php do_action( 'krusze_content_after' ); ?>

	<?php do_action( 'krusze_footer_before' ); ?>
	
	<footer id="footer" class="site-footer" role="contentinfo">
		
	<?php do_action( 'krusze_footer_top' ); ?>
	
	<?php if ( is_active_sidebar( 'footer' ) ) : ?>
	
		<div class="container">
			<div class="row">
			
				<?php get_sidebar('footer'); ?>
				
			</div><!-- .row -->
		</div><!-- .container -->
	
	<?php endif; ?>
	
	<?php if ( is_active_sidebar( 'colophon' ) ) : ?>
	
		<div id="colophon" class="colophon">
		
			<div class="container">
				<div class="row">
				
					<div id="sidebar-colophon" class="sidebar sidebar-colophon">
						<?php dynamic_sidebar( 'colophon' ); ?>
					</div><!-- #sidebar-colophon -->
					
				</div><!-- .row -->
			</div><!-- .container -->
			
		</div><!-- #colophon -->
	
	<?php else: ?>
	
	<div id="colophon" class="colophon">
	
		<div class="container">
			<div class="row">
			
				<div id="sidebar-colophon" class="sidebar sidebar-colophon">
					<aside id="text-colophon" class="widget-container widget_text">		
						<div class="textwidget">
							<p>&copy; <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="site-info" title="<?php echo esc_attr( get_bloginfo( 'name', 'display' ) ); ?>"><?php bloginfo( 'name' ); ?></a>. <a href="<?php echo esc_url( __( 'https://wordpress.org/', 'krusze' ) ); ?>" class="site-generator" title="<?php esc_attr_e( 'Powered by WordPress', 'krusze' ); ?>"><?php esc_attr_e( 'Powered by WordPress', 'krusze' ); ?></a> &amp; <a href="<?php echo esc_url( 'http://demo.krusze.com/krusze/' ); ?>" class="site-webdesign" title="Krusze Theme">Krusze Theme</a>.</p>	
						</div>
					</aside>
				</div><!-- #sidebar-colophon -->
				
			</div><!-- .row -->
		</div><!-- .container -->
		
	</div><!-- #colophon -->
	<?php endif; ?>

	<?php do_action( 'krusze_footer_bottom' ); ?>
		
	</footer><!-- #footer -->
	
	<?php do_action( 'krusze_footer_after' ); ?>

</div><!-- #wrapper -->

<?php wp_footer(); ?>

</body>
</html>
