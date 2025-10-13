from django.db import models
from django.contrib.auth.models import User
from transactions.models import Category
from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Budget(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    period_start = models.DateField(help_text="First day of the month")
    limit_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("owner", "category", "period_start")

    @property
    def month_label(self):
        return self.period_start.strftime("%B %Y")