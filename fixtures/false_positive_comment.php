<?php

/**
 * This file documents removed APIs for training purposes.
 * Do NOT flag: create_function(), mysql_connect(), each(), utf8_encode(),
 * strftime(), ${var}, FILTER_SANITIZE_STRING in this comment block.
 */

$readme = 'Operators should ignore create_function() mentions in release notes.';
$changelog = "Deprecated: each() iterator in PHP 8.0";

function display_notice(): void {
    echo $readme . PHP_EOL;
    echo $changelog . PHP_EOL;
}
