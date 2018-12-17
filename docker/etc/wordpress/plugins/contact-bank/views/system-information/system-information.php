<?php
/**
 * Template for view System Information.
 *
 * @author  Tech Banker
 * @package contact-bank/views/system-information
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
	} elseif ( SYSTEM_INFORMATION_CONTACT_BANK === '1' ) {
		?>
		<div class="page-bar">
			<ul class="page-breadcrumb">
				<li>
					<i class="icon-custom-home"></i>
					<a href="admin.php?page=contact_dashboard">
						<?php echo esc_attr( $cb_contact_bank ); ?>
					</a>
					<span>></span>
				</li>
				<li>
					<span>
						<?php echo esc_attr( $cb_system_information ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-screen-desktop"></i>
							<?php echo esc_attr( $cb_system_information ); ?>
						</div>
						<p class="premium-editions">
							<?php echo esc_attr( $cb_upgrade_need_help ); ?><a href="https://contact-bank.tech-banker.com/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_documentation ); ?></a><?php echo esc_attr( $cb_read_and_check ); ?><a href="https://contact-bank.tech-banker.com/frontend-demos/" target="_blank" class="premium-editions-documentation"><?php echo esc_attr( $cb_demos_section ); ?></a>
						</p>
					</div>
					<div class="portlet-body form">
						<form id="ux_frm_system_information">
							<div class="form-body">
								<div class="layout-system-report" id="ux_system_information">
									<textarea id="ux_txtarea_system_information" name="ux_txtarea_system_information" readonly="readonly"></textarea>
								</div>
								<div class="form-actions">
									<div class="btn-set pull-right">
										<button type="button" class="btn vivid-green  system-report" name="ux_btn_system_information"  id="ux_btn_system_information">Get System Information!</button>
									</div>
								</div>
								<div class="custom-form-body">
									<h3 class="form-section">
										Server Information
									</h3>
									<table class="table table-striped table-bordered table-hover" >
										<thead class="align-thead-left">
											<tr>
												<th class="custom-table-th-left" style="width: 40% !important;">
													Environment Key
												</th>
												<th class="custom-table-th-right">
													Environment Value
												</th>
											</tr>
										</thead>
										<tbody>
											<tr>
												<td>
													<strong>
														Home URL:
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( home_url() ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														Site URL:
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( site_url() ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														WP Version :
													</strong>
												</td>
												<td>
													<span>
														<?php echo bloginfo( 'version' ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														WP Multisite Enabled :
													</strong>
												</td>
												<td>
													<span>
														<?php
														if ( is_multisite() ) {
															echo 'Yes';
														} else {
															echo 'No';
														}
														?>
													</span>
												</td>
											</tr>
											<?php
											$request['cmd'] = '_notify-validate';
											$params         = array(
												'sslverify' => false,
												'timeout' => 60,
												'user-agent' => 'contact_bank',
												'body'    => $request,
											);
											$response       = wp_remote_post( 'https://www.paypal.com/cgi-bin/webscr', $params );
											?>
											<tr>
												<td>
													<strong>
														WP Remote Post :
													</strong>
												</td>
												<td>
													<span>
														<?php echo ( ! is_wp_error( $response ) ) ? 'Success' : 'Failed'; ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														Web Server Info :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_html( isset( $_SERVER['SERVER_SOFTWARE'] ) ? wp_unslash( filter_input( INPUT_SERVER, 'SERVER_SOFTWARE' ) ) : '' );// WPCS: input var ok. ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														PHP Version :
													</strong>
												</td>
												<td>
													<span>
														<?php
														if ( function_exists( 'phpversion' ) ) {
															echo esc_html( phpversion() );
														}
														?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														MySQL Version :
													</strong>
												</td>
												<td>
													<span>
														<?php
														global $wpdb;
														echo esc_attr( $wpdb->db_version() );
														?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														WP Debug Mode :
													</strong>
												</td>
												<td>
													<span>
														<?php
														if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
															echo 'Yes';
														} else {
															echo 'No';
														}
														?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														WP Language :
													</strong>
												</td>
												<td>
													<span>
														<?php
														if ( defined( 'WPLANG' ) && WPLANG ) {
															echo esc_attr( WPLANG );
														} else {
															echo esc_attr( get_locale() );
														}
														?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														WP Max Upload Size :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( size_format( wp_max_upload_size() ) ); ?>
													</span>
												</td>
											</tr>
											<?php if ( function_exists( 'ini_get' ) ) : ?>
												<tr>
													<td>
														<strong>
															PHP Max Script Execute Time :
														</strong>
													</td>
													<td>
														<span>
															<?php echo esc_attr( ini_get( 'max_execution_time' ) ); ?>
														</span>
													</td>
												</tr>
												<tr>
													<td>
														<strong>
															PHP Max Input Vars :
														</strong>
													</td>
													<td>
														<span>
															<?php echo esc_attr( ini_get( 'max_input_vars' ) ); ?>
														</span>
													</td>
												</tr>
												<tr>
													<td>
														<strong>
															SUHOSIN Installed :
														</strong>
													</td>
													<td>
														<span>
															<?php echo extension_loaded( 'suhosin' ) ? 'Yes' : 'No'; ?>
														</span>
													</td>
												</tr>
											<?php endif; ?>
											<tr>
												<td>
													<strong>
														Default Timezone :
													</strong>
												</td>
												<td>
													<span>
														<?php
														$timezone = date_default_timezone_get();
														if ( 'UTC' !== $timezone ) {
															echo sprintf( 'Default timezone is %s - it should be UTC', esc_attr( $timezone ) );
														} else {
															echo sprintf( 'Default timezone is %s', esc_attr( $timezone ) );
														}
														?>
													</span>
												</td>
											</tr>
											<?php
											global $wpdb, $lab;
											// Get MYSQL Version.
											$sql_version = $wpdb->get_var( 'SELECT VERSION() AS version' ); // db call ok; no-cache ok.
											// GET SQL Mode.
											$my_sql_info = $wpdb->get_results( 'SHOW VARIABLES LIKE "sql_mode"' ); // db call ok; no-cache ok.
											if ( is_array( $my_sql_info ) ) {
												$sqlmode = $my_sql_info[0]->Value;
											}
											if ( empty( $sqlmode ) ) {
												$sqlmode = 'Not set';
											}
											// Get PHP Safe Mode.
											if ( ini_get( 'safemode' ) ) {
												$safemode = 'On';
											} else {
												$safemode = 'Off';
											}
											// Get PHP allow_url_fopen.
											if ( ini_get( 'allow-url-fopen' ) ) {
												$allowurlfopen = 'On';
											} else {
												$allowurlfopen = 'Off';
											}
											// Get PHP Max Upload Size.
											if ( ini_get( 'upload_max_filesize' ) ) {
												$upload_maximum = ini_get( 'upload_max_filesize' );
											} else {
												$upload_maximum = 'N/A';
											}
											// Get PHP Output buffer Size.
											if ( ini_get( 'pcre.backtrack_limit' ) ) {
												$backtrack_lmt = ini_get( 'pcre.backtrack_limit' );
											} else {
												$backtrack_lmt = 'N/A';
											}
											// Get PHP Max Post Size.
											if ( ini_get( 'post_max_size' ) ) {
												$post_maximum = ini_get( 'post_max_size' );
											} else {
												$post_maximum = 'N/A';
											}
											// Get PHP Memory Limit.
											if ( ini_get( 'memory_limit' ) ) {
												$memory_limit = ini_get( 'memory_limit' );
											} else {
												$memory_limit = 'N/A';
											}
											// Get actual memory_get_usage.
											if ( function_exists( 'memory_get_usage' ) ) {
												$memory_usage = round( memory_get_usage() / 1024 / 1024, 2 ) . ' MByte';
											} else {
												$memory_usage = 'N/A';
											}
											// required for EXIF read.
											if ( is_callable( 'exif_read_data' ) ) {
												$exif = 'Yes ( V' . substr( phpversion( 'exif' ), 0, 4 ) . ')';
											} else {
												$exif = 'No';
											}
											// required for meta data.
											if ( is_callable( 'iptcparse' ) ) {
												$iptc = 'Yes';
											} else {
												$iptc = 'No';
											}
											// required for meta data.
											if ( is_callable( 'xml_parser_create' ) ) {
												$xml = 'Yes';
											} else {
												$xml = 'No';
											}
											?>
											<tr>
												<td>
													<strong>
														Operating System :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( PHP_OS ); ?>&nbsp;(<?php echo( esc_attr( PHP_INT_SIZE ) * 8 ); ?>&nbsp;Bit)
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														Memory usage :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $memory_usage ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														SQL Mode :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $sqlmode ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														PHP Safe Mode :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $safemode ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														PHP Allow URL fopen :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $allowurlfopen ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														PHP Memory Limit :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $memory_limit ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														PHP Max Post Size :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $post_maximum ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														PCRE Backtracking Limit :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $backtrack_lmt ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														PHP Exif support :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $exif ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														PHP IPTC support :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $iptc ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>
														PHP XML support :
													</strong>
												</td>
												<td>
													<span>
														<?php echo esc_attr( $xml ); ?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>Extensions :</strong>
												</td>
												<td>
													<span>
														<?php
														if ( function_exists( 'get_loaded_extensions' ) ) {
															$count = count( get_loaded_extensions() );
															$i     = 0;
															foreach ( get_loaded_extensions() as $extension ) {
																$seprator = ++$i !== $count ? ', ' : '.';
																echo $extension . $seprator; // XSS ok.
															}
														}
														?>
													</span>
												</td>
											</tr>
											<tr>
												<td>
													<strong>Apache Modules :</strong>
												</td>
												<td>
													<span>
														<?php
														if ( function_exists( 'apache_get_modules' ) ) {
															$count = count( apache_get_modules() );
															$i     = 0;
															foreach ( apache_get_modules() as $module ) {
																$seprator = ++$i !== $count ? ', ' : '.';
																echo $module . $seprator; // XSS ok.
															}
														}
														?>
													</span>
												</td>
											</tr>
										</tbody>
									</table>
								</div>
								<div class="custom-form-body">
									<h3 class="form-section">
										Active  Plugin Information
									</h3>
									<table class="table table-striped table-bordered table-hover">
										<thead class="align-thead-left">
											<tr>
												<th class="custom-table-th-left" style="width: 40% !important;">
													Plugin Key
												</th>
												<th class="custom-table-th-right">
													Plugin Value
												</th>
											</tr>
										</thead>
										<tbody>
											<?php
											$active_plugins = (array) get_option( 'active_plugins', array() );
											if ( is_multisite() ) {
												$active_plugins = array_merge( $active_plugins, get_site_option( 'active_sitewide_plugins', array() ) );
											}
											$get_plugins = array();
											foreach ( $active_plugins as $plugin ) {
												$plugin_data    = @get_plugin_data( WP_PLUGIN_DIR . '/' . $plugin ); // @codingStandardsIgnoreLine.
												$version_string = '';
												if ( ! empty( $plugin_data['Name'] ) ) {
													$plugin_name = $plugin_data['Name'];
													if ( ! empty( $plugin_data['PluginURI'] ) ) {
														$plugin_name = '<tr><td><strong>' . $plugin_name . ' :</strong></td><td><span> By ' . $plugin_data['Author'] . '<br/> Version ' . $plugin_data['Version'] . $version_string . '</span></td></tr>';
													}
													echo $plugin_name; // WPCS: XSS ok.
												}
											}
											?>
										</tbody>
									</table>
								</div>
								<?php
								global $wp_version;
								if ( $wp_version >= 3.4 ) {
									$active_theme = wp_get_theme();
									?>
									<div class="custom-form-body">
										<h3 class="form-section">
											Active Theme Information
										</h3>
										<table class="table table-striped table-bordered table-hover">
											<thead class="align-thead-left">
												<tr>
													<th style="width: 40% !important;" class="custom-table-th-left">
														Theme Key
													</th>
													<th class="custom-table-th-right">
														Theme Value
													</th>
												</tr>
											</thead>
											<tbody>
												<tr>
													<td>
														<strong>
															Theme Name :
														</strong>
													</td>
													<td>
														<span>
															<?php echo esc_attr( $active_theme->name ); ?>
														</span>
													</td>
												</tr>
												<tr>
													<td>
														<strong>
															Theme Version :
														</strong>
													</td>
													<td>
														<span>
															<?php echo esc_attr( $active_theme->version ); ?>
														</span>
													</td>
												</tr>
												<tr>
													<td>
														<strong>
															Author URL :
														</strong>
													</td>
													<td>
														<span>
															<a href="<?php echo esc_attr( $active_theme->{'Author URI'} ); ?>"
																target="_blank"><?php echo esc_attr( $active_theme->{'Author URI'} ); ?>
															</a>
														</span>
													</td>
												</tr>
											</tbody>
										</table>
									</div>
									<?php
								}
								?>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
	<?php
	} else {
		?>
		<div class="page-bar">
			<ul class="page-breadcrumb">
				<li>
					<i class="icon-custom-home"></i>
					<a href="admin.php?page=contact_dashboard">
						<?php echo esc_attr( $cb_contact_bank ); ?>
					</a>
					<span>></span>
				</li>
				<li>
					<span>
						<?php echo esc_attr( $cb_system_information ); ?>
					</span>
				</li>
			</ul>
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="portlet box vivid-green">
					<div class="portlet-title">
						<div class="caption">
							<i class="icon-custom-screen-desktop"></i>
							<?php echo esc_attr( $cb_system_information ); ?>
						</div>
					</div>
					<div class="portlet-body form">
						<div class="form-body">
							<strong><?php echo esc_attr( $cb_user_access_message ); ?></strong>
						</div>
					</div>
				</div>
			</div>
		</div>
		<?php
	}
}
