<?php

function connect_legacy_db() {
    $link = mysql_connect('localhost', 'root', 'secret');
    mysql_select_db('wordpress', $link);
    $result = mysql_query('SELECT ID FROM wp_posts LIMIT 1', $link);
    $row = mysql_fetch_assoc($result);
    mysql_close($link);
    return $row;
}
