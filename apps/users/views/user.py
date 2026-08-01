from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.core.mixins import AppStatsMixin
from apps.users.forms.user import UserRegisterForm, UserUpdateForm


class UserRegisterView(AppStatsMixin, CreateView):
    """View for user registration."""

    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("user-login")

    def form_valid(self, form) -> HttpResponseRedirect:
        """Custom form valid method to add a success message."""
        self.object = form.save()
        messages.success(
            self.request,
            "Your account has been created! You can log in now.",
        )
        return HttpResponseRedirect(self.get_success_url())


class UserProfileView(AppStatsMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("user-profile")

    def get_object(self, queryset=None):
        return self.request.user
