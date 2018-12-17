/**
 * Theme functions file.
 *
 * Provides helper functions to enhance the theme experience.
 */

// Better focus for hidden submenu items for accessibility.
( function( $ ) {
	$( '#navbar-navigation' ).find( 'a' ).on( 'focus.krusze blur.krusze', function() {
		$( this ).parents( '.menu-item, .page_item' ).toggleClass( 'focus' );
	} );
} )( jQuery );
