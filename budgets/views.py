from django.shortcuts import render,redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Budget

from .forms import budgetForm
# Create your views here.

@login_required
def budget(request):
    
    budgets = Budget.objects.filter(owner=request.user)
    
    template = 'budgets.html'
    
    return render(
        request,
        template,
        {'budgets':budgets}
    )
    
    
def newBudget(request):
    # return render(request, 'new_transaction.html')

    if request.method =='POST':
        budget_form = budgetForm(data=request.POST)
        if budget_form.is_valid():
            budget = budgetForm.save(commit=False)
            budget.owner = request.user
            budget.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your transaction has been sucessfully added'
            )
            return redirect("budget")

            
    
    return render(
        request,
        "new_budget.html",
        {
         "budgetForm": budgetForm,
         },
    )
    