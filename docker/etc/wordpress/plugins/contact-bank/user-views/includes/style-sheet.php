<?php
/**
 * This file is used for frontend css.
 *
 * @author Tech Banker
 * @package contact-bank/user-views/includes
 * @version 3.1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Exit if accessed directly.
$font_families_form_layout[] = isset( $layout_setting_form_data['layout_settings_form_design_title_font_family'] ) ? htmlspecialchars_decode( $layout_setting_form_data['layout_settings_form_design_title_font_family'] ) : 'Roboto Slab:700';
$font_families_form_layout[] = isset( $layout_setting_form_data['layout_settings_form_design_description_font_family'] ) ? htmlspecialchars_decode( $layout_setting_form_data['layout_settings_form_design_description_font_family'] ) : 'Roboto Slab:300';
$font_families_form_layout[] = isset( $layout_setting_form_data['layout_settings_input_field_font_family'] ) ? htmlspecialchars_decode( $layout_setting_form_data['layout_settings_input_field_font_family'] ) : 'Roboto Slab:700';
$font_families_form_layout[] = isset( $layout_setting_form_data['layout_settings_label_field_font_family'] ) ? htmlspecialchars_decode( $layout_setting_form_data['layout_settings_label_field_font_family'] ) : 'Roboto Slab:300';
$font_families_form_layout[] = isset( $layout_setting_form_data['layout_settings_button_font_family'] ) ? htmlspecialchars_decode( $layout_setting_form_data['layout_settings_button_font_family'] ) : 'Roboto Slab:700';
$font_families_form_layout[] = isset( $layout_setting_form_data['layout_settings_messages_font_family'] ) ? htmlspecialchars_decode( $layout_setting_form_data['layout_settings_messages_font_family'] ) : 'Roboto Slab:300';
$font_families_form_layout[] = isset( $layout_setting_form_data['layout_settings_error_messages_font_family'] ) ? htmlspecialchars_decode( $layout_setting_form_data['layout_settings_error_messages_font_family'] ) : 'Roboto Slab';

// Code for importing google fonts url.
$unique_font_families_form_layout = array_unique( $font_families_form_layout );
$import_font_family_form_layout   = User_Helper_Contact_Bank::unique_font_families_contact_bank( $unique_font_families_form_layout );
$font_family_form_name_layout     = User_Helper_Contact_Bank::font_families_contact_bank( $font_families_form_layout );

// Form Design Layout.
$layout_settings_form_design_width                         = isset( $layout_setting_form_data['layout_settings_form_design_width'] ) ? esc_attr( $layout_setting_form_data['layout_settings_form_design_width'] ) : '100%';
$layout_settings_form_design_position                      = isset( $layout_setting_form_data['layout_settings_form_design_position'] ) ? esc_attr( $layout_setting_form_data['layout_settings_form_design_position'] ) : 'left';
$layout_settings_form_design_background_color              = isset( $layout_setting_form_data['layout_settings_form_design_background_color'] ) ? esc_attr( $layout_setting_form_data['layout_settings_form_design_background_color'] ) : '#cccccc';
$layout_settings_form_design_background_color_contact_bank = '' !== $layout_settings_form_design_background_color ? User_Helper_Contact_Bank::hex2rgb_contact_bank( $layout_settings_form_design_background_color ) : array( '', '', '' );
$layout_settings_form_design_background_transparency       = isset( $layout_setting_form_data['layout_settings_form_design_background_transparency'] ) ? intval( $layout_setting_form_data['layout_settings_form_design_background_transparency'] ) / 100 : 1;
$layout_settings_form_design_form_margin                   = isset( $layout_setting_form_data['layout_settings_form_design_form_margin'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_form_design_form_margin'] ) ) : array( 0, 0, 0, 0 );
$layout_settings_form_design_form_padding                  = isset( $layout_setting_form_data['layout_settings_form_design_form_padding'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_form_design_form_padding'] ) ) : array( 0, 0, 0, 0 );

// Form Design Title Layout.
$layout_settings_form_design_title_html_tag   = isset( $layout_setting_form_data['layout_settings_form_design_title_html_tag'] ) ? esc_attr( $layout_setting_form_data['layout_settings_form_design_title_html_tag'] ) : 'h1';
$layout_settings_form_design_title_alignment  = isset( $layout_setting_form_data['layout_settings_form_design_title_alignment'] ) ? esc_attr( $layout_setting_form_data['layout_settings_form_design_title_alignment'] ) : 'left';
$layout_settings_form_design_title_font_style = isset( $layout_setting_form_data['layout_settings_form_design_title_font_style'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_form_design_title_font_style'] ) ) : array( 24, '#000000' );
$layout_settings_form_design_title_margin     = isset( $layout_setting_form_data['layout_settings_form_design_title_margin'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_form_design_title_margin'] ) ) : array( 0, 0, 0, 0 );
$layout_settings_form_design_title_padding    = isset( $layout_setting_form_data['layout_settings_form_design_title_padding'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_form_design_title_padding'] ) ) : array( 0, 0, 0, 0 );

// Form Design Description Layout.
$layout_settings_form_design_description_html_tag   = isset( $layout_setting_form_data['layout_settings_form_design_description_html_tag'] ) ? esc_attr( $layout_setting_form_data['layout_settings_form_design_description_html_tag'] ) : 'h1';
$layout_settings_form_design_description_alignment  = isset( $layout_setting_form_data['layout_settings_form_design_description_alignment'] ) ? esc_attr( $layout_setting_form_data['layout_settings_form_design_description_alignment'] ) : 'left';
$layout_settings_form_design_description_font_style = isset( $layout_setting_form_data['layout_settings_form_design_description_font_style'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_form_design_description_font_style'] ) ) : array( 24, '#000000' );
$layout_settings_form_design_description_margin     = isset( $layout_setting_form_data['layout_settings_form_design_description_margin'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_form_design_description_margin'] ) ) : array( 0, 0, 0, 0 );
$layout_settings_form_design_description_padding    = isset( $layout_setting_form_data['layout_settings_form_design_description_padding'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_form_design_description_padding'] ) ) : array( 0, 0, 0, 0 );

// Input Field Layout.
$layout_settings_input_field_width                         = isset( $layout_setting_form_data['layout_settings_input_field_width'] ) ? esc_attr( $layout_setting_form_data['layout_settings_input_field_width'] ) : '100%';
$layout_settings_input_field_height                        = isset( $layout_setting_form_data['layout_settings_input_field_height'] ) ? esc_attr( $layout_setting_form_data['layout_settings_input_field_height'] ) : '100%';
$layout_settings_input_field_text_alignment                = isset( $layout_setting_form_data['layout_settings_input_field_text_alignment'] ) ? esc_attr( $layout_setting_form_data['layout_settings_input_field_text_alignment'] ) : 'left';
$layout_settings_input_field_radio_button_alignment        = isset( $layout_setting_form_data['layout_settings_input_field_radio_button_alignment'] ) ? esc_attr( $layout_setting_form_data['layout_settings_input_field_radio_button_alignment'] ) : 'single_row';
$layout_settings_input_field_checkbox_alignment            = isset( $layout_setting_form_data['layout_settings_input_field_checkbox_alignment'] ) ? esc_attr( $layout_setting_form_data['layout_settings_input_field_checkbox_alignment'] ) : 'single_row';
$layout_settings_input_field_font_style                    = isset( $layout_setting_form_data['layout_settings_input_field_font_style'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_input_field_font_style'] ) ) : array( 14, '#000000' );
$layout_settings_input_field_background_color_transparency = isset( $layout_setting_form_data['layout_settings_input_field_background_color_transparency'] ) ? explode( ',', $layout_setting_form_data['layout_settings_input_field_background_color_transparency'] ) : '#000000,100';
$layout_settings_input_field_background_color              = '' !== $layout_settings_input_field_background_color_transparency[0] ? User_Helper_Contact_Bank::hex2rgb_contact_bank( $layout_settings_input_field_background_color_transparency[0] ) : array( '', '', '' );
$layout_settings_input_field_background_transparency       = $layout_settings_input_field_background_color_transparency[1] / 100;
$layout_settings_input_field_border_style                  = isset( $layout_setting_form_data['layout_settings_input_field_border_style'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_input_field_border_style'] ) ) : array( 0, 'solid', '#000000' );
$layout_settings_input_field_border_radius                 = isset( $layout_setting_form_data['layout_settings_input_field_border_radius'] ) ? intval( $layout_setting_form_data['layout_settings_input_field_border_radius'] ) : 0;
$layout_settings_input_field_margin                        = isset( $layout_setting_form_data['layout_settings_input_field_margin'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_input_field_margin'] ) ) : array( 0, 0, 0, 0 );
$layout_settings_input_field_padding                       = isset( $layout_setting_form_data['layout_settings_input_field_padding'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_input_field_padding'] ) ) : array( 0, 0, 0, 0 );

// Label Field Layout.
$layout_settings_label_field_text_alignment                = isset( $layout_setting_form_data['layout_settings_label_field_text_alignment'] ) ? esc_attr( $layout_setting_form_data['layout_settings_label_field_text_alignment'] ) : 'left';
$layout_settings_label_field_width                         = isset( $layout_setting_form_data['layout_settings_label_field_width'] ) ? esc_attr( $layout_setting_form_data['layout_settings_label_field_width'] ) : '100%';
$layout_settings_label_field_height                        = isset( $layout_setting_form_data['layout_settings_label_field_height'] ) ? esc_attr( $layout_setting_form_data['layout_settings_label_field_height'] ) : '100%';
$layout_settings_label_field_font_style                    = isset( $layout_setting_form_data['layout_settings_label_field_font_style'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_label_field_font_style'] ) ) : array( 16, '#000000' );
$layout_settings_label_field_background_color_transparency = isset( $layout_setting_form_data['layout_settings_label_field_background_color_transparency'] ) ? explode( ',', $layout_setting_form_data['layout_settings_label_field_background_color_transparency'] ) : array( '#000000', 100 );
$layout_settings_label_field_background_color              = '' !== $layout_settings_label_field_background_color_transparency[0] ? User_Helper_Contact_Bank::hex2rgb_contact_bank( $layout_settings_label_field_background_color_transparency[0] ) : array( '', '', '' );
$layout_settings_label_field_background_transparency       = $layout_settings_label_field_background_color_transparency[1] / 100;
$layout_settings_label_field_margin                        = isset( $layout_setting_form_data['layout_settings_label_field_margin'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_label_field_margin'] ) ) : array( 0, 0, 0, 0 );
$layout_settings_label_field_padding                       = isset( $layout_setting_form_data['layout_settings_label_field_padding'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_label_field_padding'] ) ) : array( 0, 0, 0, 0 );

// Button Text Layout.
$layout_settings_button_text_alignment                      = isset( $layout_setting_form_data['layout_settings_button_text_alignment'] ) ? esc_attr( $layout_setting_form_data['layout_settings_button_text_alignment'] ) : 'left';
$layout_settings_button_text                                = isset( $layout_setting_form_data['layout_settings_button_text'] ) ? esc_attr( $layout_setting_form_data['layout_settings_button_text'] ) : 'Submit';
$layout_settings_button_width                               = isset( $layout_setting_form_data['layout_settings_button_width'] ) ? esc_attr( $layout_setting_form_data['layout_settings_button_width'] ) : '100%';
$layout_settings_button_height                              = isset( $layout_setting_form_data['layout_settings_button_height'] ) ? esc_attr( $layout_setting_form_data['layout_settings_button_height'] ) : '100%';
$layout_settings_button_font_style                          = isset( $layout_setting_form_data['layout_settings_button_font_style'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_button_font_style'] ) ) : array( 12, '#ffffff' );
$layout_settings_button_background_color                    = isset( $layout_setting_form_data['layout_settings_button_background_color'] ) ? esc_attr( $layout_setting_form_data['layout_settings_button_background_color'] ) : '#000000';
$layout_settings_button_background_color_contact_bank       = isset( $layout_settings_button_background_color ) ? User_Helper_Contact_Bank::hex2rgb_contact_bank( $layout_settings_button_background_color ) : array( '', '', '' );
$layout_settings_button_background_transparency             = isset( $layout_setting_form_data['layout_settings_button_background_transparency'] ) ? intval( $layout_setting_form_data['layout_settings_button_background_transparency'] ) / 100 : 1;
$layout_settings_button_hover_background_color              = isset( $layout_setting_form_data['layout_settings_button_hover_background_color'] ) ? esc_attr( $layout_setting_form_data['layout_settings_button_hover_background_color'] ) : '#000000';
$layout_settings_button_hover_background_color_contact_bank = isset( $layout_settings_button_hover_background_color ) ? User_Helper_Contact_Bank::hex2rgb_contact_bank( $layout_settings_button_hover_background_color ) : array( '', '', '' );
$layout_settings_button_hover_background_transparency       = isset( $layout_setting_form_data['layout_settings_button_hover_background_transparency'] ) ? intval( $layout_setting_form_data['layout_settings_button_hover_background_transparency'] ) / 100 : 1;
$layout_settings_button_border_style                        = isset( $layout_setting_form_data['layout_settings_button_border_style'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_button_border_style'] ) ) : array( 0, 'none', '#000000' );
$layout_settings_button_border_hover_color                  = isset( $layout_setting_form_data['layout_settings_button_hover_border_color'] ) ? esc_attr( $layout_setting_form_data['layout_settings_button_hover_border_color'] ) : '#000000';
$layout_settings_button_border_radius                       = isset( $layout_setting_form_data['layout_settings_button_border_radius'] ) ? intval( $layout_setting_form_data['layout_settings_button_border_radius'] ) : 0;
$layout_settings_button_margin                              = isset( $layout_setting_form_data['layout_settings_button_margin'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_button_margin'] ) ) : array( 0, 0, 0, 0 );
$layout_settings_button_padding                             = isset( $layout_setting_form_data['layout_settings_button_padding'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_button_padding'] ) ) : array( 0, 0, 0, 0 );

// Message Text Layout.
$layout_settings_messages_text_alignment                = isset( $layout_setting_form_data['layout_settings_messages_text_alignment'] ) ? esc_attr( $layout_setting_form_data['layout_settings_messages_text_alignment'] ) : 'left';
$layout_settings_messages_background_color_transparency = isset( $layout_setting_form_data['layout_settings_messages_background_color_transparency'] ) ? explode( ',', $layout_setting_form_data['layout_settings_messages_background_color_transparency'] ) : array( '#000000', 100 );
$layout_settings_messages_background_color              = '' !== $layout_settings_messages_background_color_transparency[0] ? User_Helper_Contact_Bank::hex2rgb_contact_bank( $layout_settings_messages_background_color_transparency[0] ) : array( '', '', '' );
$layout_settings_messages_background_transparency       = $layout_settings_messages_background_color_transparency[1] / 100;
$layout_settings_messages_font_style                    = isset( $layout_setting_form_data['layout_settings_messages_font_style'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_messages_font_style'] ) ) : array( 24, '#000000' );
$layout_settings_messages_margin                        = isset( $layout_setting_form_data['layout_settings_messages_margin'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_messages_margin'] ) ) : array( 0, 0, 0, 0 );
$layout_settings_messages_padding                       = isset( $layout_setting_form_data['layout_settings_messages_padding'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_messages_padding'] ) ) : array( 0, 0, 0, 0 );

// Error Message Text Layout.
$layout_settings_error_messages_background_color              = isset( $layout_setting_form_data['layout_settings_error_messages_background_color'] ) ? esc_attr( $layout_setting_form_data['layout_settings_error_messages_background_color'] ) : '#000000';
$layout_settings_error_messages_background_color_contact_bank = '' !== $layout_settings_error_messages_background_color ? User_Helper_Contact_Bank::hex2rgb_contact_bank( $layout_settings_error_messages_background_color ) : array( '', '', '' );
$layout_settings_error_messages_background_transparency       = isset( $layout_setting_form_data['layout_settings_error_messages_background_transparency'] ) ? intval( $layout_setting_form_data['layout_settings_error_messages_background_transparency'] ) / 100 : 1;
$layout_settings_error_messages_font_style                    = isset( $layout_setting_form_data['layout_settings_error_messages_font_style'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_error_messages_font_style'] ) ) : array( 24, '#000000' );
$layout_settings_error_messages_margin                        = isset( $layout_setting_form_data['layout_settings_error_messages_margin'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_error_messages_margin'] ) ) : array( 0, 0, 0, 0 );
$layout_settings_error_messages_padding                       = isset( $layout_setting_form_data['layout_settings_error_messages_padding'] ) ? explode( ',', esc_attr( $layout_setting_form_data['layout_settings_error_messages_padding'] ) ) : array( 0, 0, 0, 0 );

// Language Direction.
$language_direction_contact_bank = isset( $selected_general_setting_unserialize['language_direction'] ) && 'right_to_left' === $selected_general_setting_unserialize['language_direction'] ? 'rtl' : 'ltr';
?>
<style type='text/css'>
		<?php
		echo isset( $import_font_family_form_layout ) ? htmlspecialchars_decode( $import_font_family_form_layout ) : '';// WPCS: XSS ok.
		?>
		.language_direction_contact_bank_<?php echo intval( $random ); ?>
		{
				direction:<?php echo esc_attr( $language_direction_contact_bank ); ?> !important;
		}
		label.custom-error
		{
				<?php
				if ( '' !== $layout_settings_error_messages_background_color ) {
						?>
						background: rgba(<?php echo intval( $layout_settings_error_messages_background_color_contact_bank[0] ); ?>,<?php echo intval( $layout_settings_error_messages_background_color_contact_bank[1] ); ?>,<?php echo intval( $layout_settings_error_messages_background_color_contact_bank[2] ); ?>,<?php echo floatval( $layout_settings_error_messages_background_transparency ); ?>) !important;
						<?php
				}
				?>
/*        display: inline-block;*/
				font-size: <?php echo intval( $layout_settings_error_messages_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_error_messages_font_style[1] ); ?> !important;
				margin: <?php echo intval( $layout_settings_error_messages_margin[0] ); ?>px <?php echo intval( $layout_settings_error_messages_margin[1] ); ?>px <?php echo intval( $layout_settings_error_messages_margin[2] ); ?>px <?php echo intval( $layout_settings_error_messages_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_error_messages_padding[0] ); ?>px <?php echo intval( $layout_settings_error_messages_padding[1] ); ?>px <?php echo intval( $layout_settings_error_messages_padding[2] ); ?>px <?php echo intval( $layout_settings_error_messages_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[6]; // WPCS: XSS ok. ?>
		}
		.cb-limit-input
		{
				<?php
				if ( '' !== $layout_settings_error_messages_background_color ) {
						?>
						background: rgba(<?php echo intval( $layout_settings_error_messages_background_color_contact_bank[0] ); ?>,<?php echo intval( $layout_settings_error_messages_background_color_contact_bank[1] ); ?>,<?php echo intval( $layout_settings_error_messages_background_color_contact_bank[2] ); ?>,<?php echo floatval( $layout_settings_error_messages_background_transparency ); ?>) !important;
						<?php
				}
				?>
				font-size: <?php echo intval( $layout_settings_error_messages_font_style[0] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[6]; // WPCS: XSS ok. ?>;
				padding: <?php echo intval( $layout_settings_error_messages_padding[0] ); ?>px <?php echo intval( $layout_settings_error_messages_padding[1] ); ?>px <?php echo intval( $layout_settings_error_messages_padding[2] ); ?>px <?php echo intval( $layout_settings_error_messages_padding[3] ); ?>px !important;
		}
		.divider-line-seperator_<?php echo intval( $random ); ?>
		{
				height: 1px;
				background: #717171;
				border-bottom: 1px solid #DDD;
				margin-bottom: 20px;
		}
		.main_container_contact_bank_<?php echo intval( $random ); ?>
		{
				<?php
				switch ( $layout_settings_form_design_position ) {
					case 'center':
						?>
						margin: 0 auto !important;
						<?php
						break;
					default:
						?>
						float: <?php echo esc_attr( $layout_settings_form_design_position ); ?> !important;
						<?php
						break;
				}
				?>
				width: <?php echo esc_attr( $layout_settings_form_design_width ); ?> !important;
				clear: both;
		}
		.form-layout-main-container-contact-bank_<?php echo intval( $random ); ?>
		{
				<?php
				if ( '' !== $layout_settings_form_design_background_color ) {
						?>
						background: rgba(<?php echo intval( $layout_settings_form_design_background_color_contact_bank[0] ); ?>,<?php echo intval( $layout_settings_form_design_background_color_contact_bank[1] ); ?>,<?php echo intval( $layout_settings_form_design_background_color_contact_bank[2] ); ?>,<?php echo floatval( $layout_settings_form_design_background_transparency ); ?>) !important;
						<?php
				}
				?>
				margin: <?php echo intval( $layout_settings_form_design_form_margin[0] ); ?>px <?php echo intval( $layout_settings_form_design_form_margin[1] ); ?>px <?php echo intval( $layout_settings_form_design_form_margin[2] ); ?>px <?php echo intval( $layout_settings_form_design_form_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_form_design_form_padding[0] ); ?>px <?php echo intval( $layout_settings_form_design_form_padding[1] ); ?>px <?php echo intval( $layout_settings_form_design_form_padding[2] ); ?>px <?php echo intval( $layout_settings_form_design_form_padding[3] ); ?>px !important;
		}
		.form-layout-title-contact-bank_<?php echo intval( $random ); ?> <?php echo esc_attr( $layout_settings_form_design_title_html_tag ); ?>
		{
				text-align: <?php echo esc_attr( $layout_settings_form_design_title_alignment ); ?> !important;
				font-size: <?php echo intval( $layout_settings_form_design_title_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_form_design_title_font_style[1] ); ?> !important;
				margin: <?php echo intval( $layout_settings_form_design_title_margin[0] ); ?>px <?php echo intval( $layout_settings_form_design_title_margin[1] ); ?>px <?php echo intval( $layout_settings_form_design_title_margin[2] ); ?>px <?php echo intval( $layout_settings_form_design_title_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_form_design_title_padding[0] ); ?>px <?php echo intval( $layout_settings_form_design_title_padding[1] ); ?>px <?php echo intval( $layout_settings_form_design_title_padding[2] ); ?>px <?php echo intval( $layout_settings_form_design_title_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[0]; // WPCS: XSS ok. ?>
		}
		.form-layout-description-contact-bank_<?php echo intval( $random ); ?> <?php echo esc_attr( $layout_settings_form_design_description_html_tag ); ?>
		{
				text-align: <?php echo esc_attr( $layout_settings_form_design_description_alignment ); ?> !important;
				font-size: <?php echo intval( $layout_settings_form_design_description_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_form_design_description_font_style[1] ); ?> !important;
				margin: <?php echo intval( $layout_settings_form_design_description_margin[0] ); ?>px <?php echo intval( $layout_settings_form_design_description_margin[1] ); ?>px <?php echo intval( $layout_settings_form_design_description_margin[2] ); ?>px <?php echo intval( $layout_settings_form_design_description_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_form_design_description_padding[0] ); ?>px <?php echo intval( $layout_settings_form_design_description_padding[1] ); ?>px <?php echo intval( $layout_settings_form_design_description_padding[2] ); ?>px <?php echo intval( $layout_settings_form_design_description_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[1]; // WPCS: XSS ok. ?>
		}
		<?php
		if ( 'single_row' === $layout_settings_input_field_radio_button_alignment ) {
				?>
				.input_radio_button_label_contact_bank_<?php echo intval( $random ); ?>
				{
						font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
						display:inline-block !important;
						margin-left: 8px !important;
						font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>
				}
				.input_radio_button_contact_bank_<?php echo intval( $random ); ?>
				{
           margin-left: 9px !important;
				}
				<?php
		} else {
				?>
				.input_radio_button_label_contact_bank_<?php echo intval( $random ); ?>
				{
						font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
						display:flex !important;
						margin-left: 30px !important;
						font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>
				}
				.input_radio_button_contact_bank_<?php echo intval( $random ); ?>
				{
						display:flex !important;
           /* margin-left: 9px !important; */
						position: absolute !important;
						margin-top: 10px !important;
				}
				<?php
		}
		if ( 'single_row' === $layout_settings_input_field_checkbox_alignment ) {
				?>
				.input_chk_button_label_contact_bank_<?php echo intval( $random ); ?>
				{
						font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
						font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
						display:inline-block !important;
						margin-left: 8px !important;
				}
				.input_chk_button_contact_bank_<?php echo intval( $random ); ?>
				{
/*            margin-left: 9px !important;*/
				}
				<?php
		} else {
				?>
				.input_chk_button_label_contact_bank_<?php echo intval( $random ); ?>
				{
						font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
						font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
						display:flex !important;
						margin-left: 30px !important;
				}
				.input_chk_button_contact_bank_<?php echo intval( $random ); ?>
				{
						display:flex !important;
/*            margin-left: 9px !important;*/
						position: absolute !important;
						margin-top: 10px !important;
				}
				<?php
		}
		?>
		.right-placement-input-contact-bank_<?php echo intval( $random ); ?>::-webkit-input-placeholder {
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.right-placement-input-contact-bank_<?php echo intval( $random ); ?>::-moz-placeholder {
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.right-placement-input-contact-bank_<?php echo intval( $random ); ?>
		{
				width: 60% !important;
				float: left !important;
				height: <?php echo esc_attr( $layout_settings_input_field_height ); ?> !important;
				text-align: <?php echo esc_attr( $layout_settings_input_field_text_alignment ); ?> !important;
				font-size: <?php echo intval( $layout_settings_input_field_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_input_field_font_style[1] ); ?> !important;
				border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				-webkit-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				-moz-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				-webkit-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				-moz-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				padding: <?php echo intval( $layout_settings_input_field_padding[0] ); ?>px <?php echo intval( $layout_settings_input_field_padding[1] ); ?>px <?php echo intval( $layout_settings_input_field_padding[2] ); ?>px <?php echo intval( $layout_settings_input_field_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.right-placement-input-contact-bank_credit_card_<?php echo intval( $random ); ?>::-webkit-input-placeholder{
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.right-placement-input-contact-bank_credit_card_<?php echo intval( $random ); ?>::-moz-placeholder {
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS OK. ?>;
		}
		.right-placement-input-contact-bank_credit_card_<?php echo intval( $random ); ?>
		{
				width: 60% !important;
				height: <?php echo esc_attr( $layout_settings_input_field_height ); ?> !important;
				text-align: <?php echo esc_attr( $layout_settings_input_field_text_alignment ); ?> !important;
				font-size: <?php echo intval( $layout_settings_input_field_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_input_field_font_style[1] ); ?> !important;
				border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				-webkit-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				-moz-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				-webkit-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				-moz-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				padding: <?php echo intval( $layout_settings_input_field_padding[0] ); ?>px <?php echo intval( $layout_settings_input_field_padding[1] ); ?>px <?php echo intval( $layout_settings_input_field_padding[2] ); ?>px <?php echo intval( $layout_settings_input_field_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.left-placement-input-contact-bank_<?php echo intval( $random ); ?>::-webkit-input-placeholder {
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.left-placement-input-contact-bank_<?php echo intval( $random ); ?>::-moz-placeholder {
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.left-placement-input-contact-bank_<?php echo intval( $random ); ?>
		{
				width: 60% !important;
				<?php
				if ( '' !== $layout_settings_input_field_background_color_transparency[0] ) {
					?>
							background-color: rgba(<?php echo intval( $layout_settings_input_field_background_color[0] ); ?>,<?php echo intval( $layout_settings_input_field_background_color[1] ); ?>,<?php echo intval( $layout_settings_input_field_background_color[2] ); ?>,<?php echo floatval( $layout_settings_input_field_background_transparency ); ?>) !important;
					<?php
				}
				?>
				height: <?php echo esc_attr( $layout_settings_input_field_height ); ?> !important;
				text-align: <?php echo esc_attr( $layout_settings_input_field_text_alignment ); ?> !important;
				font-size: <?php echo intval( $layout_settings_input_field_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_input_field_font_style[1] ); ?> !important;
				border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				-webkit-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				-moz-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				-webkit-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				-moz-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				margin: <?php echo intval( $layout_settings_input_field_margin[0] ); ?>px <?php echo intval( $layout_settings_input_field_margin[1] ); ?>px <?php echo intval( $layout_settings_input_field_margin[2] ); ?>px <?php echo intval( $layout_settings_input_field_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_input_field_padding[0] ); ?>px <?php echo intval( $layout_settings_input_field_padding[1] ); ?>px <?php echo intval( $layout_settings_input_field_padding[2] ); ?>px <?php echo intval( $layout_settings_input_field_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
			}
		.left-placement-input-contact-bank_credit_card_<?php echo intval( $random ); ?>::-webkit-input-placeholder {
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
			}
		.left-placement-input-contact-bank_credit_card_<?php echo intval( $random ); ?>::-moz-placeholder{
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.left-placement-input-contact-bank_credit_card_<?php echo intval( $random ); ?>
		{
				width: 60% !important;
				<?php
				if ( '' !== $layout_settings_input_field_background_color_transparency[0] ) {
				?>
				background-color: rgba(<?php echo intval( $layout_settings_input_field_background_color[0] ); ?>,<?php echo intval( $layout_settings_input_field_background_color[1] ); ?>,<?php echo intval( $layout_settings_input_field_background_color[2] ); ?>,<?php echo floatval( $layout_settings_input_field_background_transparency ); ?>) !important;
				<?php
				}
				?>
				height: <?php echo esc_attr( $layout_settings_input_field_height ); ?> !important;
				display: inline-block;
				vertical-align: middle;
				text-align: <?php echo esc_attr( $layout_settings_input_field_text_alignment ); ?> !important;
				font-size: <?php echo intval( $layout_settings_input_field_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_input_field_font_style[1] ); ?> !important;
				border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				-webkit-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				-moz-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
				border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				-webkit-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				-moz-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
				margin: <?php echo intval( $layout_settings_input_field_margin[0] ); ?>px <?php echo intval( $layout_settings_input_field_margin[1] ); ?>px <?php echo intval( $layout_settings_input_field_margin[2] ); ?>px <?php echo intval( $layout_settings_input_field_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_input_field_padding[0] ); ?>px <?php echo intval( $layout_settings_input_field_padding[1] ); ?>px <?php echo intval( $layout_settings_input_field_padding[2] ); ?>px <?php echo intval( $layout_settings_input_field_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
			}
		.input-layout-field-contact-bank_<?php echo intval( $random ); ?>
		{
				<?php
				if ( '' !== $layout_settings_input_field_background_color_transparency[0] ) {
						?>
								background-color: rgba(<?php echo intval( $layout_settings_input_field_background_color[0] ); ?>,<?php echo intval( $layout_settings_input_field_background_color[1] ); ?>,<?php echo intval( $layout_settings_input_field_background_color[2] ); ?>,<?php echo floatval( $layout_settings_input_field_background_transparency ); ?>) !important;
						<?php
				}
				?>
						height: <?php echo esc_attr( $layout_settings_input_field_height ); ?> !important;
						text-align: <?php echo esc_attr( $layout_settings_input_field_text_alignment ); ?> !important;
						font-size: <?php echo intval( $layout_settings_input_field_font_style[0] ); ?>px !important;
						color: <?php echo esc_attr( $layout_settings_input_field_font_style[1] ); ?> !important;
						border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
						-webkit-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
						-moz-border: <?php echo intval( $layout_settings_input_field_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_input_field_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_input_field_border_style[2] ); ?> !important;
						border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
						-webkit-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
						-moz-border-radius: <?php echo intval( $layout_settings_input_field_border_radius ); ?>px !important;
						margin: <?php echo intval( $layout_settings_input_field_margin[0] ); ?>px <?php echo intval( $layout_settings_input_field_margin[1] ); ?>px <?php echo intval( $layout_settings_input_field_margin[2] ); ?>px <?php echo intval( $layout_settings_input_field_margin[3] ); ?>px !important;
						padding: <?php echo intval( $layout_settings_input_field_padding[0] ); ?>px <?php echo intval( $layout_settings_input_field_padding[1] ); ?>px <?php echo intval( $layout_settings_input_field_padding[2] ); ?>px <?php echo intval( $layout_settings_input_field_padding[3] ); ?>px !important;
						width: <?php echo esc_attr( $layout_settings_input_field_width ); ?> !important;
						font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.input-layout-field-contact-bank_<?php echo intval( $random ); ?>::-webkit-input-placeholder {
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.input-layout-field-contact-bank_<?php echo intval( $random ); ?>::-moz-placeholder {
				font-family: <?php echo $font_family_form_name_layout[2]; // WPCS: XSS ok. ?>;
		}
		.label_left_placement_<?php echo intval( $random ); ?>
		{
				position: relative;
				display: inline-block;
				bottom: 2px;
				width: 30% !important;
				float: left !important;
				text-align: <?php echo esc_attr( $layout_settings_label_field_text_alignment ); ?> !important;
				height: <?php echo esc_attr( $layout_settings_label_field_height ); ?> !important;
				font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_label_field_font_style[1] ); ?> !important;
				margin: <?php echo intval( $layout_settings_label_field_margin[0] ); ?>px <?php echo intval( $layout_settings_label_field_margin[1] ); ?>px <?php echo intval( $layout_settings_label_field_margin[2] ); ?>px <?php echo intval( $layout_settings_label_field_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_label_field_padding[0] ); ?>px <?php echo intval( $layout_settings_label_field_padding[1] ); ?>px <?php echo intval( $layout_settings_label_field_padding[2] ); ?>px <?php echo intval( $layout_settings_label_field_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[3]; // WPCS: XSS ok. ?>
		}
		.radio_list_label_right_placement_<?php echo intval( $random ); ?>
		{
				float: left;
				width: 60%;
				display: inline-block;
				position: relative;
		}
		.radio_list_label_<?php echo intval( $random ); ?>
		{
				text-align: left !important;
				vertical-align: middle;
				position: relative;
				bottom: 0px;
				font-family: <?php echo $font_family_form_name_layout[3]; // WPCS: XSS ok. ?>
				font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
		}
		.checkbox_label_right_placement_<?php echo intval( $random ); ?>
		{
				float: right;
				width: 60%;
				bottom: 10px;
				position: relative;
		}
		.checkbox_input_right_placement_<?php echo intval( $random ); ?>
		{
				display: inline-block;
				position: relative;
				width: 30%;
		}
		.label-gdrp-compliance-style
		{
				font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_label_field_font_style[1] ); ?> !important;
				margin: <?php echo intval( $layout_settings_label_field_margin[0] ); ?>px <?php echo intval( $layout_settings_label_field_margin[1] ); ?>px <?php echo intval( $layout_settings_label_field_margin[2] ); ?>px <?php echo intval( $layout_settings_label_field_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_label_field_padding[0] ); ?>px <?php echo intval( $layout_settings_label_field_padding[1] ); ?>px <?php echo intval( $layout_settings_label_field_padding[2] ); ?>px <?php echo intval( $layout_settings_label_field_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[3]; // WPCS: XSS ok. ?>
		}
		.label_left_placement_credit_card_<?php echo intval( $random ); ?>
		{
				width: 30% !important;
				display: inline-block;
				vertical-align: middle;
				text-align: <?php echo esc_attr( $layout_settings_label_field_text_alignment ); ?> !important;
				height: <?php echo esc_attr( $layout_settings_label_field_height ); ?> !important;
				font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_label_field_font_style[1] ); ?> !important;
				margin: <?php echo intval( $layout_settings_label_field_margin[0] ); ?>px <?php echo intval( $layout_settings_label_field_margin[1] ); ?>px <?php echo intval( $layout_settings_label_field_margin[2] ); ?>px <?php echo intval( $layout_settings_label_field_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_label_field_padding[0] ); ?>px <?php echo intval( $layout_settings_label_field_padding[1] ); ?>px <?php echo intval( $layout_settings_label_field_padding[2] ); ?>px <?php echo intval( $layout_settings_label_field_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[3]; // WPCS: XSS ok. ?>
		}
		.label-layout-field-contact-bank_<?php echo intval( $random ); ?>
		{
				<?php
				if ( '' !== $layout_settings_label_field_background_color_transparency[0] ) {
						?>
						background: rgba(<?php echo intval( $layout_settings_label_field_background_color[0] ); ?>,<?php echo intval( $layout_settings_label_field_background_color[1] ); ?>,<?php echo intval( $layout_settings_label_field_background_color[2] ); ?>,<?php echo floatval( $layout_settings_label_field_background_transparency ); ?>) !important;
						<?php
				}
				?>
				text-align: <?php echo esc_attr( $layout_settings_label_field_text_alignment ); ?> !important;
				width: <?php echo esc_attr( $layout_settings_label_field_width ); ?> !important;
				height: <?php echo esc_attr( $layout_settings_label_field_height ); ?> !important;
				font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_label_field_font_style[1] ); ?> !important;
				margin: <?php echo intval( $layout_settings_label_field_margin[0] ); ?>px <?php echo intval( $layout_settings_label_field_margin[1] ); ?>px <?php echo intval( $layout_settings_label_field_margin[2] ); ?>px <?php echo intval( $layout_settings_label_field_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_label_field_padding[0] ); ?>px <?php echo intval( $layout_settings_label_field_padding[1] ); ?>px <?php echo intval( $layout_settings_label_field_padding[2] ); ?>px <?php echo intval( $layout_settings_label_field_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[3]; // WPCS: XSS ok. ?>
		}
		.label-gdrp-compliance-style
		{
				font-size: <?php echo intval( $layout_settings_label_field_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_label_field_font_style[1] ); ?> !important;
				margin: <?php echo intval( $layout_settings_label_field_margin[0] ); ?>px <?php echo intval( $layout_settings_label_field_margin[1] ); ?>px <?php echo intval( $layout_settings_label_field_margin[2] ); ?>px <?php echo intval( $layout_settings_label_field_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_label_field_padding[0] ); ?>px <?php echo intval( $layout_settings_label_field_padding[1] ); ?>px <?php echo intval( $layout_settings_label_field_padding[2] ); ?>px <?php echo intval( $layout_settings_label_field_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[3]; // WPCS: XSS ok. ?>
		}
		.label_tooltip_contact_bank
		{
				font-size: 12px !important;
		}
		.button-layout-contact-bank_<?php echo intval( $random ); ?>
		{
				<?php
				if ( '' !== $layout_settings_button_background_color ) {
						?>
						background: rgba(<?php echo intval( $layout_settings_button_background_color_contact_bank[0] ); ?>,<?php echo intval( $layout_settings_button_background_color_contact_bank[1] ); ?>,<?php echo intval( $layout_settings_button_background_color_contact_bank[2] ); ?>,<?php echo floatval( $layout_settings_button_background_transparency ); ?>) !important;
						<?php
				}
				?>
				text-align: <?php echo esc_attr( $layout_settings_button_text_alignment ); ?> !important;
				width: <?php echo esc_attr( $layout_settings_button_width ); ?> !important;
				height: <?php echo esc_attr( $layout_settings_button_height ); ?> !important;
				font-size: <?php echo intval( $layout_settings_button_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_button_font_style[1] ); ?> !important;
				border: <?php echo intval( $layout_settings_button_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_button_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_button_border_style[2] ); ?> !important;
				-webkit-border: <?php echo intval( $layout_settings_button_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_button_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_button_border_style[2] ); ?> !important;
				-moz-border: <?php echo intval( $layout_settings_button_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_button_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_button_border_style[2] ); ?> !important;
				border-radius: <?php echo intval( $layout_settings_button_border_radius ); ?>px !important;
				-webkit-border-radius: <?php echo intval( $layout_settings_button_border_radius ); ?>px !important;
				-moz-border-radius: <?php echo intval( $layout_settings_button_border_radius ); ?>px !important;
				margin: <?php echo intval( $layout_settings_button_margin[0] ); ?>px <?php echo intval( $layout_settings_button_margin[1] ); ?>px <?php echo intval( $layout_settings_button_margin[2] ); ?>px <?php echo intval( $layout_settings_button_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_button_padding[0] ); ?>px <?php echo intval( $layout_settings_button_padding[1] ); ?>px <?php echo intval( $layout_settings_button_padding[2] ); ?>px <?php echo intval( $layout_settings_button_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[4]; // WPCS: XSS ok. ?>;
				display: inline-block !important;
				text-transform: none !important;
		}
		.button-layout-contact-bank_<?php echo intval( $random ); ?>:hover
		{
				<?php
				if ( '' !== $layout_settings_button_hover_background_color ) {
						?>
						background: rgba(<?php echo intval( $layout_settings_button_hover_background_color_contact_bank[0] ); ?>,<?php echo intval( $layout_settings_button_hover_background_color_contact_bank[1] ); ?>,<?php echo intval( $layout_settings_button_hover_background_color_contact_bank[2] ); ?>,<?php echo floatval( $layout_settings_button_hover_background_transparency ); ?>) !important;
						border-color: <?php echo esc_attr( $layout_settings_button_border_hover_color ); ?> !important;
						<?php
				}
				?>
		}
		.file-upload-button-style-contact-bank_<?php echo intval( $random ); ?>
		{
				<?php
				if ( '' !== $layout_settings_button_background_color ) {
						?>
						background: rgba(<?php echo intval( $layout_settings_button_background_color_contact_bank[0] ); ?>,<?php echo intval( $layout_settings_button_background_color_contact_bank[1] ); ?>,<?php echo intval( $layout_settings_button_background_color_contact_bank[2] ); ?>,<?php echo floatval( $layout_settings_button_background_transparency ); ?>) !important;
						<?php
				}
				?>
				color: <?php echo esc_attr( $layout_settings_button_font_style[1] ); ?> !important;
				padding: 5px 10px 5px 10px !important;
				border: <?php echo intval( $layout_settings_button_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_button_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_button_border_style[2] ); ?> !important;
				-webkit-border: <?php echo intval( $layout_settings_button_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_button_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_button_border_style[2] ); ?> !important;
				-moz-border: <?php echo intval( $layout_settings_button_border_style[0] ); ?>px <?php echo esc_attr( $layout_settings_button_border_style[1] ); ?> <?php echo esc_attr( $layout_settings_button_border_style[2] ); ?> !important;
				font-size: 12px !important;
		}
		.file-upload-button-style-contact-bank_<?php echo intval( $random ); ?>:hover
		{
				<?php
				if ( '' !== $layout_settings_button_hover_background_color ) {
						?>
						background: rgba(<?php echo intval( $layout_settings_button_hover_background_color_contact_bank[0] ); ?>,<?php echo intval( $layout_settings_button_hover_background_color_contact_bank[1] ); ?>,<?php echo intval( $layout_settings_button_hover_background_color_contact_bank[2] ); ?>,<?php echo floatval( $layout_settings_button_hover_background_transparency ); ?>) !important;
						border-color: <?php echo esc_attr( $layout_settings_button_border_hover_color ); ?> !important;
						padding: 5px 10px 5px 10px !important;
						font-size: 12px !important;
						<?php
				}
				?>
		}
		.message-layout-contact-bank_<?php echo intval( $random ); ?>
		{
				text-align: <?php echo esc_attr( $layout_settings_messages_text_alignment ); ?> !important;
				direction: inherit !important;
				background: url(<?php echo esc_attr( plugins_url( 'assets/img/icon-succes.png', dirname( __FILE__ ) ) ); ?>) no-repeat 8px 3px <?php if ( '' !== $layout_settings_messages_background_color_transparency[0] ); ?> rgba( <?php echo intval( $layout_settings_messages_background_color[0] ); ?>,<?php echo intval( $layout_settings_messages_background_color[1] ); ?>,<?php echo intval( $layout_settings_messages_background_color[2] ); ?>,<?php echo floatval( $layout_settings_messages_background_transparency); // @codingStandardsIgnoreLine. ?> ) !important;
		}
		.custom-message
		{
				position: relative;
				display: inline-block;
				margin: 20px 0 0 0;
				margin-bottom: 0px;
				padding: 0 0 0 35px;
		}
		#success_message_text_<?php echo intval( $random ); ?>
		{
				font-size: <?php echo intval( $layout_settings_messages_font_style[0] ); ?>px !important;
				color: <?php echo esc_attr( $layout_settings_messages_font_style[1] ); ?> !important;
				margin: <?php echo intval( $layout_settings_messages_margin[0] ); ?>px <?php echo intval( $layout_settings_messages_margin[1] ); ?>px <?php echo intval( $layout_settings_messages_margin[2] ); ?>px <?php echo intval( $layout_settings_messages_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_messages_padding[0] ); ?>px <?php echo intval( $layout_settings_messages_padding[1] ); ?>px <?php echo intval( $layout_settings_messages_padding[2] ); ?>px <?php echo intval( $layout_settings_messages_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[5]; // WPCS: XSS ok. ?>
		}
		.error-message
		{
				text-align: <?php echo esc_attr( $layout_settings_messages_text_alignment ); ?> !important;
				background: url(<?php echo esc_attr( plugins_url( 'assets/img/no.png', dirname( __FILE__ ) ) ); ?>) no-repeat 8px 6px #FFBABA !important;
		}
		.error_message_text
		{
				font-size: <?php echo intval( $layout_settings_messages_font_style[0] ); ?>px !important;
				color: #D8000C !important;
				margin: <?php echo intval( $layout_settings_messages_margin[0] ); ?>px <?php echo intval( $layout_settings_messages_margin[1] ); ?>px <?php echo intval( $layout_settings_messages_margin[2] ); ?>px <?php echo intval( $layout_settings_messages_margin[3] ); ?>px !important;
				padding: <?php echo intval( $layout_settings_messages_padding[0] ); ?>px <?php echo intval( $layout_settings_messages_padding[1] ); ?>px <?php echo intval( $layout_settings_messages_padding[2] ); ?>px <?php echo intval( $layout_settings_messages_padding[3] ); ?>px !important;
				font-family: <?php echo $font_family_form_name_layout[5]; // WPCS: XSS ok. ?>
		}
		.cb-pricing-control
		{
				border: 0px none #000000 !important;
				background-color: transparent !important;
				box-shadow: none !important;
		}
		<?php
				echo htmlspecialchars_decode( $custom_css['custom_css'] );// WPCS: XSS ok.
		?>
</style>
