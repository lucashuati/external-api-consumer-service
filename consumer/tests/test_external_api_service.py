from unittest.mock import patch
from django.test import TestCase
from parameterized import parameterized
import requests

from consumer.services.external_api_service import (
    ExternalAPIService,
    ExternalAPIServiceException,
)


class ExternalAPIServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.service = ExternalAPIService(base_url="http://some_url")

    @parameterized.expand(
        [
            ("http://base_url1", "/endpoint1", "http://base_url1/endpoint1"),
            (
                "http://base_url2",
                "/endpoint/endpoint2",
                "http://base_url2/endpoint/endpoint2",
            ),
            (None, "/endpoint1", "/endpoint1"),
        ]
    )
    def test_build_url(self, base_url, endpoint, builded_url):
        service = ExternalAPIService(base_url=base_url)
        url = service.build_url(endpoint)
        self.assertEqual(url, builded_url)

    @patch("consumer.services.external_api_service.requests.get", return_value=None)
    def test_get_call_requests_get(self, mock):
        self.service.get("/endpoint", params={"some": 132})
        mock.assert_called_with("http://some_url/endpoint", params={"some": 132})

    @parameterized.expand(
        [
            (requests.RequestException,),
            (requests.Timeout,),
            (requests.URLRequired,),
            (requests.TooManyRedirects,),
            (requests.HTTPError,),
            (requests.ConnectionError,),
            (requests.FileModeWarning,),
            (requests.ConnectTimeout,),
            (requests.ReadTimeout,),
            (requests.JSONDecodeError,),
        ]
    )
    @patch("consumer.services.external_api_service.requests.get")
    def test_get_raise_custom_exception_when_request_exception_was_raised(
        self, exception, mock
    ):
        mock.side_effect = exception()

        with self.assertRaises(ExternalAPIServiceException):
            self.service.get("/endpoint", params={"some": 132})
