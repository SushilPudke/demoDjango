from django.utils.translation import ugettext_lazy as _
from trench.backends import AbstractMessageDispatcher
from trench.backends.application import ApplicationBackend
from trench.utils import create_qr_link

from authentication.websms import WebSmsClient


client = WebSmsClient()


class TwoFactorPhoneAuthBackend(AbstractMessageDispatcher):
    SMS_BODY = _('Your verification code is: ')

    def dispatch_message(self):
        """
        Sends a SMS with verification code.
        :return:
        """
        print(self.to)
        code = self.create_code()

        self.send_sms(self.to, code)

        print('~CODE', code)
        return {'message': _('SMS message with MFA code has been sent.')}

    def send_sms(self, user_mobile, code):
        client = self.provider_auth()
        client.send_text_message(self.SMS_BODY + code, user_mobile)

    def provider_auth(self):
        return client


class ExtendedApplicationBackend(ApplicationBackend):
    def dispatch_message(self):
        return {
            'qr_link': create_qr_link(self.obj.secret, self.user),
            'key': self.obj.secret
        }
