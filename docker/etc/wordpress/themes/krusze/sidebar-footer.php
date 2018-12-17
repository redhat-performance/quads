<?php
/**
 * Sidebar footer widget area.
 *
 * @link https://developer.wordpress.org/themes/functionality/sidebars/
 *
 * @package WordPress
 * @subpackage Krusze
 */
?>

<?php if ( is_active_sidebar( 'footer' ) ) : ?>

	<div id="sidebar-footer" class="sidebar sidebar-footer">
		<?php dynamic_sidebar( 'footer' ); ?>
	</div><!-- .sidebar-footer -->
	
<?php endif; ?>