from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ProjectForm
from .models import WorkflowStep
from .workflow import DEFAULT_WORKFLOW_STEPS


def landing_page(request):
    """Render the public Codex Studio landing page."""
    return render(request, 'projects/landing.html')


@login_required
def dashboard(request):
    """Render the authenticated workspace and its projects."""
    return render(request, 'projects/dashboard.html', {'projects': request.user.projects.all()})


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Create a user-owned project and its initial workflow steps."""

    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        with transaction.atomic():
            response = super().form_valid(form)
            WorkflowStep.objects.bulk_create(
                [
                    WorkflowStep(
                        project=self.object,
                        step_name=step_name,
                        step_order=step_order,
                        status=WorkflowStep.Status.PENDING,
                    )
                    for step_order, step_name in enumerate(DEFAULT_WORKFLOW_STEPS, start=1)
                ],
            )
        messages.success(self.request, 'Project created. Your workflow is ready.')
        return response
