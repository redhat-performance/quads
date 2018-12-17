<?php
/**
 * Sidebar widget area.
 *
 * @link https://developer.wordpress.org/themes/functionality/sidebars/
 *
 * @package WordPress
 * @subpackage Krusze
 */
?>

<?php do_action('krusze_sidebars_before'); ?>

<?php if ( is_active_sidebar( 'sidebar-1' ) && krusze_post_layout() != 'one-column' ) : ?>

	<div id="sidebar-primary" class="sidebar sidebar-primary" role="complementary">
		
		<?php do_action('krusze_sidebar_top'); ?>
		
		<?php dynamic_sidebar( 'sidebar-1' ); ?>
		
		<?php do_action('krusze_sidebar_bottom'); ?>
		
	</div><!-- #sidebar-primary -->
	
<?php endif; ?>
		
<?php do_action('krusze_sidebars_after'); ?>
