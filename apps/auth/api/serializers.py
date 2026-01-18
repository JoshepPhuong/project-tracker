from django.conf import settings
from django.contrib.auth import (
    authenticate,
    password_validation,
    tokens,
)
from django.core.exceptions import ValidationError
from django.utils import encoding, http
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from libs.open_api.serializers import OpenApiSerializer

from apps.users.api.serializers import UserSerializer
from apps.users.models import User

from .. import services


class AuthTokenSerializer(serializers.Serializer):
    """Custom auth serializer to use email instead of username.

    Copied from rest_framework.authtoken.serializers.AuthTokenSerializer

    """

    email = serializers.CharField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )

    def validate(self, attrs: dict) -> dict:
        """Authenticate with input data."""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user.is_active:
            msg = _(
                "The email and/or password entered is incorrect. Please try again.",
            )
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict) -> None:
        """Escape warning."""

    def update(self, instance, validated_data) -> None:
        """Escape warning."""


class TokenSerializer(OpenApiSerializer):
    """Auth token for entire app."""

    expiry = serializers.IntegerField(
        help_text=f"Token expires in {settings.REST_KNOX['TOKEN_TTL']}",
    )
    token = serializers.CharField(help_text="Token itself")
    user = UserSerializer()


class ResetPasswordRequestSerializer(serializers.Serializer):
    """Request for resetting user's password."""

    email = serializers.EmailField(
        help_text="Email of account which requests for password reset",
    )
    _user: User

    def validate_email(self, email: str) -> str:
        """Check that we have user with input email."""
        user = User.objects.filter(email=email).first()
        if not user:
            raise ValidationError(
                _("There is no user with such email"),
            )
        self._user = user
        return email

    def create(self, validated_data: dict):
        return services.request_reset_password(user=self._user)

    def update(self, instance, validated_data):
        """Escape warning."""


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Request for resetting user's password.

    Explanation of token and uid

    Example `MQ-5b2-e2c1ce64d63673f0e78f`, where `MQ` - is `uid` or user id and
    `5b2-e2c1ce64d63673f0e78f` - `token` for resetting password

    """

    password = serializers.CharField(
        max_length=128,
    )
    password_confirm = serializers.CharField(
        max_length=128,
    )
    uid = serializers.CharField()
    token = serializers.CharField()
    _token_generator = tokens.PasswordResetTokenGenerator()
    _user: User

    def validate_uid(self, uid: str) -> str:
        """Validate that uid can be decoded and it's valid."""
        try:
            user_pk = encoding.force_str(http.urlsafe_base64_decode(uid))
        except encoding.DjangoUnicodeDecodeError as error:
            raise serializers.ValidationError(_("Invalid uid")) from error
        if not (user := User.objects.filter(pk=user_pk).first()):
            raise serializers.ValidationError(_("Invalid uid"))
        self._user = user
        return uid

    def validate_token(self, token: str) -> str:
        """Validate token."""
        if not self._token_generator.check_token(
            getattr(self, "_user", None),
            token,
        ):
            raise serializers.ValidationError(_("Invalid token"))
        return token

    def validate(self, attrs):
        """Validate passwords."""
        password = attrs["password"]
        password_confirm = attrs["password_confirm"]
        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": _("Passwords mismatch")},
            )
        password_validation.validate_password(password, self._user)
        return attrs

    def create(self, validated_data: dict) -> User:
        password = validated_data["password"]
        self._user.set_password(password)
        self._user.save()
        return self._user

    def update(self, instance, validated_data):
        """Escape warning."""


class ResetPasswordSerializer(serializers.Serializer):
    """Reset a user's password."""

    email = serializers.EmailField(
        help_text="Email of account which password should be reset",
        required=False,
    )

    def validate(self, attrs: str) -> str:
        """Check that we have user with input email."""
        attrs = super().validate(attrs)
        email = attrs["email"]
        user = User.objects.filter(email=email).first()
        if not user or user.deactivated_at:
            raise serializers.ValidationError(
                _("Your account has been deleted"),
            )
        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict):
        """Reset user's password."""
        return services.reset_user_password(user=validated_data["user"])

    def update(self, instance, validated_data):
        """Escape warning."""
