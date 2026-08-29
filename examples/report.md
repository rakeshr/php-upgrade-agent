# PHP Upgrade Readiness Report

**Decision:** NO-GO

Found 14 blocking error(s) and 9 warning(s). Resolve errors before upgrading to PHP 8.3+.

Files scanned: 12
Issues found: 23

## Issues

- `create_function.php:7` [error] **create_function** — create_function() was removed in PHP 8.0; use anonymous functions
  ```php
  add_filter('the_content', create_function('$content', 'return strtoupper($content);'));
  ```
- `dollar_brace_var.php:4` [warning] **dollar_brace_var** — ${var} string interpolation deprecated in PHP 8.2; use {$var}
  ```php
  $message = "Hello ${name}, welcome back.";
  ```
- `each_removed.php:4` [error] **each** — each() was removed in PHP 8.0; use foreach
  ```php
  while (list($key, $value) = each($items)) {
  ```
- `filter_sanitize_string.php:4` [error] **filter_sanitize_string** — FILTER_SANITIZE_STRING removed in PHP 8.1; use htmlspecialchars or custom filter
  ```php
  return filter_var($raw, FILTER_SANITIZE_STRING);
  ```
- `implicit_nullable.php:3` [warning] **implicit_nullable** — Implicit nullable parameter types deprecated in PHP 8.4; use ?Type
  ```php
  function save_meta(string $key, string $value = null): void {
  ```
- `multi_issue.php:4` [error] **mysql_extension** — mysql_* functions were removed in PHP 7.0; use mysqli or PDO
  ```php
  $link = mysql_connect('db', 'wp', 'pass');
  ```
- `multi_issue.php:5` [error] **mysql_extension** — mysql_* functions were removed in PHP 7.0; use mysqli or PDO
  ```php
  mysql_select_db('clientsite', $link);
  ```
- `multi_issue.php:7` [error] **create_function** — create_function() was removed in PHP 8.0; use anonymous functions
  ```php
  $handler = create_function('$x', 'return strtoupper($x);');
  ```
- `multi_issue.php:8` [warning] **dollar_brace_var** — ${var} string interpolation deprecated in PHP 8.2; use {$var}
  ```php
  $title = utf8_encode("Launch ${brand}");
  ```
- `multi_issue.php:8` [warning] **utf8_encode** — utf8_encode/decode deprecated in 8.2, removed in 8.4; use mb_convert_encoding
  ```php
  $title = utf8_encode("Launch ${brand}");
  ```
- `multi_issue.php:10` [error] **each** — each() was removed in PHP 8.0; use foreach
  ```php
  while (list(, $row) = each($_POST)) {
  ```
- `multi_issue.php:11` [error] **filter_sanitize_string** — FILTER_SANITIZE_STRING removed in PHP 8.1; use htmlspecialchars or custom filter
  ```php
  $clean = filter_var($row, FILTER_SANITIZE_STRING);
  ```
- `multi_issue.php:12` [warning] **strftime** — strftime() deprecated in PHP 8.1; use IntlDateFormatter or DateTime::format
  ```php
  echo strftime('%Y-%m-%d', time()) . $clean;
  ```
- `multi_issue.php:15` [error] **mysql_extension** — mysql_* functions were removed in PHP 7.0; use mysqli or PDO
  ```php
  mysql_close($link);
  ```
- `multi_issue.php:18` [warning] **implicit_nullable** — Implicit nullable parameter types deprecated in PHP 8.4; use ?Type
  ```php
  function legacy_optional(string $note = null): void {
  ```
- `mysql_legacy.php:4` [error] **mysql_extension** — mysql_* functions were removed in PHP 7.0; use mysqli or PDO
  ```php
  $link = mysql_connect('localhost', 'root', 'secret');
  ```
- `mysql_legacy.php:5` [error] **mysql_extension** — mysql_* functions were removed in PHP 7.0; use mysqli or PDO
  ```php
  mysql_select_db('wordpress', $link);
  ```
- `mysql_legacy.php:6` [error] **mysql_extension** — mysql_* functions were removed in PHP 7.0; use mysqli or PDO
  ```php
  $result = mysql_query('SELECT ID FROM wp_posts LIMIT 1', $link);
  ```
- `mysql_legacy.php:7` [error] **mysql_extension** — mysql_* functions were removed in PHP 7.0; use mysqli or PDO
  ```php
  $row = mysql_fetch_assoc($result);
  ```
- `mysql_legacy.php:8` [error] **mysql_extension** — mysql_* functions were removed in PHP 7.0; use mysqli or PDO
  ```php
  mysql_close($link);
  ```
- `strftime_deprecated.php:4` [warning] **strftime** — strftime() deprecated in PHP 8.1; use IntlDateFormatter or DateTime::format
  ```php
  return strftime('%B %d, %Y', $timestamp);
  ```
- `utf8_encode.php:4` [warning] **utf8_encode** — utf8_encode/decode deprecated in 8.2, removed in 8.4; use mb_convert_encoding
  ```php
  return utf8_encode($title);
  ```
- `utf8_encode.php:8` [warning] **utf8_encode** — utf8_encode/decode deprecated in 8.2, removed in 8.4; use mb_convert_encoding
  ```php
  return utf8_decode($title);
  ```
