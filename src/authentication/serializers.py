from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from trench.serializers import (
    RequestMFAMethodActivationSerializer,
    RequestMFAMethodDeactivationSerializer,
)
from trench.utils import user_token_generator
from trench.serializers import MFA_METHODS
from trench.settings import api_settings

from accounts.models import User


class TwoFactorPhoneSerializerCreate(RequestMFAMethodActivationSerializer):
    phone_number = serializers.RegexField(regex=r'^\+[1-9]\d{1,14}$')

    default_error_messages = {
        **RequestMFAMethodActivationSerializer.default_error_messages,
        **{
            'already_in_use': _('This phone number is already in use')
        }
    }

    def validate_phone_number(self, val):
        if User.objects.filter(phone_number=val).exclude(pk=self.user.pk).exists():
            raise self.fail('already_in_use')

        return val


class ProtectedPasswordActionSerializer(serializers.Serializer):
    requires_password = None

    password = serializers.CharField(
        required=False,
    )

    default_error_messages = {
        'password_missing': _('Password not provided.'),
        'incorrect_password': _('Incorrect password'),
    }

    def _validate_password(self, value):
        if not value:
            self.fail('password_missing')

        obj = self.context['obj']
        user = obj.user

        if not user.check_password(value):
            self.fail('incorrect_password')

        return value

    def validate(self, data):
        if self.requires_password:
            self._validate_password(data.get('password'))

        return super().validate(data)


class TwoFactorPhoneRequestMFAMethodDeactivationSerializer(
    ProtectedPasswordActionSerializer,
    RequestMFAMethodDeactivationSerializer
):
    requires_password = False
    requires_mfa_code = True


class ChangePrimaryMFAMethodSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=MFA_METHODS)

    default_error_messages = {
        'not_enabled': _('2FA is not enabled.'),
        'invalid_code': _('Invalid or expired code.'),
        'missing_method': _('Target method does not exist or is not active.'),
        'already_primary': _('This method already setted as primary.')
    }

    def validate(self, attrs):
        user = self.context.get('request').user
        try:
            current_method = user.mfa_methods.get(
                is_primary=True,
                is_active=True,
            )
        except ObjectDoesNotExist:
            self.fail('not_enabled')
        try:
            new_primary_method = user.mfa_methods.get(
                name=attrs.get('method'),
                is_active=True,
            )
        except ObjectDoesNotExist:
            self.fail('missing_method')
        if current_method == new_primary_method:
            self.fail('already_primary')

        attrs.update(new_method=new_primary_method)
        attrs.update(old_method=current_method)
        return attrs

    def save(self):
        new_method = self.validated_data.get('new_method')
        old_method = self.validated_data.get('old_method')
        new_method.is_primary = True
        old_method.is_primary = False
        new_method.save()
        old_method.save()


class RequestMFACodeSerializer(serializers.Serializer):
    """
    Validates given token and method.
    """
    ephemeral_token = serializers.CharField()
    method = serializers.CharField()

    default_error_messages = {
        'invalid_token': _('Invalid or expired token.'),
        'mfa_method_not_exists': _('Requested MFA method does not exists'),
    }

    def validate_method(self, value):
        if value and value not in api_settings.MFA_METHODS:
            self.fail('mfa_method_not_exists')
        return value

    def validate(self, attrs):
        ephemeral_token = attrs.get('ephemeral_token')
        self.user = user_token_generator.check_token(ephemeral_token)
        if not self.user:
            self.fail('invalid_token')
        return attrs


class OAuth2InputAccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class SocialAuthRegistrationStepSerializer(serializers.Serializer):
    ephemeral_token = serializers.CharField()
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)
    email = serializers.EmailField(required=False)

    def validate_email(self, value):
        value = value.lower()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _("This email has been already registered in our system.")
            )

        return value

    @property
    def partial_details(self):
        return self.context['partial'].data['kwargs']['details']

    def validate(self, attrs):
        if self.partial_details.get('email'):
            attrs.pop('email', None)
        elif not attrs.get('email'):
            raise serializers.ValidationError('Email is required')

        return attrs
