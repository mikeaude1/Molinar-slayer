from django.urls import path
from . import views

app_name = 'practiceareas'

urlpatterns = [
    path('', views.practiceareas, name='practiceareas'),
    path('derechocivil', views.derechocivil, name='derechocivil'),
    path('derechopenal', views.derechopenal, name='derechopenal'),
    path('derechofamiliar', views.derechofamiliar, name='derechofamiliar'),
    path('derechomercantil', views.derechomercantil, name='derechomercantil'),
    path('derecholaboral', views.derecholaboral, name='derecholaboral'),
    path('derechofiscal', views.derechofiscal, name='derechofiscal'),
]