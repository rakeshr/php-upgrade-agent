<?php

function save_meta(string $key, string $value = null): void {
    if ($value === null) {
        return;
    }
    update_option($key, $value);
}
