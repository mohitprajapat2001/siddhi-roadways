from rest_framework.viewsets import ReadOnlyModelViewSet
from siddhi_transport.api.serializers import CitySerializer, UserSerializer
from django.contrib.auth import get_user_model
from cities_light.models import City


class CityViewSet(ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
