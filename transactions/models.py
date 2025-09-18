from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Account (models.Model):
    name = models.CharField(max_length= 100, unique=True)
    
    type_choices= [
        ("Cash", "Cash"),
        ("Bank", "Bank"),
        ("Card", "Card"),
    ]
    
    type = models.CharField(max_length=4, choices=type_choices, default='')
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Category (models.Model):
    name = models.CharField(max_length= 100, unique=True)
    
    type_choices= [
        ("Income", "Income"),
        ("Expenses", "Expenses"),
    ]
    
    type = models.CharField(max_length=8, choices=type_choices, default='')
    
    is_global = models.BooleanField(default=False)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Transaction (models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    date = models.DateTimeField(auto_now=True)
    is_recurring = models.BooleanField(default=False)