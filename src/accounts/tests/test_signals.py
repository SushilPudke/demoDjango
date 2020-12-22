from mock import patch
from django.db.models.signals import post_save
from django_dynamic_fixture import G

from base.tests import BaseTestCase
from accounts.tests import factories as account_f
from accounts.models import AgencyProfile
from payments.declared_signals import post_membership_activate
from accounts.declared_signals import post_profile_activate
from accounts.signals import (
    membership_activate_check_profile_activated,
    profile_save_check_profile_activated,
    agency_profile_activation
)


class AccountApiTests(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.agency_user = account_f.create_agency_user()

        post_membership_activate.connect(membership_activate_check_profile_activated)
        post_save.connect(profile_save_check_profile_activated, sender=AgencyProfile)
        post_profile_activate.connect(agency_profile_activation, sender=AgencyProfile)

    @patch('accounts.signals.send_agency_profile_activation_mail')
    def test_agency_profile_activation(self, agency_profile_activation=None):
        G(AgencyProfile, user=self.agency_user)

        agency_profile_activation.assert_not_called()

        # Activate membership
        post_membership_activate.send(sender=AgencyProfile, user=self.agency_user)

        agency_profile_activation.assert_called_once()
