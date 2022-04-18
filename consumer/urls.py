from rest_framework import routers

from consumer.views import ToDoViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register("todos", ToDoViewSet, basename="todo")

urlpatterns = [*router.urls]
