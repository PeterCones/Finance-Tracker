import django_filters as df
from django import forms
from .models import Transaction, Category, Account
        
        
class TransactionFilter(df.FilterSet):
    
    date = df.DateFromToRangeFilter(
        field_name="date",
        label='Date Range',
        widget=df.widgets.RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    categories = df.ModelMultipleChoiceFilter(
        field_name="category",
        label='Category',
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        method="filter_categories_or",
    )
    
    account = df.ModelMultipleChoiceFilter(
        field_name="account",
        label='Account',
        queryset=Account.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        method="filter_accounts_or",
    )
    
    class Meta:
        model=Transaction
        fields=["date", "category", "account"]
        
    def filter_categories_or(self, queryset, name, value):
        if not value:
            return queryset
        # any of the selected categories
        return queryset.filter(category__in=value).distinct()
    
    def filter_accounts_or(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(account__in=value).distinct()