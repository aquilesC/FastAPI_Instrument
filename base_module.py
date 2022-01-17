import logging

import requests
from requests.exceptions import InvalidSchema

logger = logging.getLogger(__name__)


class BaseModule:
    def __init__(self, ip, port):
        logger.info(f'Module: {ip}:{port}')
        self.ip = ip
        self.port = port

    def get(self, endpoint):
        logger.info(f'Getting endpoint {endpoint}')
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        url = f'{self.ip}:{self.port}/{endpoint}'
        try:
            result = requests.get(url)
            return result.json()
        except InvalidSchema:
            return {'error': f'No connection adapters were found for {url}'}

    def put(self, endpoint, data):
        logger.info(f'Put on endpoint {endpoint}')
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        url = f'{self.ip}:{self.port}/{endpoint}'
        try:
            result = requests.put(url, data=data)
            return result.status_code
        except InvalidSchema:
            return {'error': f'No connection adapters were found for {url}'}

    def __str__(self):
        return f'Module on {self.ip}:{self.port}'