from django.contrib.auth import get_user_model

from apps.core.api.serializers import ModelBaseSerializer

User = get_user_model()


class UserSerializer(ModelBaseSerializer):
    """Serializer for representing `User`."""

    class Meta:
        model = User
        read_only_fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "avatar",
            "is_active",
        )
        fields = read_only_fields


class UserCreateSerializer(UserSerializer):
    """Serializer for creating `User`."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ()
        fields = UserSerializer.Meta.fields + ("password",)

    def create(self, validated_data) -> User:
        """Create a new User instance."""
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(ModelBaseSerializer):
    """Serializer for User profile."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "avatar",
            "is_active",
        )
