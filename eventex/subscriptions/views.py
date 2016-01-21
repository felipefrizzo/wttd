from django.conf import settings
from django.core import mail
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r_url
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionsForm
from eventex.subscriptions.models import Subscription


def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def empty_form(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionsForm()})


def create(request):
    form = SubscriptionsForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = form.save()

    _send_email('Confirmação de inscrição',
                settings.DEFAULT_FROM_EMAIL,
                subscription.email,
                'subscriptions/subscripiton_email.txt',
                {'subscription': subscription})

    return HttpResponseRedirect(r_url('subscriptions:detail', subscription.pk))


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html', {'subscription': subscription})


def _send_email(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])