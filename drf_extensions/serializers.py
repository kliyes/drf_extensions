from rest_framework import serializers

from .fields import TZDateTimeField
from .models import ExpirationToken


class BaseModelSerializer(serializers.ModelSerializer):
    created_at = TZDateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = TZDateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")


class ExpirationTokenSerializer(serializers.ModelSerializer):
    expired_at = TZDateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    token = serializers.ReadOnlyField(source="key")

    class Meta:
        model = ExpirationToken
        exclude = ("created", "key")
