import django_filters
from .models import Transaction, Category


class TransactionFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(field_name="category",
                                                queryset=Category.objects.all(),
                                                empty_label="All"
    )
    
    class Meta:
        model = Transaction
        fields = ["category"]