import http

from django.test.client import Client
from django.urls import reverse

from apps.users.models import User


def test_logout_view(staff_user: User):
    """Ensure logged-in user can log out."""
    staff_client = Client()
    staff_client.force_login(staff_user)

    response = staff_client.post(reverse("user-logout"))
    assert response.status_code == http.HTTPStatus.OK
    assert "You have been logged out" in response.content.decode()
