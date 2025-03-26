from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from rest_framework.views import APIView
from accounts.api.serializers import (
    CitySerializer,
    UserSerializer,
    LoginSerializer,
)
from django.contrib.auth import get_user_model
from cities_light.models import City
from django.db.models import Q
from utils.auth_service import AuthService
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from http import HTTPStatus


class CityViewSet(ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def filter_queryset(self, queryset):
        q = self.request.query_params.get("q")
        if q:
            return (
                super()
                .filter_queryset(queryset)
                .filter(Q(name__icontains=q) | Q(name_ascii__icontains=q))
            ).distinct()
        return super().filter_queryset(queryset)


class UserViewSet(CreateModelMixin, ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

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

    @action(detail=False, methods=["GET"])
    def me(self, request):
        return Response(self.serializer_class(request.user).data, status=HTTPStatus.OK)


class LoginApiView(APIView):
    serializer_class = LoginSerializer
    service_class = AuthService

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(validated_data=serializer.validated_data)
        return Response(
            self.service_class().get_auth_tokens_for_user(user=user),
            status=HTTPStatus.OK,
        )
