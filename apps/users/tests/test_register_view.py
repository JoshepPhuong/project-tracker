import http

from django.conf import settings
from django.test.client import Client
from django.urls import reverse

import pytest

from apps.users.models import User


@pytest.fixture
def new_user_data() -> dict[str, str]:
    """Return a dictionary with new user data."""
    return {
        "email": "testuser@email.com",
        "username": "TestUser",
        "password": "testing123",
    }


def test_get_register_view(unauthenticated_client: Client):
    """Ensure user register view can be rendered."""
    response = unauthenticated_client.get(reverse("user-register"))
    assert response.status_code == http.HTTPStatus.OK


def test_user_register_view(
    unauthenticated_client: Client,
    new_user_data: dict[str, str],
):
    """Ensure user can register a new account."""
    response = unauthenticated_client.post(
        reverse("user-register"),
        data={
            "email": new_user_data["email"],
            "username": new_user_data["username"],
            "password1": new_user_data["password"],
            "password2": new_user_data["password"],
        },
    )
    assert response.status_code == http.HTTPStatus.FOUND
    assert response.url == settings.LOGIN_URL

    assert User.objects.filter(
        email=new_user_data["email"],
        username=new_user_data["username"],
    ).exists()
