from unittest.mock import patch
from django.test import TestCase
from parameterized import parameterized
from rest_framework import serializers
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from consumer.helpers.viewset import ExternalAPIViewSet
from helpers.mock import MockRequest, MockResponse


class ExternalAPIViewset(TestCase):
    def setUp(self) -> None:
        self.viewset = ExternalAPIViewSet(serializer_class=serializers.Serializer)

    @patch("consumer.helpers.viewset.ExternalAPIService.get", return_value=MockResponse())
    def test_get_queryset_call_external_api_service(self, mock):
        self.viewset.get_queryset()
        mock.assert_called()

    @parameterized.expand(
        [
            (3, [0, 1, 2]),
            (5, [0, 1, 2, 3, 4]),
            (None, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ]
    )
    @patch("consumer.helpers.viewset.ExternalAPIService.get")
    def test_get_queryset_slice_response(self, response_limit, expected_data, mock):
        response_data = list(range(10))
        mock.return_value = MockResponse(data=response_data)
        self.viewset.response_limit = response_limit
        qs = self.viewset.get_queryset()
        self.assertEqual(qs, expected_data)

    @patch("consumer.helpers.viewset.ExternalAPIService.get")
    @patch("consumer.helpers.viewset.Response")
    def test_list_return_response_with_error_serializer(
        self, mock_response, mock_external_api_service
    ):
        self.viewset.request = MockRequest()
        mock_external_api_service.side_effect = TypeError("some error")
        self.viewset.list(request=MockRequest())
        mock_response.assert_called_with(
            {"error": {"reason": "some error"}}, status=HTTP_500_INTERNAL_SERVER_ERROR
        )
