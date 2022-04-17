from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("auth/token/obtain", TokenObtainPairView.as_view(), name="obtain_token_pair"),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="refresh_token"),
]
