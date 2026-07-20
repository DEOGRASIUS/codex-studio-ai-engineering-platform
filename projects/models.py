from django.conf import settings
from django.db import models


class Project(models.Model):
    """
    Represents a user-owned software project.

    A project passes through multiple AI engineering stages
    from requirements gathering to final documentation.
    """

    class Complexity(models.TextChoices):
        SIMPLE = "simple", "Simple"
        MODERATE = "moderate", "Moderate"
        COMPLEX = "complex", "Complex"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_PROGRESS = "in_progress", "In Progress"
        WAITING_APPROVAL = "waiting_approval", "Waiting Approval"
        APPROVED = "approved", "Approved"
        NEEDS_CHANGES = "needs_changes", "Needs Changes"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        ARCHIVED = "archived", "Archived"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    technology = models.CharField(
        max_length=255,
        blank=True,
    )

    complexity = models.CharField(
        max_length=20,
        choices=Complexity.choices,
        default=Complexity.MODERATE,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-updated_at",
            "-created_at",
        ]

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    """
    Represents one AI engineer in the software engineering pipeline.

    Example:

    - Requirements Analyst
    - Project Manager
    - System Architect
    - UI/UX Designer
    - Database Engineer
    - Backend Engineer
    - Frontend Engineer
    - QA Engineer
    - Documentation Engineer
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        WAITING_APPROVAL = "waiting_approval", "Waiting Approval"
        APPROVED = "approved", "Approved"
        NEEDS_CHANGES = "needs_changes", "Needs Changes"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    class ApprovalStatus(models.TextChoices):
        NOT_REQUIRED = "not_required", "Not Required"
        WAITING = "waiting", "Waiting For Approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="workflow_steps",
    )

    step_name = models.CharField(max_length=100)

    step_order = models.PositiveSmallIntegerField()

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )

    approval_status = models.CharField(
        max_length=30,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.NOT_REQUIRED,
    )

    feedback = models.TextField(
        blank=True,
        help_text="User feedback when requesting changes.",
    )

    error_message = models.TextField(
        blank=True,
        help_text="Stores AI execution errors for retry purposes.",
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_workflow_steps",
    )

    class Meta:
        ordering = [
            "project_id",
            "step_order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "project",
                    "step_order",
                ],
                name="unique_project_workflow_step_order",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "project",
                    "status",
                ]
            ),
        ]

    def __str__(self):
        return (
            f"{self.project.name} - "
            f"{self.step_order}: "
            f"{self.step_name}"
        )


class GeneratedArtifact(models.Model):
    """
    Stores AI-generated outputs produced by workflow steps.

    Examples:
    - Requirements documents
    - System architecture
    - Database schema
    - Backend code
    - Frontend code
    - Test plans
    """

    workflow_step = models.ForeignKey(
        WorkflowStep,
        on_delete=models.CASCADE,
        related_name="artifacts",
    )

    title = models.CharField(max_length=255)

    artifact_type = models.CharField(max_length=100)

    content = models.TextField()

    approved = models.BooleanField(default=False)

    version = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "workflow_step_id",
            "-version",
            "-created_at",
        ]

    def __str__(self):
        return f"{self.title} (v{self.version})"