from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('edit/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('change_password',views.change_password, name='change_password'),
    path('users', views.users, name='users'),
]
