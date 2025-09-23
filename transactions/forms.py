from .models import Transaction
from django import forms

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('account','category','amount','is_recurring',)