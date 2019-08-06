import json
import sys
from .provider import Provider


class Github(Provider):
    AGENT = 'GitHub-Hookshot'  # User-Agent in Headers
    EVENT_ID = 'x-github-event'  # x-{provider}-event in Headers

    def __init__(self):
        print('Initializing Github Provider', file=sys.stdout)

    def __str__(self):
        return 'Github Provider'

    def get_url_from_json_payload(self, payload):
        # Convert the JSON to Dict
        data = json.loads(payload)

        # Modify the path to the URL
        # according to the Git Provider
        if 'url' in data['repository']:
            return data['repository']['url']
