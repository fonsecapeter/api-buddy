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


class Shellectric(Style):  # type: ignore
    default_style = ""
    styles = {
        Text: '#ansifuchsia',
        Comment: '#ansilightgray',
        Keyword: '#ansigreen',
        Keyword.Constant: '#ansiturquoise',  # constant
        Keyword.Namespace: '#ansilightgray',
        Keyword.Pseudo: '#ansilightgray',
        Name: '#ansibrown',
        Name.Builtin.Pseudo: '#ansilightgray',  # self
        Name.Function: '#ansiturquoise',
        Name.Class: '#ansiturquoise',
        Name.Exception: '#ansiturquoise',
        Name.Decorator: '#ansiturquoise',
        String: '#ansired',
        String.Other: '#ansibrown',
        Literal: '#ansired',
        Number: '#ansiblue',
        Operator: '#ansilightgray',
        Error: '#ansiyellow',
        Punctuation: '#ansilightgray',
    }
