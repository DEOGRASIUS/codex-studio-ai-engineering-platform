from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import WorkflowStep
from .services.workflow import (
    approve_step,
    pause_step,
    request_changes,
    resume_step,
    retry_step,
)

@login_required
@require_POST
def approve_workflow_step(request, pk):

    step = get_object_or_404(
        WorkflowStep,
        pk=pk,
        project__owner=request.user,
    )

    approve_step(step, request.user)

    messages.success(
        request,
        "Step approved successfully."
    )

    return redirect(
        "projects:detail",
        pk=step.project.pk,
    )

@login_required
@require_POST
def request_workflow_changes(request, pk):

    step = get_object_or_404(
        WorkflowStep,
        pk=pk,
        project__owner=request.user,
    )

    feedback = request.POST.get(
        "feedback",
        ""
    )

    request_changes(
        step,
        feedback,
    )

    messages.warning(
        request,
        "Changes requested."
    )

    return redirect(
        "projects:detail",
        pk=step.project.pk,
    )

@login_required
@require_POST
def retry_workflow_step(request, pk):

    step = get_object_or_404(
        WorkflowStep,
        pk=pk,
        project__owner=request.user,
    )

    retry_step(step)

    messages.success(
        request,
        "Workflow restarted."
    )

    return redirect(
        "projects:detail",
        pk=step.project.pk,
    )

@login_required
@require_POST
def pause_workflow_step(request, pk):

    step = get_object_or_404(
        WorkflowStep,
        pk=pk,
        project__owner=request.user,
    )

    pause_step(step)

    messages.info(
        request,
        "Workflow paused."
    )

    return redirect(
        "projects:detail",
        pk=step.project.pk,
    )

@login_required
@require_POST
def resume_workflow_step(request, pk):

    step = get_object_or_404(
        WorkflowStep,
        pk=pk,
        project__owner=request.user,
    )

    resume_step(step)

    messages.success(
        request,
        "Workflow resumed."
    )

    return redirect(
        "projects:detail",
        pk=step.project.pk,
    )


