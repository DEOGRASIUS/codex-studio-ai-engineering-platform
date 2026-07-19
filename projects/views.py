from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def landing_page(request):
    """Render the public Codex Studio landing page."""
    return render(request, 'projects/landing.html')


@login_required
def dashboard(request):
    """Render the authenticated workspace placeholder."""
    return render(request, 'projects/dashboard.html')
