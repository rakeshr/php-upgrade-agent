<?php

/**
 * Legacy callback registration using create_function (removed PHP 8.0).
 */
function register_legacy_filter() {
    add_filter('the_content', create_function('$content', 'return strtoupper($content);'));
}
