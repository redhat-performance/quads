<?php
/**
 * Template for Short-code Button
 *
 * @author  Tech Banker
 * @package contact-bank/lib
 * @version3.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
} // Exit if accessed directly
if ( ! is_user_logged_in() ) {
	return;
} else {
	$access_granted = false;
	foreach ( $user_role_permission as $permission ) {
		if ( current_user_can( $permission ) ) {
			$access_granted = true;
			break;
		}
	}
	if ( ! $access_granted ) {
		return;
	} else {
		?>
		<div id="contact-bank" style="display:none;">
			<div class="fluid-layout responsive">
			<div style="padding:20px 0 10px 15px;">
				<h3 class="label-shortcode"><?php echo esc_attr( $cb_shortcode_button_insert_form ); ?></h3>
				<span>
					<i><?php echo esc_attr( $cb_shortcode_button_add ); ?></i>
				</span>
			</div>
			<div class="layout-span12 responsive" style="padding:15px 15px 0 0;">
				<div class="layout-control-group">
					<label class="custom-layout-label" for="ux_form_name"><?php echo esc_attr( $cb_select_form ); ?> : </label>
					<select id="add_contact_form_id" class="layout-span9">
						<option value=""><?php echo esc_attr( $cb_shortcode_button_select_form ); ?>  </option>
						<?php
						global $wpdb;
						$get_contact_bank = $wpdb->get_results(
							$wpdb->prepare(
								'SELECT *  FROM ' . $wpdb->prefix . 'contact_bank_meta
								INNER JOIN ' . $wpdb->prefix . 'contact_bank ON ' . $wpdb->prefix . 'contact_bank_meta.meta_id = ' . $wpdb->prefix . 'contact_bank.id WHERE ' . $wpdb->prefix . 'contact_bank.type = %s and ' . $wpdb->prefix . 'contact_bank_meta.meta_key = %s ORDER BY meta_id DESC', 'form', 'form_data'
							)
						);// WPCS: db call ok, cache ok.

						$unserialized_forms_data_array = array();
						foreach ( $get_contact_bank as $key ) {
							$unserialized_data                = array();
							$unserialized_data                = maybe_unserialize( $key->meta_value );
							$unserialized_data['old_form_id'] = $key->old_form_id;
							$unserialized_data['id']          = $key->id;
							$unserialized_data['meta_key']    = $key->meta_key;// WPCS: slow query ok.
							$unserialized_data['meta_id']     = $key->meta_id;
							array_push( $unserialized_forms_data_array, $unserialized_data );
						}
						foreach ( $unserialized_forms_data_array as $data ) {
							?>
							<option value="<?php echo intval( $data['old_form_id'] ); ?>"><?php echo '' !== $data['form_title'] ? esc_attr( $data['form_title'] ) : 'Untitled Form'; ?></option>
							<?php
						}
						?>
					</select>
				</div>
				<div class="layout-control-group" style="padding:20px 0 0 0;">
					<label class="custom-layout-label"><?php echo esc_attr( $cb_form_title ); ?> : </label>
					<select id="add_contact_form_id_title" class="layout-span3">
						<option value="show"><?php echo esc_attr( $cb_shortcode_button_show ); ?></option>
						<option value="hide"><?php echo esc_attr( $cb_shortcode_button_hide ); ?></option>
					</select>
					<label class="custom-layout-label description-contact-bank"><?php echo esc_attr( $cb_form_description ); ?> :</label>
					<select id="add_contact_form_id_description" class="layout-span3">
						<option value="show"><?php echo esc_attr( $cb_shortcode_button_show ); ?></option>
						<option value="hide"><?php echo esc_attr( $cb_shortcode_button_hide ); ?></option>
					</select>
				</div>
				<div class="layout-control-group" style="padding:25px 0 0 0;">
					<label class="custom-layout-label"></label>
					<input type="button" class="button-primary" value="<?php echo esc_attr( $cb_shortcode_insert_form ); ?>" onclick="generate_shortcode_contact_bank();"/>&nbsp;&nbsp;&nbsp;
					<a class="button" style="color:#bbb;" href="#" onclick="tb_remove(); return false;"><?php echo esc_attr( $cb_shortcode_cancel ); ?></a>
				</div>
			</div>
		</div>
	</div>
	<script type="text/javascript">
	function generate_shortcode_contact_bank()
	{
		var form_id = jQuery("#add_contact_form_id").val();
		var form_title = jQuery("#add_contact_form_id_title").val();
		var form_description = jQuery("#add_contact_form_id_description").val();
		if (form_id == "")
		{
				alert("<?php echo esc_attr( $cb_shotcode_button_choose_form ); ?>");
				return;
			}
			window.send_to_editor("[contact_bank form_id=\"" + form_id + "\" form_title=\"" + form_title + "\" form_description=\"" + form_description + "\"][/contact_bank]");
		}
	</script>
		<?php
	}
}
