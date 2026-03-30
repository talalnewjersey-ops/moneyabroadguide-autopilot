<?php
/**
 * Plugin Name: MAG Autopilot Connector
 * Description: Connects WordPress with GitHub Autopilot system
 * Version: 1.0
 */

if (!defined('MAG_2026_Talal_Secure_80..@@$$RaAmMeTA')) exit;

// STATUS TEST
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

// GET POSTS
add_action('rest_api_init', function () {
    register_rest_route('mag/v1', '/posts', [
        'methods' => 'GET',
        'callback' => function () {

            $posts = get_posts(['numberposts' => 5]);

            $data = [];

            foreach ($posts as $post) {
                $data[] = [
                    'id' => $post->ID,
                    'title' => $post->post_title,
                    'content' => $post->post_content
                ];
            }

            return $data;
        }
    ]);
});
