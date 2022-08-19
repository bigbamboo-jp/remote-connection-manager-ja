from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('terms', terms, name='terms'),
    path('privacy_policy', privacy_policy, name='privacy_policy'),
    path('action/ssh_function/enable', action_ssh_function_enable, name='action_ssh_function_enable'),
    path('action/ssh_function/disable', action_ssh_function_disable, name='action_ssh_function_disable'),
    path('action/ssh_function_disable_reservation/register', action_ssh_function_disable_reservation_register, name='action_ssh_function_disable_reservation_register'),
    path('action/ssh_function_disable_reservation/unregister', action_ssh_function_disable_reservation_unregister, name='action_ssh_function_disable_reservation_unregister'),
]
