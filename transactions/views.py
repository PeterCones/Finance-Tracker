from django.shortcuts import render,get_object_or_404

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .filters import TransactionFilter

from .models import Transaction, Category
from .forms import TransactionForm

# Create your views here.
@login_required
def transaction(request):
    
    base_qs = (
        Transaction.objects
        .filter(owner=request.user)
        .select_related("account", "category")
        .order_by("-date", "-id")
    )
    
    filter_qs = TransactionFilter(request.GET or None, queryset=base_qs)
    
    
    
    template = 'transactions.html'
    
    paginator = Paginator(filter_qs.qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    params = request.GET.copy()
    params.pop("page", None)
    preserved_qs = params.urlencode()          
    
    return render(
    request,
    template,
    {   
        "filter":filter_qs,
        "page_obj":page_obj,
        "preserved_qs": preserved_qs}
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
    