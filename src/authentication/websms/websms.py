"""
WebSms messaging class.

Copyright © 2018 confirm IT solutions
"""

__all__ = (
    'WebSms',
)

from urllib.request import Request, urlopen
from base64 import b64encode
from json import dumps

API_URL = 'https://api.websms.com/rest'


class WebSms:
    """
    API class to send text messages and WhatsApp messages via the API of
    websms.com.

    .. seealso::

        https://developer.websms.com/web-api/
    """

    def __init__(self, token=None, username=None, password=None):
        """
        :param str token: The token used for a login with an access token (option A)
        :param str username: The username used for a login with credentials (option B)
        :param str password: The password used for a login with credentials (option B)
        """
        if token:
            authorization_header = 'Bearer ' + token
        elif username and password:
            base64_credentials = b64encode('{}:{}'.format(username, password))
            authorization_header = 'Basic ' + base64_credentials
        else:
            raise TypeError('WebSms needs to be instantiated with a username & password OR a token')

        self.request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': authorization_header,
        }

    def request(self, endpoint, data):
        """
        Send a HTTP POST request to the API endpoint.

        :param str endpoint: The URL of the API endpoint
        :param dict data: The POST data
        :return: The HTTP (JSON) response
        :rtype: str
        """
        url = API_URL + endpoint
        data = dumps(data).encode()
        request = Request(url=url, headers=self.request_headers, data=data)
        response = urlopen(request).read().decode()

        return response

    def send_text_message(self, message, recipients, sender_address=None, flash_sms=False):
        """
        Sends a text message to a list of recipients.

        :param str text: The message content
        :param list recipients: The list of E164 formatted MSISDN recipients
        :param senderAddress: The address of the sender
        :type senderAddress: None or str
        :param bool flashSms: Send the message as flash SMS
        """
        if isinstance(recipients, (int, str)):
            recipients = [recipients]

        data = {
            'messageContent': message,
            'recipientAddressList': recipients,
            'sendAsFlashSms': flash_sms
        }

        if sender_address:
            data['senderAddress'] = sender_address
            if not sender_address.isnumeric():
                data['senderAddressType'] = 'alphanumeric'

        return self.request('/smsmessaging/text', data)

    def send_whatsapp_message(self, message, recipients):
        """
        Sends a whatsapp message (broadcast) to a list of recipients.

        :param str message: The message content
        :param list recipients: The list of E164 formatted MSISDN recipients
        """
        data = {
            'messageContent': message,
            'recipientAddressList': self.convert_to_msisdn_numbers(recipients),
        }

        return self.request('/converged/whatsapp', data)
