<?php

function legacy_bootstrap(): void {
    $link = mysql_connect('db', 'wp', 'pass');
    mysql_select_db('clientsite', $link);

    $handler = create_function('$x', 'return strtoupper($x);');
    $title = utf8_encode("Launch ${brand}");

    while (list(, $row) = each($_POST)) {
        $clean = filter_var($row, FILTER_SANITIZE_STRING);
        echo strftime('%Y-%m-%d', time()) . $clean;
    }

    mysql_close($link);
}

function legacy_optional(string $note = null): void {
    echo $note ?? 'n/a';
}
