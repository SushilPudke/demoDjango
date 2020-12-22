from social_core.backends.facebook import FacebookOAuth2 as _FacebookOAuth2

from base.utils import absolute_static_path
from authentication.social.common import SocialBackendBase


class FacebookOAuth2(SocialBackendBase, _FacebookOAuth2):
    LABEL = 'Facebook'
    ICON = absolute_static_path('social/facebook.png')
