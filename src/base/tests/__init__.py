from rest_framework.test import APITestCase, APIClient
from django.db.models import signals
from django.core.cache import cache

from accounts.tests import factories as account_f


class BaseTestCase(APITestCase):
    """
    Extends the APITestCase, adds a user
    and handles the client credentials setup.
    """

    def setUp(self):
        super(BaseTestCase, self).setUp()

        self.user = account_f.create_user(password='test123')

        self.client = APIClient()

        # Fixtures
        self.technologies = account_f.generate_technologies()

        signals.post_save.receivers = []
        signals.pre_save.receivers = []
        signals.m2m_changed.receivers = []
        signals.post_delete.receivers = []

    def login(self, user):
        self.client.logout()
        self.client.force_authenticate(user=user)

    def tearDown(self):
        super(BaseTestCase, self).tearDown()

        # Clear cache
        cache.clear()
