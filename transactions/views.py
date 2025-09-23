from django.shortcuts import render

from django.contrib import messages

from django.contrib.auth.decorators import login_required


from .models import Transaction
from .forms import TransactionForm

# Create your views here.
@login_required
def transaction(request):
    transactions = Transaction.objects.filter(owner=request.user)
    template = 'transactions.html'          
    
    return render(
    request,
    template,
    {"transactions":transactions}
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