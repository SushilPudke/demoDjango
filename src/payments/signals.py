import logging

from django.dispatch import receiver
from django.conf import settings
from django.forms.models import model_to_dict
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.signals import valid_ipn_received

from accounts.models import User
from payments.declared_signals import post_membership_activate

logger = logging.getLogger(__name__)


@receiver(valid_ipn_received)
def paypal_ipn_handler(sender: PayPalIPN, **kwargs):
    ipn_obj = sender

    logger.info('Income Paypal payment request: \n {}'.format(model_to_dict(ipn_obj)))

    if ipn_obj.payment_status != ST_PP_COMPLETED:
        logger.error('Order status is not success')

    try:
        user = User.objects.get(pk=ipn_obj.invoice)
    except User.DoesNotExist:
        logger.error('Wrong order {}'.format(ipn_obj.invoice))

        return

    if settings.PAYPAL_BUSINESS not in (
            ipn_obj.receiver_email,
            ipn_obj.receiver_id
    ):
        # Not a valid payment
        logger.error('Wrong Paypal Receiver Email')

        return

    if float(ipn_obj.mc_gross) != settings.PAYMENT_AGENCY_MEMBERSHIP_PRICE \
            or ipn_obj.mc_currency != settings.PAYMENT_CURRENCY:
        logger.error('Wrong amount or currency\n'
                     'Order Amount: {} | IPN Amount: {}\n'
                     'Order Currency: {} | IPN Currency: {}'
                     .format(settings.PAYMENT_AGENCY_MEMBERSHIP_PRICE,
                             ipn_obj.mc_gross,
                             settings.POSTFINANCE_CURRENCY,
                             ipn_obj.mc_currency)
                     )

        return None

    # Activating agency membership
    user.activate_membership()

    # Emitting signal
    post_membership_activate.send(sender=user.agency.__class__, user=user)
