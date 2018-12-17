<?php
/**
 * Header Template
 * The area of the page that contains the header.
 *
 * @link https://codex.wordpress.org/Designing_Headers
 *
 * @package WordPress
 * @subpackage Krusze
 */
?><!DOCTYPE html>
<?php do_action( 'krusze_html_before' ); ?>
<html <?php language_attributes(); ?>>
<head>
	<?php do_action('krusze_head_top'); ?>

	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="profile" href="http://gmpg.org/xfn/11">
	<link rel="pingback" href="<?php bloginfo( 'pingback_url' ); ?>">
	<!--[if lt IE 9]>
	<script src="<?php echo esc_url( get_template_directory_uri() ); ?>/js/html5shiv/html5shiv.min.js?ver=3.7.3" type="text/javascript"></script>
	<![endif]-->
	<!-- Krusze v0.9.7 - http://wordpress.org/themes/krusze -->

	<?php do_action('krusze_head_bottom'); ?>
	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>

<div id="wrapper">
	<a class="skip-link screen-reader-text sr-only" href="#content" title="<?php esc_attr_e( 'Skip to content', 'krusze' ); ?>"><?php _e( 'Skip to content', 'krusze' ); ?></a>
		
	<?php do_action( 'krusze_header_before' ); ?>
	
	<header id="header" <?php krusze_header_class(); ?> role="banner">
	
		<?php do_action( 'krusze_header_top' ); ?>
	
		<div class="container">
			<div class="row">
			
				<div class="site-brand">
				
				<?php if ( is_home() || is_front_page() ) { ?>
					<h1 class="site-title">
				<?php } else { ?>
					<p class="site-title">
				<?php } ?>
						<a href="<?php echo esc_url( home_url( '/' ) ); ?>" title="<?php echo esc_attr( get_bloginfo( 'name', 'display' ) ); ?>">
							<?php bloginfo( 'name' ); ?>
						</a>
				<?php if ( is_home() || is_front_page() ) { ?>
					</h1>
				<?php } else { ?>
					</p>
				<?php }
				
				$description = get_bloginfo( 'description', 'display' );
				if ( $description || is_customize_preview() ) : ?>
					<p class="site-description"><?php echo $description; ?></p>
				<?php endif; ?>
					
				</div><!-- .site-brand -->
		
				<?php if ( is_active_sidebar( 'header' ) ) : ?>
				
					<div class="sidebar sidebar-header" role="complementary">
						<?php dynamic_sidebar( 'header' ); ?>
					</div>
					
					<?php if ( has_nav_menu( 'menu-navigation' ) ) : ?>
					<input type="checkbox" id="navbar-navigation-toggle" />
					<label for="navbar-navigation-toggle" class="navigation-toggle">
						<span class="screen-reader-text sr-only"><?php _e( 'Navigation', 'krusze' ); ?></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</label>	
					<nav id="navbar-navigation" class="navigation navbar-navigation navbar-collapse" role="navigation">
						<?php wp_nav_menu( array( 'theme_location' => 'menu-navigation', 'container' => false, 'menu_class' => 'menu menu-navigation nav navbar-nav navbar-left', 'fallback_cb' => false ) ); ?>
					</nav>
					<?php endif; // end has_nav_menu( 'menu-navigation' ) ?>
					
				<?php else : 
				
					if ( has_nav_menu( 'site-navigation' ) || has_nav_menu( 'menu-navigation' ) ) : ?>
					<input type="checkbox" id="navbar-navigation-toggle" />
					<label for="navbar-navigation-toggle" class="navigation-toggle">
						<span class="screen-reader-text sr-only"><?php _e( 'Navigation', 'krusze' ); ?></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</label>	
					<nav id="navbar-navigation" class="navigation navbar-navigation navbar-collapse" role="navigation">
						<?php wp_nav_menu( array( 'theme_location' => 'site-navigation', 'container' => false, 'menu_class' => 'menu site-navigation nav navbar-nav navbar-right', 'fallback_cb' => false ) ); ?>
						<?php wp_nav_menu( array( 'theme_location' => 'menu-navigation', 'container' => false, 'menu_class' => 'menu menu-navigation nav navbar-nav navbar-left', 'fallback_cb' => false ) ); ?>
					</nav>
					<?php 
					endif; // end has_nav_menu( 'site-navigation' ) || has_nav_menu( 'menu-navigation' )
					
				endif; // end is_active_sidebar( 'header' )
				?>
			
			</div><!-- .row -->
		</div><!-- .container -->
		
		<?php do_action( 'krusze_header_bottom' ); ?>
		
	</header><!-- #header -->
	
	<?php do_action( 'krusze_header_after' ); ?>

	<?php do_action( 'krusze_content_before' ); ?>
	
	<div id="content" class="site-content">
		
		<?php do_action( 'krusze_content_top' ); ?>
		