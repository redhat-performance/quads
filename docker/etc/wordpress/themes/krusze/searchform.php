<?php
/**
 * Template for displaying search forms.
 *
 * @link https://codex.wordpress.org/Function_Reference/get_search_form
 *
 * @package WordPress
 * @subpackage Krusze
 */
?>

<form role="search" method="get" class="search-form" action="<?php esc_url( home_url( '/' ) ); ?>">
	<label>
		<span class="screen-reader-text sr-only"><?php echo _x( 'Search for:', 'label', 'krusze' ); ?></span>
		<input type="search" class="search-field" placeholder="<?php echo esc_attr_x( 'Search &hellip;', 'placeholder', 'krusze' ); ?>" value="<?php echo get_search_query(); ?>" name="s" title="<?php echo esc_attr_x( 'Search for:', 'label', 'krusze' ); ?>" />
	</label>
	<input type="submit" class="search-submit" value="<?php echo esc_attr_x( 'Search', 'submit button', 'krusze' ); ?>" />
</form>