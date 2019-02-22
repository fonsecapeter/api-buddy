import random
from typing import NoReturn


class APIBuddyException(Exception):
    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message


def exit_with_exception(err: APIBuddyException) -> NoReturn:
    emoji = random.choice((
        '⚠️',
        '😭',
        '😮',
        '🙊',
        '🐛',
        '🔥',
    ))
    pleasantry = random.choice((
        'Oh no',
        'Whoops',
        'Oops',
        'Crikey',
        'Dang',
    ))
    print(f'{pleasantry}!\n{err.title} {emoji}\n{err.message}')
    exit(1)
