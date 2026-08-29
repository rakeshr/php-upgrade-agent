<?php

function greet_user(string $name): string {
    $message = "Hello ${name}, welcome back.";
    return $message;
}
