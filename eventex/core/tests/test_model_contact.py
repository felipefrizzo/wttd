from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Felipe Frizzo',
            slug='felipe-frizzo',
            photo='http://google.com',
        )

    def test_email(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.EMAIL, value='felipefrizzo@gmail.com')

        self.assertTrue(Contact.objects.exists)

    def test_photo(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.PHONE, value='4599230342')

        self.assertTrue(Contact.objects.exists)

    def test_choices(self):
        """Contact king should be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='a', value='b')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL, value='felipefrizzo@gmail.com')
        self.assertEqual('felipefrizzo@gmail.com', str(contact))
