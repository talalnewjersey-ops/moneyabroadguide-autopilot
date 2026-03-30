<?php
/**
 * Plugin Name: MAG Autopilot Connector
 * Description: Connects WordPress with GitHub Autopilot system
 * Version: 1.0
 */

if (!defined('ABSPATH')) exit;

// 🔐 TA CLÉ API ICI
define('MAG_API_KEY', 'MAG_2026_Talal_Secure_80..@@$$RaAmMeTA');

// STATUS
add_action('rest_api_init', function () {
    register_rest_route('mag/v1', '/status', [
        'methods' => 'GET',
        'callback' => function () {
            return [
                'status' => 'connected',
                'site' => get_bloginfo('name'),
                'url' => home_url()
            ];
        }
    ]);
});
