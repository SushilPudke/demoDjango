from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from accounts.permissions import IsCompanyOrAgency
from base.utils import build_frontend_url

from .serializers import EmployeeManagementSerializer, InviteUserSerializer
from .utils import remove_permissions, set_permissions


class InviteUserAPIView(generics.CreateAPIView):
    """
    Invite and saves a User with the given email and password.
    """
    serializer_class = InviteUserSerializer
    permission_classes = (IsAuthenticated, IsCompanyOrAgency)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        employer = self.request.user
        password = User.objects.make_random_password()
        user_type = User.USER_TYPE_EMPLOYEE
        employee_type = serializer.validated_data.get('employee_type')
        user_obj = User(email=email, user_type=user_type, employer=employer,
                        is_active=True, employee_type=employee_type)
        user_obj.set_password(password)
        user_obj.save(user_obj)
        set_permissions(user_obj)
        token = ResetPasswordToken(user=user_obj)
        token.save()
        key = user_obj.password_reset_tokens.all().last().key
        url = build_frontend_url(f'invite/reset-password/{key}')
        html_message = loader.render_to_string(
            'accounts/invitation_letter.html',
            {
                'confirmation_url': url,
                'position': user_obj.readable_employee_type,
                'employer': user_obj.employer_organization_name
            }
        )
        send_mail(
            subject=_('Invitation to join a team '),
            message=_('Invitation to join a team '),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_obj.email],
            html_message=html_message
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmployeeListView(generics.ListAPIView):
    serializer_class = EmployeeManagementSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == User.USER_TYPE_COMPANY or user.user_type == User.USER_TYPE_AGENCY:
            return user.employees.all()


class EmployeeManagementView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeManagementSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == User.USER_TYPE_COMPANY or user.user_type == User.USER_TYPE_AGENCY:
            return user.employees.all()
        if user.user_type == User.USER_TYPE_EMPLOYEE:
            employer = user.employer
            return employer.employees.all()

    def put(self, request, *args, **kwargs):
        employee = self.get_object()
        employee_type = self.request.data['employee_type']
        if employee_type != employee.employee_type:
            self.change_permissions(employee, employee_type)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        employee = self.get_object()
        employee_type = self.request.data['employee_type']
        if employee_type != employee.employee_type:
            self.change_permissions(employee, employee_type)
        return self.partial_update(request, *args, **kwargs)

    def change_permissions(self, employee, employee_type):
        remove_permissions(employee)
        employee.employee_type = employee_type
        set_permissions(employee)
        employee.save()
