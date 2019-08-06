import json
import sys
from .provider import Provider


class Gogs(Provider):
    AGENT = 'GogsServer'  # User-Agent in Headers
    EVENT_ID = 'x-gogs-event'  # x-{provider}-event in Headers

    def __init__(self):
        print('Initializing Gogs Provider', file=sys.stdout)

    def __str__(self):
        return 'Gogs Provider'

    def get_url_from_json_payload(self, payload):
        # Convert the JSON to Dict
        data = json.loads(payload)

        # Modify the path to the URL
        # according to the Git Provider
        if 'html_url' in data['repository']:
            return data['repository']['html_url']
