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


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Felipe Frizzo',
            slug='felipe-frizzo',
            photo='http://google.com'
        )

        s.contact_set.create(kind=Contact.EMAIL, value='felipefrizzo@gmail.com')
        s.contact_set.create(kind=Contact.PHONE, value='4599230342')

    def test_email(self):
        qs = Contact.objects.emails()
        expected = ['felipefrizzo@gmail.com']

        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phone(self):
        qs = Contact.objects.phones()
        expected = ['4599230342']

        self.assertQuerysetEqual(qs, expected, lambda o: o.value)
