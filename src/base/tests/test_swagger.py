from django.urls import reverse

from base.tests import BaseTestCase
from accounts.tests import factories as account_f


class PositionApiTests(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.company = account_f.create_company()
        self.candidate = account_f.create_candidate()

    def test_swagger_response_ok(self):
        url = reverse('swagger-docs')
        users = [None, self.company.user, self.candidate.user]

        for user in users:
            if not user:
                self.client.logout()
            else:
                self.login(user)

            response = self.client.get(url)
            assert response.status_code == 200
