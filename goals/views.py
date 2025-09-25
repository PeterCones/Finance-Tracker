from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Goal

# Create your views here.

@login_required
def goals(request):
    
    goals = Goal.objects.filter(owner=request.user)
    
    template = 'goals.html'
    
    return render(
        request,
        template,
        {'goals':goals}
    )

