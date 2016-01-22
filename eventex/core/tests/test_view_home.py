from django.test import TestCase
from django.shortcuts import resolve_url as r_url


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r_url('home'))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        expected = 'href="{}"'.format(r_url('subscriptions:new'))
        self.assertContains(self.response, expected)

    def test_speakers(self):
        """Must show keynotes speakers"""
        contents = ['Grace Hopper',
                    'http://hbn.link/hopper-pic',
                    'Alan Turing',
                    'http://hbn.link/turing-pic'
        ]

        for content in contents:
            with self.subTest():
                self.assertContains(self.response, content)

    def test_spearkers_link(self):
        expected = 'href="{}#speakers"'.format(r_url('home'))
        self.assertContains(self.response, expected)
