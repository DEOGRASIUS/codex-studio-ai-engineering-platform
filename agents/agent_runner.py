"""
Orchestration entry points for the Codex Studio workflow.

Controls AI engineer execution lifecycle:

Pending
    ↓
In Progress
    ↓
Waiting Approval
    ↓
Human Approval
    ↓
Approved
    ↓
Next Engineer Unlocked
"""

from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from projects.models import (
    GeneratedArtifact,
    WorkflowStep,
)

from .services.requirements import generate_requirements


REQUIREMENTS_ANALYST_STEP = "Requirements Analyst"



def run_requirements_agent(project):
    """
    Execute the Requirements Analyst workflow step.

    Lifecycle:

    PENDING
        |
        ↓
    IN_PROGRESS
        |
        ↓
    WAITING_APPROVAL
        |
        ↓
    APPROVED
        |
        ↓
    Next workflow engineer
    """

    workflow_step = project.workflow_steps.get(
        step_name=REQUIREMENTS_ANALYST_STEP
    )


    # ---------------------------------
    # Start execution
    # ---------------------------------

    workflow_step.status = (
        WorkflowStep.Status.IN_PROGRESS
    )

    workflow_step.started_at = (
        workflow_step.started_at
        or timezone.now()
    )


    # Clear previous errors/review comments
    workflow_step.feedback = ""
    workflow_step.error_message = ""


    workflow_step.approval_status = (
        WorkflowStep.ApprovalStatus.NOT_REQUIRED
    )


    workflow_step.save(
        update_fields=[
            "status",
            "started_at",
            "feedback",
            "error_message",
            "approval_status",
        ]
    )



    # ---------------------------------
    # Run AI generation
    # ---------------------------------

    try:

        content = generate_requirements(
            project
        )


    except Exception as exc:


        workflow_step.status = (
            WorkflowStep.Status.FAILED
        )

        workflow_step.error_message = str(exc)


        workflow_step.save(
            update_fields=[
                "status",
                "error_message",
            ]
        )


        raise



    # ---------------------------------
    # Save generated artifact
    # Move step to approval queue
    # ---------------------------------

    with transaction.atomic():


        latest_version = (
            workflow_step.artifacts.aggregate(
                latest=Max("version")
            )["latest"]
            or 0
        )



        artifact = GeneratedArtifact.objects.create(

            workflow_step=workflow_step,

            title="Requirements Analysis",

            artifact_type="requirements_document",

            content=content,

            approved=False,

            version=latest_version + 1,

        )



        workflow_step.status = (
            WorkflowStep.Status.WAITING_APPROVAL
        )


        workflow_step.approval_status = (
            WorkflowStep.ApprovalStatus.WAITING
        )


        workflow_step.completed_at = (
            timezone.now()
        )



        workflow_step.save(
            update_fields=[
                "status",
                "approval_status",
                "completed_at",
            ]
        )



    return artifact