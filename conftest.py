"""Configuration file for pytest."""

import collections.abc
import typing

from django.conf import settings
from django.core.files.storage import default_storage
from django.test.client import Client

from rest_framework import test

import pytest
import pytest_django

from apps.users import factories as users_factories
from apps.users.models import User


def pytest_configure() -> None:
    """Set up Django settings for tests.

    `pytest` automatically calls this function once when tests are run.

    """
    settings.DEBUG = False
    settings.RESTRICT_DEBUG_ACCESS = True
    settings.TESTING = True

    # The default password hasher is rather slow by design.
    # https://docs.djangoproject.com/en/dev/topics/testing/overview/
    settings.PASSWORD_HASHERS = (
        "django.contrib.auth.hashers.MD5PasswordHasher",
    )
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # To disable celery in tests
    settings.CELERY_TASK_ALWAYS_EAGER = True

    # To separate test files from prod files
    settings.AWS_LOCATION = "test-files"


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup) -> None:  # noqa: ANN001
    """Set up test db for testing."""


@pytest.fixture(autouse=True)
def _enable_db_access_for_all_tests(django_db_setup, db) -> None:  # noqa: ANN001
    """Enable access to DB for all tests."""


@pytest.fixture(scope="session", autouse=True)
def _clean_up_test_files() -> collections.abc.Generator[None, None, None]:
    """Clear test files after finishing tests."""
    yield
    for obj in default_storage.bucket.objects.filter(
        Prefix=settings.AWS_LOCATION,
    ):
        obj.delete()


@pytest.fixture
def api_client() -> test.APIClient:
    """Return a normal, not logged in api client fixture."""
    return test.APIClient()


@pytest.fixture(scope="module")
def user(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> typing.Generator[User, None, None]:
    """Create default user."""
    with django_db_blocker.unblock():
        return users_factories.UserFactory()


@pytest.fixture(scope="module")
def staff_user(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> typing.Generator[User, None, None]:
    """Create default staff user."""
    with django_db_blocker.unblock():
        return users_factories.UserFactory(is_staff=True)


@pytest.fixture(scope="module")
def superuser(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> typing.Generator[User, None, None]:
    """Create default superuser."""
    with django_db_blocker.unblock():
        return users_factories.UserFactory(is_superuser=True, is_staff=True)


@pytest.fixture(scope="module")
def unauthenticated_client() -> Client:
    """Return an unauthenticated client."""
    return Client()
