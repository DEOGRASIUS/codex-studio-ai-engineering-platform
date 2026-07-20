"""
URL routes for project management.
"""

from django.urls import path


from .views import (
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    project_detail,
    run_requirements,
    approve_step,
    request_changes,
)


from .workflow_views import (
    retry_workflow_step,
    pause_workflow_step,
    resume_workflow_step,
)



app_name = "projects"



urlpatterns = [

    # ----------------------------
    # Project CRUD
    # ----------------------------

    path(
        "create/",
        ProjectCreateView.as_view(),
        name="create",
    ),


    path(
        "<int:pk>/edit/",
        ProjectUpdateView.as_view(),
        name="edit",
    ),


    path(
        "<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="delete",
    ),


    path(
        "<int:pk>/",
        project_detail,
        name="detail",
    ),



    # ----------------------------
    # AI Engineer Execution
    # ----------------------------

    path(
        "<int:pk>/run-requirements/",
        run_requirements,
        name="run_requirements",
    ),



    # ----------------------------
    # Workflow Approval System
    # ----------------------------

    path(
        "workflow/<int:pk>/approve/",
        approve_step,
        name="approve_step",
    ),


    path(
        "workflow/<int:pk>/changes/",
        request_changes,
        name="request_changes",
    ),



    # ----------------------------
    # Workflow Controls
    # Retry / Pause / Resume
    # ----------------------------

    path(
        "workflow/<int:pk>/retry/",
        retry_workflow_step,
        name="retry_step",
    ),


    path(
        "workflow/<int:pk>/pause/",
        pause_workflow_step,
        name="pause_step",
    ),


    path(
        "workflow/<int:pk>/resume/",
        resume_workflow_step,
        name="resume_step",
    ),

]