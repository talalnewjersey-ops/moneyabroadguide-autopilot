// 📄 GET POSTS (SECURED)
add_action('rest_api_init', function () {
    register_rest_route('mag/v1', '/posts', [
        'methods' => 'GET',
        'callback' => function (\WP_REST_Request $request) {

            // 🔐 Vérifier API KEY
            $api_key = $request->get_header('x-mag-api-key');

            if ($api_key !== MAG_API_KEY) {
                return new WP_Error(
                    'forbidden',
                    'Invalid API Key',
                    ['status' => 403]
                );
            }

            // 📄 Récupérer articles
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
