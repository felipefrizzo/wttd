from django.views.generic.detail import DetailView
from eventex.subscriptions.forms import SubscriptionsForm
from eventex.subscriptions.mixins import EmailCreateView
from eventex.subscriptions.models import Subscription


new = EmailCreateView.as_view(model=Subscription,
                              form_class=SubscriptionsForm,
                              email_subject='Confirmação de inscrição')

detail = DetailView.as_view(model=Subscription)