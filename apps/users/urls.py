from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path(
        "user/register/",
        views.UserRegisterView.as_view(),
        name="user-register",
    ),
    path(
        "user/login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="user-login",
    ),
    path(
        "user/logout/",
        auth_views.LogoutView.as_view(
            template_name="users/logged_out.html",
        ),
        name="user-logout",
    ),
    path(
        "user/profile/",
        views.UserProfileView.as_view(),
        name="user-profile",
    ),
]
