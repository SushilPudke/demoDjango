from django.conf import settings
from django.http import Http404, HttpResponseBadRequest
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_social_auth.views import SocialJWTPairOnlyAuthView as _SocialJWTPairOnlyAuthView
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend
from social_django.utils import load_backend, load_strategy

from accounts.serializers import JWTAuthSerializer
from accounts.views import ExtendedMFACredentialsLoginMixin
from authentication.serializers import OAuth2InputAccessTokenSerializer, SocialAuthRegistrationStepSerializer
from authentication.social.facebook import FacebookOAuth2
from authentication.social.linkedin import LinkedinOAuth2
from authentication.social.google import GoogleOAuth2
from authentication.utils import get_mfa_ath_method


class RequireAccountTypeView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SocialAuthRegistrationStepSerializer

    def get_partial(self):
        strategy = load_strategy()
        partial = strategy.partial_load(self.request.data.get('ephemeral_token'))

        if not partial:
            raise Http404()

        return partial

    def post(self, request, *args, **kwargs):
        partial = self.get_partial()
        backend = load_backend(load_strategy(),
                               partial.backend, None)

        serializer = self.get_serializer_class()(data=request.data, context={
            'partial': partial
        })
        serializer.is_valid(raise_exception=True)

        if isinstance(backend, BaseOAuth2):
            access_token = partial.data['kwargs']['response']['access_token']
        else:
            return HttpResponseBadRequest()

        serializer.data.pop('ephemeral_token')
        user = backend.do_auth(access_token, **serializer.data)

        # cleanup
        partial.delete()

        return Response(JWTAuthSerializer(user).data)


class SocialJWTPairAccessTokenView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OAuth2InputAccessTokenSerializer

    def post(self, request, provider=None, *args, **kwargs):
        try:
            backend = load_backend(load_strategy(), provider, None)
        except MissingBackend:
            raise Http404('Backend not found')

        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = backend.do_auth(serializer.data['access_token'])

        if isinstance(response, Response):
            return response

        # Checking 2FA
        mfa = get_mfa_ath_method(response)

        if mfa:
            response = ExtendedMFACredentialsLoginMixin().handle_mfa_response(response, mfa)
            response.data['action'] = '2FA'

            return response

        return Response(JWTAuthSerializer(response).data)


class SocialJWTPairOnlyAuthView(_SocialJWTPairOnlyAuthView):
    serializer_class = JWTAuthSerializer


class SocialProvidersView(GenericAPIView):
    permission_classes = (AllowAny,)
    PROVIDERS = [
        LinkedinOAuth2,
        FacebookOAuth2,
        GoogleOAuth2,
    ]

    def get(self, request, *args, **kwargs):
        data = []

        for cls in self.PROVIDERS:
            backend = cls(
                redirect_uri=settings.SOCIAL_AUTH_REDIRECT_URL.format(PROVIDER=cls.name)
            )

            data.append({
                'label': backend.get_label(),
                'name': backend.name,
                'icon': backend.get_icon(),
                'auth_url': backend.auth_url(),
                'client_id': backend.get_key_and_secret()[0],
            })

        return Response(data)
