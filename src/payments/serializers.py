from rest_framework import serializers
from django.conf import settings

from accounts.models import User
from payments.utils import generate_agency_membership_payment_url


class AgencySubscriptionSerializer(serializers.ModelSerializer):
    redirect_url = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'redirect_url',
            'amount',
        )

    def get_redirect_url(self, obj):
        return generate_agency_membership_payment_url(obj)

    def get_amount(self, obj):
        return settings.PAYMENT_AGENCY_MEMBERSHIP_PRICE
