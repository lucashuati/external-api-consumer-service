from urllib.parse import urljoin

import requests


class ExternalAPIService:
    def __init__(self, base_url) -> None:
        self.base_url = base_url

    def build_url(self, endpoint):
        return urljoin(self.base_url, endpoint)

    def get(self, endpoint, params):
        url = self.build_url(endpoint)
        return requests.get(url, params=params)
