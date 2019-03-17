import json
from copy import deepcopy
from typing import Any, Callable, Dict, List, Union
from ..utils.typing import Options, Preferences


def _interpolate(thing: str, name: str, val: str) -> str:
    return thing.replace(f'#{{{name}}}', val)


def _interpolate_these(name: str, val: str) -> Callable[[str], str]:
    def wrapper(thing: str) -> str:
        return _interpolate(thing, name, val)
    return wrapper


def _interpolate_params(
            params: Dict[str, Union[str, List[str]]],
            name: str,
            val: str,
        ) -> Dict[str, Union[str, List[str]]]:
    interpolated_params: Dict[str, Union[str, List[str]]] = {}
    for query_name, query_val in params.items():
        if isinstance(query_val, list):
            interpolated_params[query_name] = list(map(
                _interpolate_these(name, val),
                query_val,
            ))
        else:  # is str
            interpolated_params[query_name] = _interpolate(
                query_val,
                name,
                val,
            )
    return interpolated_params


def _interpolate_data(
            data: Any,
            name: str,
            val: str,
        ) -> Any:
    # there's probably a faster way but eh this is safe / simple
    json_data = json.dumps(data)
    interpolated_json_data = _interpolate(json_data, name, val)
    return json.loads(interpolated_json_data)


def interpolate_variables(
            opts: Options,
            prefs: Preferences
        ) -> Options:
    """Replace any instances of variables with their values"""
    interpolated_opts = deepcopy(opts)
    for name, val in prefs['variables'].items():
        interpolated_opts['<endpoint>'] = _interpolate(
            interpolated_opts['<endpoint>'],
            name,
            val,
        )
        interpolated_opts['<params>'] = _interpolate_params(
            interpolated_opts['<params>'],
            name,
            val,
        )
        interpolated_opts['<data>'] = _interpolate_data(
            interpolated_opts['<data>'],
            name,
            val,
        )
    return interpolated_opts
