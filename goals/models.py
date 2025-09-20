from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Goal(models.Model):
    name = models.CharField(max_length= 100)
    target_amount = models.DecimalField(decimal_places=2, max_digits=100)
    target_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)