from rest_framework import HTTP_HEADER_ENCODING

from drf_spectacular.authentication import TokenScheme as DRFTokenScheme


def get_auth_header(request):
    """Return request's 'auth:' header, as a bytestring.

    Copied from `rest_framework.authentication.get_authorization_header`.

    """
    auth = request.META.get("HTTP_AUTH", b"")
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class CustomTokenScheme(DRFTokenScheme):
    """Provide scheme for our custom webapp authentication class."""

    target_class = "apps.auth.auth_classes.CustomTokenAuthentication"
    name = "webAppTokenAuth"
    match_subclasses = True
