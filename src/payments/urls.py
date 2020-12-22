from django.conf.urls import include, url
from rest_framework import routers

from payments.views import AgencySubscriptionView


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'accounts/me/payment/membership', AgencySubscriptionView,
                basename='payment-agency-membership')

urlpatterns = router.urls + [
    url(r'^payment/paypal/webhook', include('paypal.standard.ipn.urls')),
]
