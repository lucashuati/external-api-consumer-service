from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    error = serializers.SerializerMethodField()

    def get_error(self, obj):
        return {
            "reason": obj["error"],
        }
