"""Offset helpers for comment/string classification."""

from __future__ import annotations

from php_upgrade_agent.php_tokenizer import TokenKind, tokenize_php


def offset_in_non_code(source: str, offset: int) -> bool:
    for token in tokenize_php(source):
        if token.start <= offset < token.start + len(token.text):
            return token.kind != TokenKind.CODE
    return False


def line_is_only_non_code(source: str, line_no: int) -> bool:
    """True when every token touching this line is comment or string."""
    touched_code = False
    touched_non_code = False
    for token in tokenize_php(source):
        start_line = source.count("\n", 0, token.start) + 1
        end_line = source.count("\n", 0, token.start + len(token.text) - 1) + 1
        if start_line <= line_no <= end_line:
            if token.kind == TokenKind.CODE and token.text.strip():
                touched_code = True
            elif token.kind != TokenKind.CODE:
                touched_non_code = True
    return touched_non_code and not touched_code
