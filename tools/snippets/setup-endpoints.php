// Temporary admin-only REST endpoints used during site setup. Remove when setup is done.
add_action( 'rest_api_init', function () {
	$admin = function () { return current_user_can( 'manage_options' ); };

	register_rest_route( 'wowstyle/v1', '/option', array(
		array( 'methods' => 'GET', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			return array( 'value' => get_option( $r['name'] ) );
		} ),
		array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$value = $r->get_json_params()['value'];
			if ( null === $value ) { return array( 'deleted' => delete_option( $r['name'] ) ); }
			return array( 'updated' => update_option( $r['name'], $value ) );
		} ),
	) );

	register_rest_route( 'wowstyle/v1', '/options', array(
		'methods' => 'GET', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			global $wpdb;
			return $wpdb->get_col( $wpdb->prepare(
				"SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE %s ORDER BY option_name",
				'%' . $wpdb->esc_like( $r['search'] ) . '%'
			) );
		},
	) );

	register_rest_route( 'wowstyle/v1', '/meta', array(
		array( 'methods' => 'GET', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			return $r['key'] ? array( 'value' => get_post_meta( (int) $r['post'], $r['key'], true ) )
				: array( 'keys' => array_keys( get_post_meta( (int) $r['post'] ) ) );
		} ),
		array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$p = $r->get_json_params();
			if ( null === $p['value'] ) { return array( 'deleted' => delete_post_meta( (int) $p['post'], $p['key'] ) ); }
			$value = is_string( $p['value'] ) ? wp_slash( $p['value'] ) : $p['value'];
			update_post_meta( (int) $p['post'], $p['key'], $value );
			if ( class_exists( '\Elementor\Plugin' ) ) { \Elementor\Plugin::$instance->files_manager->clear_cache(); }
			return array( 'updated' => true );
		} ),
	) );

	// Read-only grep inside the theme or its addon plugin, to look up widget control names.
	register_rest_route( 'wowstyle/v1', '/grep', array(
		'methods' => 'GET', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$base = realpath( 'theme' === $r['dir'] ? get_template_directory() : WP_PLUGIN_DIR . '/rivax-addon' );
			$out  = array();
			$it   = new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $base ) );
			foreach ( $it as $file ) {
				if ( substr( $file, -4 ) !== '.php' ) { continue; }
				foreach ( file( $file ) as $n => $line ) {
					if ( false !== stripos( $line, $r['q'] ) ) {
						$out[] = str_replace( $base, '', $file ) . ':' . ( $n + 1 ) . ': ' . trim( $line );
					}
				}
			}
			return array_slice( $out, 0, 200 );
		},
	) );

	// Install the site's must-use plugin (wp-content/mu-plugins/wowstyle-site.php).
	register_rest_route( 'wowstyle/v1', '/mu-plugin', array(
		'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			wp_mkdir_p( WPMU_PLUGIN_DIR );
			$bytes = file_put_contents( WPMU_PLUGIN_DIR . '/wowstyle-site.php', $r->get_json_params()['content'] );
			return array( 'written' => $bytes );
		},
	) );

	// Remove files that reveal the WordPress version.
	register_rest_route( 'wowstyle/v1', '/cleanup', array(
		'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function () {
			$out = array();
			foreach ( array( 'readme.html', 'wp-config-sample.php' ) as $f ) {
				$out[ $f ] = file_exists( ABSPATH . $f ) ? unlink( ABSPATH . $f ) : 'missing';
			}
			return $out;
		},
	) );

	// Rebuild rewrite rules (same as saving Settings → Permalinks).
	register_rest_route( 'wowstyle/v1', '/flush', array(
		'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function () {
			delete_option( 'rewrite_rules' );
			add_action( 'shutdown', 'flush_rewrite_rules' );
			return array( 'scheduled' => true );
		},
	) );

	// Install a language pack and switch the site language (Settings → General → Site Language).
	register_rest_route( 'wowstyle/v1', '/language', array(
		'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			require_once ABSPATH . 'wp-admin/includes/file.php';
			require_once ABSPATH . 'wp-admin/includes/translation-install.php';
			$locale    = sanitize_text_field( $r->get_json_params()['locale'] );
			$installed = wp_download_language_pack( $locale );
			if ( $installed ) { update_option( 'WPLANG', $installed ); }
			return array( 'installed' => $installed, 'WPLANG' => get_option( 'WPLANG' ) );
		},
	) );

	register_rest_route( 'wowstyle/v1', '/term-meta', array(
		'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$p = $r->get_json_params();
			return array( 'updated' => (bool) update_term_meta( (int) $p['term'], $p['key'], $p['value'] ) );
		},
	) );

	register_rest_route( 'wowstyle/v1', '/user-meta', array(
		'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$p = $r->get_json_params();
			return array( 'updated' => (bool) update_user_meta( (int) $p['user'], $p['key'], $p['value'] ) );
		},
	) );
} );
