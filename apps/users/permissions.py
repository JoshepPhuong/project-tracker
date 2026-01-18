from rest_framework.permissions import IsAuthenticated


class IsStaff(IsAuthenticated):
    """Allow staff user to access endpoints."""

    def has_permission(self, request, view):
        """Allow staff user."""
        if not super().has_permission(request, view):
            return False
        return request.user.is_staff
