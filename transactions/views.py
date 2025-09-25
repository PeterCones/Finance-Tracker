from django.shortcuts import render,get_object_or_404

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django_filters.views import FilterView
from .filters import TransactionFilter

from .models import Transaction, Category
from .forms import TransactionForm

# Create your views here.
@login_required
def transaction(request):
    transactions = Transaction.objects.filter(owner=request.user).values(
    'amount',
    'date', 
    'account__name',           # Account name
    'account__type',           # Account type
    'category__category',      # Category name
    'type',
)
    template = 'transactions.html'
    
    paginator = Paginator(transactions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)          
    
    return render(
    request,
    template,
    {"page_obj":page_obj,
     "page_number": page_number}
    )      
                
            
            
            
def newTransaction(request):
    # return render(request, 'new_transaction.html')

    if request.method =='POST':
        transaction_form = TransactionForm(data=request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.owner = request.user
            transaction.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your transaction has been sucessfully added'
            )
    
    return render(
        request,
        "new_transaction.html",
        {
         "TransactionForm": TransactionForm,
         },
    )
    
class TransactionFilterView(FilterView):
    filterset_class = TransactionFilter
    template_name = "transactions.html"
    paginate_by = 5

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related("category")
    
    