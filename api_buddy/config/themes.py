from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
)

SHELLECTRIC = 'shellectric'
BRIGHT_BLUE = 'ansibrightblue'
BRIGHT_CYAN = 'ansibrightcyan'
BRIGHT_GREEN = 'ansibrightgreen'
BRIGHT_MAGENTA = 'ansibrightmagenta'
BRIGHT_RED = 'ansibrightred'
BRIGHT_YELLOW = 'ansibrightyellow'
GRAY = 'ansigray'
YELLOW = 'ansiyellow'


class Shellectric(Style):  # type: ignore
    default_style = ""
    styles = {
        Comment: GRAY,
        Error: BRIGHT_YELLOW,
        Keyword: BRIGHT_GREEN,
        Keyword.Constant: BRIGHT_CYAN,
        Keyword.Namespace: GRAY,
        Keyword.Pseudo: GRAY,
        Literal: BRIGHT_RED,
        Name: YELLOW,
        Name.Builtin.Pseudo: GRAY,
        Name.Class: BRIGHT_CYAN,
        Name.Decorator: BRIGHT_CYAN,
        Name.Exception: BRIGHT_CYAN,
        Name.Function: BRIGHT_CYAN,
        Name.Tag: BRIGHT_YELLOW,
        Number: BRIGHT_BLUE,
        Operator: GRAY,
        Punctuation: GRAY,
        String: BRIGHT_RED,
        String.Other: YELLOW,
        Text: BRIGHT_MAGENTA,
    }
