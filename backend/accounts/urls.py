from django.urls import path
from .views import *

urlpatterns = [
    path('users/', create_user, name='create_user'),
    path('users/list/', list_users, name='list_users'),
    path('users/<int:user_id>/', update_user, name='update_user'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),
]