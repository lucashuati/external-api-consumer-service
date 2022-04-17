import jwt

from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import RefreshToken
from users.factories import UserFactory


class ObtainJWTTokenTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.correct_credentials = {
            "username": "user",
            "password": "123",
        }
        cls.wrong_credentials = {
            "username": "wrong_user",
            "password": "123456",
        }
        cls.user = UserFactory(**cls.correct_credentials)
        cls.url = reverse("obtain_token_pair")

    def test_obtain_jwt_token_with_correct_credentials(self):
        response = self.client.post(self.url, self.correct_credentials)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("refresh", response.data.keys())
        self.assertIn("access", response.data.keys())

    def test_obtain_jwt_token_with_wrong_credentials(self):
        response = self.client.post(self.url, self.wrong_credentials)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "No active account found with the given credentials"
        )


class RefreshJWTTokenTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.refresh_token = RefreshToken.for_user(cls.user)
        cls.invalid_refresh_token = jwt.encode(
            {
                "token_type": "refresh",
                "user_id": cls.user.pk,
                "exp": 1516239022,
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        cls.url = reverse("refresh_token")

    def test_refresh_access_token_with_valid_refresh_token(self):
        response = self.client.post(self.url, {"refresh": str(self.refresh_token)})
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("access", response.data.keys())

    def test_refresh_access_token_with_invalid_refresh_token(self):
        response = self.client.post(
            self.url, {"refresh": str(self.invalid_refresh_token)}
        )
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Token is invalid or expired")
