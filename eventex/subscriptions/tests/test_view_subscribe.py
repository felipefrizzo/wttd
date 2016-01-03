from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionsForm


class SubscribeGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscricao/ must return status code 200."""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscripitons_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """html must contains input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """Html must cotains csrf_token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscriptions_form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionsForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Felipe Frizzo', cpf='12345678901', email='felipefrizzo@gmail.com', phone='45-9923-0342')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEquals(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEquals(1, len(mail.outbox))


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionsForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        data = dict(name='Felipe Frizzo', cpf='12345678901', email='felipefrizzo@gmail.com', phone='45-9923-0342')
        self.response = self.client.post('/inscricao/', data, follow=True)

    def test_message(self):
        self.assertContains(self.response, 'Inscrição realizada com sucesso!')
