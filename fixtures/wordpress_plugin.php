<?php
/**
 * Plugin Name: Acme Event Widget
 * Description: Small calendar widget for agency client sites.
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('widgets_init', function () {
    register_widget('Acme_Event_Widget');
});

class Acme_Event_Widget extends WP_Widget {
    public function widget($args, $instance) {
        $title = apply_filters('widget_title', $instance['title'] ?? 'Events');
        echo $args['before_widget'];
        echo esc_html($title);
        echo $args['after_widget'];
    }
}

function acme_get_events(): array {
    return get_posts([
        'post_type' => 'event',
        'posts_per_page' => 5,
        'no_found_rows' => true,
    ]);
}
