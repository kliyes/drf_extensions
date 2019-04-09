import six

from dateutil.parser import parse

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import timezone

from rest_framework.fields import DateTimeField, CharField, FileField, \
    ImageField, ChoiceField
from rest_framework.relations import PrimaryKeyRelatedField

from utils.validators import ExplicitLengthValidator, MaxFileSizeValidator


class SerializedPKRelatedField(PrimaryKeyRelatedField):
    """
    Like serializers.PrimaryKeyRelatedField
    but return serialized data rather than just pk
    Example:
        db = SerializedPKRelatedField(
            serializer_class=DatabaseSerializer,
            queryset=Database.objects.all()
        )
    """

    def __init__(self, serializer_class, **kwargs):
        self.serializer_class = serializer_class
        super(SerializedPKRelatedField, self).__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        return self.serializer_class(value).data


class TZDateTimeField(DateTimeField):

    def to_representation(self, value):
        if value:
            if isinstance(value, six.string_types):
                value = parse(value)
            value = timezone.localtime(value)
        return super(TZDateTimeField, self).to_representation(value)


class ExplicitLengthCharField(CharField):

    def __init__(self, explicit_length, **kwargs):
        super(ExplicitLengthCharField, self).__init__(**kwargs)
        validator = ExplicitLengthValidator(limit_value=explicit_length)
        self.validators.append(validator)


class LimitSizeFileField(FileField):

    def __init__(self, *args, **kwargs):
        self.limit_size = kwargs.pop("limit_size", None)
        super(LimitSizeFileField, self).__init__(*args, **kwargs)
        validator = MaxFileSizeValidator(limit_value=self.limit_size)
        self.validators.append(validator)


class LimitSizeImageField(LimitSizeFileField, ImageField):
    pass


class OssStyleImageMixin(object):

    def __init__(self, *args, **kwargs):
        self.style_name = kwargs.pop("style_name", None)
        super(OssStyleImageMixin, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        value = super(OssStyleImageMixin, self).to_representation(value)
        if not value:
            return None

        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            return None
        else:
            url = value
            if self.style_name:
                url = "{}@!{}".format(value, self.style_name)
            return url


class OssStyleLimitSizeImageField(OssStyleImageMixin, LimitSizeImageField):
    pass


class OssStyleImageField(OssStyleImageMixin, ImageField):
    pass


class DisplayChoiceField(ChoiceField):
    """
    """
    def to_representation(self, value):
        value = super(DisplayChoiceField, self).to_representation(value)
        return self.choices.get(value, value)
