"""
Generic workflow execution engine for Codex Studio.

Controls all AI engineering stages:
Requirements Analyst
Project Manager
System Architect
Designer
Database Engineer
Backend Engineer
Frontend Engineer
QA Engineer
Documentation Engineer
"""


from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from projects.models import (
    GeneratedArtifact,
    WorkflowStep,
)


# Import AI services here as they are created
from .services.requirements import generate_requirements



# Future agents will be added here

AGENT_HANDLERS = {

    "Requirements Analyst":
        generate_requirements,

    # "Project Manager":
    #     generate_project_plan,

    # "System Architect":
    #     generate_architecture,

    # "Designer":
    #     generate_design,

    # "Database Engineer":
    #     generate_database_design,

    # "Backend Engineer":
    #     generate_backend,

    # "Frontend Engineer":
    #     generate_frontend,

    # "QA Engineer":
    #     generate_testing,

    # "Documentation Engineer":
    #     generate_documentation,

}





def run_workflow_step(step):
    """
    Execute any AI engineer step.

    Workflow:

    Pending
        |
        v
    In Progress
        |
        v
    Waiting Approval
        |
        v
    Approved
    """


    agent = AGENT_HANDLERS.get(
        step.step_name
    )


    if not agent:

        raise Exception(
            f"No AI agent configured for {step.step_name}"
        )



    step.status = (
        WorkflowStep.Status.IN_PROGRESS
    )

    step.started_at = (
        step.started_at
        or timezone.now()
    )


    step.error_message = ""

    step.feedback = ""


    step.save(
        update_fields=[
            "status",
            "started_at",
            "error_message",
            "feedback",
        ]
    )



    try:

        content = agent(
            step.project
        )


    except Exception as exc:


        step.status = (
            WorkflowStep.Status.FAILED
        )


        step.error_message = str(exc)


        step.save(
            update_fields=[
                "status",
                "error_message",
            ]
        )


        raise




    with transaction.atomic():


        latest_version = (
            step.artifacts.aggregate(
                latest=Max("version")
            )["latest"]
            or 0
        )



        artifact = GeneratedArtifact.objects.create(

            workflow_step=step,

            title=f"{step.step_name} Output",

            artifact_type=(
                step.step_name.lower()
                .replace(" ", "_")
            ),

            content=content,

            version=latest_version + 1,

        )



        step.status = (
            WorkflowStep.Status.WAITING_APPROVAL
        )


        step.approval_status = (
            WorkflowStep.ApprovalStatus.WAITING
        )


        step.completed_at = timezone.now()



        step.save(
            update_fields=[
                "status",
                "approval_status",
                "completed_at",
            ]
        )


    return artifact