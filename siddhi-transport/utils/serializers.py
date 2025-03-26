from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    DateField,
    CharField,
    ValidationError,
)
from utils.constants import ValidationErrorConstants, AppLabelsModel
from django.utils.timezone import now, timedelta
from utils.utils import get_model

Station = get_model(**AppLabelsModel.STATION)
Train = get_model(**AppLabelsModel.TRAIN)


class TrainNumberBaseSerializer(Serializer):
    train = CharField(max_length=5, required=True)

    def validate_train(self, value):
        if 0 > len(value) > 5:
            raise ValidationError(ValidationErrorConstants.INVALID_TRAIN_NUMBER)
        try:
            value = Train.objects.get(number=value)
        except Train.DoesNotExist:
            raise ValidationError(ValidationErrorConstants.INVALID_TRAIN_NUMBER)
        return value


class DynamicModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DynamicModelSerializer, self).__init__(*args, **kwargs)
        fields = kwargs.pop("fields", None)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DateFromToBaseSerializer(Serializer):
    dt = DateField()
    from_station = CharField(max_length=5)
    to_station = CharField(max_length=5)

    def validate_dt(self, value):
        """Date must not be in past and not after 3 months from today"""
        if value < now().date():
            raise ValidationError(ValidationErrorConstants.DATE_IN_PAST)
        if value > now().date() + timedelta(days=90):
            raise ValidationError(ValidationErrorConstants.DATE_AFTER_THREE_MONTHS)
        return value

    def validate(self, data):
        if data["from_station"].lower() == data["to_station"].lower():
            raise ValidationError(ValidationErrorConstants.FROM_TO_STATION_SAME)
        return super(DateFromToBaseSerializer, self).validate(data)

    def validate_from_station(self, value):
        try:
            return Station.objects.get(code=value.upper()).name_code_format
        except Station.DoesNotExist:
            raise ValidationError(ValidationErrorConstants.STATION_NOT_FOUND)

    def validate_to_station(self, value):
        try:
            return Station.objects.get(code=value.upper()).name_code_format
        except Station.DoesNotExist:
            raise ValidationError(ValidationErrorConstants.STATION_NOT_FOUND)
