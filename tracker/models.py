from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.crypto import get_random_string
from pricetracker.settings import AUTH_USER_MODEL


# Create your models here.


class MyUser(AbstractUser):
    telegram_id = models.CharField(max_length=200)
    telegram_status = models.BooleanField(default=False)
    telegram_auth_string = models.CharField(max_length=20)
    user_product_count = models.CharField(max_length=5)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    store = models.CharField(max_length=50)
    requested_price = models.TextField(default=10)
    last_price = models.IntegerField(null=True, blank=True)
    discount_price = models.CharField(max_length=100, null=True, blank=True)
    product_url = models.CharField(max_length=600)
    alert = models.BooleanField(default=True)
    alert_price = models.TextField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
