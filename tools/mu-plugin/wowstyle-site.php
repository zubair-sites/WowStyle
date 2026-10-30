<?php
/**
 * Plugin Name: The Wow Style – site tweaks
 * Description: Brand styles on top of the Kayleen theme, author avatar fallback and light security hardening. Source: github.com/zubair-sites/WowStyle (tools/mu-plugin).
 * Version: 1.0.0
 */

defined( 'ABSPATH' ) || exit;

/* ------------------------------------------------------------------------
 * Brand styles: one palette (ink, ivory, stone, taupe) for theme parts that
 * have no colour option of their own.
 * --------------------------------------------------------------------- */
add_action( 'wp_enqueue_scripts', function () {
	$css = <<<'CSS'
:root { --wow-ink:#111111; --wow-ivory:#F7F4EF; --wow-stone:#E9E3DA; --wow-taupe:#8C7A66; --wow-line:#DDD5CA; }
::selection { background: var(--wow-ink); color: var(--wow-ivory); }

/* Share buttons: monochrome instead of each network's colour */
.single-share-box a, .single-share-box .share-link-btn { background: transparent !important; color: var(--wow-ink) !important;
  border: 1px solid var(--wow-line) !important; border-radius: 0 !important; box-shadow: none !important; }
.single-share-box a:hover, .single-share-box .share-link-btn:hover { background: var(--wow-ink) !important; color: var(--wow-ivory) !important; border-color: var(--wow-ink) !important; }
.single-share-box-container .title, .single-next-prev-posts-title, .comments-title, .comment-reply-title { font-family: "Bodoni Moda", serif; font-weight: 500; }

/* Author box */
.single-author-box-avatar img { border-radius: 0 !important; box-shadow: none !important; }
.single-author-box-desc .button.more-articles, .button, button, input[type=submit] { border-radius: 0 !important; box-shadow: none !important; }
.single-author-box-desc .button.more-articles { background: var(--wow-ink) !important; color: var(--wow-ivory) !important; letter-spacing: .12em; text-transform: uppercase; font-size: 11px; }
.single-author-box-desc .written-by { color: var(--wow-taupe); letter-spacing: .2em; text-transform: uppercase; font-size: 11px; }
.comments-list-collapse-btn { background: var(--wow-ink) !important; color: var(--wow-ivory) !important; border-radius: 0 !important; box-shadow: none !important; }

/* Category badge on posts and archive title box */
.single-hero-title-1 .category a, .single-hero-title-2 .category a { border-radius: 0 !important; letter-spacing: .14em; text-transform: uppercase; font-size: 11px; }
.blog-archive-title { background: var(--wow-ivory) !important; border: 0 !important; border-radius: 0 !important; box-shadow: none !important; }
.blog-archive-title .title { font-family: "Bodoni Moda", serif; }

/* Article typography */
.single-content, .entry-content { font-size: 1.05rem; line-height: 1.8; }
.single-content h2, .entry-content h2 { margin-top: 2.2em; }
.single-content a, .entry-content a { text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1px; }
.single-content blockquote, .entry-content blockquote { border-left: 2px solid var(--wow-ink); background: var(--wow-ivory); }

/* "Quick answer" summary box at the top of articles */
.wow-quick-answer { background: var(--wow-ivory); border-left: 2px solid var(--wow-ink); padding: 22px 26px; margin: 0 0 2em; }
.wow-quick-answer p { margin: 0; }
.wow-quick-answer strong:first-child { display: block; font-family: Jost, sans-serif; font-size: 12px; letter-spacing: .2em; text-transform: uppercase; color: var(--wow-taupe); margin-bottom: 8px; }

/* Rank Math FAQ block */
.rank-math-faq-item { border-top: 1px solid var(--wow-line); padding: 18px 0 4px; }
.rank-math-faq-item:last-child { border-bottom: 1px solid var(--wow-line); }
.rank-math-question { font-size: 1.15rem !important; margin: 0 0 8px !important; }

/* Page title for standard pages */
.wow-page-header { text-align: center; padding: 70px 0 50px; margin-bottom: 40px; border-bottom: 1px solid var(--wow-line); }
.wow-page-title { font-family: "Bodoni Moda", serif; font-weight: 500; font-size: clamp(34px, 5vw, 54px); line-height: 1.1; margin: 0; }

/* Comfortable side margins for articles and pages on phones */
@media (max-width: 767px) { .content-wrapper > .container { padding-left: 20px; padding-right: 20px; } }

/* Forms */
input[type=text], input[type=email], input[type=url], input[type=search], textarea { border-radius: 0 !important; border-color: var(--wow-line) !important; }
input:focus, textarea:focus { border-color: var(--wow-ink) !important; outline: none; }
CSS;
	wp_register_style( 'wowstyle-brand', false, array(), '1.0.0' );
	wp_enqueue_style( 'wowstyle-brand' );
	wp_add_inline_style( 'wowstyle-brand', $css );
}, 100 );

/* The theme's page.php has its title commented out, so standard (non-Elementor)
 * pages have no H1. Add one at the top of the content. */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_page() || ! in_the_loop() || ! is_main_query() || 'builder' === get_post_meta( get_the_ID(), '_elementor_edit_mode', true ) ) {
		return $content;
	}
	return '<header class="wow-page-header"><h1 class="wow-page-title">' . esc_html( get_the_title() ) . '</h1></header>' . $content;
}, 5 );

/* Plainer wording for the author box button. */
add_filter( 'gettext', function ( $translation, $text ) {
	return 'Follow Me' === $text ? 'More articles' : $translation;
}, 10, 2 );

/* ------------------------------------------------------------------------
 * Author avatar: use the brand icon until the author uploads a photo.
 * --------------------------------------------------------------------- */
add_filter( 'pre_get_avatar_data', function ( $args, $id_or_email ) {
	$user_id = $id_or_email instanceof WP_User ? $id_or_email->ID : ( is_numeric( $id_or_email ) ? (int) $id_or_email : 0 );
	if ( $id_or_email instanceof WP_Comment ) {
		$user_id = (int) $id_or_email->user_id;
	} elseif ( is_string( $id_or_email ) && is_email( $id_or_email ) ) {
		$user    = get_user_by( 'email', $id_or_email );
		$user_id = $user ? $user->ID : 0;
	}
	$photo = $user_id ? (int) get_user_meta( $user_id, 'wowstyle_avatar_id', true ) : 0;
	if ( ! $photo && 1 === $user_id ) {
		$photo = (int) get_option( 'site_icon' );
	}
	if ( $photo && ( $src = wp_get_attachment_image_url( $photo, 'thumbnail' ) ) ) {
		$args['url']          = $src;
		$args['found_avatar'] = true;
	}
	return $args;
}, 10, 2 );

/* ------------------------------------------------------------------------
 * Hardening
 * --------------------------------------------------------------------- */
add_filter( 'xmlrpc_enabled', '__return_false' );
add_filter( 'the_generator', '__return_empty_string' );
remove_action( 'wp_head', 'wp_generator' );

// Stop ?author=N from revealing login names.
add_action( 'template_redirect', function () {
	if ( isset( $_GET['author'] ) && ! is_user_logged_in() ) {
		wp_safe_redirect( home_url( '/' ), 301 );
		exit;
	}
}, 1 ); // before redirect_canonical()

// Hide the user list from the public REST API (logged-in editors still have it).
add_filter( 'rest_endpoints', function ( $endpoints ) {
	if ( ! is_user_logged_in() ) {
		unset( $endpoints['/wp/v2/users'], $endpoints['/wp/v2/users/(?P<id>[\d]+)'] );
	}
	return $endpoints;
} );
