from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('details/<int:project_id>', views.details, name='details'),
    path('edit/<int:project_id>', views.edit, name='edit'),
]
