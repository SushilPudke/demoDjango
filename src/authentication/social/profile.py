import logging

from social_django.models import UserSocialAuth

logger = logging.getLogger(__name__)


class ProfileExtracter(object):
    fields_mapping = {}

    def __init__(self, social_auth: UserSocialAuth):
        self.social_auth = social_auth
        self.data = self.social_auth.extra_data

    def extract_field(self, name):
        raise NotImplementedError

    def extract_data(self):
        try:
            return {
                key: self.extract_field(orig_key)
                for key, orig_key in self.fields_mapping.items()
            }
        except Exception as exc:
            logger.exception(exc)

        return {}


class ProfileExtractLinkedin(ProfileExtracter):
    fields_mapping = {
        'first_name': 'first_name',
        'last_name': 'last_name',
    }

    def extract_field(self, name):
        obj = self.data.get(name, dict())

        if not obj:
            return None

        localized = obj.get('localized')

        if not isinstance(obj['localized'], dict) or not localized:
            return None

        return list(localized.values())[0]
