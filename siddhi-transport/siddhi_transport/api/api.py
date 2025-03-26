from rest_framework.viewsets import ReadOnlyModelViewSet
from siddhi_transport.api.serializers import CitySerializer, UserSerializer
from django.contrib.auth import get_user_model
from cities_light.models import City
from django.db.models import Q


class CityViewSet(ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def filter_queryset(self, queryset):
        q = self.request.query_params.get("q")
        if q:
            return (
                super()
                .filter_queryset(queryset)
                .filter(Q(name__icontains=q) | Q(name_ascii__icontains=q))
            ).distinct()
        return super().filter_queryset(queryset)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset):
        q = self.request.query_params.get("q")
        if q:
            return (
                super()
                .filter_queryset(queryset)
                .filter(
                    Q(first_name__icontains=q)
                    | Q(last_name__icontains=q)
                    | Q(username__icontains=q)
                )
            ).distinct()
        return super().filter_queryset(queryset)
