from django.urls import path
from . import views

urlpatterns = [
    path('registervendorsss', views.registervendor, name='registervendors'),
]
