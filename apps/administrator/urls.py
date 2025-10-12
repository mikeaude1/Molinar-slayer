from django.urls import path
from . import views

app_name = 'administrator'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('portal/background/', views.edit_portal_background, name='portal_bg'),
    path('about/background/', views.edit_aboutus_background, name='aboutus_bg'),
    # Usuarios
    path('users/', views.users_list, name='users_list'),
    path('users/create/', views.users_create, name='users_create'),
    path('users/<int:user_id>/edit/', views.users_edit, name='users_edit'),
    path('users/<int:user_id>/toggle-active/', views.users_toggle_active, name='users_toggle_active'),
    # Áreas de práctica
    path('practice-areas/', views.practiceareas_list, name='practiceareas_list'),
    path('practice-areas/create/', views.practiceareas_create, name='practiceareas_create'),
    path('practice-areas/<int:area_id>/edit/', views.practiceareas_edit, name='practiceareas_edit'),
    path('practice-areas/<int:area_id>/toggle-active/', views.practiceareas_toggle_active, name='practiceareas_toggle_active'),
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:post_id>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:post_id>/toggle-active/', views.blog_toggle_active, name='blog_toggle_active'),
]