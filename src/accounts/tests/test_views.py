from nose.tools import eq_
from django.urls import reverse

from base.tests import BaseTestCase
from accounts.tests import factories as account_f


class AccountApiTests(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.company = account_f.create_company_user(password="1rM9oETJ")
        self.candidate = account_f.create_candidate_user()

    def test_user_creation(self):
        url = reverse("create")
        password = "1rM9oETJ",

        # Company user
        response = self.client.post(
            url,
            {
                "email": 'company_user@test.com',
                "password": password,
                "user_type": "COMPANY"
            }
        )
        eq_(response.status_code, 201)

        # Candidate user
        response = self.client.post(
            url,
            {
                "email": 'candidate_user@test.com',
                "password": password,
                "user_type": "CANDIDATE"
            }
        )
        eq_(response.status_code, 201)

        # Wrong email
        response = self.client.post(
            url,
            {
                "email": 'wrong_email.test.com',
                "password": password,
                "user_type": "CANDIDATE"
            }
        )
        eq_(response.status_code, 400)
        eq_(response.content, b'{"email":["Enter a valid email address."]}')

        # Existing email
        response = self.client.post(
            url,
            {
                "email": 'candidate_user@test.com',
                "password": password,
                "user_type": "CANDIDATE"
            }
        )
        eq_(response.status_code, 400)
        eq_(response.content, b'{"email":["This email has been already registered in our system."]}')

        # Wrong user_type
        response = self.client.post(
            url,
            {
                "email": 'spectrator_user@test.com',
                "password": password,
                "user_type": "SPECTATOR"
            }
        )
        eq_(response.status_code, 400)
        eq_(response.content, b'{"user_type":["\\"SPECTATOR\\" is not a valid choice."]}')

        # Common password
        response = self.client.post(
            url,
            {
                "email": 'common_password@test.com',
                "password": "Qq123456",
                "user_type": "CANDIDATE"
            }
        )
        eq_(response.status_code, 400)
        eq_(response.content, b'{"password":["This password is too common."]}')

        # Short password
        response = self.client.post(
            url,
            {
                "email": 'short_password@test.com',
                "password": "Qq123",
                "user_type": "CANDIDATE"
            }
        )
        eq_(response.status_code, 400)
        eq_(response.content, b'{"password":["This password is too short. It must contain at least 8 characters."]}')

        # Numeric password
        response = self.client.post(
            url,
            {
                "email": 'numeric_password@test.com',
                "password": "776493483",
                "user_type": "CANDIDATE"
            }
        )
        eq_(response.status_code, 400)
        eq_(response.content, b'{"password":["This password is entirely numeric."]}')

        # Lowercase password
        response = self.client.post(
            url,
            {
                "email": 'lowercase_password@test.com',
                "password": password[0].lower(),
                "user_type": "CANDIDATE"
            }
        )
        eq_(response.status_code, 400)
        eq_(response.content, b'{"password":["The password must contain at least 1 uppercase letter"]}')

    def test_change_password(self):
        url = reverse('change_password')
        old_password = "1rM9oETJ"
        new_password = "eDkq6vRY"
        self.login(self.company)

        # Test change password without old_password
        response = self.client.put(
            url,
            {
                "new_password": new_password
            }
        )
        eq_(response.status_code, 400)

        # Change password
        response = self.client.put(
            url,
            {
                "old_password": old_password,
                "new_password": new_password
            }
        )
        eq_(response.status_code, 200)

        # Wrong old_password
        response = self.client.put(
            url,
            {
                "old_password": old_password,
                "new_password": new_password
            }
        )
        eq_(response.status_code, 400)

    def test_change_password_without_password(self):
        self.login(self.company)

        url = reverse('change_password')
        password = "eDkq6vRY"
        new_password = "1rM9oETJ"

        # Test change password without old_password
        response = self.client.put(
            url,
            {
                "new_password": password
            }
        )
        eq_(response.status_code, 400)

        # Setting has_password to True
        self.company.has_password = False
        self.company.save()

        # Change password
        response = self.client.put(
            url,
            {
                "new_password": password
            }
        )
        eq_(response.status_code, 200)

        # trying to change it again without old_password
        response = self.client.put(
            url,
            {
                "new_password": password
            }
        )
        eq_(response.status_code, 400)

        # trying to change it again with new_password

        # Wrong old_password
        response = self.client.put(
            url,
            {
                "old_password": password,
                "new_password": new_password
            }
        )
        eq_(response.status_code, 200)
