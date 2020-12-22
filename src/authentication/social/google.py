from social_core.backends.google import GoogleOAuth2 as _GoogleOAuth2

from base.utils import absolute_static_path
from authentication.social.common import SocialBackendBase


class GoogleOAuth2(SocialBackendBase, _GoogleOAuth2):
    LABEL = 'Google'
    ICON = absolute_static_path('social/google.png')
