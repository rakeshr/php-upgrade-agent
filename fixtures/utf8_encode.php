<?php

function normalize_title(string $title): string {
    return utf8_encode($title);
}

function decode_title(string $title): string {
    return utf8_decode($title);
}
