from social_core.backends.linkedin import LinkedinOAuth2 as _LinkedinOAuth2

from base.utils import absolute_static_path
from authentication.social.common import SocialBackendBase
from authentication.social.profile import ProfileExtractLinkedin


class LinkedinOAuth2(SocialBackendBase, _LinkedinOAuth2):
    LABEL = 'LinkedIn'
    ICON = absolute_static_path('social/linkedin.png')
    profile_extractor = ProfileExtractLinkedin
