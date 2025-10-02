from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


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
    def __str__(self):
        return self.name


class Category (models.Model):

    category = models.CharField(max_length= 100, default='')
    
    is_global = models.BooleanField(default=False)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.category
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'category'],
                condition=Q(is_global=False),
                name='uniq_category_per_owner',
            ),
            models.UniqueConstraint(
                fields=['category'],
                condition=Q(is_global=True),
                name='uniq_global_category_name',
            ),
        ]
    
class Transaction (models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='transactions')
    type_choices= [
        ("Income", "Income"),
        ("Outgoing", "Outgoing"),
    ]
    type = models.CharField(max_length=8, choices=type_choices, default='')
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    date = models.DateField()
    is_recurring = models.BooleanField(default=False)
