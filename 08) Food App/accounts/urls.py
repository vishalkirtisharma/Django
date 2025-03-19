from django.urls import path
from . import models,views
from vendor.views import registervendor,login,logout,dashboard,myaccounts,custdashboard,vendordashboard

urlpatterns = [
    path('registeruser/',views.registeruser,name='registeruser'),
    path('registervendor/',registervendor,name='registervendor'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('myaccounts/',myaccounts,name='myaccounts'),
    path('dashboard/',dashboard,name='dashboard'),
    path('custdashboard/',custdashboard,name='custdashboard'),
    path('vendordashboard/',vendordashboard,name='vendordashboard'),
]
