from django.core import mail
from django.test.testcases import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Felipe Frizzo', cpf='12345678901', email='felipefrizzo@gmail.com', phone='45-9923-0342')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email(self):
        expect = 'Confirmação de inscrição'

        self.assertEquals(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEquals(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'felipefrizzo@gmail.com']

        self.assertEquals(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Felipe Frizzo', '12345678901', 'felipefrizzo@gmail.com', '45-9923-0342']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
