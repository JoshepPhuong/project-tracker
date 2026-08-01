import http

from django.conf import settings
from django.test.client import Client
from django.urls import reverse

from apps.users.factories.user import DEFAULT_PASSWORD
from apps.users.models import User


def test_get_login_view(unauthenticated_client: Client):
    """Ensure login view can be rendered."""
    response = unauthenticated_client.get(reverse("user-login"))
    assert response.status_code == http.HTTPStatus.OK


def test_user_login_view(unauthenticated_client: Client, user: User):
    """Ensure user can log in with valid credentials."""
    response = unauthenticated_client.post(
        settings.LOGIN_URL,
        data={
            "username": user.username,
            "password": DEFAULT_PASSWORD,
        },
    )
    assert response.status_code == http.HTTPStatus.FOUND
    assert response.url == settings.LOGIN_REDIRECT_URL
