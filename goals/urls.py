from django.urls import path
from . import views

urlpatterns = [
    path("", views.goals, name="goals"),
    path("goals/add/", views.new_goal, name="new_goal"),
    path("goals/<int:goal_id>/adjust/", views.adjust_goal, name="adjust_goal"),
    path('edit/<int:goal_id>',views.goal_edit, name='edit_goal'),
    path('delete/<int:goal_id>',views.goal_delete, name='delete_goal'),
]