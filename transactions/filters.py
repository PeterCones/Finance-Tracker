import django_filters as df
from django import forms
from .models import Transaction, Category
        
        
class TransactionFilter(df.FilterSet):
    
    categories = df.ModelMultipleChoiceFilter(
        field_name="category",
        label='Category',
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        method="filter_categories_or",
    )
    
    class Meta:
        model=Transaction
        fields=["category"]
        
    def filter_categories_or(self, queryset, name, value):
        if not value:
            return queryset
        # any of the selected categories
        return queryset.filter(category__in=value).distinct()