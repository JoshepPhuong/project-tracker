from rest_framework.views import APIView

from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.plumbing import build_basic_type
from drf_spectacular.types import OpenApiTypes

from libs.open_api.view_fixers import ApiViewFix


def fix_api_view_warning(class_to_fix: type[APIView]):
    """Fix warning `This is graceful fallback handling for APIViews`."""

    class FixedApiView(ApiViewFix):
        """Generated fixed class."""

        target_class = f"{class_to_fix.__module__}.{class_to_fix.__name__}"

    return FixedApiView


class TimezoneFieldFix(OpenApiSerializerFieldExtension):
    """Provide swagger fix for TimeZoneSerializerField."""

    target_class = "timezone_field.rest_framework.TimeZoneSerializerField"

    def map_serializer_field(self, auto_schema, direction):
        """Build field as string type."""
        return build_basic_type(OpenApiTypes.STR)
