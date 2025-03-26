from cities_light.models import City
from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    ValidationError,
)
from accounts.constants import FormValdationMessages
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "display_name", "name_ascii", "region", "country")


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "first_name", "last_name", "email", "get_full_name")


class LoginSerializer(Serializer):
    username = CharField(required=True)
    password = CharField(required=True)

    def validate_username(self, value):
        """Validate User Object Exists"""
        if not get_user_model().objects.filter(username=value).exists():
            raise ValidationError(FormValdationMessages.USER_NOT_FOUND)
        return value

    def validate_password(self, value):
        """Validate Password"""
        return validate_password(value)

    def save(self, validated_data):
        """Authenticate User"""
        user = authenticate(**validated_data)
        if not user:
            raise ValidationError(FormValdationMessages.INVALID_CREDENTIALS)
        return user
