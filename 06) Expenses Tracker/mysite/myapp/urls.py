from django.urls import path
from . import views

"""
URL configuration for the Expenses Tracker application.

Defines the URL patterns and maps them to their corresponding views.
"""

app_name = 'myapp'  # Namespace for the application's URLs

urlpatterns = [
    # Home page - displays expense list and form
    path('', views.index, name='index'),
    
    # Edit page - allows editing an existing expense
    path('edit/<int:id>/', views.edit, name='edit'),
    
    # Delete endpoint - handles expense deletion
    path('delete/<int:id>/', views.delete, name='delete'),
]
