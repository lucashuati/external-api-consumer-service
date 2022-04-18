from django.test import TestCase
from consumer.serializers import ToDoSerializer


class ToDoSerializerTestCase(TestCase):
    def test_data(self):
        raw_data = {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": False,
        }
        self.assertDictEqual(
            ToDoSerializer(raw_data).data, {"id": 1, "title": "delectus aut autem"}
        )
