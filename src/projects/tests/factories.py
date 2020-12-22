from django.apps import apps
from django_dynamic_fixture import G

from accounts.constants import JOB_TYPE


def create_project(company, **kwargs):
    Project = apps.get_model('projects', 'Project')

    return G(Project, company=company, **kwargs)


def create_position(project, **kwargs):
    Position = apps.get_model('projects', 'Position')

    return G(Position,
             project=project,
             company=project.company,
             job_type=[JOB_TYPE[0][0]],
             **kwargs)


def create_project_with_position(company, project_kwargs=None, position_kwargs=None):
    project_kwargs = project_kwargs or {}
    position_kwargs = position_kwargs or {}

    return create_position(
        create_project(
            company,
            **project_kwargs
        ),
        **position_kwargs
    )


def create_multiply_projects_with_positions(*args, count=5, **kwargs):
    return [
        create_project_with_position(*args, **kwargs) for _ in range(count)
    ]
