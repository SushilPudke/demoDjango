from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.conf import POSTBACK_ENDPOINT, SANDBOX_POSTBACK_ENDPOINT

from base.utils import (
    build_backend_url,
    build_frontend_url,
    add_url_params,
)
from accounts.models import User


def generate_paypal_payment_url():
    return SANDBOX_POSTBACK_ENDPOINT if settings.PAYPAL_TEST else POSTBACK_ENDPOINT


def generate_form_paypal(order_id, amount, **kwargs):
    form_params = {
        "business": settings.PAYPAL_BUSINESS,
        "item_name": str(_("Agency membership")),
        "currency_code": settings.PAYMENT_CURRENCY,
        "invoice": str(order_id),
        "notify_url": build_backend_url(reverse('paypal-ipn')),
        "return": build_frontend_url(settings.PAYPAL_FRONTEND_SUCCESS_URL),
        "cancel_return": build_frontend_url(settings.PAYPAL_FRONTEND_CANCEL_URL),
        "no_note": 1,
        "no_shipping": 1,
        "amount": amount,
    }
    form_params.update(kwargs)

    return {
        f.name: f.value()
        for f in PayPalPaymentsForm(initial=form_params)
    }


def generate_form_paypal_agency_membership(user: User):
    return generate_form_paypal(user.pk, settings.PAYMENT_AGENCY_MEMBERSHIP_PRICE)


def generate_agency_membership_payment_url(user: User):
    return add_url_params(
        generate_paypal_payment_url(),
        generate_form_paypal_agency_membership(user)
    )
