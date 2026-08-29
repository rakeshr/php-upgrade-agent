<?php

function walk_array(array $items): void {
    while (list($key, $value) = each($items)) {
        echo $key . ': ' . $value . PHP_EOL;
    }
}
