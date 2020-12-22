from django.apps import apps
from django.conf import settings
from django_dynamic_fixture import G

from accounts.constants import JOB_TYPE


def create_user(**kwargs):
    """Create an user along with their dependencies."""
    User = apps.get_model(settings.AUTH_USER_MODEL)
    user = G(User, **kwargs)
    user.set_password(kwargs.get('password', 'test'))
    user.save()
    return user


def create_company_user(**kwargs):
    User = apps.get_model(settings.AUTH_USER_MODEL)

    return create_user(user_type=User.USER_TYPE_COMPANY, **kwargs)


def create_candidate_user(**kwargs):
    User = apps.get_model(settings.AUTH_USER_MODEL)

    return create_user(user_type=User.USER_TYPE_CANDIDATE, **kwargs)


def create_agency_user(**kwargs):
    User = apps.get_model(settings.AUTH_USER_MODEL)

    return create_user(user_type=User.USER_TYPE_AGENCY, **kwargs)


def create_company(**kwargs):
    CompanyProfile = apps.get_model('accounts', 'CompanyProfile')
    ContactPerson = apps.get_model('accounts', 'ContactPerson')

    company = G(
        CompanyProfile,
        user=create_company_user(),
        **kwargs
    )

    G(ContactPerson, company=company)

    return company


def create_candidate(**kwargs):
    CandidateProfile = apps.get_model('accounts', 'CandidateProfile')

    return G(
        CandidateProfile,
        user=create_candidate_user(),
        job_type=[JOB_TYPE[0][0]],
        **kwargs
    )


# STATIC STUFF
def generate_technologies(amount=5):
    Technology = apps.get_model('accounts', 'Technology')

    return [
        G(Technology) for i in range(amount)
    ]
