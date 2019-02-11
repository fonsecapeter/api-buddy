from os import path
import yaml
from typing import Dict, Union

DEFAULT_API_URL = 'https://api.23andme.com/3/'
EXAMPLE_PREFS = f'''---
client_id: your_client_id
client_secret: your_client_secret
profile_id: your_profile_id
account_id: your_account_id
api_url: {DEFAULT_API_URL}
'''

DEFAULT_PREFS: Dict[str, object] = {
    'profile_id': 'demo_profile_id',
    'account_id': 'demo_account_id',
    'api_url': DEFAULT_API_URL,
}


def load_prefs(
            file_name: Union[str, None] = None
        ) -> Dict[str, object]:
    if file_name is None or not path.isfile(file_name):
        return DEFAULT_PREFS
    with open(file_name, 'r') as yamls:
        try:
            file_prefs = yaml.load(yamls)
        except yaml.YAMLError as exc:
            print(
                f'There was a problem reading {file_name} 😭\n'
                'Please make sure it\'s valid yaml: http://www.yaml.org/start.html'
            )
            exit(1)
    merged_prefs = DEFAULT_PREFS.copy()
    merged_prefs.update(file_prefs)
    return merged_prefs
