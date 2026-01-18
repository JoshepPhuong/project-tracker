from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r"",
    viewset=views.UsersViewSet,
    basename="users",
)
urlpatterns = [
    *router.urls,
]
