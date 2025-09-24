from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Budget

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