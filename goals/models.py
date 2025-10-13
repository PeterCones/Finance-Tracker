from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.functions import Now, TruncDate
from django.db.models import Q
from datetime import date  # added

# Create your models here.

class Goal(models.Model):
    name = models.CharField(max_length= 100, unique=True)
    target_amount = models.DecimalField(decimal_places=2, max_digits=100)
    target_date = models.DateField()
    saved_amount = models.DecimalField(decimal_places=2, max_digits=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def clean(self):
        # App-level guard (used by ModelForm)
        if self.target_date and self.target_date <= date.today():
            raise ValidationError({'target_date': 'Please choose a future date.'})

    @property
    def days_left(self):
        """Non-negative days until target_date."""
        if not self.target_date:
            return 0
        return max((self.target_date - date.today()).days, 0)
    
    def actual_amount(self):
        return (self.target_amount - self.saved_amount)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='goal_target_date_in_future',
                check=Q(target_date__gt=TruncDate(Now())),
            ),
        ]