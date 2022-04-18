from urllib.parse import urljoin

import requests


class ExternalAPIServiceException(Exception):
    def __init__(self, *args, original_exception=None) -> None:
        self.original_exception = original_exception
        super().__init__(*args)


class ExternalAPIService:
    def __init__(self, base_url=None) -> None:
        self.base_url = base_url

    def build_url(self, endpoint):
        return urljoin(self.base_url, endpoint)

    def get(self, endpoint, params=None):
        try:
            url = self.build_url(endpoint)
            return requests.get(url, params=params)
        except (
            requests.RequestException,
            requests.Timeout,
            requests.URLRequired,
            requests.TooManyRedirects,
            requests.HTTPError,
            requests.ConnectionError,
            requests.FileModeWarning,
            requests.ConnectTimeout,
            requests.ReadTimeout,
            requests.JSONDecodeError,
        ) as e:
            raise ExternalAPIServiceException(*e.args, original_exception=e) from e
