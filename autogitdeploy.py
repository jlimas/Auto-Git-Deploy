import sys
import yaml
import os
import pyclbr
import importlib

from yaml import CLoader
from http.server import BaseHTTPRequestHandler, HTTPServer


class AutoGitDeployServer(BaseHTTPRequestHandler):
    config = None
    hostname = None
    port_number = None
    repos = []
    providers = []

    @classmethod
    def get_configuration(cls):
        try:
            # Parse the Yaml from config file
            config = yaml.load(open('config.yml'), Loader=CLoader)

            # Setup the class
            cls.hostname = config['hostname']
            cls.port_number = config['port']

            # Getting the Repos
            for repo in config['repos']:
                cls.repos.append(repo)
                print(f'Loaded Git Repository: {repo["name"]}')
        except yaml.YAMLError as e:
            print(e, file=sys.stderr)
            sys.exit('Unable to parse the configuration file (config.yml)')

    @classmethod
    def load_providers(cls):
        # Search Provider Files in the Directory
        for pfile in os.listdir('Providers'):
            # Discard non-Python files
            if '.py' not in pfile:
                continue

            # Discard provider.py and __init__.py Files
            if 'provider.py' in pfile or '__init__.py' in pfile:
                continue

            # Remove .py extension
            pfile = pfile[:-3]

            # Get Classes names in Modules
            for provider in pyclbr.readmodule(f'Providers.{pfile}').keys():
                # Getting the module
                module = importlib.import_module(f'Providers.{pfile}')

                # Getting the Class
                class_ = getattr(module, provider)

                # Instanciate the Class
                instance = class_()

                # Add the Provider Instance to the Providers List
                cls.providers.append(instance)

    def do_POST(self):
        # Get the Agent
        agent = self.headers.get('User-Agent', None)

        # Get the length of the request body
        length = int(self.headers['content-length'])

        # Read the request body
        payload = self.rfile.read(length)

        # Detect provider by using User Agent
        if agent:
            for provider in self.providers:
                if provider.AGENT == agent:
                    print(f'Detected {provider} User Agent', file=sys.stdout)
                    url = provider.get_url_from_json_payload(payload)

        # Fallback to Event Id if no provided has been detected
        if url is None:
            print(f'Fallingback to Event Id', file=sys.stdout)
            for provider in self.providers:
                if provider.EVENT_ID in self.headers:
                    url = provider.get_url_from_json_payload(payload)

        # Handle the deploy for the URL
        if url is not None:
            self.handle_deploy_for_url(url)
            self.send_response(204)
            self.end_headers()
            return

    @classmethod
    def handle_deploy_for_url(cls, url):
        # Search the URL in the Repos
        for repo in cls.repos:
            if url == repo['url']:
                print(f'Deploying Git Repo {repo["name"]}', file=sys.stdout)


def main():
    try:
        # Load the Config YAML file
        AutoGitDeployServer.get_configuration()

        # Load the Git Providers from directory
        AutoGitDeployServer.load_providers()

        # Create the HTTP Server
        server = HTTPServer(
            (AutoGitDeployServer.hostname, AutoGitDeployServer.port_number),
            AutoGitDeployServer
        )
        print(f'Server Listening on Port {AutoGitDeployServer.port_number}',
              file=sys.stdout)

        # Starting the HTTP Server
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
