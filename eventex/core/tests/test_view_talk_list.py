from django.test import TestCase
from django.shortcuts import resolve_url as r_url
from eventex.core.models import Talk, Speaker, Course


class TalkListGet(TestCase):
    def setUp(self):
        t1 = Talk.objects.create(title='Titulo da Palestra', start='10:00', description='Descrição da Palestra')
        t2 = Talk.objects.create(title='Titulo da Palestra', start='13:00', description='Descrição da Palestra')
        c1 = Course.objects.create(title='Titulo do Curso', start='09:00', description='Descrição do Curso', slots=20)

        speaker = Speaker.objects.create(
            name='Felipe Frizzo',
            slug='felipe-frizzo',
            website='http://google.com'
        )

        t1.speakers.add(speaker)
        t2.speakers.add(speaker)
        c1.speakers.add(speaker)

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
            (3, '/palestrantes/felipe-frizzo/'),
            (3, 'Felipe Frizzo'),
            (2, 'Descrição da Palestra'),
            (1, 'Titulo do Curso'),
            (1, '09:00'),
            (1, 'Descrição do Curso'),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected, count)

    def test_context(self):
        variables = ['talk_list']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.response.context)


class TalkListEmpty(TestCase):
    def test_get_empty(self):
        response = self.client.get(r_url('talk_list'))

        self.assertContains(response, 'Ainda não existem palestras de Manhã')
        self.assertContains(response, 'Ainda não existem palestras de Tarde')
