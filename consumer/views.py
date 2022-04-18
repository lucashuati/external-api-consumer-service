from consumer.helpers.viewset import ExternalAPIViewSet

from consumer.serializers import ToDoSerializer


class ToDoViewSet(ExternalAPIViewSet):
    external_api_endpoint = "https://jsonplaceholder.typicode.com/todos"
    response_limit = 5
    serializer_class = ToDoSerializer
