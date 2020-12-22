from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView

from trench.views import (
    RequestMFAMethodActivationView,
    RequestMFAMethodDeactivationView,
    ChangePrimaryMethod
)
from trench.utils import get_mfa_model, user_token_generator
from trench.settings import api_settings

from authentication.serializers import (
    TwoFactorPhoneSerializerCreate,
    TwoFactorPhoneRequestMFAMethodDeactivationSerializer,
    ChangePrimaryMFAMethodSerializer,
    RequestMFACodeSerializer
)


__all__ = ('TwoFactorPhoneActivationView', 'TwoFactorDeactivationView', 'ChangePrimaryMFAMethodView',
           'RequestMFACodeView')


MFAMethod = get_mfa_model()


class TwoFactorPhoneActivationView(RequestMFAMethodActivationView):
    serializer_class = TwoFactorPhoneSerializerCreate

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.phone_number and not user.mfa_methods.filter(is_active=True, name='sms').exists():
            user.phone_number = None
            user.save()

        return super().post(request, *args, **kwargs)


class TwoFactorDeactivationView(RequestMFAMethodDeactivationView):
    serializer_class = TwoFactorPhoneRequestMFAMethodDeactivationSerializer


class ChangePrimaryMFAMethodView(ChangePrimaryMethod):
    serializer_class = ChangePrimaryMFAMethodSerializer
    queryset = ''


class RequestMFACodeView(GenericAPIView):
    serializer_class = RequestMFACodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mfa_method_name = serializer.validated_data.get('method')
        ephemeral_token = serializer.validated_data.get('ephemeral_token')
        user = user_token_generator.check_token(ephemeral_token)
        if mfa_method_name:
            obj = get_object_or_404(
                MFAMethod,
                user=user,
                name=mfa_method_name,
                is_active=True,
            )

        conf = api_settings.MFA_METHODS.get(mfa_method_name)

        if not conf:
            return Response(
                {'error', _('Requested MFA method does not exists')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        handler = conf.get('HANDLER')(
            user=user,
            obj=obj,
            conf=conf,
        )
        dispatcher_resp = handler.dispatch_message()
        return Response(dispatcher_resp)
