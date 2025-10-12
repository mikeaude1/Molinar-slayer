from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('lawyer/dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('dashboard/', views.profile_dashboard, name='dashboard'),
    # Perfil Abogado
    path('lawyer/clients/', views.lawyer_clients, name='lawyer_clients'),
    path('lawyer/cases/', views.lawyer_cases, name='lawyer_cases'),
    path('lawyer/agenda/', views.lawyer_agenda, name='lawyer_agenda'),
    path('lawyer/invoices/pending/', views.lawyer_invoices_pending, name='lawyer_invoices_pending'),
    path('lawyer/invoices/paid/', views.lawyer_invoices_paid, name='lawyer_invoices_paid'),
]