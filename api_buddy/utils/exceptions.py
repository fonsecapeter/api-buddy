import random
from typing import NoReturn
from api_buddy.utils import PREFS_FILE


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


class PrefsException(APIBuddyException):
    TITLE_HEADERS = (
        'There\'s a problem with your preferences',
        'Your preferences appear to be borked',
        'Your preferences aren\'t quite right',
        'Your preferences are a bit off',
        'It looks like your preferences are messed up',
    )
    MESSAGE_FOOTERS = (
        f'Open up {PREFS_FILE}',
        f'Crack open {PREFS_FILE}',
        f'Check out {PREFS_FILE}',
        f'Take a look at {PREFS_FILE}',
    )

    def __init__(self, title: str, message: str) -> None:
        header = random.choice(self.TITLE_HEADERS)
        footer = random.choice(self.MESSAGE_FOOTERS)
        prefs_title = f'{header}.\n{title}'
        prefs_msg = f'{message}.\n{footer}'
        return super().__init__(prefs_title, prefs_msg)
