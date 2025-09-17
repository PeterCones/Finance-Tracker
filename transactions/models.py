from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Account (models.Model):
    name = models.CharField(max_length= 100, unique=True)
    
    type_choices= [
        ("Cash", "Cash")
        ("Bank", "Bank")
        ("Card", "Card")
    ]
    
    type = models.CharField(max_length=4, choices=type_choices, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
