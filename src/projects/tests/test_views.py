import mock
from nose.tools import eq_, ok_
from django.urls import reverse

from base.tests import BaseTestCase
from accounts.tests import factories as account_f
from projects.tests import factories as project_f


class PositionApiTests(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.company = account_f.create_company()
        self.candidate = account_f.create_candidate()

    def test_project_creation(self):
        url = reverse('project-list')

        self.login(self.candidate.user)

        project_data = {
            'project_name': 'project_name',
            'project_description': 'A' * 256,
            'location': 'location'
        }

        # Wrong user type
        response = self.client.post(url, project_data)
        eq_(response.status_code, 403)

        # Company user without profile
        company_empty_user = account_f.create_company_user()
        self.login(company_empty_user)

        response = self.client.post(url, project_data)
        eq_(response.status_code, 403)

        # Correct user type
        self.login(self.company.user)

        response = self.client.post(url, project_data)
        eq_(response.status_code, 201)

    def test_company_projets(self):
        url = reverse('project-company-projets')
        project_f.create_multiply_projects_with_positions(self.company, count=5)

        # Wrong user type
        self.login(self.candidate.user)
        response = self.client.get(url)
        eq_(response.status_code, 403)

        # Correct user type
        self.login(self.company.user)
        response = self.client.get(url)
        eq_(response.status_code, 200)
        eq_(len(response.data), 5)

        # Test with another company
        company_2 = account_f.create_company()
        project_f.create_multiply_projects_with_positions(company_2, count=2)

        self.login(company_2.user)
        response = self.client.get(url)
        eq_(response.status_code, 200)
        eq_(len(response.data), 2)

    def test_project_list(self):
        url = reverse('project-list')
        project_f.create_multiply_projects_with_positions(self.company, count=5)
        self.client.logout()

        response = self.client.get(url)
        eq_(response.status_code, 200)
        eq_(len(response.data['results']), 5)

    def test_project_detail(self):
        self.client.logout()
        position = project_f.create_project_with_position(self.company)
        project = position.project
        url = reverse('project-detail', kwargs={'pk': project.pk})

        response = self.client.get(url)
        eq_(response.status_code, 200)

    @mock.patch('projects.views.send_mail')
    def test_apply_to_position(self, send_mail_mock):
        self.client.logout()
        self.client.force_authenticate(user=self.user)

        # Project and position creation
        position = project_f.create_project_with_position(self.company)
        url = reverse('position-apply', kwargs={
            'pk': position.pk
        })

        # Applying without candidate profile
        response = self.client.post(url)
        eq_(response.status_code, 403)

        self.client.logout()
        self.client.force_authenticate(user=self.candidate.user)

        # # Wrong position id request
        # response = self.client.post(reverse('position-apply', kwargs={
        #     'pk': 'WRONG_PK'
        # }))
        # eq_(response.status_code, 404)

        # # Application success
        # response = self.client.post(url)
        # eq_(response.status_code, 204)
        # ok_(send_mail_mock.called)

        # # Application duplication error
        # response = self.client.post(url)
        # eq_(response.status_code, 400)


class CompanyProjectApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.company = account_f.create_company()

    def test_positions(self):
        self.login(self.company.user)
        url = reverse('position-company-positions')

        position = project_f.create_project_with_position(self.company)

        response = self.client.get(url)
        eq_(response.status_code, 200)

        eq_(len(response.data), 1)
        ok_(all([field in response.data[0] for field in [
            'offers',
            'requirements',
            'project'
        ]]))
        eq_(response.data[0]['project'], str(position.pk))

        # Checking all jobs list
        url = reverse('position-list')
        response = self.client.get(url)
        eq_(response.status_code, 200)

        ok_('project' not in response.data['results'][0])
