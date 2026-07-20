import os

from agents.providers.router import generate_with_ai
from agents.prompts.requirements import REQUIREMENTS_ANALYST_SYSTEM_PROMPT


def generate_requirements(project):
    """
    Generate a requirements document for a project
    using the configured AI provider.
    """

    project_context = f"""
Project name: {project.name}

Description:
{project.description or 'No description provided.'}

Technology stack:
{project.technology or 'Not specified.'}

Complexity:
{project.get_complexity_display()}
""".strip()

    content = generate_with_ai(
        REQUIREMENTS_ANALYST_SYSTEM_PROMPT,
        project_context,
    )

    if not content:
        raise ValueError(
            "The Requirements Analyst returned no content."
        )

    return content