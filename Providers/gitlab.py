import json
import sys
from .provider import Provider


class Github(Provider):
    AGENT = 'GitLab'  # User-Agent in Headers
    EVENT_ID = 'x-gitlab-event'  # x-{provider}-event in Headers

    def __init__(self):
        print('Initializing GitLab Provider', file=sys.stdout)

    def __str__(self):
        return 'GitLab Provider'

    def get_url_from_json_payload(self, payload):
        # Convert the JSON to Dict
        data = json.loads(payload)

        # Modify the path to the URL
        # according to the Git Provider
        if 'url' in data['repository']:
            return data['repository']['url']
