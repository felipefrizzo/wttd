from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Felipe Frizzo',
            cpf='12345678901',
            email='felipefrizzo@gmail.com',
            phone='45-99230342'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_create_date(self):
        """Subscription must have an auto created_at attrs."""
        self.assertIsInstance(self.obj.created_at, datetime)
