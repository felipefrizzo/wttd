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

    def test_str(self):
        self.assertEquals('Felipe Frizzo', str(self.obj))

    def test_paid_default_to_False(self):
        """By default paid must be False."""
        self.assertEqual(False, self.obj.paid)
