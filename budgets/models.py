from django.db import models
from django.contrib.auth.models import User
from transactions.models import Category
from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    period_start = models.DateField()
    limit_amount = models.DecimalField(decimal_places=2, max_digits=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)