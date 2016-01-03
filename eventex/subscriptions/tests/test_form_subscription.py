from django.test.testcases import TestCase
from eventex.subscriptions.forms import SubscriptionsForm


class SubscriptionFormTest(TestCase):
    def setUp(self):
        self.form = SubscriptionsForm()

    def test_form_has_filters(self):
        """Form must have 4 fields"""
        expect = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expect, list(self.form.fields))
