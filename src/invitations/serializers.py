from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from accounts.models import User


class InviteUserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(default=User.USER_TYPE_EMPLOYEE, read_only=True)
    employee_type = serializers.ChoiceField(choices=User.EMPLOYEE_TYPE_CHOICES)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'user_type',
            'employee_type'
        )

    def validate_email(self, value):
        norm_email = value.lower()
        if User.objects.filter(email=norm_email).exists():
            raise serializers.ValidationError(
                _("This email has been already registered in our system.")
            )
        return norm_email


class EmployeeManagementSerializer(serializers.ModelSerializer):
    employee_type = serializers.ChoiceField(choices=User.EMPLOYEE_TYPE_CHOICES)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'employee_type', 'last_login']
