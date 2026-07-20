from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, DeleteView

from agents.agent_runner import (
    REQUIREMENTS_ANALYST_STEP,
    run_requirements_agent,
)

from .forms import ProjectForm
from .models import (
    GeneratedArtifact,
    Project,
    WorkflowStep,
)
from .workflow import DEFAULT_WORKFLOW_STEPS



def landing_page(request):
    """
    Public Codex Studio landing page.
    """
    return render(
        request,
        "projects/landing.html"
    )



@login_required
def dashboard(request):
    """
    User project dashboard.
    """
    return render(
        request,
        "projects/dashboard.html",
        {
            "projects": request.user.projects.all()
        }
    )



@login_required
def project_detail(request, pk):
    """
    Display project workspace,
    workflow pipeline and artifacts.
    """

    project = get_object_or_404(
        Project.objects.prefetch_related(
            "workflow_steps__artifacts"
        ),
        pk=pk,
        owner=request.user,
    )


    artifacts = GeneratedArtifact.objects.filter(
        workflow_step__project=project
    ).select_related(
        "workflow_step"
    )


    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
            "artifacts": artifacts,

            "requirements_step_name":
                REQUIREMENTS_ANALYST_STEP,

            "pending_status":
                WorkflowStep.Status.PENDING,

            "completed_status":
                WorkflowStep.Status.COMPLETED,

            "waiting_approval_status":
                WorkflowStep.Status.WAITING_APPROVAL,

            "failed_status":
                WorkflowStep.Status.FAILED,

            "paused_status":
                WorkflowStep.Status.PAUSED,
        },
    )



@login_required
@require_POST
def run_requirements(request, pk):
    """
    Start Requirements Analyst.
    """

    project = get_object_or_404(
        Project,
        pk=pk,
        owner=request.user,
    )


    try:

        run_requirements_agent(project)


    except Exception:

        messages.error(
            request,
            "Requirements Analysis failed. Try again."
        )


    else:

        messages.success(
            request,
            "Requirements Analysis completed."
        )


    return redirect(
        "projects:detail",
        pk=project.pk
    )





class ProjectCreateView(LoginRequiredMixin, CreateView):

    form_class = ProjectForm

    template_name = (
        "projects/project_create.html"
    )

    success_url = reverse_lazy(
        "dashboard"
    )


    def form_valid(self, form):

        form.instance.owner = self.request.user


        with transaction.atomic():

            response = super().form_valid(form)


            WorkflowStep.objects.bulk_create(
                [
                    WorkflowStep(
                        project=self.object,
                        step_name=name,
                        step_order=index,
                        status=WorkflowStep.Status.PENDING,
                    )

                    for index, name in enumerate(
                        DEFAULT_WORKFLOW_STEPS,
                        start=1
                    )
                ]
            )


        messages.success(
            self.request,
            "Project created successfully."
        )


        return response





@login_required
@require_POST
def approve_step(request, pk):
    """
    Approve current engineer
    and unlock next engineer.
    """


    step = get_object_or_404(
        WorkflowStep,
        pk=pk,
        project__owner=request.user,
    )


    step.status = WorkflowStep.Status.APPROVED

    step.approval_status = (
        WorkflowStep.ApprovalStatus.APPROVED
    )

    step.approved_at = timezone.now()

    step.approved_by = request.user


    step.save(
        update_fields=[
            "status",
            "approval_status",
            "approved_at",
            "approved_by",
        ]
    )


    step.artifacts.update(
        approved=True
    )



    next_step = WorkflowStep.objects.filter(
        project=step.project,
        step_order=step.step_order + 1
    ).first()



    if next_step:

        next_step.status = (
            WorkflowStep.Status.PENDING
        )

        next_step.save(
            update_fields=[
                "status"
            ]
        )

        step.project.status = (
            Project.Status.IN_PROGRESS
        )


    else:

        step.project.status = (
            Project.Status.COMPLETED
        )


    step.project.save(
        update_fields=[
            "status"
        ]
    )



    messages.success(
        request,
        f"{step.step_name} approved. "
        "Next engineer unlocked."
    )


    return redirect(
        "projects:detail",
        pk=step.project.pk
    )





@login_required
@require_POST
def request_changes(request, pk):
    """
    Return workflow step for revision.
    """


    step = get_object_or_404(
        WorkflowStep,
        pk=pk,
        project__owner=request.user,
    )


    step.feedback = request.POST.get(
        "feedback",
        ""
    ).strip()


    step.status = (
        WorkflowStep.Status.NEEDS_CHANGES
    )


    step.approval_status = (
        WorkflowStep.ApprovalStatus.REJECTED
    )


    step.save(
        update_fields=[
            "feedback",
            "status",
            "approval_status",
        ]
    )


    messages.warning(
        request,
        "Changes requested."
    )


    return redirect(
        "projects:detail",
        pk=step.project.pk
    )





class ProjectUpdateView(
    LoginRequiredMixin,
    UpdateView
):

    model = Project

    form_class = ProjectForm

    template_name = (
        "projects/project_edit.html"
    )


    def get_queryset(self):

        return Project.objects.filter(
            owner=self.request.user
        )


    def form_valid(self, form):

        messages.success(
            self.request,
            "Project updated successfully."
        )

        return super().form_valid(form)



    def get_success_url(self):

        return reverse_lazy(
            "projects:detail",
            kwargs={
                "pk": self.object.pk
            }
        )





class ProjectDeleteView(
    LoginRequiredMixin,
    DeleteView
):

    model = Project

    template_name = (
        "projects/project_delete.html"
    )


    def get_queryset(self):

        return Project.objects.filter(
            owner=self.request.user
        )


    def form_valid(self, form):

        messages.success(
            self.request,
            "Project deleted successfully."
        )

        return super().form_valid(form)



    def get_success_url(self):

        return reverse_lazy(
            "dashboard"
        )