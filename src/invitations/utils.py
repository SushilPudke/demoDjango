from django.contrib.auth.models import Permission
from guardian.shortcuts import remove_perm

from accounts.models import User

from .constants import (
    AGENCY_ADMIN_PERMISSIONS,
    AGENCY_HR_PERMISSIONS,
    AGENCY_MANAGER_PERMISSIONS,
    COMPANY_ADMIN_PERMISSIONS,
    COMPANY_HR_PERMISSIONS,
    COMPANY_MANAGER_PERMISSIONS,
)


def get_organization_profile(user):
    if user.user_type != User.USER_TYPE_EMPLOYEE:
        if user.agency:
            return user.agency
        if user.company:
            return user.company
    if user.user_type == User.USER_TYPE_EMPLOYEE:
        if user.employer.agency:
            return user.employer.agency
        if user.employer.company:
            return user.employer.company


def get_permission_list(user):
    if user.employer.user_type == User.USER_TYPE_AGENCY:
        if user.employee_type == User.EMPLOYEE_TYPE_ADMINISTRATOR:
            return AGENCY_ADMIN_PERMISSIONS
        if user.employee_type == User.EMPLOYEE_TYPE_MANAGER:
            return AGENCY_MANAGER_PERMISSIONS
        if user.employee_type == User.EMPLOYEE_TYPE_HR:
            return AGENCY_HR_PERMISSIONS
    if user.employer.user_type == User.USER_TYPE_COMPANY:
        if user.employee_type == User.EMPLOYEE_TYPE_ADMINISTRATOR:
            return COMPANY_ADMIN_PERMISSIONS
        if user.employee_type == User.EMPLOYEE_TYPE_MANAGER:
            return COMPANY_MANAGER_PERMISSIONS
        if user.employee_type == User.EMPLOYEE_TYPE_HR:
            return COMPANY_HR_PERMISSIONS


def set_permissions(user):
    permission_list = get_permission_list(user)
    obj = get_organization_profile(user)
    for perm in permission_list:
        user.user_permissions.add(Permission.objects.get(codename=perm))
        user.add_obj_perm(perm, obj)


def remove_permissions(user):
    permission_list = get_permission_list(user)
    obj = get_organization_profile(user)
    user.user_permissions.clear()
    user.save()
    for perm in permission_list:
        remove_perm(perm, user, obj)
    user.user_permissions.clear()
