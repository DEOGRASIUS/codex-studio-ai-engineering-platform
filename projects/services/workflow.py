from django.utils import timezone

from projects.models import (
    Project,
    WorkflowStep,
)


def get_next_step(current_step):
    """
    Returns the next workflow step
    for the same project.
    """

    return (
        WorkflowStep.objects
        .filter(
            project=current_step.project,
            step_order__gt=current_step.step_order,
        )
        .order_by("step_order")
        .first()
    )


def approve_step(step, user):
    """
    Approves the current workflow step.
    """

    step.approval_status = WorkflowStep.ApprovalStatus.APPROVED
    step.status = WorkflowStep.Status.COMPLETED

    step.approved_at = timezone.now()
    step.approved_by = user

    step.save()

    project = step.project

    next_step = get_next_step(step)

    if next_step:

        next_step.status = WorkflowStep.Status.PENDING
        next_step.save()

        project.status = Project.Status.IN_PROGRESS

    else:

        project.status = Project.Status.COMPLETED

    project.save()

    return next_step


def request_changes(step, feedback):
    """
    Sends the engineer back for revision.
    """

    step.status = WorkflowStep.Status.NEEDS_CHANGES
    step.approval_status = WorkflowStep.ApprovalStatus.REJECTED
    step.feedback = feedback

    step.save()

    return step


def retry_step(step):
    """
    Retry a failed engineer.
    """

    step.status = WorkflowStep.Status.PENDING
    step.error_message = ""

    step.save()

    return step


def pause_step(step):
    """
    Pause the current engineer.
    """

    step.status = WorkflowStep.Status.PAUSED
    step.save()

    return step


def resume_step(step):
    """
    Resume a paused engineer.
    """

    step.status = WorkflowStep.Status.PENDING
    step.save()

    return step