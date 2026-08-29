<?php

function sanitize_legacy_input(string $raw): string {
    return filter_var($raw, FILTER_SANITIZE_STRING);
}
