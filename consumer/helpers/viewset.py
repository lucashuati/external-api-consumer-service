from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from consumer.services.external_api_service import (
    ExternalAPIService,
    ExternalAPIServiceException,
)
from helpers.serializers import ErrorSerializer


class ExternalAPIViewSet(GenericViewSet, ListModelMixin):
    external_api_endpoint = None
    response_limit = None

    def get_queryset(self):
        response = ExternalAPIService().get(endpoint=self.external_api_endpoint)
        data = response.json()
        return data[: self.response_limit] if self.response_limit else data

    def list(self, *args, **kwargs):
        try:
            return super().list(*args, **kwargs)
        except (TypeError, ExternalAPIServiceException) as e:
            error_data = dict(error=str(e))
            return Response(ErrorSerializer(error_data).data)
