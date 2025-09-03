from django.urls import path
from .views import *

urlpatterns = [
    path('', create_branch, name='create_branch'),
    path('list/', list_branches, name='list_branches'),
    path('<int:branch_id>/', update_branch, name='update_branch'),
    path('<int:branch_id>/delete/', delete_branch, name='delete_branch'),
]