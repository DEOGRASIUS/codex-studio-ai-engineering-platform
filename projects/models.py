from django.conf import settings
from django.db import models


class Project(models.Model):
    """A user's software project and its high-level delivery state."""

    class Complexity(models.TextChoices):
        SIMPLE = 'simple', 'Simple'
        MODERATE = 'moderate', 'Moderate'
        COMPLEX = 'complex', 'Complex'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        IN_PROGRESS = 'in_progress', 'In progress'
        COMPLETED = 'completed', 'Completed'
        ARCHIVED = 'archived', 'Archived'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    technology = models.CharField(max_length=255, blank=True)
    complexity = models.CharField(
        max_length=20,
        choices=Complexity.choices,
        default=Complexity.MODERATE,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    """One ordered stage in a project's AI-assisted engineering workflow."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In progress'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='workflow_steps',
    )
    step_name = models.CharField(max_length=100)
    step_order = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['project_id', 'step_order']
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'step_order'],
                name='unique_project_workflow_step_order',
            ),
        ]

    def __str__(self):
        return f'{self.project.name} — {self.step_order}: {self.step_name}'


class GeneratedArtifact(models.Model):
    """A versioned output produced during a workflow step."""

    workflow_step = models.ForeignKey(
        WorkflowStep,
        on_delete=models.CASCADE,
        related_name='artifacts',
    )
    title = models.CharField(max_length=255)
    artifact_type = models.CharField(max_length=100)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['workflow_step_id', '-version', '-created_at']

    def __str__(self):
        return f'{self.title} (v{self.version})'
