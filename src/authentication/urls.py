from django.conf.urls import include, url
from trench.settings import api_settings

from authentication import views


mfa_methods_choices = '|'.join(api_settings.MFA_METHODS.keys())


urlpatterns = [
    url(
        r'^accounts/me/2fa/(?P<method>(sms))/activate/$',
        views.TwoFactorPhoneActivationView.as_view(),
        name='mfa-activate-sms',
    ),
    url(
        r'^accounts/me/2fa/(?P<method>({}))/deactivate/$'.format(mfa_methods_choices),
        views.TwoFactorDeactivationView.as_view(),
        name='mfa-deactivate',
    ),
    url(
        r'^accounts/me/2fa/mfa/change-primary-method/$',
        views.ChangePrimaryMFAMethodView.as_view(),
        name='mfa-change-primary-method',
    ),
    url(r'^accounts/me/2fa/', include('trench.urls')),
    # Social auth
    url(r'^token/social/providers/$', views.SocialProvidersView.as_view()),
    url(r'^token/social/jwt-pair/(?:(?P<provider>[a-zA-Z0-9_-]+)/?)?$',
        views.SocialJWTPairOnlyAuthView.as_view()),
    url(r'^token/social/access-token/(?:(?P<provider>[a-zA-Z0-9_-]+)/?)?$',
        views.SocialJWTPairAccessTokenView.as_view()),
    url(r'^token/social/registration/$', views.RequireAccountTypeView.as_view()),
]
