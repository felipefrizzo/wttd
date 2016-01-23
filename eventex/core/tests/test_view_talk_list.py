from django.test import TestCase
from django.shortcuts import resolve_url as r_url
from eventex.core.models import Talk, Speaker


class TalkListGet(TestCase):
    def setUp(self):
        t1 = self.Talk = Talk.objects.create(title='Titulo da Palestra', start='10:00', description='Descrição da Palestra')
        t2 = self.Talk = Talk.objects.create(title='Titulo da Palestra', start='13:00', description='Descrição da Palestra')

        speaker = Speaker.objects.create(
            name='Felipe Frizzo',
            slug='felipe-frizzo',
            website='http://google.com'
        )

        t1.speakers.add(speaker)
        t2.speakers.add(speaker)

        self.response = self.client.get(r_url('talk_list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/talk_list.html')

    def test_html(self):
        contents = [
            (2, 'Titulo da Palestra'),
            (1, '10:00'),
            (1, '13:00'),
            (2, '/palestrantes/felipe-frizzo/'),
            (2, 'Felipe Frizzo'),
            (2, 'Descrição da Palestra'),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_context(self):
        variables = ['morning_talks', 'afternoon_talks']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)


class TalkListEmpty(TestCase):
    def test_get_empty(self):
        response = self.client.get(r_url('talk_list'))

        self.assertContains(response, 'Ainda não existem palestras de Manhã')
        self.assertContains(response, 'Ainda não existem palestras de Tarde')
