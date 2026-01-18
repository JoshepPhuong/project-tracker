import http

from django.test.client import Client
from django.urls import reverse

import pytest
import pytest_lazy_fixtures

from apps.users.models import User


@pytest.mark.parametrize(
    argnames="test_user",
    argvalues=[
        None,
        pytest_lazy_fixtures.lf("user"),
        pytest_lazy_fixtures.lf("staff_user"),
        pytest_lazy_fixtures.lf("superuser"),
    ],
)
def test_index_view(test_user: User | None):
    """Ensure index page can be rendered."""
    client = Client()
    if test_user:
        client.force_login(test_user)
    response = client.get(reverse("index"))
    assert response.status_code == http.HTTPStatus.OK
