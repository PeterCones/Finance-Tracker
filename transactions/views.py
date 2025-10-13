from django.shortcuts import render,redirect, get_object_or_404

from django.contrib import messages

from django.db.models import Sum, Case, When, F, DecimalField, Value

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .filters import TransactionFilter

from .models import Transaction, Category
from .forms import TransactionForm

import json

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
    paginator = Paginator(filter_qs.qs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    params = request.GET.copy()
    params.pop("page", None)
    preserved_qs = params.urlencode()

    # Overall balance (use filter_qs.qs instead if you want filtered balance)
    balance = base_qs.aggregate(
        balance=Sum(
            Case(
                When(type=Transaction.TYPE_INCOME, then=F('amount')),
                When(type=Transaction.TYPE_EXPENSE, then=-F('amount')),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
    )['balance'] or 0

    income = base_qs.aggregate(
        income=Sum(
            Case(
                When(type=Transaction.TYPE_INCOME, then=F('amount')),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
    )['income'] or 0

    expense = base_qs.aggregate(
        expense=Sum(
            Case(
                When(type=Transaction.TYPE_EXPENSE, then=F('amount')),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
    )['expense'] or 0

    pie_labels = ["Income", "Expenses"]
    pie_values = [float(income or 0), float(expense or 0)]

    pie_labels_json = json.dumps(pie_labels)
    pie_values_json = json.dumps(pie_values)

    return render(
        request,
        template,
        {
            "filter": filter_qs,
            "page_obj": page_obj,
            "preserved_qs": preserved_qs,
            "balance": balance,
            "income": income,
            "expense": expense,
            "pie_labels_json": pie_labels_json,
            "pie_values_json": pie_values_json,
        },
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
            return redirect("transaction")

            
    
    return render(
        request,
        "new_transaction.html",
        {
         "TransactionForm": TransactionForm,
         },
    )
    
    
# edit transaction
@login_required
def transaction_edit(request, transaction_id):
    qs = Transaction.objects.filter(owner=request.user)
    transaction = get_object_or_404(qs, id=transaction_id)

    if request.method == 'POST':        
        form = TransactionForm(request.POST,instance=transaction)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Transaction Updated!')
            return redirect('transaction')
        messages.add_message(request, messages.ERROR, 'Error updating Transaction!')
    else:
        form = TransactionForm(instance=transaction)
    
    return render(
        request,
        "new_transaction.html",
        {
            "TransactionForm": form,  # keep key consistent with your create view
        },
    )

@login_required    
def transaction_delete(request, transaction_id):
    qs = Transaction.objects.filter(owner=request.user)
    transaction = get_object_or_404(qs, id=transaction_id)
    if request.method == "POST":
        transaction.delete()
        messages.add_message(request, messages.SUCCESS, 'Transaction deleted!')
        return redirect('transaction')  
    return redirect('transaction')

