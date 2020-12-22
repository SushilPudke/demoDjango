from rest_framework import status
from rest_framework.response import Response
from social_core.pipeline.partial import partial

from accounts.models import User


class ResponseError(Response):
    def __init__(self, detail, *args, **kwargs):
        kwargs.setdefault('status', status.HTTP_400_BAD_REQUEST)

        response = {
            'detail': detail,
        }

        code = kwargs.pop('code', None)

        if code:
            response.update({'code': code})

        super().__init__(response, *args, **kwargs)


USER_FIELDS = ['email']


def check_email(backend, details, response, *args, **kwargs):
    if not details.get('email'):
        return ResponseError(
            'Unable to retrieve email',
            code='email_required'
        )

    details['email'] = details['email'].lower()


@partial
def require_city(strategy, details, user=None, is_new=False, *args, **kwargs):
    required_fields = (
        'user_type',
        'email',
    )

    # Skipping for existing users or for fields
    if not is_new or all([field in required_fields for field in kwargs]):
        return

    requested_fields = []

    for field in required_fields:
        if not details.get(field):
            val = kwargs.get(field)

            if val:
                details[field] = val
            else:
                requested_fields.append(field)

    if requested_fields:
        current_partial = kwargs.get('current_partial')

        return Response({
            'action': 'REGISTRATION',
            'ephemeral_token': current_partial.token,
            'required_fields': requested_fields
        })


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = {}
    user_exists = User.objects.filter(email=details['email']).exists()

    # Checking if user exists for further linking
    if not user_exists:
        fields = dict((name, kwargs.get(name, details.get(name)))
                      for name in backend.setting('USER_FIELDS', USER_FIELDS))
        if not fields:
            return

    user = strategy.create_user(is_active=True, **fields)

    if not user_exists:
        user.has_password = False
        user.save()

    return {
        'is_new': True,
        'user': user
    }
