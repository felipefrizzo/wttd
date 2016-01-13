from django import forms
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apensa numeros.', 'digits')

    if len(value) != 11:
        raise ValidationError('CPF deve ter 11 números.', 'length')


class SubscriptionsForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validate_cpf])
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Telefone')
