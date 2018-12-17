=== Krusze ===
Contributors: kruszepl
Donate link: http://krusze.com/krusze
Tags: accessibility-ready, custom-background, custom-header, editor-style, fluid-layout, full-width-template, left-sidebar, one-column, post-formats, responsive-layout, right-sidebar, rtl-language-support, sticky-post, threaded-comments, translation-ready, two-columns
Requires at least: 4.2
Tested up to: 4.4
Stable tag: 0.9.7
License: GNU General Public License v2.0
License URI: http://www.gnu.org/licenses/gpl-2.0.html

== Description ==
Krusze is an ultimate responsive WordPres theme based on Bootstrap, from Twitter. Sleek, 
clean and simple design, intuitive, and powerful mobile first front-end framework for faster 
and easier web development. 

Krusze looks great on any device and allow you to create any type of website you want. 
It's perfect for a personal site or portfolio, professional magazine, an ecommerce online store, 
a minimalist blog, or even a corporate website. In short, you can have whatever you want, 
however you want. Make it yours! 

Krusze features: adjustable site layout, adjustable posts and pages layout, 
cross-browser compatible, custom background, customizer options, developer friendly, 
drop-down menu, editor styles, fast loading, header image, 
highly customizable and adaptable, Multisite ready, post formats support, print styles, 
RTL, responsive, Search Engine Friendly, threaded comments, 
translation ready (currently translated into 28 languages), W3C valid, widget-ready areas, 
WooCommerce ready & more... 

Developers will love it's clean and extensible code making it easy to customise and extend. 

For a live demo go to http://demo.krusze.com/krusze/

Sources and credits:

* [html5shiv] (https://github.com/aFarkas/html5shiv/) | License: [MIT] (http://www.opensource.org/licenses/MIT) & [GPL2] (http://www.gnu.org/licenses/gpl-2.0.html)
* [normalize.css] (http://necolas.github.io/normalize.css/) | License: [MIT] (http://www.opensource.org/licenses/mit-license.php)
* [Respond] (https://github.com/scottjehl/Respond) | License: [MIT] (http://www.opensource.org/licenses/MIT) & [GPL2] (http://www.gnu.org/licenses/gpl-2.0.html)

== Installation ==

Manual installation:

1. Download Krusze theme from [Themes Directory] (http://wordpress.org/themes/krusze)
1. Unzip and upload the `krusze` folder to the `/wp-content/themes/` directory
1. Activate the Theme through the 'Themes' menu in WordPress

Installation using "Add New Theme":

1. From your Admin UI (Dashboard), use the menu to select Themes -> Add New
1. Search for 'Krusze'
1. Click the 'Install' button to open the theme's repository listing
1. Activate the Theme

== Frequently Asked Questions ==

= I need a helping hand with theme? =

If you have any questions, suggestions, bug reports or feature requests feel free to visit 
[support forum] (http://wordpress.org/support/theme/krusze).

== Screenshots ==

1. Theme screenshot screenshot.png

== Changelog ==

= 0.9.7 - 22.12.2015 =
* Bugfix : added a visual focus when the responsive menu checkbox is focused on it's label in CSS
* Bugfix : fixed empty search form action in searchform.php
* Bugfix : added to select field `max-width: 100%` value in order to fit its container
* Changed : fixed footer widgets layout on mobile devices
* Changed : screenshot.png update

= 0.9.6 - 17.12.2015 =
* Bugfix : make responsive menu toggle keyboard accessible (now checkbox is hidden using screen reader text)
* Bugfix : make navigation menus navigable using the tab key
* Bugfix : fixed various contrast issues
* Bugfix : fixed empty search form label in searchform.php
* Changed : added functions krusze_entry_header and krusze_entry_footer
* Changed : minor css changes
* Changed : update screenshot.png to preferred 1200x900 size

= 0.9.5.1 - 24.11.2015 =
* Bugfix : correct color #777777 to #666666 in order to meet level AA contrast ratio (4.5:1) specified in the 
Web Content Accessibility Guidelines (WCAG) 2.0

= 0.9.5 - 13.11.2015 =
* Changed : move krusze_post_thumbnail() above entry header
* Changed : added krusze_header_class() which displays the classes for the header element
* Changed : minor css changes

= 0.9.4 - 09.11.2015 =
* Changed : reset heading elements to have their margin-top removed (preparation for Bootstrap 4)
* Changed : changed body font size from 14px to 16px and line-height to 1.5 and update font-size of various elements, 
i.e. 'h1, h2, h3, h4, h5, h6' (preparation for Bootstrap 4)
* Changed : update editor-style.css
* Changed : remove ie8.css

= 0.9.3 - 12.10.2015 =
* Changed : remove unused function krusze_get_attachment_id_from_url() from customizer.php
* Changed : remove unused function krusze_sanitize_integer() from customizer.php
* Changed : remove unused npm.js file from `/inc/bootstrap/bootstrap/js/`
* Changed : move function_exists() above every function description
* Changed : added 20px of padding-top on #colophon .container

= 0.9.2 - 18.08.2015 =
* Bugfix : css fix for menu-navigation (added clear: both)
* Bugfix : css fix for site-brand height for various font-family 
* Changed : minor CSS fixes

= 0.9.1 - 11.08.2015 =
* Bugfix : fixed empty <footer class="entry-footer"> on pages
* Changed : removed bootstrap-custom.js
* Changed : removed krusze_meta_entry_header on pages
* Changed : remove .navigation > div form style.css
* Changed : secure post meta in post-custom-meta-post-layout.php and post-custom-meta-site-layout.php
* Changed : minor css fixes
* Changed : upgrade html5shiv to 3.7.3

= 0.9 - 24.06.2015 =
Initial release.

== Upgrade Notice ==

= 0.9.7 =
Update release.

= 0.9.6 =
Update release.

= 0.9.5.1 =
Update release.

= 0.9.5 =
Update release.

= 0.9.4 =
Update release.

= 0.9.3 =
Update release.

= 0.9.2 =
Update release.

= 0.9.1 =
Update release.

= 0.9 =
Initial release.