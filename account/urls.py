from django.urls import path
from account.views import account_register, account_activate, dashboard

app_name = 'account'

urlpatterns = [
    path('register/', account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name='activate' ),
    # User dashboard
    path('dashboard/', dashboard, name='dashboard')
]