<?php
/**
 * This file contains plugin header section..
 *
 * @author  Tech Banker
 * @package contact-bank/includes
 * @version 3.0
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
		<div class="page-container">
			<div id="manage_messages" style="display:none;">
				<div class="radio">
					<input type="radio" value="success" checked="checked" />
				</div>
			</div>
			<div id="toastTypeGroup_error" style="display:none;">
				<div class="radio">
					<input type="radio" value="error" checked=""/>
				</div>
			</div>
		<?php
	}
}
