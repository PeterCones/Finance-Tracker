from django.db import models
from django.contrib.auth.models import User
from transactions.models import Category

# Create your models here.

class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    period_start = models.DateField(auto_now=True)
    limit_amount = models.DecimalField(decimal_places=2, max_digits=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)