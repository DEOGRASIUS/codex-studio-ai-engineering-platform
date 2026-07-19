from django.contrib import admin

from .models import GeneratedArtifact, Project, WorkflowStep


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'technology', 'complexity', 'status', 'updated_at')
    list_filter = ('status', 'complexity', 'technology')
    search_fields = ('name', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WorkflowStep)
class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = ('step_name', 'project', 'step_order', 'status', 'started_at', 'completed_at')
    list_filter = ('status',)
    search_fields = ('step_name', 'project__name')
    ordering = ('project_id', 'step_order')


@admin.register(GeneratedArtifact)
class GeneratedArtifactAdmin(admin.ModelAdmin):
    list_display = ('title', 'artifact_type', 'workflow_step', 'version', 'approved', 'created_at')
    list_filter = ('artifact_type', 'approved')
    search_fields = ('title', 'content', 'workflow_step__project__name')
    readonly_fields = ('created_at',)
