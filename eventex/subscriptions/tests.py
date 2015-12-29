from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionsForm


class SubscribeTest(TestCase):
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
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """Html must cotains csrf_token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscriptions_form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionsForm)

    def test_form_has_filters(self):
        """Form must have 4 fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Felipe Frizzo', cpf='12345678901', email='felipefrizzo@gmail.com', phone='45-9923-0342')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEquals(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEquals(1, len(mail.outbox))

    def test_subscription_email(self):
        expect = 'Confirmação de inscrição'

        self.assertEquals(expect, self.email.subject)

    def test_subscripiton_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEquals(expect, self.email.from_email)

    def test_subcription_email_to(self):
        expect = ['contato@eventex.com.br', 'felipefrizzo@gmail.com']

        self.assertEquals(expect, self.email.to)

    def test_subcription_email_body(self):
        self.assertIn('Felipe Frizzo', self.email.body)
        self.assertIn('12345678901', self.email.body)
        self.assertIn('felipefrizzo@gmail.com', self.email.body)
        self.assertIn('45-9923-0342', self.email.body)


class SubscribeInvalidPost(TestCase):
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


class SubscribeSucessMessage(TestCase):
    def setUp(self):
        data = dict(name='Felipe Frizzo', cpf='12345678901', email='felipefrizzo@gmail.com', phone='45-9923-0342')
        self.response = self.client.post('/inscricao/', data, follow=True)

    def test_message(self):
        self.assertContains(self.response, 'Inscrição realizada com sucesso!')
