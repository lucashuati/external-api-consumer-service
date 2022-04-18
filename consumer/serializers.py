from rest_framework import serializers


class ToDoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
