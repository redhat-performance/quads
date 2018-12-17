<?php
/**
 * This file is used for Widget Form Layout.
 *
 * @author Tech Banker
 * @package contact-bank/user-views/includes
 * @version 3.1.0
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
		$unserialized_forms_data_array = get_contact_dashboard_bank_data( 'form', 'form_data' );
		?>
		<div style="margin-top: 10px;">
				<div style="margin-bottom:15px;">
					<label style="margin-top:1px;font-weight:500;" title="form_name"> <?php echo esc_attr( $cb_select_form ); ?>: </label>
						<select style="height:34px;display:inline-block;width:100%;font-size:14px;margin-top:10px;" id='<?php echo esc_attr( $this->get_field_id( 'ux_ddl_shortcode_form_name' ) ); ?>'  name="<?php echo esc_attr( $this->get_field_name( 'ux_ddl_shortcode_form_name' ) ); ?>">
								<option value=""><?php echo esc_attr( $cb_choose_form ); ?></option>
								<?php
								foreach ( $unserialized_forms_data_array as $data ) {
										?>
										<option <?php echo isset( $instance['form_name'] ) && $instance['form_name'] || isset( $instance['form_id'] ) === $data['old_form_id'] ? 'selected=selected' : ''; ?> value="<?php echo intval( $data['old_form_id'] ); ?>"><?php echo isset( $data['form_title'] ) && '' !== $data['form_title'] ? esc_attr( $data['form_title'] ) : esc_attr( $cb_untitled_form ); ?></option>
										<?php
								}
								?>
						</select>
				</div>
				<div class="form-group" style="margin-bottom:15px;">
						<label class="control-label" title="form_title"> <?php echo esc_attr( $cb_form_title ); ?> : </label>
						<select style="height:34px;display:inline-block;width:100%;font-size:14px;margin-top:10px;" id='<?php echo esc_attr( $this->get_field_id( 'ux_ddl_shortcode_form_title' ) ); ?>' name="<?php echo esc_attr( $this->get_field_name( 'ux_ddl_shortcode_form_title' ) ); ?>">
								<option <?php echo isset( $instance['form_title'] ) && 'show' === $instance['form_title'] ? 'selected=selected' : ''; ?> value="show"><?php echo esc_attr( $cb_shortcode_button_show ); ?></option>
								<option <?php echo isset( $instance['form_title'] ) && 'hide' === $instance['form_title'] ? 'selected=selected' : ''; ?> value="hide"><?php echo esc_attr( $cb_shortcode_button_hide ); ?></option>
						</select>
				</div>
				<div style="margin-bottom:15px;">
						<label style="margin-top:1px;font-weight:500;" title="form_description"> <?php echo esc_attr( $cb_form_description ); ?> :</label>
						<select style="height:34px;display:inline-block;width:100%;font-size:14px;margin-top:10px;" id="<?php echo esc_attr( $this->get_field_id( 'ux_ddl_shortcode_form_description' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'ux_ddl_shortcode_form_description' ) ); ?>">
								<option <?php echo isset( $instance['form_description'] ) && 'show' === $instance['form_description'] ? 'selected=selected' : ''; ?> value="show"><?php echo esc_attr( $cb_shortcode_button_show ); ?></option>
								<option <?php echo isset( $instance['form_description'] ) && 'hide' === $instance['form_description'] ? 'selected=selected' : ''; ?> value="hide"><?php echo esc_attr( $cb_shortcode_button_hide ); ?></option>
						</select>
				</div>
		</div>
		<?php
	}
}
