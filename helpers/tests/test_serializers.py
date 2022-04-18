from django.test import TestCase
from parameterized import parameterized

from helpers.serializers import ErrorSerializer


class ErrorSerializerTestCase(TestCase):
    @parameterized.expand(
        [
            ("error 1"),
            ("error 2"),
            ("error 3"),
        ]
    )
    def test_reason_dict_format_correctly(self, error):
        self.assertDictEqual(
            ErrorSerializer(dict(error=error)).data, {"error": {"reason": error}}
        )
