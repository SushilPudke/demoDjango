from django.conf import settings

from .websms import WebSms


class WebSmsClient(WebSms):

    def __init__(self, *args, **kwargs):
        super().__init__(token=settings.WEBSMS_API_TOKEN)
