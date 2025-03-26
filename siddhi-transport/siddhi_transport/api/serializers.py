from cities_light.models import City
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "display_name", "name_ascii", "region", "country")


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "first_name", "last_name", "email", "get_full_name")
