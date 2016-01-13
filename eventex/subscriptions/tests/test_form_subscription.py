from django.test.testcases import TestCase
from eventex.subscriptions.forms import SubscriptionsForm


class SubscriptionFormTest(TestCase):

    def test_form_has_filters(self):
        """Form must have 4 fields"""
        form = SubscriptionsForm()
        expect = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expect, list(form.fields))

    def test_cpf_is_digit(self):
        """CPF must only accept digits"""
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assert_form_error_code(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits"""
        form = self.make_validated_form(cpf='1234')
        self.assert_form_error_code(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """Name must be capitalized"""
        form = self.make_validated_form(name='FELIPE frizzo')
        self.assertEqual('Felipe Frizzo', form.cleaned_data['name'])

    def assert_form_error_code(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assert_form_error_message(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Felipe Frizzo', cpf='12345678901', email='felipefrizzo@gmail.com', phone='45-9923-0342')
        data = dict(valid, **kwargs)
        form = SubscriptionsForm(data)
        form.is_valid()

        return form
