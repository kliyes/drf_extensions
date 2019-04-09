from rest_framework import serializers

from .fields import TZDateTimeField


class BaseModelSerializer(serializers.ModelSerializer):
    created_at = TZDateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = TZDateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
