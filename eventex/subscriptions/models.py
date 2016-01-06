from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=225)
    cpf = models.CharField(max_length=11)
    email = models.EmailField()
    phone = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
