from unittest.mock import patch

from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK
from django.urls import reverse

from consumer.serializers import ToDoSerializer
from users.factories import UserFactory
from helpers.mock import MockResponse


class ToDoViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.url = reverse("todo-list")

    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(user=self.user)

    @patch("consumer.helpers.viewset.ExternalAPIService.get")
    def test_list_todo(self, mock):
        mock_response_data = [
            {"userId": 1, "id": 1, "title": "delectus aut autem", "completed": False},
            {
                "userId": 1,
                "id": 2,
                "title": "quis ut nam facilis et officia qui",
                "completed": False,
            },
            {"userId": 1, "id": 3, "title": "fugiat veniam minus", "completed": False},
            {"userId": 1, "id": 4, "title": "et porro tempora", "completed": True},
            {
                "userId": 1,
                "id": 5,
                "title": "laboriosam mollitia et enim quasi adipisci quia provident illum",
                "completed": False,
            },
        ]
        mock.return_value = MockResponse(data=mock_response_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.data, ToDoSerializer(mock_response_data, many=True).data
        )
