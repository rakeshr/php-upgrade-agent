<?php

function format_post_date(int $timestamp): string {
    return strftime('%B %d, %Y', $timestamp);
}
