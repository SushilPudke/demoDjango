from trench.settings import api_settings as trench_settings


def get_mfa_ath_method(user):
    auth_method = (
        user.mfa_methods
            .filter(is_primary=True, is_active=True)
            .first()
    )
    if auth_method:
        conf = trench_settings.MFA_METHODS[auth_method.name]
        handler = conf['HANDLER'](
            user=user,
            obj=auth_method,
            conf=conf,
        )
        handler.dispatch_message()

        return auth_method
