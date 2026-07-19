from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import RegistrationForm


def register(request):
    """Register a user and send them to the login page."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('accounts:login')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


class UserLoginView(LoginView):
    """Django's login view with a confirmation message."""

    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Login successful.')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """Django's POST-only logout view with a confirmation message."""

    next_page = reverse_lazy('landing')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(request, 'Logout successful.')
        return response
