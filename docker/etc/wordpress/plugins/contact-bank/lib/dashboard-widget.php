<?php
/**
 * This file is used for displaying dashboard widget.
 *
 * @author   Tech Banker
 * @package  contact-bank/lib
 * @version 3.0
 */

	/**
	 * This file is used for count.
	 *
	 * @param string $type passes parameter as type.
	 */
function get_count_of_data_contact_bank( $type ) {
	global $wpdb;
	$cb_total_data_count = $wpdb->get_var(
		$wpdb->prepare(
			'SELECT count(meta_id) FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s', $type
		)
	);// WPCS: db call ok, cache ok.
	return $cb_total_data_count;
}
global $wpdb;
$cb_total_controls    = $wpdb->get_results(
	$wpdb->prepare(
		'SELECT *  FROM ' . $wpdb->prefix . 'contact_bank_meta WHERE meta_key = %s', 'form_data'
	)
);// WPCS: db call ok, cache ok.
$form_serialized_data = array();
$forms_controls_count = 0;
foreach ( $cb_total_controls as $form_data ) {
	$form_serialized_data = maybe_unserialize( $form_data->meta_value );
	$forms_controls_count = $forms_controls_count + count( $form_serialized_data['controls'] );
}
?>
<style>
	.cb-statistics-list {
		overflow: hidden;
		margin: 0;
		margin-top: -12px !important;
	}
	.cb-controls-added,.cb-forms-added{
		border-top: 0px !important;
		border-bottom: 1px solid #ececec !important;
	}
	.cb-statistics-list li a:hover {
		color: #2ea2cc;
	}
	.cb-statistics-list li a {
		display: block;
		color: #aaa;
		padding: 9px 12px;
		-webkit-transition: all ease .5s;
		transition: all ease .5s;
		position: relative;
		font-size: 12px;
	}
	.cb-statistics-list li {
		width: 50%;
		float: left;
		padding: 0;
		box-sizing: border-box;
		margin: 0;
		border-top: 1px solid #ececec;
		color: #aaa;
	}
	.cb-statistics-list li.cb-forms-added {
		border-right: 1px solid #ececec;
	}
	.cb-statistics-list li.cb-form-submissions {
		width: 100%;
		border-right: 0px solid #ececec !important;
	}
	.cb-statistics-list li a strong {
		font-size: 18px;
		line-height: 1.2em;
		font-weight: 400;
		display: block;
		color: #21759b;
	}
	.cb-statistics-list li a::before {
		font-family: WooCommerce;
		speak: none;
		font-weight: 400;
		font-variant: normal;
		text-transform: none;
		line-height: 1;
		-webkit-font-smoothing: antialiased;
		margin: 0;
		text-indent: 0;
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		text-align: center;
		content: "";
		font-size: 2em;
		position: relative;
		width: auto;
		line-height: 1.2em;
		color: #464646;
		float: left;
		margin-right: 12px;
		margin-bottom: 12px;
	}
	.cb-statistics-list li.cb-forms-added a::before {
		font-family: Dashicons;
		content: "\f314";
	}
	.cb-statistics-list li.cb-controls-added a::before {
		font-family: Dashicons;
		content: "\f211";
	}
	.cb-statistics-list li.cb-form-submissions a::before {
		font-family: Dashicons;
		content: "\f123";
	}
	.cb-statistics-list li.cb-tags-data a::before {
		font-family: Dashicons;
		content: "\f323";
	}
	.cb-statistics-list li.cb-upgrade-now a::before {
		font-family: Dashicons;
		content: "\f132";
	}
	.cb-statistics-list li.cb-upgrade-now {
		width: 100%;
		margin-bottom: -10px;
	}
</style>
<ul class="cb-statistics-list">
	<li class="cb-forms-added">
		<a href="admin.php?page=contact_dashboard">
			<strong><?php echo intval( get_count_of_data_contact_bank( 'form_data' ) ); ?> <?php echo esc_attr( __( 'Forms', 'contact-bank' ) ); ?></strong>
		</a>
	</li>
	<li class="cb-controls-added">
		<a href="admin.php?page=contact_dashboard">
			<strong><?php echo esc_attr( $forms_controls_count ); ?> <?php echo esc_attr( __( 'Controls', 'contact-bank' ) ); ?></strong>
		</a>
	</li>
	<li class="cb-form-submissions">
		<a href="admin.php?page=cb_submissions">
			<strong><?php echo intval( get_count_of_data_contact_bank( 'submission_form_data' ) ); ?> <?php echo esc_attr( __( 'Form Submissions', 'contact-bank' ) ); ?></strong>
		</a>
	</li>
	<li class="cb-upgrade-now">
		<a href="https://contact-bank.tech-banker.com/">
				<strong><?php echo esc_attr( __( 'Upgrade Now to Premium Editions', 'contact-bank' ) ); ?></strong>
			</a>
	</li>
</ul>
