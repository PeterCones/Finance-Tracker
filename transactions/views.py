from django.shortcuts import render

from django.contrib import messages

from .forms import TransactionForm

# Create your views here.

def transaction(request):
  return render(request, 'transactions.html')          
            
            
            
            
            
def newTransaction(request):
    # return render(request, 'new_transaction.html')

    if request.method =='POST':
        transaction_form = TransactionForm(data=request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.account = request.user
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