from django.contrib.auth import get_user_model

from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.core.api import views as core_views
from apps.users import permissions

from .. import serializers

User = get_user_model()


class UsersViewSet(core_views.CRUDViewSet):
    """ViewSet for viewing accounts."""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    serializers_map = {
        "create": serializers.UserCreateSerializer,
        "profile": serializers.UserProfileSerializer,
        "default": serializers.UserSerializer,
    }
    extra_permission_classes = (IsAuthenticated,)
    extra_permissions_map = {
        "create": (permissions.IsStaff,),
    }
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    ordering_fields = (
        "first_name",
        "last_name",
        "email",
    )

    @action(detail=False, methods=("get",))
    def profile(self, *args, **kwargs) -> response.Response:
        """Return user profile of current user."""
        serializer = self.get_serializer(self.request.user)
        return response.Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
