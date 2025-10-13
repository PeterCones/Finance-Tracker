from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Goal
from .forms import GoalForm, AdjustGoalForm

@login_required
def goals(request):
    qs = Goal.objects.filter(owner=request.user).order_by("-id")
    page_obj = Paginator(qs, 3).get_page(request.GET.get("page"))
    return render(request, "goals.html", {"page_obj": page_obj})

@login_required
def new_goal(request):
    if request.method == "POST":
        form = GoalForm(request.POST, user=request.user)
        if form.is_valid():
            g = form.save(commit=False)
            g.owner = request.user
            g.save()
            messages.success(request, "Goal saved.")
            return redirect("goals")
        messages.error(request, "Please fix the errors below.")
    else:
        form = GoalForm(user=request.user)
    return render(request, "new_goal.html", {"form": form})

@login_required
def adjust_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, owner=request.user)
    if request.method != "POST":
        return redirect("goals")

    form = AdjustGoalForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please enter a valid amount.")
        return redirect("goals")

    amt = form.cleaned_data["amount"]
    op = form.cleaned_data["operation"]
    delta = amt if op == "inc" else -amt

    # compute and clamp between 0 and target (optional upper clamp)
    new_value = goal.saved_amount + delta
    if new_value < 0:
        new_value = 0
    # Optional: cap at target
    # if new_value > goal.target_amount:
    #     new_value = goal.target_amount

    goal.saved_amount = new_value
    goal.save(update_fields=["saved_amount"])

    verb = "Added" if op == "inc" else "Removed"
    messages.success(request, f"{verb} £{amt} for “{goal.name}”.")
    return redirect("goals")


@login_required
def goal_edit(request, goal_id):
    qs = Goal.objects.filter(owner=request.user)
    goal = get_object_or_404(qs, id=goal_id)

    if request.method == 'POST':        
        form = GoalForm(request.POST,instance=goal)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Goal Updated!')
            return redirect('goals')
        messages.add_message(request, messages.ERROR, 'Error updating Goal!')
    else:
        form = GoalForm(instance=goal)
    
    return render(
        request,
        "new_goal.html",
        {
            "form": form,  # keep key consistent with your create view
        },
    )

@login_required    
def goal_delete(request, goal_id):
    qs = Goal.objects.filter(owner=request.user)
    goal = get_object_or_404(qs, id=goal_id)
    if request.method == "POST":
        goal.delete()
        messages.add_message(request, messages.SUCCESS, 'Goal deleted!')
        return redirect('goals')  
    return redirect('goals')