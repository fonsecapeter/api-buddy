import requests
from typing import Callable, Dict
from .auth.oauth2 import get_oauth2_session, reauthenticate_oauth2
from ..utils.typing import Options, Preferences
from ..utils.auth import OAUTH2

SessionInitializer = Callable[
    [Options, Preferences, str],
    requests.Session,
]
SESSIONS: Dict[str, SessionInitializer] = {
    OAUTH2: get_oauth2_session,
}
ReauthenticatStrategy = Callable[
    [requests.Session, Preferences, str],
    requests.Session,
]
REAUTHENTICATIONS: Dict[str, ReauthenticatStrategy] = {
    OAUTH2: reauthenticate_oauth2,
}


def get_session(
            opts: Options,
            prefs: Preferences,
            prefs_file_name: str,
        ) -> requests.Session:
    auth_type = prefs['auth_type']
    if auth_type is None:
        return requests.Session()
    session_initializer = SESSIONS[auth_type]
    sesh = session_initializer(opts, prefs, prefs_file_name)
    sesh.headers.update(prefs['headers'])
    return sesh


def reauthenticate(
            sesh: requests.Session,
            prefs: Preferences,
            prefs_file: str,
        ) -> requests.Session:
    auth_type = prefs['auth_type']
    if auth_type is None:
        return sesh
    reauthenticate_strategy = REAUTHENTICATIONS[auth_type]
    new_sesh = reauthenticate_strategy(sesh, prefs, prefs_file)
    new_sesh.headers.update(prefs['headers'])
    return new_sesh
