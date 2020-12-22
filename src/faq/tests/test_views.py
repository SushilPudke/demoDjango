from nose.tools import eq_
from django.urls import reverse

from base.tests import BaseTestCase


class QuestionsApiTests(BaseTestCase):

    def test_get_questions(self):
        url = reverse('question-list')
        response = self.client.get(url)
        eq_(response.status_code, 200)
