from base.utils import build_frontend_url, build_backend_url


def build_candidate_url(pk):
    return build_frontend_url('/candidate/{}'.format(str(pk)))


def build_position_url(pk):
    return build_frontend_url('/position/{}'.format(str(pk)))


def build_candidate_admin_url(pk):
    return build_backend_url(f'admin/accounts/candidateprofile/{pk}/')


def build_agency_admin_url(pk):
    return build_backend_url(f'admin/accounts/agencyprofile/{pk}/')


def build_position_admin_url(pk):
    return build_backend_url(f'admin/accounts/position/{pk}/')


def build_company_admin_url(pk):
    return build_backend_url(f'admin/accounts/companyprofile/{pk}/')


def build_candidate_cv_url(pk):
    return build_backend_url(f'/admin/accounts/candidatecv/{pk}')
