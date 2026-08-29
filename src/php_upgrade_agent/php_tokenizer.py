"""Lightweight PHP lexer for comment/string-aware scanning."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


class TokenKind(str, Enum):
    CODE = "code"
    COMMENT = "comment"
    STRING = "string"
    HEREDOC = "heredoc"


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    text: str
    start: int
    line: int


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def tokenize_php(source: str) -> list[Token]:
    """Split PHP source into code, comment, and string regions."""
    tokens: list[Token] = []
    i = 0
    n = len(source)
    while i < n:
        if source.startswith("<?php", i) or source.startswith("<?=", i):
            tag = "<?=" if source.startswith("<?=", i) else "<?php"
            tokens.append(Token(TokenKind.CODE, tag, i, _line_of(source, i)))
            i += len(tag)
            continue

        if source.startswith("//", i):
            start = i
            line = _line_of(source, i)
            while i < n and source[i] != "\n":
                i += 1
            tokens.append(Token(TokenKind.COMMENT, source[start:i], start, line))
            continue

        if source.startswith("#", i):
            start = i
            line = _line_of(source, i)
            while i < n and source[i] != "\n":
                i += 1
            tokens.append(Token(TokenKind.COMMENT, source[start:i], start, line))
            continue

        if source.startswith("/*", i):
            start = i
            line = _line_of(source, i)
            end = source.find("*/", i + 2)
            if end == -1:
                end = n
            else:
                end += 2
            tokens.append(Token(TokenKind.COMMENT, source[start:end], start, line))
            i = end
            continue

        if source[i] in "\"'":
            quote = source[i]
            start = i
            line = _line_of(source, i)
            i += 1
            while i < n:
                ch = source[i]
                if ch == "\\":
                    i += 2
                    continue
                if ch == quote:
                    i += 1
                    break
                i += 1
            tokens.append(Token(TokenKind.STRING, source[start:i], start, line))
            continue

        heredoc = re.match(
            r"<<<['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?\s*\n",
            source[i:],
        )
        if heredoc:
            label = heredoc.group(1)
            start = i
            line = _line_of(source, i)
            i += heredoc.end()
            pattern = re.compile(rf"^\s*{re.escape(label)}\s*;\s*$", re.MULTILINE)
            match = pattern.search(source, i)
            end = match.end() if match else n
            tokens.append(Token(TokenKind.HEREDOC, source[start:end], start, line))
            i = end
            continue

        start = i
        line = _line_of(source, i)
        while i < n:
            if source.startswith("//", i) or source.startswith("/*", i) or source[i] in "\"'":
                break
            if source.startswith("<<<", i):
                break
            if source[i] == "#" and (i == 0 or source[i - 1] != "\\"):
                break
            i += 1
        if i == start:
            i += 1
        tokens.append(Token(TokenKind.CODE, source[start:i], start, line))

    return tokens


def code_regions(source: str) -> list[tuple[str, int]]:
    """Return (code_text, base_line) slices safe for pattern matching."""
    regions: list[tuple[str, int]] = []
    for token in tokenize_php(source):
        if token.kind == TokenKind.CODE:
            regions.append((token.text, token.line))
    return regions


def line_at_offset(source: str, offset: int) -> int:
    return _line_of(source, offset)
